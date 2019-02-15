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

3. 插入裸机中安装机器

4. [配置ssh](./centos7配置SSH.md)

5. 安装完成后查看基本的设置

   * 时区信息

     ```shell
     timedatectl
     ```

6. 设置yum源的地址

   ```shell
   wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
   yum clean all
   yum makecache
   ```


#### 参考资料

* [LINUX 下刻录iso到u盘](https://www.jianshu.com/p/177a78770d0a)
* [设置yum源](https://www.jianshu.com/p/541c737bc947)