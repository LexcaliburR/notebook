<!--
 * @Author: lishiqi
 * @LastEditors: lishiqi
-->
# 一.cuda 程序代码流程
## 1. 分配需要的cpu内存空间
T* A = (T*)malloc(size)
## 2. 分配需要的gpu显存空间
T* cu_A
cudaMalloc(&cu_A, size)
## 3. 将cpu中的数据copy到显存中
cudaMemcpy(cu_A, A, size, cudaMemcpyHostToDevice)
## 4. 运行核函数
func<<<BlockPerGrid, threadPerBlock>>>
## 5. 将显存中的数据copy出来，进行访问
cudaMemcpy(A, cu_A, size, cudaMemcpyDeviceToHost)
## 6. free memory
cudaFree(cu_A)


# 二. thread id和threadsPerBlock的对应关系
## 1.threadsPerBlock 为1维时
threadsPerBlock(N)  
thread id 和 block的size一一对应

## 2.threadsPerBlock 为2维时
threadsPerBlock的size为(Dx, Dy)  
下标为(x, y)的threadid为  
thread_id = x + y * Dx

## 3.threadsPerBlock 为3维时
threadsPerBlock的size为(Dx, Dy, Dz)  
下标为(x,y,z)的thread_id为  
thread_id = x + y * Dx + z * Dx * Dy

# 三. shared memory
声明固定尺寸的共享的数组  
__shared__ float sh_data[THREAD_SIZE];  
声明动态尺寸的共享的数组  
extern __shared__ float sh_data[];
