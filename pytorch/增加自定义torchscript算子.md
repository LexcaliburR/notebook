<!--
 * @Author: lexcalibur
 * @Date: 2021-12-10 09:40:29
 * @LastEditors: lexcaliburr
 * @LastEditTime: 2021-12-10 09:51:57
-->

# torchscript简介
torchscript是torch python的子集，torchscript的代码可以被torchScript compiler解释，编译和优化，也可以直接保存下来，通过cpp或者python进行调用

torchscript支持torch的大部分算子，可以实现pytorch标准库里的一系列算子。对于自定义的cpp和cuda算子，可以通过ATen实现。

**ATen为pytorch的高性能cpp算子库**

# 流程概要
1. 在cpp中使用tensor，实现算子功能
2. 在TorchSCript中注册自己的算子
3. 编译算子
4. 在python和cpp中使用算子

# 1.cpp实现算子
