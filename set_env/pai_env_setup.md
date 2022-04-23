<!--
 * @Author: L.
 * @Date: 2022-04-23 15:41:04
 * @LastEditTime: 2022-04-23 15:53:17
 * @LastEditors: Please set LastEditors
 * @Description: 
 * @FilePath: /notebook/set_env/pai_env_setup.md
-->

# 1. set pip/conda/apt source

condarc/pip.conf/source.list 在user/xxx/目录下

condarc/pip.conf cp到/root目录下

source.list 复制到/etc/apt/目录下


# 2. jupyter-lab 中添加anaconda kernel
a. 激活虚拟环境安装ipykernel  
`pip install ipykernel`  

b. 在jupyter添加环境  
`python -m ipykernel install --name {环境变量名称} --display-name "{jupyter 中显示的名称}"`  

c. 如果在jupyter中激活kernel时显示无权限，可能是anaconda安装在了root下  
```sh
sudo su # 取得管理员
cd / # 进入根目录
chmod +x ./root # 给root添加可执行权限，注意不可使用777等，避免未知错误
```


