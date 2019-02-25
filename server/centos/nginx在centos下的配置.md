# nginx在centos下的配置

1. 安装nginx

   ```shell
   yum install epel-release
   yum -y install nginx
   
   service nginx start
   systemctl enable nginx
   ```

2. 卸载centos

   ```shell
   service nginx stop
   chkconfig nginx off
   rm -rf /usr/sbin/nginx
   rm -rf /etc/nginx
   rm -rf /etc/init.d/nginx
   yum remove nginx
   ```

3. nginx的使用

   1. nginx命令

      ```shell
      # 启动nginx
      service service nginx start
         
      # 重启nginx
      service nginx restart
         
      # 暂停nginx
      service nginx stop
      
      # 设置开机自启动
      sudo systemctl enable nginx.service
      ```

   2. nginx日志查看

      默认的nginx日志文件位于`/var/log/nginx/`目录下

      ```shell
      cd /var/log/nginx
      ```

   3. nginx配置

      <span style="color: red;">nginx配置只能用**空格**，不要使用`tab`</span>

      * [负载均衡配置](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
          ```shell
          sudo vi /etc/nginx/nginx.conf
          ```
        * 在`http`中添加`upstream`
         
          ```shell
          http {
              ...
               upstream backend {
                  server 127.0.0.1:8000;
                  server 127.0.0.1:8001;
              }
              ...
          }
          ```

          然后配置转发

          ```shell
          http {
              ...
              server {
                  listen      0.0.0.0:8080 default_server;
          
                  location / {
                      proxy_pass http://backend;
                  }
              }
              ...
          }
          ```

        * 在centos上配置nginx的负载均衡，需要解决`(13 Permission denied)`的错误

          ```
          connect() to 127.0.0.1:8080 failed (13: Permission denied)
          ```

          [解决方法](https://blog.csdn.net/oydaybreak/article/details/46594639)

          ```shell
          sudo setsebool -P httpd_can_network_connect 1
          ```

        * 随后访问时又遇到`502`错误，查看错误日志`(/var/log/nginx/error.log)`

          ```shell
          connect() failed (111: Connection refused) while connecting to upstream
          ```
          [解决方法](https://serverfault.com/questions/317393/connect-failed-111-connection-refused-while-connecting-to-upstream/576488#576488)

          ```shell
          # 修改localhost为127.0.0.1
          # listen 8080; 改为 listen 0.0.0.0:8080;
          ```

        范例：

        ```shell
        # For more information on configuration, see:
        #   * Official English Documentation: http://nginx.org/en/docs/
        #   * Official Russian Documentation: http://nginx.org/ru/docs/
        
        user nginx;
        worker_processes auto;
        error_log /var/log/nginx/error.log;
        pid /run/nginx.pid;
        
        # Load dynamic modules. See /usr/share/nginx/README.dynamic.
        include /usr/share/nginx/modules/*.conf;
        
        events {
            worker_connections 1024;
        }
        
        http {
            log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                              '$status $body_bytes_sent "$http_referer" '
                              '"$http_user_agent" "$http_x_forwarded_for"';
        
            access_log  /var/log/nginx/access.log  main;
        
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
            include /etc/nginx/conf.d/*.conf;
        
            upstream backend {
                server 127.0.0.1:8000;
                server 127.0.0.1:8001;
            }
        
        
            server {
                listen      0.0.0.0:8080 default_server;
        
                location / {
                    proxy_pass http://backend;
                }
            }
        }
        ```

        


​        


