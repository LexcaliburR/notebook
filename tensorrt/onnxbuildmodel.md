<!--
 * @Author: Lexcalibur
 * @Date: 2021-12-19 23:24:56
 * @LastEditors: Lexcalibur
 * @LastEditTime: 2022-01-16 11:50:42
 * @FilePath: /notebook/tensorrt/onnxbuildmodel.md
-->

## 1.初始化Plugin
```cpp
initLibNvInferPlugins(&trtCommon::gLogger, "");
```
## 2. Create build
在初始化builder/refitter/runtime时，都需要传入ILogger,log的等级可以通过`setReportableSeverity(Severity severity)`成员方法设置
```cpp
auto builder = TRTUniquePtr<nvinfer1::IBuilder>(nvinfer1::createInferBuilder(trtCommon::gLogger.getTRTLogger()));
if (!builder)
{
    return false;
}
```
## 3. Create network
- createNetworkV2可以设置动态维度
- 而动态维度的设置需要设置Flag，kEXPLICIT_BATCH
- INetworkDefinition，定义了网络的结构，通过IBuild在engine中构建，network要么隐式的有个batch dimensions（如[3, 800, 600]作为输入） 要么在运行过程中给显示的dimentions(必须[1, 3, 800, 600]作为输入)。

```cpp
const auto explicitBatch = 1U << static_cast<uint32_t>(NetworkDefinitionCreationFlag::kEXPLICIT_BATCH);
auto network = TRTUniquePtr<nvinfer1::INetworkDefinition>(builder->createNetworkV2(explicitBatch));
if (!network)
{
    return false;
    }
```
## 4. Create IBuilderConfig
config配置了builder生成engine的的所有特性
```cpp
auto config = TRTUniquePtr<nvinfer1::IBuilderConfig>(builder->createBuilderConfig());
if (!config)
{
    return false;
}
```

## 5. Create Parser
- 解析onnx模型，用于生成tensorRT network
- 在debug时，可以通过`parseFromFile(const char* onnxModelFile, int verbosity)`
```cpp
auto parser
    = TRTUniquePtr<nvonnxparser::IParser>(nvonnxparser::createParser(*network, trtCommon::gLogger.getTRTLogger()));
if (!parser)
{
    return false;
}
```

## 6. load onnx model file and construct network
- 设置网络网络的优化方式，如fp32，fp16，dla等
- 设置模型推理时gpu可使用的最大gpu 内存，这个内存的大小影响优化engine时所选择的算法，另一方面限制同时运行的gpu程序，1gb的内存足够使用所有的算法
- 设置dla，dla为深度学习加速器，
- 设置max batchsieze，这个值为推理时能用到的最大的batchsize，同样也是优化engine时的目标batchsize
```cpp
auto constructed = constructNetwork(builder, network, config, parser);
if (!constructed)
{
    return false;
}


bool SampleOnnxMNIST::constructNetwork(SampleUniquePtr<nvinfer1::IBuilder>& builder,
    SampleUniquePtr<nvinfer1::INetworkDefinition>& network, SampleUniquePtr<nvinfer1::IBuilderConfig>& config,
    SampleUniquePtr<nvonnxparser::IParser>& parser)
{
    auto parsed = parser->parseFromFile(locateFile(mParams.onnxFileName, mParams.dataDirs).c_str(),
        static_cast<int>(sample::gLogger.getReportableSeverity()));
    if (!parsed)
    {
        return false;
    }

    config->setMaxWorkspaceSize(16_MiB);
    if (mParams.fp16)
    {
        config->setFlag(BuilderFlag::kFP16);
    }
    if (mParams.int8)
    {
        config->setFlag(BuilderFlag::kINT8);
        samplesCommon::setAllDynamicRanges(network.get(), 127.0f, 127.0f);
    }

    samplesCommon::enableDLA(builder.get(), config.get(), mParams.dlaCore);

    return true;
}

```

## 7. createOptimizationProfile
- 从builder创建，与builder绑定
- 从builder返回一个原始指针，不需要释放这个指针
- 如果有动态维度则必须要设置

```cpp



```

## 7. setOptimizationProfile
Optimization Profile主要服务于动态的输入shape和dim。当输入有动态维度(如输入的某个维度为-1)时，用户需要定义一个profile，profile按照index0， 1， 2， 3 的序列排序。  

tensorrt默认自定一个index为0的profile，当没有显式的选择profile时，系统会自动徐纳则这个index0的profile，如果输入没有动态维度，系统也会自动调用这个profile。这个profile定义了动态维度的最小值，最大值和最优值，builder则会根据profile以最小化运行时间的准则选择核函数。

- 必须要运行3次，分别设置最小值，最大值，最优值
- 如果启用了DLA，最小dim，最优dim，最大dim必须要相同

**注意： 如果开启了DLA，最小值，最优值和最大值必须一样**
```cpp



```

    // CUDA stream used for profiling by the builder.
    auto profileStream = trtCommon::makeCudaStream();
    if (!profileStream)
    {
        return false;
    }
    config->setProfileStream(*profileStream);

    m_engine_ = std::shared_ptr<nvinfer1::ICudaEngine>(
        builder->buildEngineWithConfig(*network, *config), trtCommon::InferDeleter());
    if (!m_engine_)
    {
        return false;
    }

    assert(network->getNbInputs() == 1);
    m_inputDims_ = network->getInput(0)->getDimensions();
    assert(m_inputDims_.nbDims == 4);

    assert(network->getNbOutputs() == 1);
    m_outputDims_ = network->getOutput(0)->getDimensions();
    assert(m_outputDims_.nbDims == 2);

    return true;
