<!--
 * @Author: Lexcalibur
 * @Date: 2022-01-16 11:53:47
 * @LastEditors: Lexcalibur
 * @LastEditTime: 2022-01-16 13:38:55
 * @FilePath: /notebook/tensorrt/createNetwork.md
-->

# CreateNetwork

nvinfer1::INetworkDefinition* nvinfer1::IBuilder::createNetworkV2(NetworkDefinitionCreationFlags flags)  

通过Flag指定期望建立的网络的格式,有两种选择
- kDEFAULT,默认设置，此时起到createNetwork()函数的功能
- kEXPLICIT_BATCH 

# CreateNetwork vs CreateNetworkV2

## CreateNetwork
老版本的api，不支持动态维度(dynamic shapes)

## CreateNetworkV2
新版本的api，支持动态输入，动态batch size；但是在创建网络时，需要显示的指定flag。使用时需要注意如下要求
- 定义flag
- 添加optimizationProfile  


当使用动态维度的时候，engine有如下特性
- ICudaEngine::hasImplicitBatchDimension 返回false

# example

```cpp
// A 动态维度/CreateNetworkV2
// A.1 CreateNetworkV2
auto preprocessorNetwork = makeUnique(
    builder->createNetworkV2(1U << static_cast<uint32_t>(NetworkDefinitionCreationFlag::kEXPLICIT_BATCH)));
if (!preprocessorNetwork)
{
    sample::gLogError << "Create network failed." << std::endl;
    return false;
}

// A.2 设置动态维度
// A.2.1 添加输入层, 模型要求的图片输入形状为[1, 1, 28, 28], NCWH， 
// 指定NWH为动态的,
auto input = preprocessorNetwork->addInput("input", nvinfer1::DataType::kFLOAT, Dims4{-1, 1, -1, -1});

auto preprocessorConfig = makeUnique(builder->createBuilderConfig());
// A.2.2 创建profile
auto profile = builder->createOptimizationProfile();
// A.2.3 设置profile
// - 如下设置，起到的作用为，图片输入尺寸为[(1, 1, 1, 1), (1, 1, 56, 56)] 范围
// - tensorrt会以(1, 1, 28, 28)的输入优化模型
profile->setDimensions(input->getName(), OptProfileSelector::kMIN, Dims4{1, 1, 1, 1});
profile->setDimensions(input->getName(), OptProfileSelector::kOPT, Dims4{1, 1, 28, 28});
profile->setDimensions(input->getName(), OptProfileSelector::kMAX, Dims4{1, 1, 56, 56});
preprocessorConfig->addOptimizationProfile(profile);
```


