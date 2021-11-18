<!--
 * @Author: lishiqi
 * @LastEditors: lishiqi
-->

1. 运行docker
docker run -it -v {path_to_mount}:{path_in_docker} {docker image name} /bin/bash
2. 离线保存加载docker
docker save -o {savepath}/xxx.tar {docker image name}
docker load --input {IMAGE_FILE_PATH}