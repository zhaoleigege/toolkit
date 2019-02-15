# TAR命令基本教程

1. 创建一个归档文件

   ```SH
   tar cvf target.tar source1 source2 ...
   ```

   ```shell
   c -------表明我们想创建一个归档文件
   v -------让程序在加载文件列表时打印出文件名字
   f -------指定输出文件的名字
   ```


2. 展开一个归档文件

   ```shell
   tar xvf target.tar
   ```

   ```SHELL
   x -------提取文件
   ```


3. 查看归档文件的基本信息

   ```SHELL
   # 提取文件前查看文件的基本信息
   
   tar -tf target.tar
   ```


4. 归档文件的时候同时压缩归档后的文件

   ```SHELL
   # 归档多个文件后使用gzip的压缩方式压缩文件
   tar cvzf target.tar.gz source1 sourve2 ...
   
   # 解压上述文件
   gunzip target.tar.gz
   tar xvf tartget.tar
   
   ------------------------------------------------
   
   # 归档多个文件后使用bzip2的压缩方式压缩文件
   tar cvjf target.tar.bz source1 sourve2 ...
   
   # 解压上述文件
   bunzip2 target.tar.bz
   tar xvf tartget.tar
   ```
