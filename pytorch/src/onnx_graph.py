import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.onnx.symbolic_opset9 as sym


class MyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.elu = nn.ELU()

    def forward(self, x):
        return self.elu(x)


if __name__ == '__main__':
    print(torch.jit.trace(
        nn.ELU(),
        torch.ones(1)).graph
    )

    model = MyNet()
    torch.onnx.export(model, torch.ones(3), "elu.onnx", verbose=True)