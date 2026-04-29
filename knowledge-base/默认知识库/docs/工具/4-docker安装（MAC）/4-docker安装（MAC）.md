#### 一、安装地址
官网下载地址：[https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/)

m1芯片选择图中地址下载。![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671158369541-7feeaf72-9759-4ad9-b814-df4f13da6426.png)



#### 二、docker镜像搜索
[https://hub.docker.com](https://hub.docker.com/)



#### 三、启动命令相关参数：
+ 设置容器名：`--name mongow`
+ 设置网络模式：`<font style="color:rgb(77, 77, 77);">--net </font>bridge`
+ 设置端口映射（容器端口映射到本地端口）：`-p 27017:27017`
+ 设置挂载宿主机的目录：`-v /Users/xulingfeng/mongodb:/etc/mongo`（冒号":"前面的目录是宿主机目录，后面的目录是容器内目录。）
+ 设置容器环境变量：`-e ALLOW_EMPTY_PASSWORD=yes`
+ 设置后台运行容器：`-d mongo`(mongo：镜像名)
+ 设置配置文件的路径：`--config /etc/mongo/mongod.yaml`（`mongod`默认不读取配置文件，需要读取时，需要指定带有配置文件路径的`--config`选项）

```bash
docker run --name mongow --net bridge  -p 27017:27017 -v /Users/xulingfeng/mongodb:/etc/mongo -e ALLOW_EMPTY_PASSWORD=yes  -d mongo --config /etc/mongo/mongod.yaml
```



