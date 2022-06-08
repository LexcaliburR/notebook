<!--
 * @Author: Lexcaliburr lishiqi0111@gmail.com
 * @Date: 2022-05-24 20:16:30
 * @LastEditors: Lexcaliburr lishiqi0111@gmail.com
 * @LastEditTime: 2022-05-24 20:20:28
 * @FilePath: /notebook/bug记录/onnx.ModelProto_has_no_field_named_version.md
 * @Description: 
-->

### 描述
使用tensorrt加载onnx权重生成engine时报错
```sh
Error parsing text-format onnx.ModelProto: 1:9: Message type "onnx.ModelProto" has no field named "version"
```

### 原因
当权重文件为git submodule时，拉取权重文件会出错，拉下来的只是几百k的文件

### 解决方法
重新拉取正确的权重即可