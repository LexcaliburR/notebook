<!--
 * @Author: lexcalibur
 * @Date: 2021-12-21 16:47:52
 * @LastEditors: lexcaliburr
 * @LastEditTime: 2021-12-21 17:03:20
 * @reference： https://www.jianshu.com/p/987e95cc79f4
 * 16:48:55
-->
# 添加到工程
## 方法一：使用Jsoncpp包中的.cpp和.h文件（验证）

- 解压上面下载的jsoncpp-master.zip文件，把jsoncpp-master\include\json文件夹和jsoncpp-master\src\lib_json文件夹里的全部文件拷贝到工程目录下，并且添加到到VS工程中。
- 在需要使用JsonCpp的文件中包含json头文件即可，如：#include "json/json.h"。另外，需要将json_reader.cpp、json_value.cpp和json_writer.cpp三个文件的Precompiled Header属性设置为Not Using Precompiled Headers，否则编译会出现错误。

## 方法二：Amalgamated（验证）

- 运行Amalgamated source脚本
- copy dist下的.h/.cpp文件到项目工程

## 方法三：使用Jsoncpp生成的lib文件（未验证）

- 解压上面下载的jsoncpp-master.zip文件，在jsoncpp-master\makefiles\vs71目录里找到jsoncpp.sln，用VS编译，默认生成静态链接库。 在工程中引用，只需要包含include/json下的头文件及生成的.lib文件即可。
- 在需要使用JsonCpp的文件中添加#pragma comment(lib."json_vc71_libmt.lib")，在工程属性中Linker下Input中Additional Dependencies写入lib文件名字（Release下为json_vc71_libmt.lib，Debug为json_vc71_libmtd.lib）注意：Jsoncpp的lib工程编译选项要和VS工程中的编译选项保持一致。如lib文件工程编译选项为MT（或MTd），VS工程中也要选择MT（或MTd），否则会出现编译错误问题。

# 使用详情
JsonCpp 主要包含三种类型的 class：Value、Reader、Writer。JsonCpp 中所有对象、类名都在 namespace Json 中，包含 json.h 即可。  
Json::Value 只能处理 ANSI 类型的字符串，如果 C++ 程序是用 Unicode 编码的，最好加一个 Adapt 类来适配。

- 通过字符串创建Json对象
```cpp
std::string strValue = “{\”key\”:\”value1\”,\
\”array\”:[{\"arraykey\":1},{\"arraykey\":2}]}”; 

Json::Reader reader; 
Json::Value root; 
// reader将Json字符串解析到root，root将包含Json里所有子元素
if (reader.parse(strValue, root))   
{ 
   if (!root["key"].isNull())
   {
    std::string strValue= root["key"].asString(); 
    std::cout << strValue<< std::endl; 
  }
  Json::Value arrayObj = root["array"]; 
  for (int i=0; i<arrayObj.size(); i++) 
  { 
    int iarrayValue = arrayObj[i]["arraykey"].asInt(); 
    std::cout << iarrayValue << std::endl;  
  } 
}

```
- 构建Json对象序列化为字符串
```cpp
Json::Value root; 
Json::Value arrayObj;
Json::Value item; 

root["key"] = “value1″; 
for (int i=0; i<10; i++)
{ 
  item["arraykey"] = i; 
  arrayObj.append(item);  //添加新的数组成员
} 
root["array"] = arrayObj; 
std::string out = root.toStyledString();  //将Json对象序列化为字符串
std::cout << out << std::endl;

```
- 向文件中插入Json对象
```cpp
void WriteJsonData(const char* filename)
{    
  Json::Reader reader;
  Json::Value root;
  ifstream is;
  is.open(filename, std::ios::binary);
  if (reader.parse(is, root, FALSE))
  {
    Json::Value item; 

    root["key"] = “value1″; 
    //添加数组成员
    item["arraykey"] = 2; 
    root["array"].append(item)

    Json::FastWriter writer;
    string strWrite = writer.write(root);
    ofstream ofs;
    ofs.open(filename);
    ofs << strWrite;
    ofs.close();
  }
  is.close();  
}

```
- 清空Json对象中的数组
```cpp
root["array"].resize(0);
```
- 删除Json对象
```cpp
root.removeMember("key");
```