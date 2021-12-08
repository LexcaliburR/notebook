<!--
 * @Author: lexcalibur
 * @Date: 2021-12-07 16:31:38
 * @LastEditors: lexcaliburr
 * @LastEditTime: 2021-12-07 16:47:21
-->

# Tracing
使用`torch.onnx.export()`  
1. 直接输入继承了nn.Module的模型  
2. 输入一个样例输入  
框架运行推理，记录各个层的参数，相当于把动态图转换为静态图并生成onnx  

# Scripting
1. 首先使用`torch.jit.script()`生成ScriptModule，ScriptModule相当于已经预编译好的静态模型
2. 调用`torch.onnx.export()`生成onnx模型，此时需要设置`example_outputs`参数  