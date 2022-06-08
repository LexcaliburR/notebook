# c_cpp_properties.json配置
通过配置includePath和defines可以在vscode中正常显示库文件
```json
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
            ],
            "defines": [],
            "compilerPath": "/usr/bin/gcc",
            "cStandard": "c11",
            "cppStandard": "gnu++14",
            "intelliSenseMode": "linux-gcc-x64"
        }
    ],
    "version": 4
}
```

# 自动格式化 .clang-format
```json
Language: Cpp
BasedOnStyle: Google

# 访问说明符(public、private等)的偏移
AccessModifierOffset: -4

# 构造函数的初始化列表的缩进宽度
ConstructorInitializerIndentWidth: 4

# 延续的行的缩进宽度
ContinuationIndentWidth: 4

# 缩进宽度
IndentWidth: 4

# 连续空行的最大数量
MaxEmptyLinesToKeep: 1

# tab宽度
TabWidth: 4

ColumnLimit: 80

BreakBeforeBraces: Custom
# 大括号换行，只有当BreakBeforeBraces设置为Custom时才有效
BraceWrapping:
  # class定义后面
  AfterClass: true
  # 控制语句后面
  AfterControlStatement: false
  # enum定义后面
  AfterEnum: false
  # 函数定义后面
  AfterFunction: true
  # 命名空间定义后面
  AfterNamespace: false
  # struct定义后面
  AfterStruct: true
  # union定义后面
  AfterUnion: true
  # extern之后
  AfterExternBlock: false
  # catch之前
  BeforeCatch: false
  # else之前
  BeforeElse: false
  # 缩进大括号
  IndentBraces: false
  # 分离空函数
  SplitEmptyFunction: false
  # 分离空语句
  SplitEmptyRecord: false
  # 分离空命名空间
  SplitEmptyNamespace: true

# false表示函数实参要么都在同一行，要么都各自一行
BinPackArguments: false

# false表示所有形参要么都在同一行，要么都各自一行
BinPackParameters: true

# 总是在多行string字面量前换行
AlwaysBreakBeforeMultilineStrings: false

# 总是在template声明后换行
AlwaysBreakTemplateDeclarations: true

# 允许排序#include
SortIncludes: false

# 允许重新排版注释
ReflowComments: true

# 指针和引用的对齐: Left, Right, Middle
DerivePointerAlignment: false
PointerAlignment: Left

# 命名空间的缩进: None, Inner(缩进嵌套的命名空间中的内容), All
NamespaceIndentation: None

#EscapeNewlineAlignmentStyle: ENAS_DontAlign
```