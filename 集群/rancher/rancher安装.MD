# rancher2.x安装

1. 选择一个coreOS系统作为rancher server

   ```shell
   sudo docker run -d --restart=unless-stopped \
   -p 80:80 -p 443:443 \
   -v ${rancherAddr}:/var/lib/rancher \
   -v ${logAddr}:/var/log/auditlog \
   rancher/rancher:stable
   ```


2. 配置rancher server

   在浏览器中打开配置有rancher server地址的服务的80端口，第一次登录需要配置基本信息。

   1. 创建初始密码
   2. 设置rancher server URL
   


3. 配置rancher client
  
    在rancher client中设置docker开机自启动
    
    ```shell
    # 设置开机自启动
    sudo systemctl enable docker
    
    # 启动docker
    sudo systemctl start docker
    
    # 添加docker到用户组以便开机有权限启动
    sudo usermod -aG docker zhaolei
    
    # 重启生效配置
    sudo shutdown -r now
    
    # 查看docker是否启动
    sudo systemctl status docker
    ```

#### 参考资料

* [rancher官网快速入门](https://www.cnrancher.com/docs/rancher/v2.x/cn/overview/quick-start-guide/)
* [rancher2.1安装部署](http://www.cnblogs.com/xzkzzz/p/9995956.html)

