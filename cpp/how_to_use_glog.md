<!--
 * @Author: Lexcaliburr lishiqi0111@gmail.com
 * @Date: 2022-05-20 09:24:11
 * @LastEditors: Lexcaliburr lishiqi0111@gmail.com
 * @LastEditTime: 2022-05-20 09:56:23
 * @FilePath: /notebook/cpp/how_to_use_glog.md
 * @Description: 
-->
# How to Use Glog

## 1. CMakeLists Setting
```cmake
cmake_minimum_required (VERSION 3.16)
project (myproj VERSION 1.0)

find_package (glog 0.6.0 REQUIRED)

add_executable (myapp main.cpp)
# inlcude 此处为默认安装的路径，如果将glog改为单独的库，include路径设置为glog头文件的include路径即可
target_include_directories(myapp /usr/local/include)
target_link_libraries (myapp glog::glog)
```

## 2. 常用函数及宏

### 2.1 glog的初始及其配置
```cpp
#include <glog/logging.h>

int main(int argc, char* argv[])
{
    // A.配置glog
    // configure 1, default, 不进行任何配置
    // 终端中不显示log信息，所有的log日志被保存在/tmp/*下

    // configure 2, 只配置它时只在终端中进行输出，此flag具有最高优先级
    FLAGS_logtostderr = true; 

    // configure 3, 只配置其时，不会在终端输出，将log保存在log_dir
    FLAGS_log_dir = "../"; 

    // configure 4, 同时在终端输出log信息，保存log信息，log信息的保存路径按照默认路径或者FLAGS_log_dir设置
    FLAGS_alsologtostderr = true;

    // B.初始化
    google::InitGoogleLogging(argv[0]);


    // C.LOG 输出
    // C.1 正常log输出, loglevel有 INFO/WARNING/ERROR/FATAL
    LOG(INFO) << "output 1";

    // C.2 只在dbug编译时进行输出， loglevel有 INFO/WARNING/ERROR/FATAL
    DLOG(WARNING) << "warning output 2";


    // D. VLOG

    // E. CHECK
    // Last
    google::ShutdownGoogleLogging();
}




```