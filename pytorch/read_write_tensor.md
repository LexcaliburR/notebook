# python 读， python写




# cpp读，cpp写

```cpp
torch::Tensor data = torch::randn((3, 4));
torch::save(data, path);
torch::Tenosr read;
torch::read(read, path)
std::cout << read << std::endl;
```

# cpp写，python读
```cpp
torch::Tensor data = torch::randn((3, 4));
torch::save(data, path);
```


```python
import torch
data = torch.load(path)
for d in data.parameters():
    readed = d;
print(readed)

```

