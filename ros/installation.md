<!--
 * @Author: lexcalibur
 * @Date: 2021-12-30 13:19:02
 * @LastEditors: lexcaliburr
 * @LastEditTime: 2021-12-30 13:38:13
-->
# 因缺libeigen3-dev导致ros安装不上
### 问题：
直接装libeigen3-dev显示有安装最新版本  
sudo apt-get install libeigen3-dev
但是在安装ros时，又显示缺这个包
### 解决方法:
~~~sh
# 1.更新db
sudo updatedb

# 2.查看eigen3的文件
locate eigen3

# 2.1 结果如下
# /var/cache/apt/archives/libeigen3-dev_3.3.4-4_all.deb

# 3.手动安装eigen3
sudo dpkg -i /var/cache/apt/archives/libeigen3-dev_3.3.4-4_all.deb

# 4.安装成功后通过步骤1和步骤2检测是否安装成功

# 5.按照ros官网教程安装ros
~~~

# The 'rosdep==0.21.0' distribution was not found and is required by the application
通常是因为ros需要使用python2， 但是电脑默认的python为python3版本所导致
~~~sh
# 1. 列出所有python版本
update-alternatives --list python
# 2. 将python版本更换为pyton2
sudo update-alternatives --config python
# 3. 运行ros init
sudo rosdep init
~~~

# 安装jsk
~~~sh
sudo apt-get install ros-melodic-jsk-recognition-msgs
sudo apt-get install ros-melodic-jsk-rviz-plugins
~~~