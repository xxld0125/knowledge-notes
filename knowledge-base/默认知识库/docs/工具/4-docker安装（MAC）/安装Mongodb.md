#### 一、安装mongodb
1、在`dockerhub`上搜索`mongodb`。

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671159203482-c87333fd-5626-4e9d-8ef0-38540becf12f.png)



2、找到对应的安装命令，

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671545524424-dcd7b3c0-ced3-4119-b376-21e9ade8f4c1.png)



3、下载完成镜像

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671545673037-2ef7d1bd-1a58-4b87-bb4d-a160902b64b7.png)





#### 二、运行mongodb容器(服务端)
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671545795507-fa290ab3-6d64-482a-8345-ede3bbc4d73b.png)

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671545831017-c01ca434-96e5-4590-a8e5-8faf729faf85.png)



#### 三、进入mongo客户端
输入`mongosh`,进入`mongo`客户端

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671545936595-833e8121-722f-4063-b934-fab1b1327dac.png)

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671545966277-6954ccbd-cfaa-4414-8629-cb9274510582.png)



#### 四、mongo客户端操作
##### 1、进入客户端
```bash
mongosh
```



##### 2、退出客户端
```bash
exit
```



##### 3、查看数据库
```bash
show dbs
```



##### 4、添加账号
+ 先切换到admin库

```bash
use admin;
```

	

+ <font style="color:rgb(77, 77, 77);">添加用户并赋予角色</font>

```bash
db.createUser( {
    user: "root",
    pwd: "123456",
    roles: [ { role: "root", db: "admin" } ]
  });
```



+ <font style="color:rgb(77, 77, 77);">既然已经添加了用户，用root账号登录</font>

```bash
db.auth('root','root');
```



##### 5、停止服务
<font style="color:rgb(77, 77, 77);">先通过客户端连接到需要停止的服务,然后停止服务</font>

```bash
use admin
db.shutdownServer()
```



