import torch
import torch.nn as nn

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
        super(FooModel, self).__init__()
        self.attr1 = attr1
        self.attr2 = attr2

    def forward(self, input1, input2):
        # Calling custom op
        return torch.ops.custom_ops.foo_forward(input1, input2, self.attr1, self.attr2)

model = FooModel(2, 3)
torch.onnx.export(
  model,
  (torch.Tensor(1), torch.Tensor(2)),
  "model.onnx",
  # only needed if you want to specify an opset version > 1.
  custom_opsets={"custom_domain": 2},
operator_export_type=torch.onnx.OperatorExportTypes.ONNX_FALLTHROUGH)