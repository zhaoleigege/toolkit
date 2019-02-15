# centos安装

1. 下载centos最小版

   ```shell
   https://www.centos.org/download/
   # 点击Minimal ISO然后检索huawei，下载华为云的镜像
   ```

2. 写入iso镜像到U盘中

   ```shell
   sudo fdisk -l 	# 查找U盘在系统的挂载点
   sudo dd bs=4M if=.../CentOS-7-x86_64-Minimal-1810.iso of=/dev/sdb	# iso写入到u盘中
   ```

3. 插入裸机中安装机器(**语言选择english**)

**以下命令除非特别说明都是在root权限下执行的**

1. ip地址设置

   由于裸机安装的centos7没有开启自动获取ip地址的功能，所以我们需要配置ip地址自动获取功能。

   ```shell
   cd /etc/sysconfig/network-scripts
   ls # 查看网卡的名称
   vi ifcfg-enp3s0 # 视情况定
   ```

   使用以下配置先获得自动分配的ip地址等信息

   ```shell
   ONBOOT=yes # 修改为开机使用此配置
   ```

    ```shell
   service network restart # 重启网络服务
   ip addr # 查看ip地址
    ```

   **配置静态IP**

   ```
   vi ifcfg-enp3s0 # 视情况定
   ```

   ```shell
   BOOTPROTO=static # 修改为静态ip地址
   IPADDR=192.168.124.135 # 静态IP
   GATEWAY=192.168.124.1 # 默认网关
   NETMASK=255.255.255.0 # 子网掩码
   DNS1=192.168.0.6 # DNS 配置
   ```

   上诉相关参数的获取可以参考[coreOS设置静态ip](../../集群/coreOS/coreOS安装.MD)的章节

   ```shell
   service network restart # 重启网络服务
   ip addr # 查看ip地址
   ```

   ```shell
   ping www.baidu.com # 测试是否设置成功
   ```

2. [配置ssh](./centos7配置SSH.md)

3. 安装完成后查看基本的设置

   * 时区信息

     ```shell
     timedatectl
     ```

4. 设置yum源的地址

   ```shell
   cd /etc/yum.repos.d
   mv CentOS-Base.repo CentOS-Base.repo-copy
   curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
   yum clean all
   yum makecache
   ```

5. 基本开发环境的配置

   1. 安装docker

      ```shell
      # 添加yum软件源
      sudo yum-config-manager --add-repo https://mirrors.ustc.edu.cn/docker-ce/linux/centos/docker-ce.repo
      # 执行以下命令安装依赖
      sudo yum install -y yum-utils device-mapper-persistent-data lvm2
      
      # 更新yum源
      sudo yum makecache fast
      # 下载docker
      sudo yum install docker-ce
      
      # 启动docker
      sudo systemctl enable docker
      sudo systemctl start docker
      
      # 建立docker用户组
      sudo groupadd docker
      # 添加当前用户到docker组中（该命令可以不是root账户）
      sudo usermod -aG docker $USER # 在root账户下，可以把$USER替换为没有root权限的别的账户，如
      # sudo usermod -aG docker buse
      
      # 测试docker是否安装成功
      docker run hello-world
      ```

   2. 下载docker-compose

      ```shell sudo curl -L https://github.com/docker/compose/releases/download/1.17.1/docker-compose-`uname -s`-`uname -m` &gt; /usr/local/bin/docker-compose
      curl -L https://github.com/docker/compose/releases/download/${version}/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
      # ${version}前往https://github.com/docker/compose/releases/ 查看并自行选择
      sudo chmod +x /usr/local/bin/docker-compose
      ```

      查看docker-compose版本

      ```shell
      docker-compose --version
      ```

   3. 下载git

      ```shell
      sudo yum install git
      
      git --version
      ```

   4. 下载java

      ```shell
      curl -o java.tar.gz https://download.java.net/java/GA/jdk11/9/GPL/openjdk-${version}_linux-x64_bin.tar.g
      # 版本查看官网https://jdk.java.net/11/
      tar -xvf java.tar.gz
       mv jdk-${version}/ java
       echo "export PATH=$PATH:/home/das/java/bin" >> .bashrc
      ```

   5. 下载maven

      ```shell
      curl -o maven.tar.gz http://mirrors.hust.edu.cn/apache/maven/maven-3/${version}/binaries/apache-maven-3.6.0-bin.tar.gz
      # 版本查看官网https://maven.apache.org/download.cgi
      tar -xvf maven.tar.gz
      mv apache-maven-${version}/ maven
      echo "export PATH=$PATH:/home/das/maven/bin" >> .bashrc
      ```

      maven相关配置请查看[这里](https://github.com/zhaoleigege/java/tree/master/doc/maven)

   使得上述配置文件生效

   ```shell
    source .bashrc
    
    # 查看配置是否正确
    java -version
    mvn -v
   ```


#### 参考资料

* [LINUX 下刻录iso到u盘](https://www.jianshu.com/p/177a78770d0a)
* [设置yum源](https://www.jianshu.com/p/541c737bc947)