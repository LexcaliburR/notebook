环境：本地及远程端ubuntu 18.04
需求：本地vscode ssh到远程端利用远程端环境进行开发

## 基本步骤
1. 本地安装remote ssh 插件
2. 本地配置ssh config
3. 本地生成ssh私钥公钥(optimal)
4. 将本地生成的公钥写入远程端机器(optimal)

### 完成前两个步骤已经可以通过vscode和ssh进行远程开发了，但是每次远程连接时都需要输入密码，完成步骤3和步骤4后连接时不需要输入密码

## 步骤1 本地安装remote ssh 插件
vscode中安装，操作略过

## 步骤2 本地配置ssh config
2.1 vscode中点击左侧远程资源管理器(图标为一个显示器，显示器右下角有个小圆圈)  
2.2 远程资源管理器的下拉选项选择为 SSH Targets
2.3 点击齿轮进行配置，会弹出一个command platte，通常选择第一个，路径如下
```
{USER_PATH}/.ssh/config
```
2.4 进入config，配置对应的值
```sh
Host alias               # 对应这台远程机器的名字，可以自定义设置
    HostName hostname    # 远程机器的连接地址，通常为ip地址或者网址
    User user            # 连接远程端，想在远程端登录的用户
    Port 22              # ssh端口，默认为22，如果远程端设置了转发，需要改为对应端口
    IdentityFile {USER_PATH}/.ssh/id_rsa   # 可选，当进行了步骤3后生成的私钥的地址
```

## 步骤3 本地生成ssh私钥公钥(optimal)
本地终端中输入
```
ssh-keygen
```
该命令在```~/.ssh/```路径下生成id_rsa（私钥）和id_rsa.pub(公钥)

## 步骤4 将本地生成的公钥写入远程端机器(optimal)
4.1 复制本地id_rsa.pub公钥的内容，可以通过cat、vim、vi等
4.2 通过终端ssh到远程端
```sh
# a. 连接
ssh -p {端口号} {USER}@ip
# b. 输入该User的密码
cd ~/.ssh
# c. 打开或者新建 authorized_keys
vim ./authorized_keys
# d. 粘贴之前copy的公钥
```
