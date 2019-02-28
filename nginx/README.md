# nginx

负载均衡是在大量客户端的请求情况下，后台有多台服务器共同处理这些请求，避免请求全部由一台服务器承受，这样可以提高服务器的请求量。

反向代理是指接受客户端请求的地址和实际处理该请求的服务器地址不一定一样，而是通过一定的转发方式派发给别的服务器处理，达到隐藏真实服务器地址和分流的作用。

在nginx中我们可以使用反响代理技术把客户端的请求分发给后台的多台服务器以达到负载均衡的目的。

**本文是基于使用wrk进行压力测试时出现`Non-2xx or 3xx responses`错误而找到的解决方法汇成的记录**

1. nginx安装

   请查看在[centos中配置nginx](./nginx在centos下的配置.md)

2. nginx配置

   * 因为nginx接受客户端的请求时是需要消耗`file discriptor(fd，文件描述符)`，所以我们需要配置系统的最大文件打开数。当出现`socket() failed (24: Too many open files) while connecting to upstream`错误时可以使用此方法解决

     设置nginx的最大文件打开数

     ```shell
     # 使用shell脚本查看nginx每个进程可以打开的最大文件数
     for pid in `ps aux |grep nginx |grep -v grep|awk '{print $2}'`
     do
     cat /proc/${pid}/limits |grep 'Max open files'
     done
     ```

     * 非centos系统

       ```shell
       # 1. 使用上诉命令查看nginx每个进程可以打开的最大文件数
       
       # 2. 编辑/etc/sysctl.conf文件设置最大文件打开数
       vi /etc/sysctl.conf
       fs.file-max = 500000 # 添加到最后一行
       
       # 3. 编辑/etc/security/limits.conf
       vi /etc/security/limits.conf
       # 添加到最后一行
       nginx soft nofile 500000
       nginx hard nofile 500000
       
       # 4.执行重载命令
       sysctl -p
       
       # 5. 添加最大文件限制数到/etc/nginx/nginx.conf文件中
       vi /etc/nginx/nginx.conf
       	worker_rlimit_nofile 500000; # 添加该项
       
       # 6. 重启nginx
       nginx -s reload;
       	# 使用1的方法查看是否改变成功，如果不成功执行以下命令
       	nginx -s quit
       		# 要是不行就kill掉nginx进程
       		kill -9 $(ps aux |grep nginx |grep -v grep|awk '{print $2}')
       		systemctl start nginx.service # 开启nginx进程
       ```

     **在centos中使用上述方式时会出现`setrlimit(RLIMIT_NOFILE, 2342) failed (13: Permission denied)`的错误，在centos中配置nginx最大文件的方法如下**

     ```shell
     # 查看最大连接数
     cat /proc/$(cat /var/run/nginx.pid)/limits|grep open.files
     
     # 查看错误信息
     tail -s 10 /var/log/nginx/error.log
     # setrlimit(RLIMIT_NOFILE, 120000) failed (13: Permission denied)
     # ....
     
     # 1.创建一个系统服务目录给nginx
     mkdir /etc/systemd/system/nginx.service.d
     # 2. 编辑如下文件并添加最大连接数
     vi /etc/systemd/system/nginx.service.d/nofile_limit.conf
     
     	[Service]
     	LimitNOFILE=500000
     # 3. 添加最大文件限制数到/etc/nginx/nginx.conf文件中
     vi /etc/nginx/nginx.conf
     	worker_rlimit_nofile 500000;
     	
     # 4. 重启服务以生效
     systemctl daemon-reload
     systemctl restart nginx.service
     
     # 5. 验证设置成功
     cat /proc/$(cat /var/run/nginx.pid)/limits|grep open.files
     ```

     

   * nginx单个线程的最大连接数(`worker_connections`)为1024，这里我们可以把它设置成10W，而nginx总的最大连接数为`worker_processes * worker_connections `，而设置`worker_processes`时一般设为服务器的cpu核心数。

     ```shell
     worker_processes 12;
     ...
     events {
         use epoll;
         worker_connections 100000;
     }
     ```

   * nginx设置反响代理时默认为http1.0，而这是短连接，我们需要把它设置为长连接，即需要在`upstream`中添加`keepalive`，并且设置`proxy_http_version`为http1.1。

     ```shell
     upstream backend {
         server 127.0.0.1:8000 max_fails=0;
         server 127.0.0.1:8001 max_fails=0;
         keepalive 1024; # 设置长连接池的大小
     }
     
     ...
     server {
             listen      0.0.0.0:8080 default_server;
     
             location / {
                 proxy_http_version 1.1;
                 proxy_pass http://backend;
                 ...
             }
     }
     ```

3. 操作系统参数配置

   * 配置服务器可以打开的文件数

     ```shell
     ulimit -a # 查看open files的值
     
     vi /etc/security/limits.conf
     
     # 添加如下内容
     * soft nofile 65536
     * hard nofile 65536
     
     # 重启就可以看到效果
     ```

   * 设置IP连接时端口的范围

     ```shell
     sysctl net.ipv4.ip_local_port_range # 查看端口范围
     
     #编辑该文件设置端口范围
     vi /etc/sysctl.conf
     
     # 在文件最后添加新的端口范围
     net.ipv4.ip_local_port_range = 1024 65535
     ```

4. nginx.conf配置示例

   ```shell
   user nginx;
   worker_processes 1; # 实际时用系统的逻辑cpu核心数替换
   error_log /var/log/nginx/error.log; # 错误日志开启好定位问题
   pid /run/nginx.pid;
   
   worker_rlimit_nofile 500000; # 设置nginx可以开启的最大文件数
   
   include /usr/share/nginx/modules/*.conf;
   
   events {
       use epoll;   # nginx使用epoll I/O模式
       worker_connections 100000; # 每个线程的连接数
   }
   
   http {
       log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                         '$status $body_bytes_sent "$http_referer" '
                         '"$http_user_agent" "$http_x_forwarded_for"';
   
       access_log  /var/log/nginx/access.log  main; # 访问日志开启
   
       sendfile            on;
       tcp_nopush          on;
       tcp_nodelay         on;
       keepalive_timeout   65;
       types_hash_max_size 2048;
   
       include             /etc/nginx/mime.types;
       default_type        application/octet-stream;
   
       # Load modular configuration files from the /etc/nginx/conf.d directory.
       # See http://nginx.org/en/docs/ngx_core_module.html#include
       # for more information.
       include /etc/nginx/conf.d/*.conf; # 读取自定义配置文件的位置
   
       # 设置反向代理
       upstream backend { 
          least_conn; # nginx派发请求给服务器的算法
          server 127.0.0.1:8000;
          # max_fails=0;
          server 127.0.0.1:8001;
          # max_fails=0;
          keepalive 512; # 长连接池大小
       }
   
       server {
           listen      0.0.0.0:8080 default_server; # nginx监听8080端口
   
           location / {
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
              proxy_cache_bypass $cookie_nocache $arg_nocache $arg_comment;
              proxy_cache_bypass $http_pragma $http_authorization;
              proxy_no_cache $cookie_nocache $arg_nocache $arg_comment;
              proxy_no_cache $http_pragma $http_authorization;
              proxy_http_version 1.1;
              proxy_read_timeout 180;
              
              proxy_pass http://backend; # 方向代理
           }
       }
   }
   ```

**<span style="color: red;">出现这些问题的主要原因是，把nginx和两个tomcat进程部署在了同一台服务器，这样测试nginx时会让nginx再创建大量socket连接请求tomcat的进程，进而导致系统的文件数使用过多。由此得出，系统上线时不应该在同一台服务器上即部署nginx又部署多个tomcat进程，尽量nginx和tomcat进程分布在不同的机器上。</span>**

#### 参考资料

* [网站集群搭建的博文](https://www.cnblogs.com/youzhibing/category/743343.html)
* [借助nginx搭建反响代理服务器](https://www.cnblogs.com/edisonchou/p/4126742.html)
* [Tuning NGINX for Performance](https://www.nginx.com/blog/tuning-nginx/)     **nginx官网给出的调优方案**
* [记一次压测引起的nginx负载均衡性能调优](./http://xiaorui.cc/2016/06/26/%E8%AE%B0%E4%B8%80%E6%AC%A1%E5%8E%8B%E6%B5%8B%E5%BC%95%E8%B5%B7%E7%9A%84nginx%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98/)  **推荐**
* [Nginx错误汇总](https://corejava2008.iteye.com/blog/2202076)   **参考了这里配置连接端口的大小**
* [ulimit到底谁说了算?](http://blog.ihipop.info/2011/01/2053.html)    **参考了查看nginx可以打开的最大文件数的脚本**
* [配置nginx最大连接数](https://gist.github.com/joewiz/4c39c9d061cf608cb62b)
* [How to Solve CentOS 7 raise nofile limit for Nginx](https://caradede.blogspot.com/2017/12/how-to-solve-centos-7-nofile-limit-nginx.html)   **真正解决centos设置nginx最大文件打开数的方法**
* [nginx TIME_WAIT优化](https://zhuanlan.zhihu.com/p/54473742)
* [nginx对页面进行缓存](https://zhuanlan.zhihu.com/p/54668409)
* 关于nginx的讨论
  * [Nginx 反向代理为什么可以提高网站性能？](https://www.zhihu.com/question/19761434)
  * [关于高并发](https://zhuanlan.zhihu.com/p/38636111)
  * [NGINX、HAProxy和Traefik负载均衡能力对比](https://zhuanlan.zhihu.com/p/41354937)

**还没有看的参考资料**

* [Nginx 单机百万QPS环境搭建](https://www.cnblogs.com/wunaozai/p/6073731.html)
* [一次qps测试实践（续）](https://blog.csdn.net/silyvin/article/details/79143761÷)

