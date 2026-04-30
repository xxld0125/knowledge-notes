### 前言
:::color1
该文档主要是记录学习linux中的一些笔记，便于自己日后查询使用

:::

### 一、权限
<font style="color:rgb(51, 51, 51);">Linux 系统是一种多用户系统，它将文件访问者身份分为三种：</font>

#### <font style="color:rgb(51, 51, 51);">文件所有者（Owner）</font>
<font style="color:rgb(51, 51, 51);">当创建一个用户的时候，Linux 会为该用户创建一个主目录，路径为 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">/home/<username></font><font style="color:rgb(51, 51, 51);">，我们可以使用 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">cd ~</font><font style="color:rgb(51, 51, 51);">，快捷进入主目录。如果你想放一个私密文件，就可以放在自己的主目录里，然后设置只能自己查看。</font>

<font style="color:rgb(51, 51, 51);"></font>

#### <font style="color:rgb(51, 51, 51);">群组（Group）</font>
<font style="color:rgb(51, 51, 51);">每个用户都有一个用户组，方便多人操作的时候，为一群人分配权限。当创建用户的时候，会自动创建一个与它同名的用户组。</font>

<font style="color:rgb(51, 51, 51);">如果一个用户同时属于多个组，用户需要在用户组之间切换，才能具有其他用户组的权限。</font>

<font style="color:rgb(51, 51, 51);"></font>

#### <font style="color:rgb(51, 51, 51);">其他人（Others）</font>
<font style="color:rgb(51, 51, 51);">既不是文件所有者又不是文件所属群组成员的用户，就是其他人。</font>

<font style="color:rgb(51, 51, 51);"></font>

#### <font style="color:rgb(51, 51, 51);">超级用户（Root）</font>
<font style="color:rgb(51, 51, 51);">Root 用户是一类特殊的用户，该用户可以访问所有文件。</font>

<font style="color:rgb(51, 51, 51);"></font>

### 二、<font style="color:rgb(51, 51, 51);">adduser 添加用户 和 passwd 更改密码</font>
```bash
# 添加一个名为 git 的用户
adduser git
# 设置 git 用户的密码
passwd git
```

但是由于创建的用户权限较低，有的时候我们需要为用户提权，此时我们可以这样做：

```bash
# 会打开 sudoers 配置文件
sudo visudo
```

注意同样是编辑 sudoers 配置文件，使用这个命令会比使用 sudo vim /etc/ sudoers 更安全， 除了对语法有校验，并且还会在多用户编辑的时候锁住文件。

打开 sudoers 配置文件后，我们添加这样一行配置：

```bash
# Allow git to run any commands anywhere
git ALL=(ALL:ALL) ALL 
```

简单解释下这句话 `git ALL=(ALL:ALL) ALL` ：

+ git 表示规则应用的用户名
+ 第一个 ALL 表示规则应用于所有 hosts
+ 第二个 ALL 表示规则应用于所有 users
+ 第三个 ALL 表示规则应用于所有 groups
+ 第四个 ALL 表示规则应用于所有 commands

我们保存退出后，git 用户就会获得 root 权限。



### 三、<font style="color:rgb(51, 51, 51);">ls 列出文件和目录</font>
#### 1、<font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">ls</font><font style="color:rgb(51, 51, 51);"> 列出文件和目录</font>
```bash
[root@iZ2zej10s0yqr7q56mfszjZ /]# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```



#### 2、<font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">ls -la</font><font style="color:rgb(51, 51, 51);"> 由 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">-a</font><font style="color:rgb(51, 51, 51);"> 显示所有文件和目录（包括隐藏）和 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">-l</font><font style="color:rgb(51, 51, 51);"> 显示详细列表组成：</font>
```bash
[root@iZ2zej10s0yqr7q56mfszjZ /]# ls -la
total 24
dr-xr-xr-x.  17 root root  244 Jul  7 12:52 .
dr-xr-xr-x.  17 root root  244 Jul  7 12:52 ..
-rw-r--r--    1 root root    0 Apr 28 10:10 .autorelabel
lrwxrwxrwx.   1 root root    7 Jun 22  2021 bin -> usr/bin
dr-xr-xr-x.   5 root root 4096 Apr 28 18:14 boot
drwxr-xr-x   19 root root 2940 Jul  7 23:01 dev
drwxr-xr-x. 107 root root 8192 Jul 12 12:36 etc
drwxr-xr-x.   3 root root   18 Jul  8 11:10 home
lrwxrwxrwx.   1 root root    7 Jun 22  2021 lib -> usr/lib
lrwxrwxrwx.   1 root root    9 Jun 22  2021 lib64 -> usr/lib64
drwxr-xr-x.   2 root root    6 Jun 22  2021 media
drwxr-xr-x.   2 root root    6 Jun 22  2021 mnt
drwxr-xr-x.   2 root root    6 Jun 22  2021 opt
dr-xr-xr-x  105 root root    0 Jul  7 22:40 proc
dr-xr-x---.   7 root root  217 Jul  8 14:19 root
drwxr-xr-x   32 root root  940 Jul  7 22:40 run
lrwxrwxrwx.   1 root root    8 Jun 22  2021 sbin -> usr/sbin
drwxr-xr-x.   2 root root    6 Jun 22  2021 srv
dr-xr-xr-x   13 root root    0 Jul  7 22:40 sys
drwxrwxrwt.   9 root root 4096 Jul 12 14:00 tmp
drwxr-xr-x.  13 root root  158 Apr 28 18:06 usr
drwxr-xr-x.  21 root root 4096 Apr 28 10:10 var
```

<font style="color:rgb(51, 51, 51);">每一行都有 7 列，我们以 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">home</font><font style="color:rgb(51, 51, 51);"> 为例讲解每列的含义:</font>

| drwxrwxr-x | 3 | root | root | 18 | Jul  8 11:10 | home |
| --- | --- | --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">文件类型和权限信息</font> | <font style="color:rgb(51, 51, 51);">链接数或者一级子目录数</font> | <font style="color:rgb(51, 51, 51);">所有者</font> | <font style="color:rgb(51, 51, 51);">所属组</font> | <font style="color:rgb(51, 51, 51);">文件大小，单位字节</font> | <font style="color:rgb(51, 51, 51);">最后修改时间</font> | <font style="color:rgb(51, 51, 51);">文件名</font> |


重点看第 1 列的内容，以 drwxrwxr-x 为例，这里一共 10 位，第 1 位表示文件类型，其中 - 表示普通文件，d 表示目录文件。

第 2 到第 4 位，表示所有者权限，其中 r 表示读权限，w 表示写权限，x 表示可执行权限， -表示无权限，第 2 到 5 位为 rwx，表示所有者可读可写可执行。

第 5 到第 7 位，表示组用户权限，这里也是 rwx。

第 8 到第 10 位，表示其他用户权限，这里是 r-x，表示有可读可执行权限，无写入权限。

这里再额外补充一点：

像 root 用户创建文件夹的默认权限为 `rwxr-xr-x`:

<font style="color:rgb(51, 51, 51);">而创建文件的默认权限是 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">rw-r--r--</font><font style="color:rgb(51, 51, 51);">，注意创建文件默认会去掉 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">x</font><font style="color:rgb(51, 51, 51);"> 权限：</font>

<font style="color:rgb(51, 51, 51);">这就是为什么我们有的时候需要在创建文件后，又加上执行权限。</font>

<font style="color:rgb(51, 51, 51);"></font>

### 四、<font style="color:rgb(51, 51, 51);">chown 更改文件属主，也可以同时更改文件属组</font>
**<font style="color:rgb(51, 51, 51);">chown (change owner)</font>**<font style="color:rgb(51, 51, 51);"> 语法：</font>

```bash
# -R：递归更改文件属组
chown [–R] 属主名 文件名
chown [-R] 属主名：属组名 文件名
```

<font style="color:rgb(51, 51, 51);"></font>

<font style="color:rgb(51, 51, 51);">将 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">index.html</font><font style="color:rgb(51, 51, 51);"> 的所有者更改为 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">git</font><font style="color:rgb(51, 51, 51);">：</font>

```bash
[root@iZ2ze www]# chown git index.html
[root@iZ2ze www]# ls -

-rw-r--r-- 1 git  root  0 12月 17 23:54 index.html
```

  
<font style="color:rgb(51, 51, 51);">将 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">index.html</font><font style="color:rgb(51, 51, 51);"> 的所有者和群组都改为 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">git</font><font style="color:rgb(51, 51, 51);">：</font>

```bash
[root@iZ2ze www]# chown git:git index.html
[root@iZ2ze www]# ls -l

-rw-r--r-- 1 git  git   0 12月 17 23:54 index.html
```



### 五、<font style="color:rgb(51, 51, 51);">chmod 更改文件权限</font>
<font style="color:rgb(51, 51, 51);">权限除了用</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">r</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">w</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">x</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">这种方式表示，也可以用数字表示，数字与字母的对应关系为：</font>

+ <font style="color:rgb(51, 51, 51);">r:4</font>
+ <font style="color:rgb(51, 51, 51);">w:2</font>
+ <font style="color:rgb(51, 51, 51);">x:1</font>

<font style="color:rgb(51, 51, 51);"></font>

<font style="color:rgb(51, 51, 51);">之所有如此对应关系，主要还是为了方便推导，比如我们希望一个文件可读可写，那我们可以方便的设置权限为 6（4 + 2），同样，如果我们知道一个权限为 3，我们也可以推导出权限为可写可执行，因为只有 2 + 1 才可能等于 3。</font>

<font style="color:rgb(51, 51, 51);"></font>

<font style="color:rgb(51, 51, 51);">我们看下 </font>**<font style="color:rgb(51, 51, 51);">chmod （change mode）</font>**<font style="color:rgb(51, 51, 51);"> 的具体语法：</font>

```bash
# -R：递归更改文件属组
chmod [-R] xyz 文件或目录
```

	<font style="color:rgb(51, 51, 51);">其中 xyz 分别表示 Owner、Group、Others 的权限，如果我们这样设置一个文件的权限：</font>

```bash
chmod 750 index.html
```

	<font style="color:rgb(51, 51, 51);">我们可以得知，Owner 的权限为 7，为可读可写可执行，Group 的权限为 5，为可读可执行，Others 的权限为 0，表示不可读写不可执行。对应字母为：</font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">rwxr-x---</font><font style="color:rgb(51, 51, 51);">。</font>

<font style="color:rgb(51, 51, 51);"></font>

<font style="color:rgb(51, 51, 51);">除了这种数字的方式，还有一种使用符号类型改变权限的方式：</font>

<font style="color:rgb(51, 51, 51);">在这种方式里，我们将三种身份 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">Owner</font><font style="color:rgb(51, 51, 51);">、</font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">Group</font><font style="color:rgb(51, 51, 51);">、</font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">Others</font><font style="color:rgb(51, 51, 51);">，分别简写为 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">u（User）</font><font style="color:rgb(51, 51, 51);">、</font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">g</font><font style="color:rgb(51, 51, 51);">、</font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">o</font><font style="color:rgb(51, 51, 51);">，用 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">a</font><font style="color:rgb(51, 51, 51);"> 表示所有身份，再使用 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">+</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">-</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">=</font><font style="color:rgb(51, 51, 51);"> 表示加入、去除、设定一个权限，</font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">r</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">w</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">x</font><font style="color:rgb(51, 51, 51);"> 则继续表示读，写，执行权限，举个例子：</font>

```bash
chmod u+x,g-x,o-x index.html
```

<font style="color:rgb(51, 51, 51);">意思就是</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">Owner</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">加上执行权限，</font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">Group</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">和</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">Others</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">去除执行权限。</font>

<font style="color:rgb(51, 51, 51);">当然我们也可以直接设定权限</font>

```bash
chmod u=rwx,g=rx,o=r index.html
```

	<font style="color:rgb(51, 51, 51);">此时文件的权限就相当于</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">-rwxr-xr--</font><font style="color:rgb(51, 51, 51);">。</font>

<font style="color:rgb(51, 51, 51);">此外，我们还可以省略不写 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">ugoa</font><font style="color:rgb(51, 51, 51);"> 这类身份内容，直接写：</font>

```bash
chmod +x index.html
```

	<font style="color:rgb(51, 51, 51);">此时相当于使用了 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">a</font><font style="color:rgb(51, 51, 51);">，会给所有身份添加执行权限。</font>

<font style="color:rgb(51, 51, 51);"></font>

### <font style="color:rgb(51, 51, 51);">六、su 切换身份</font>
```bash
# 切换为 git 用户
su git
```

### 
### 七、<font style="color:rgb(51, 51, 51);">whoami 显示用户名</font>
```bash
# whoami 
root
```



### 八、<font style="color:rgb(51, 51, 51);">pwd 显示当前目录</font>
```bash
[git@iZ2ze www]$ pwd
/home/www
```

### 
### <font style="color:rgb(51, 51, 51);">九. cd 切换工作目录</font>
```bash
# 进入 /home/www/
cd /home/www

# 进入自己的主目录
cd ~

# 进入当前目录的上上两层 :
cd ../..
```



### 十、<font style="color:rgb(51, 51, 51);">mkdir 创建目录</font>
1. <font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">mkdir</font><font style="color:rgb(51, 51, 51);"> 创建目录：</font>

```bash
mkdir new_folder
```



2. <font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">mkdir -p</font><font style="color:rgb(51, 51, 51);"> 递归创建目录：</font>

```bash
mkdir -p one/two/three
```



### 十一、<font style="color:rgb(51, 51, 51);">touch 创建文件</font>
<font style="color:rgb(51, 51, 51);">用于修改文件或者目录的时间属性，当文件不存在，系统会创建空白文件</font>

```bash
touch new_file
```



### 十二、<font style="color:rgb(51, 51, 51);">echo 打印输出</font>
<font style="color:rgb(51, 51, 51);">echo 是 Shell 命令，用于打印输出：</font>

```bash
# 显示转义字符
echo "\"test content\""
```

	

<font style="color:rgb(51, 51, 51);">创建或覆盖文件内容为 "test content"：</font>

```bash
echo "test content" > index.html
```

	

<font style="color:rgb(51, 51, 51);">如果是想追加内容，就用 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">>></font><font style="color:rgb(51, 51, 51);"> ：</font>

```bash
[root@iZ2ze www]# echo "test content" > index.html
[root@iZ2ze www]# cat index.html
test content
[root@iZ2ze www]# echo "test content" >> index.html
[root@iZ2ze www]# cat index.html
test content
test content
```



### 十三、<font style="color:rgb(51, 51, 51);">cat 连接文件并打印输出</font>
查看文件内容：

```bash
cat ~/.ssh/id_rsa.pub
```



清空 index.html 内容：

```bash
cat /dev/null > index.html
```



把 index.html 的内容写入 second.html：

```bash
cat index.html > second.html
```



把 index.html 的内容追加写入 second.html：

```bash
cat index.html >> second.html
```



把 index.html 和 second.html 追加写入 third.html：

```bash
cat index.html second.html >> third.html
```



### 十四、cp 复制文件或目录
<font style="color:rgb(51, 51, 51);">将目录 website/ 下的所有文件复制到新目录 static 下：</font>

```bash
# -r：若给出的源文件是一个目录文件，此时将复制该目录下所有的子目录和文件。
cp –r website/ static
```



### 十五、<font style="color:rgb(51, 51, 51);">mv 移动并重命名</font>
<font style="color:rgb(51, 51, 51);">文件改名：</font>

```bash
mv index.html index2.html
```



<font style="color:rgb(51, 51, 51);">隐藏文件：</font>

```bash
# 文件名上加上 .
mv index.html .index.html
```



<font style="color:rgb(51, 51, 51);">移动文件：</font>

```bash
# 仅仅移动
mv  /home/www/index.html   /home/static/
# 移动又重命名
mv /home/www/index.html   /home/static/index2.html
```



<font style="color:rgb(51, 51, 51);">批量移动：</font>

```bash
mv  /home/www/website/*  /home/www/static
```



### 十六、<font style="color:rgb(51, 51, 51);">rm 删除一个文件或者目录</font>
```bash
# 系统会询问
rm file

# -f 表示直接删除
# -r 表示目录下的所有文件删除

# 删除当前目录下的所有文件及目录
rm -r  * 

# 跑路
rm -rf /*
```



### 十七、<font style="color:rgb(51, 51, 51);">vi/vim</font>
<font style="color:rgb(51, 51, 51);">Linux 内建 vi 文书编辑器，Vim 是从 vi 发展出来的一个文本编辑器。</font>

基本上 vi/vim 共分为三种模式，分别是**命令模式（Command mode）**，**输入模式（Insert mode**）和**底线命令模式（Last line mode）**。我们边操作边介绍这三种模式： 我们执行 vim index.html，如果没有该文件，则会创建文件：

```bash
vim index.html
```

<font style="color:rgb(51, 51, 51);">此时界面为：</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1657688259733-ce028151-f5ba-4ef3-8011-1fbc093ea2c0.png)

<font style="color:rgb(51, 51, 51);">此时是</font>**<font style="color:rgb(51, 51, 51);">命令模式</font>**<font style="color:rgb(51, 51, 51);">，在命令模式下，输入的任何字符都会被视为命令，接下来几个常用的命令：</font>

+ <font style="color:rgb(51, 51, 51);">i 切换到输入模式。</font>
+ <font style="color:rgb(51, 51, 51);">x 删除当前光标所在处的字符。</font>
+ <font style="color:rgb(51, 51, 51);">: 切换到底线命令模式。</font>

<font style="color:rgb(51, 51, 51);"></font>

<font style="color:rgb(51, 51, 51);">我们按下 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">i</font><font style="color:rgb(51, 51, 51);">，便会进入</font>**<font style="color:rgb(51, 51, 51);">输入模式</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1657688290290-aaf0a651-a15c-418f-9b29-f50e7f13f286.png)

<font style="color:rgb(51, 51, 51);">输入模式下，左下角有</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">-- INSERT --</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">标志：</font>

<font style="color:rgb(51, 51, 51);">此时我们可以进行各种输入，当输入完毕后，按下 ESC 回到命令模式：</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1657688305930-3be8deeb-30ff-400b-97cc-195f3f9f679e.png)

<font style="color:rgb(51, 51, 51);">此时左下角的 INSERT已经消失不见了，如果我们要保存退出，我们先输入 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">:</font><font style="color:rgb(51, 51, 51);"> ，进入</font>**<font style="color:rgb(51, 51, 51);">底线命令模式</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1657688319387-a5910785-f25c-4602-95e9-65d06206d5d2.png)

<font style="color:rgb(51, 51, 51);">在底线命令模式中，常见的命令有：</font>

+ <font style="color:rgb(51, 51, 51);">w 保存文件</font>
+ <font style="color:rgb(51, 51, 51);">q 退出程序</font>

<font style="color:rgb(51, 51, 51);">我们输入 </font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);">wq</font><font style="color:rgb(51, 51, 51);">，表示保存并退出，此时我们就会发现并创建了一个 HTML 文件。</font>

<font style="color:rgb(51, 51, 51);"></font>

### 十八、<font style="color:rgb(51, 51, 51);">ssh 远程连接工具</font>
<font style="color:rgb(51, 51, 51);">注意 ssh 监听是 22 端口。</font>

<font style="color:rgb(51, 51, 51);">其基本语法为：</font>

```bash
ssh [OPTIONS] [-p PORT] [USER@]HOSTNAME [COMMAND]
```

	

<font style="color:rgb(51, 51, 51);">监听端口示例：</font>

```bash
ssh -p 300 git@8.8.8.8
```

	

<font style="color:rgb(51, 51, 51);">打开调试模式：</font>

```bash
# -v 冗详模式，打印关于运行情况的调试信息
ssh -v root@8.8.8.8
```



### 参考
+ [https://juejin.cn/post/7044099175838908424](https://juejin.cn/post/7044099175838908424#heading-12)
+ [https://juejin.cn/post/6917096816118857736](https://juejin.cn/post/6917096816118857736)
+ [https://q.shanyue.tech/command/#%E6%B3%A8%E6%84%8F](https://q.shanyue.tech/command/#%E6%B3%A8%E6%84%8F)





