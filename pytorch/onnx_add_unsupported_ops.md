<!--
 * @Author: lexcalibur
 * @Date: 2021-12-07 16:43:10
 * @LastEditors: lexcaliburr
 * @LastEditTime: 2021-12-08 16:24:46
-->
# 1.引入
**注：此版本适用于torch 1.10版本，1.5.1版本略有不同**
```
RuntimeError: ONNX export failed: Couldn't export operator {UNSUPPORT_OPS， eg. foo}
```

增加torch.onnx.export对自定义算子的支持需要修改pytorch源码。  

在导出模型时，TorchScript graph的每个Node以拓扑结构遍历，在遍历到每个Node时，会为每个node找到对应的注册过的 symbolic 函数。 symbolic函数都是通过python实现的， 如下便为一个名为foo的symbolic函数，注意其第一个参数总是为g，为`torch._C.Graph`类型，代表着张计算图

torch._C的定义可以在`/torch/csrc/jit/ir/ir.h`中找到
```python
def foo(
  g: torch._C.Graph,
  input_0: torch._C.Value,
  input_1: torch._C.Value) -> Union[None, torch._C.Value, List[torch._C.Value]]:
  """
  Modifies g (e.g., using "g.op()"), adding the ONNX operations representing
  this PyTorch function.

  Args:
    g (Graph): graph to write the ONNX representation into.
    input_0 (Value): value representing the variables which contain
        the first input for this operator.
    input_1 (Value): value representing the variables which contain
        the second input for this operator.

  Returns:
    A Value or List of Values specifying the ONNX nodes that compute something
    equivalent to the original PyTorch operator with the given inputs.
    Returns None if it cannot be converted to ONNX.
  """
```

# 2.修改torch源码

- 在`symbolic_opset<version>.py`中定义symbolic函数。 确保定义的function和ATen function的函数名相同，ATen函数在`torch/_C/_VariableFunctions.pyi`中或者`torch/nn/functional.pyi`中被申明，注意pyi文件是在编译时生成的，因此如果没有编译pytorch的话时找不到对于的*.ipy文件的
- 函数的第一个参数通常都是需要被导出的onnx计算图. 其他的参数名字必须与`.pyi`文件中的名字相同
- 在symbolic函数中，如果各操作算子都是`ONNX standard operator set`，我们只需要在图中创造一个node去实现onnx操作。否则的话，需要创造有数个标准算子的计算图，这些标准算子和ATen 的算子起到同样的作用
- 如果输入的参数是Tensor，需要显示(explicitly)的转换为scalar,使用`symbolic_helper._scalar()`和`symbolic_helper._if_scalar_type_as()`

举例： 
```python
print(
  torch.jit.trace(torch.nn.ELU(), # module
                  torch.ones(1)   # example input
                  ).graph)

################ result ################################################
graph(%self : __torch__.torch.nn.modules.activation.___torch_mangle_0.ELU,
      %input : Float(1, strides=[1], requires_grad=0, device=cpu)):
  %4 : float = prim::Constant[value=1.]()
  %5 : int = prim::Constant[value=1]()
  %6 : int = prim::Constant[value=1]()
  %7 : Float(1, strides=[1], requires_grad=0, device=cpu) = aten::elu(%input, %4, %5, %6)
  return (%7)

```

上例如果注释了 symbolic_opset<version>.py中的elu函数，会导出onnx模型报错

# 3.torch.autograd.Functions
如果操作是`torch.autograd.Function`的子类，有两种方式导出onnx模型  

## 3.1 Static Symbolic Method，给对应的类增加`symbolic`静态方法
此时的返回值为通过onnx算子实现的函数功能，如下所示
```python
class MyRelu(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input: torch.Tensor) -> torch.Tensor:
        ctx.save_for_backward(input)
        return input.clamp(min=0)

    @staticmethod
    def symbolic(g: torch._C.graph, input: torch._C.Value) -> torch._C.Value:
        return g.op("Clip", input, g.op("Constant", value_t=torch.tensor(0, dtype=torch.float)))
```


## 3.2 PythonOp Symbolic
注册一个自定义的symbolic function. 这种方法有更大的可操作空间

在torchScript计算图中，所有的autograd Function都表现为prim::PythonOp nodes. 为了区别不同的Fuction子类，symbolic function应该使用 name 参数

`register_custom_op_symbolic()`不允许在`prim`命名空间中注册算子，自己注册的算子需要在在`::prim_PythonOp`命名空间下  

自定义的Symbolic functions在返回值时，应该通过调用Value objects的`setType(...)`(函数实现位于`torch::jit::Value::setType`)函数增加type和shape信息，举例:`pytorch/test/onnx/test_operators.py`中的`test_aten_embedding_2`

下例说明了怎么通过`Node`object访问修改`requires_grad`：
```python
class MyClip(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, min):
        ctx.save_for_backward(input) # # ave input for backward, can be accessed through the :attr:`saved_tensors`
        return input.clamp(min=min) # 小于最小值被最小值替代，大于最小值返回原值

class MyRelu(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return input.clamp(min=0) # 小于0被0替代，大于0返回原值

# 以上两个function不用写反向传播的逻辑吗？

def symbolic_pythonop(g: torch._C.Graph, n: torch._C.Node, *args, **kwargs):
    print("original node: ", n)
    # 每个输出，是否需要计算梯度
    for i, out in enumerate(n.outputs()):
        print("original output {}: {}, requires grad: {}".format(i, out, out.requiresGrad()))
    import torch.onnx.symbolic_helper as sym_helper
    
    # 遍历每个输入，显示每个输入是否需要计算梯度
    for i, arg in enumerate(args):
        requires_grad = arg.requiresGrad() if sym_helper._is_value(arg) else False
        print("arg {}: {}, requires grad: {}".format(i, arg, requires_grad))

    # 取出算子的名字，根据名字调用不同的算子
    name = kwargs["name"]
    ret = None
    if name == "MyClip":
        ret = g.op("Clip", args[0], min_f=args[1])
    elif name == "MyRelu":
        ret = g.op("Relu", args[0])
    else:
        # Logs a warning and returns None
        return _unimplemented("prim::PythonOp", "unknown node kind: " + name)
    # Copy type and shape from original node.
    ret.setType(n.type())
    return ret

from torch.onnx import register_custom_op_symbolic
register_custom_op_symbolic("::prim_PythonOp", symbolic_pythonop, 1)
```

## 3.3 torch.onnx.export
operator_export_type (enum, default OperatorExportTypes.ONNX)
- OperatorExportTypes.ONNX: All ops are exported as regular ONNX ops (所有算子都是onnx标准算子)
- OperatorExportTypes.ONNX_ATEN: All ops are exported as ATen ops (所有算子都被作为ATen算子导出)
- OperatorExportTypes.ONNX_ATEN_FALLBACK: If an ATen op is not supported in ONNX or its symbolic is missing, fall back on ATen op. Registered ops are exported to ONNX regularly. (如果一个ATen算子在ONNX中不支持，或者没有对于的symbolic, 跳过该ATen算子)
- OperatorExportTypes.RAW: Export raw ir.
- OperatorExportTypes.ONNX_FALLTHROUGH: If an op is not supported in ONNX, fall through and export the operator as is, as a custom ONNX op. Using this mode, the op can be exported and implemented by the user for their runtime backend. (如果onnx不支持该算子，将会把该算子作为自定义onnx算子进行导出，在使用这个模式时，算子能够被导出，用户可以在后端运行时实现该算子)

```sh
# -------------- ONNX_ATEN_FALLBACK --------------------------------
# example
graph(%0 : Float)::
    %3 : int = prim::Constant[value=0]()
    %4 : Float = aten::triu(%0, %3) # missing op
    %5 : Float = aten::mul(%4, %0)  # registered op
    return (%5)

# result
graph(%0 : Float)::
    %1 : Long() = onnx::Constant[value={0}]()
    %2 : Float = aten::ATen[operator="triu"](%0, %1)  # missing op
    %3 : Float = onnx::Mul(%2, %0) # registered op
    return (%3)

# -------------- ONNX_FALLTHROUGH -----------------------
# example
graph(%x.1 : Long(1, strides=[1]))::
    %1 : None = prim::Constant()
    %2 : Tensor = aten::sum(%x.1, %1)
    %y.1 : Tensor[] = prim::ListConstruct(%2)
    return (%y.1)

# results
graph(%x.1 : Long(1, strides=[1]))::
    %1 : Tensor = onnx::ReduceSum[keepdims=0](%x.1)
    %y.1 : Long() = prim::ListConstruct(%1)
    return (%y.1)
```

# 4. 自定义算子 Custom operators
如果模型使用了c++实现的算子，能按照如下的例子导出这个模型

```python
from torch.onnx import register_custom_op_symbolic
from torch.onnx.symbolic_helper import parse_args

# Define custom symbolic function
@parse_args("v", "v", "f", "i")
def symbolic_foo_forward(g, input1, input2, attr1, attr2):
    return g.op("custom_domain::Foo", input1, input2, attr1_f=attr1, attr2_i=attr2)

# Register custom symbolic function
register_custom_op_symbolic("custom_ops::foo_forward", symbolic_foo_forward, 9)

class FooModel(torch.nn.Module):
    def __init__(self, attr1, attr2):
        super(FooModule, self).__init__()
        self.attr1 = attr1
        self.attr2 = attr2

    def forward(self, input1, input2):
        # Calling custom op
        return torch.ops.custom_ops.foo_forward(input1, input2, self.attr1, self.attr2)

model = FooModel(attr1, attr2)
torch.onnx.export(
  model,
  (example_input1, example_input1),
  "model.onnx",
  # only needed if you want to specify an opset version > 1.
  custom_opsets={"custom_domain": 2})

```