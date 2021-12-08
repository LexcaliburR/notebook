<!--
 * @Author: lexcalibur
 * @Date: 2021-12-08 17:09:34
 * @LastEditors: lexcaliburr
 * @LastEditTime: 2021-12-08 20:09:59
-->

# Function实现
```python
class MyFunction(torch.autograd.Function)
    # 第一个参数总是g，表示onnx的计算图
    # 接下来的参数首先是Tensor格式的输入
    # 之后为权重偏差等其他arg
    # arg之后则是名字等其他属性，要求以{变量名}_{数据格式}的方式命名，s: string, i: int, f: float, b: bool, t: tensor is: list(int), fs: list(float)
    # 在onnx计算图中，tensor显示为input，其他的arg显示为attribute
    @staticmethod
    def symbolic(g, input, bias):
        return g.op("Plugin", input, bias, name_s="MReLU", info_s=json.dumps({
            "kernel_size": 3,
            "eps": 3e-2,
            "other": "Hello Onnx Plugin"
        }))

    # 参数与symbolic一致
    @staticmethod
    def forward(ctx, i, bias):
        ctx.save_for_backward(i)
        return F.relu(i) + bias
```