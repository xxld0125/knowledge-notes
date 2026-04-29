#### 一、安装5.7版本
```bash
docker pull ibex/debian-mysql-server-5.7
```

#### 
#### 二、启动mysql
![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1674116322871-4219384e-d6db-479e-963f-67fc19774cda.png)



#### 三、设置允许远程访问
+ 登录mysql

```bash
mysql -uroot -p;
```

+ 切换到mysql库

```bash
use mysql;
```

+ 查询当前用户可登录的客户端情况，从`mysql`的`user`表查询

```bash
show user,host from user;
```

+ 更新root用户可登录的客户端情况

```bash
update user set host='%' where user='root' and host='localhost' limit 1;

// 刷新
flush privileges;
```





