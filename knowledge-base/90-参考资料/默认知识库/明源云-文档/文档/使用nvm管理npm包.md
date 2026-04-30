#### 前言：
<font style="color:rgb(64, 64, 64);">在实际的前端开发过程中，可能会经常遇见 node.js 的版本问题，不同的项目需要使用不同的 node.js 版本。直接安装的话，只能安装和使用 node.js 的一个版本。可以使用 nvm 来安装和管理不同版本的 node.js。</font>

<font style="color:rgb(53, 53, 53);">nvm全英文也叫node.js version management，是一个nodejs的版本管理工具。nvm和n都是node.js版本管理工具，为了解决node.js各种版本存在不兼容现象可以通过它可以安装和切换不同版本的node.js。</font>

<font style="color:rgb(53, 53, 53);"></font>

#### 一、nvm下载
##### 1、mac下载


打开终端，输入下方的命令，会自动下载nvm。

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```



`v0.39.1`是当前`nvm`的版本号，最新的版本号可以在[github](https://github.com/nvm-sh/nvm/blob/master/README.md)上查看。



执行完成后，可以通过`nvm -v`确认是否安装成功。



如果出现`command not found: nvm`, 可能是因为配置文件<font style="color:rgb(36, 41, 47);">(</font><font style="color:rgb(36, 41, 47);">~/.bash_profile</font><font style="color:rgb(36, 41, 47);">, </font><font style="color:rgb(36, 41, 47);">~/.zshrc</font><font style="color:rgb(36, 41, 47);">, </font><font style="color:rgb(36, 41, 47);">~/.profile</font><font style="color:rgb(36, 41, 47);">, or </font><font style="color:rgb(36, 41, 47);">~/.bashrc</font><font style="color:rgb(36, 41, 47);">)</font>中缺少配置信息， 可以通过输入下方命令将配置信息补充到配置文件中。



```bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```

  
这样我们就安装好了nvm。



备注：目前m1的mac系统没感觉到有兼容性问题



**配置环境变量**

1. **bash**

```bash
vim ~/.bash_profile
```

<font style="color:rgb(77, 77, 77);">然后将下面的配置信息输入保存</font>

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

<font style="color:rgb(77, 77, 77);">输入之后 </font>`<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">:wq</font>`<font style="color:rgb(77, 77, 77);">保存并退出编辑</font>

<font style="color:rgb(79, 79, 79);"></font>

<font style="color:rgb(79, 79, 79);">刷新环境变量：执行如下命令</font>

```bash
source ~/.bash_profile
```

<font style="color:rgb(77, 77, 77);"></font>

2. **zsh**

```bash
vim ~/.zshrc
```

<font style="color:rgb(77, 77, 77);">然后将下面的配置信息输入保存</font>

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

```

<font style="color:rgb(77, 77, 77);">输入之后 </font><font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">:wq</font><font style="color:rgb(77, 77, 77);">保存并退出编辑</font>

<font style="color:rgb(77, 77, 77);"></font>

<font style="color:rgb(79, 79, 79);">刷新环境变量：执行如下命令</font>

```bash
source ~/.bash_profile
```



##### 2、windows安装
[window安装参考链接](https://juejin.cn/post/7070002101841035295)



#### 二、使用nvm
+ 安装node版本
    1. 安装指定版本-version

```bash
$ nvm install <version>	
```

    2. 安装最新稳定版本

```bash
$ nvm install stable
```



+ 删除node版本-version

```bash
$ nvm uninstall <version>
```



+ 切换使用指定版本node

```bash
$ nvm use <version>
```

+ 列出所有node
    1. <font style="color:rgb(51, 51, 51);">列出所有安装的版本</font>

```bash
$ nvm ls
```

    2. <font style="color:rgb(51, 51, 51);">列出所有远程服务器的版本</font>

```bash
$ nvm ls-remote
```

    3. <font style="color:rgb(51, 51, 51);">显示当前的版本</font>

```bash
$ nvm current
```

+ 别名功能
    1. <font style="color:rgb(51, 51, 51);">设置默认版本</font>

```bash
$ nvm alias default <version>
```

    2. <font style="color:rgb(51, 51, 51);">给不同的版本号添加别名</font>

```bash
$ nvm alias <name> <version>
```

    3. <font style="color:rgb(51, 51, 51);">删除已定义的别名</font>

```bash
$ nvm unalias <name>
```

    4. <font style="color:rgb(51, 51, 51);">在当前版本 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">node</font><font style="color:rgb(51, 51, 51);"> 环境下，重新全局安装指定版本号的 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">npm</font><font style="color:rgb(51, 51, 51);"> 包</font>

```bash
$ nvm reinstall-packages <version>
```

+ <font style="color:rgb(51, 51, 51);">更多功能</font>

```bash
$ nvm
```



