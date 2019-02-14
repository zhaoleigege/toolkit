# ubuntu相关命令

#### 删除下载应用程序

```shell
sudo apt-get remove packagename 或者 sudo apt-get --purge remove package-name

sudo apt-get purge packagename 或者 sudo apt-get remove --purge packagename

sudo apt-get autoremove

sudo aptitude remove packagename 或者 sudo aptitude purge packagename
```

#### 安装更新出错时执行以下命令恢复

```shell
sudo apt install -y -f dpkg

sudo apt -y autoremove
```

#### 安装ssh-server

ubuntu默认安装了ssh-client，但是没有安装ssh-server，通过一下命令安装ssh-server

```shell
# 下载openssh-server
sudo apt-get install -y openssh-server
# 启动ssh-server服务
sudo /etc/init.d/ssh start
# 查看是否启动成功
ps -e | grep ssh

# 配置ssh-server
cd /etc/ssh
vi sshd_config
# 去掉Port、ListenAddress、PermitRootLogin、PasswordAuthentication前的 # 符号
```

#### 安装deb包

```shell
dpkg -i xxxx.deb
```

