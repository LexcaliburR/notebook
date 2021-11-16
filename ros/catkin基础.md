# catkin_make 的三种编译方式
1. 编译工作空间下的所有功能包
```sh
catkin_make
```

2. 编译工作空间下的指定功能包
```sh
catkin_make -DCATKIN_WHITELIST_PACKAGES=”package1;package2“
```

3. 编译工作空间下的指定功能包
```sh
catkin_make --pkg package_name
```

**注: package_name在每个工作包的package.xml下找，如下所示：**
```xml
<?xml version="1.0"?>
<package format="2">
  <name>lane_pub</name>   # package name
  <version>0.0.0</version>
```