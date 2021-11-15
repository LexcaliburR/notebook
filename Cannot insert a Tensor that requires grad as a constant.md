---
titile: Cannot insert a Tensor that requires grad as a constant. Consider making it a parameter or input, or detaching the gradient
data: 2021-08-26
---

---
# Cannot insert a Tensor that requires grad as a constant. Consider making it a parameter or input, or detaching the gradient

在导出onnx模型时，出现如上错误，可能是因为使用了python的List而不是torch.nn.ModuleList

```python
# 模型导出ONNX正常
class MyModel(torch.nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.line1 = nn.Linear(10, 20)
        self.line2 = nn.Linear(20, 20)
        self.line3 = nn.Linear(20, 10)
    
    def forward(self, x):
        x = self.line1(x)
        x = self.line2(x)
        x = self.line3(x)
        return x

# 模型导出报上述错误
class Py(torch.nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.layers = [nn.Linear(10, 20), nn.Linear(20, 20), nn.Linear(20, 10)]
    
    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x


# 模型导出正常
class Py(torch.nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.layers = torch.nn.ModuleList([nn.Linear(10, 20), nn.Linear(20, 20), nn.Linear(20, 10)])
    
    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

```
