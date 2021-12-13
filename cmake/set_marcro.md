```c
// 1.版本
cmake_minimum_required(VERSION 3.1 FATAL_ERROR)
// 2.项目名称
project(warp_perspective)
// 3.编译时的flag设置，注意要在对于的findpackage前
set(CMAKE_PREFIX_PATH "/home/lexcalibur/anaconda3/envs/pt110/lib/python3.8/site-packages/torch/share/cmake")
// 4.找到对应的包
find_package(Torch REQUIRED)
```