#### 一、重新设置mysql密码
##### 1、关闭mysql
**系统设置 -> 进入**`**mysql**`**，点击**`**Stop MySQL Server**`**。**

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1674097605808-ce968d17-2870-4250-9074-a9d3d115addd.png)



##### 2、进入终端设置
+ <font style="color:rgb(18, 18, 18);">进入终端输入</font>

```bash
cd /usr/local/mysql/bin
```

<font style="color:rgb(18, 18, 18);"></font>

+ <font style="color:rgb(18, 18, 18);">获取管理员权限</font>

```bash
sudo su
```



+ <font style="color:rgb(18, 18, 18);">禁止</font>`<font style="color:rgb(18, 18, 18);">mysql</font>`<font style="color:rgb(18, 18, 18);">验证功能，</font>`<font style="color:rgb(18, 18, 18);">mysql</font>`<font style="color:rgb(18, 18, 18);">会重启，偏好设置中的</font>`<font style="color:rgb(18, 18, 18);">mysql</font>`<font style="color:rgb(18, 18, 18);">状态会变成</font>`<font style="color:rgb(18, 18, 18);">running</font>`

```bash
./mysqld_safe --skip-grant-tables
```

<font style="color:rgb(18, 18, 18);"></font>

+ <font style="color:rgb(18, 18, 18);">进入</font>`<font style="color:rgb(18, 18, 18);">mysql</font>`

```bash
./mysql
```



+ <font style="color:rgb(18, 18, 18);">重置密码</font>

```bash
flush privileges;
ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
```

<font style="color:rgb(18, 18, 18);"></font>

+ <font style="color:rgb(18, 18, 18);">退出</font>`<font style="color:rgb(18, 18, 18);">mysql</font>`

```bash
quit;
```

<font style="color:rgb(18, 18, 18);"></font>

+ <font style="color:rgb(18, 18, 18);">退出</font>`<font style="color:rgb(18, 18, 18);">sudo</font>`

```bash
exit;
```



+ <font style="color:rgb(18, 18, 18);">密码重置完毕，重新登录</font>`<font style="color:rgb(18, 18, 18);">mysql</font>`

```bash
mysql -uroot -p
```





