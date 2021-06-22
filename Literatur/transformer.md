<!-- --- -->
<!-- title: Transformer note -->

<!-- description:  -->



<!-- --- -->

Transormer 抛弃了CNN/RNN，整个网络结构完全由Attention机制构成。更准确的讲，
Transformer由且仅由self-Attention和Feed Forward Neural Network构成。作者
的实验是通过搭建encoder和decoder各6层，总共12层的Encoder-Decoder。

作者采用这种算法的原因之一是 RNN（LSTM,GRU）等时，计算限制为顺序的，要么从左到右
要么从右到左。本文通过如下方式解决：
1. 采用Attention机制，将序列中的任意两个位置之间的距离缩小为一个常量；
2. 不是类似RNN的顺序结构，具有更好的并行性

**原文Transformer定义:**
Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence aligned RNNs or convolution。

**Encoder运算**
首先通过‘self-attention’模块得到加权后的特征向量Z：<br>
$$ Attention\(Q,K,V\) $$

https://zhuanlan.zhihu.com/p/48508221

http://jalammar.github.io/illustrated-transformer/
