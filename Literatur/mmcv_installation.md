1. 安装cudatoolkit
2. 安装pytorch/torchision等
3. 安装mmcv
   - pip install openmim
   - mim install mmcv-full
4. 安装mmdet
   - mim install mmdet
5. 安装mmsegmentation
   - mim install mmsegmentation
6. base环境中更新cudatoolkit
7. 安装mmdet3d
   - cd mmdetection3d
   - pip install -v -e .


debug：
1. 查看当前torch使用的cuda版本
   - print(torch.version.cuda)