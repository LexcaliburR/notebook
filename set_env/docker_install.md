

# 1.1简单版安装docker
```sh
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun

DIST=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$DIST/libnvidia-container.list | \
  sudo tee /etc/apt/sources.list.d/libnvidia-container.list
sudo apt-get update
```
# 1.2从repo安装doker
```sh
sudo apt-get install nvidia-container-toolkit  
sudo apt-get install nvidia-container-runtime  

sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo docker run hello-world
```

# 2.修改docker使用要加sudo
```sh
cat /etc/group | grep docker  
# 如果打印出东西，跳过这一步  
sudo groupadd docker  
# 添加用户到docker分组  
sudo usermod -aG docker [username]  
```
**查看是否生效**  
cat /etc/group  
**重启docker**  
sudo systemctl restart docker  
**给docker.sock添加权限**  
sudo chmod a+rw /var/run/docker.sock


# 3.修改docker images的保存路径
sudo service docker stop  
修改/etc/docker/daemon.json为如下内容,注意无空格
```sh
{"data-root":"/home/lexcalibur/HDD1/docker"}
```
sudo service docker start 或者 reboot

```sh
docker info # 查看是否已经改变
```



# 4.卸载docker
sudo service docker start/stop

sudo apt-get purge docker-ce
sudo apt-get remove docker docker-engine docker.io containerd runc

sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd