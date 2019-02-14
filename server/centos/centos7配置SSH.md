# centos7配置SSH

​	使用centos Minimal版本，是最干净的centos发行版，没有任何别的附加功能，但是为了能够远程操作centos系统，我们需要配置SSH服务。

1. 安装ssh-server

   centos Minimal系统中已经安装好了SSH服务但是没有启动，可以通过以下命令查看系统中的SSH服务（这里指SSH-server和SSH-client）是否安装。

   ```shell
   # 查看是否有ssh-server服务
   yum list installed | grep openssh-server
   ```

   ![1540371778(./1540371778(1).png)](./1540371778(1).png)

   ​	显示如上图所示则有安装，否则执行如下命令安装

   ```shell
   # 安装ssh-server服务
   yum install openssh-server
   ```

2. 配置ssh-server

   ```shell
   cd /etc/ssh
   vi sshd_config
   # 去掉Port、ListenAddress、PermitRootLogin、PasswordAuthentication前的 # 符号
   ```

   保存修改并退出

3. 开启sshd服务

   ```shell
   # 开启sshd服务
   service sshd start
   # 检查sshd服务是否已经开启
   ps -e | grep sshd
   # 查看22号端口是否开启监听
   netstat -an | grep 22
   
   # 开机自启动ssh-server
   systemctl enable sshd.service
   # 查看是否开启了sshd服务自启动
   systemctl list-unit-files | grep sshd
   ```

4. 错误处理

   * 执行查看查看22号端口是否开启时会遇到 `command not found` 的错误，这是因为Minimal版本的centos不包含大部分的网路套件，执行以下命令下载相关包。

     ```shell
     yum install net-tools
     ```

     * 执行上一步时可能出现 `cannot find a valid baseurl for repo: ... ` 的错误，这个错误出现的原因是是虚拟机配置时网路设置为 `桥接模式` ，更改为`网络地址转换(NAT)` 即可，但是这样的的主机是访问不到虚拟机的，所以需要采取别的做法。<span style="color: red"> 待补</span>

5. 主机访问虚拟机的ssh-server服务

   ```shell
   # 其中root为用户名 192.168.123.61为虚拟机的ip地址
   ssh root@192.168.123.61
   ```

   