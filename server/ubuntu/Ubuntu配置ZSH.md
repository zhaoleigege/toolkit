# Ubuntu配置ZSH

1、下载zsh

```shell
# 1、更新软件
sudo apt-get update
# 2、安装zsh
sudo apt-get install zsh
# 3、查看zsh版本
zsh --version
```

2、设置zsh为默认bash

```shell
# 1、查看zsh安装位置
whereis zsh
# 2、设置zsh为默认bash
sudo usermod -s /usr/bin/zsh $(whoami)
# 重启后就能看到效果
```

3、让zsh更加漂亮

```shell
# 1、安装Powerline和Powerline font
sudo apt-get install powerline fonts-powerline
# 2、安装主题(可选择)
	sudo apt-get install zsh-theme-powerlevel9k
	# 使主题生效
	echo "source /usr/share/powerlevel9k/powerlevel9k.zsh-theme" >> ~/.zshrc
	# 重启查看效果
# 3、添加高量格式
	sudo apt-get install zsh-syntax-highlighting
	# 使主题生效
	echo "source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
```

4、安装git和oh-my-zsh

```shell
# 1、安装git
sudo apt-get install git
# 2、安装oh-my-zsh
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
	# 因为安装oh-my-zsh后，前面安装的powerlevel9k和高量格式都失效了，所以要重新输入配置文件中
	echo "source /usr/share/powerlevel9k/powerlevel9k.zsh-theme" >> ~/.zshrc
	echo "source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
```



#### 参考资料

[ubuntu安装zsh](https://linuxhint.com/install_zsh_shell_ubuntu_1804/)