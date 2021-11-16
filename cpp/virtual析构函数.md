```cpp
class BaseExample {
public:
    BaseExample()
    virtual ~BaseExample()
}

```
因为当基类指针指向实现类的对象时，会首先调用基类的方法，如果不将基类的析构函数写为虚函数，会导致析构时调用父类的函数
