```cpp
// Example program
#include <iostream>
#include <string>
#include <memory>

struct A {
    int element1;
    int element2 = 0;
    std::shared_ptr<int> element3;
    std::shared_ptr<int> element4 = std::make_shared<int>(1);
};
    
int main()
{
    A a;
    std::cout << "element2:  " << a.element2 << std::endl;
    std::cout << "element1:  " << a.element1 << std::endl;
    std::cout << "element4:  " << *a.element4 << std::endl;
    if (a.element3)
    {
        std::cout << "element3:  " << *a.element3 << std::endl;
    }
    else {
        std::cout << "element3 is False/Null" << std::endl;
    }
}
```

```shell
element2:  0
element1:  1
element4:  1
element3 is False/Null
```
