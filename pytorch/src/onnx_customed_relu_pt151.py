import torch
import torch.nn as nn


class MyRelu1(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return input.clamp(min=0)

    @staticmethod
    def symbolic(g, input):
        return g.op("Clip", input, g.op("Constant", value_t=torch.tensor(0, dtype=torch.float)))


class Net1(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = MyRelu1()
    def forward(self, x):
        return self.relu.apply(x)


class MyRelu2(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return input.clamp(min=0)


class Net2(nn.Module):
    def __init__(self):
        super().__init__()
    def forward(self, x):
        return MyRelu2.apply(x)


if __name__ == '__main__':
    net1 = Net1()
    net2 = Net2()

    torch.onnx.export(net1, torch.ones(1), "net1.onnx", verbose=True,
                      operator_export_type=torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK)
    # error code
    # torch.onnx.export(net2, dummy_input, "net2.onnx", verbose=True,
    #                   operator_export_type=torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK)