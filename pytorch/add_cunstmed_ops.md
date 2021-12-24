<!--
 * @Author: lexcalibur
 * @Date: 2021-12-14 13:23:58
 * @LastEditors: lexcaliburr
 * @LastEditTime: 2021-12-14 16:51:07
 * @Reference: https://blog.csdn.net/gzq0723/article/details/115410050
-->
# 方法总览
1. Native_functions.yaml方法
2. C++ extention方法(PYBIND11_MODULE/PYTORCH_LIBRARY)
3. OP Register 方法

# 1. Native_functions.yaml方法
wait...

# 2. C++ extention方法(PYBIND11_MODULE/PYTORCH_LIBRARY)
wait...

# 3. OP Register 方法导出ONNX技术路线
### 1.实现cpp算子
```cpp
#include "torch/script.h"

// 函数实现
torch::Tensor mline(torch::Tensor input, torch::Tensor weight) {
    torch::Tensor ret = input.matmul(weight);
    return ret;
}

// 注册
TORCH_LIBRARY(my_ops, m) {
    m.def("mline", mline);
}
```

### 2.python调用算子,完成Module的实现
```python
import torch
import torch.nn as nn
from torch.onnx import register_custom_op_symbolic
from torch.onnx.symbolic_helper import parse_args

torch.ops.load_library("/home/lishiqi/myrepos/MyCodeRepo/trt_deploy_demo/model/customed_op/build/libmline.so")
class SimpleClassifier(torch.nn.Module):
    def __init__(self, in_channel, num_class):
        super().__init__()
        self.line = nn.Linear(in_channel, 16)
        self.mline_weight = torch.nn.Parameter(torch.ones(16, num_class))

    def forward(self, x):
        assert len(x.shape) == 2
        # Calling custom op
        x = self.line(x)
        return torch.ops.my_ops.mline(x, self.mline_weight)

def test_call_cpp_op():
    model = SimpleClassifier(3, 10)
    input = torch.randn([5, 3])
    output = model(input)
    print(output.shape)

test_call_cpp_op()

```

### 3.注册算子到onnx
```python

@parse_args("v", "v")
def mline(g, input, weight):
    return g.op("my_ops::mline", input, weight)

register_custom_op_symbolic("my_ops::mline", mline, 9)

```


### 4.导出onnx
```python
def exportONNX():
    model = SimpleClassifier(3, 10)
    input = torch.randn([5, 3])
    torch.onnx.export(model, input, "mline_cpp.onnx")

exportONNX()
```