# Centos7 anaconda-ks.cfg自动化centos安装

当第一次手动安装好 `centos7` 后会自动在当前目录下生成 `anaconda-ks.cfg` 文件，通过该文件可以自动化后续的 `centos7` 的安装。

1. 把 `anaconda-ks.cfg` 文件放在服务器中，可以被别的机子通过 `http` 协议访问到。

2. 在 `virtualbox` 中新建一个 `centos7` 镜像。

3. 启动新建的镜像，选择 `centos7` 的 `iso` 文件。

4. 启动到这个画面是点击键盘上的 `Esc` 按钮。

   ![](./1540376782(1).png)

   5. 在 `boot：` 后面输入 `anaconda-ks.cfg` 的地址。

      ```shell
      boot: linux ks=http://192.168.123.70:5500/anaconda-ks.cfg
      ```

   6. 等待自动安装完成，点击 `reboot`， 随后拔掉 `iso` 文件。
