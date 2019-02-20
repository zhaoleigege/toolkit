#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

sourcePath = "需要被转换成utf-8编码的文件夹"
distPath = "转换生成的文件所在目录"

sourceIndex = sourcePath.find('教程')


def dirsFunc(path):
    dirs = os.listdir(path)

    for dir in dirs:
        dirPath = os.path.join(path, dir)
        if(os.path.isdir(dirPath)):
            dirsFunc(dirPath)
        elif dir.endswith(".txt"):
            fileDir = distPath + dirPath[sourceIndex + 3:dirPath.rindex("/")]
            if(os.path.isdir(fileDir) == False):
                os.makedirs(fileDir)
            distFile = distPath + dirPath[sourceIndex + 3:]
            print(distFile)
            os.system("iconv -f GBK -t UTF-8 %s > %s" % (dirPath, distFile))


dirsFunc(sourcePath)
