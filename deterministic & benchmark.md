## torch.backends.cudnn.deterministic
if true, cuDNN 只会使用 deterministic 卷积算法

**deterministic官方说明及理解**  
torch docs
```
Sets whether PyTorch operations must use “deterministic” algorithms. 
That is, algorithms which, given the same input, and when run on the 
same software and hardware, always produce the same output. When True, 
operations will use deterministic algorithms when available, and if 
only nondeterministic algorithms are available they will throw a :class:RuntimeError
when called.
```
```
deterministic算法指，当被给相同的输入，并且在痛殴一软件和硬件平台下，
总是会产生相同的输出。

当使用deterministic为true时：
如果deterministic算法可用，运算操作会使用deterministic算法，如果某个
操作只存在nondeterministic算法，这时会丢出 runtimeError
```
**什么是deterministic algorithms？**  
这个涉及到P与NP问题，此文不便阐述。 这里简单说一下自己对确定性算法和非确定性算法的理解。

确定性算法：由一连串的步骤唯一地确定，也就是说，给定一个输入和执行过程中的某一步，那么
该算法中的下一步是唯一的。

非确定性算法：在给定一个输入和执行过程中的某一步，在该算法中的下一步是不确定的。
（这里的理解可能有问题，需要日后深究，20210812）


## torch.backends.cudnn.benchmark
if true, cuDNN 会评价不同的卷积算法，然后选择最快的卷积算法进行运算

