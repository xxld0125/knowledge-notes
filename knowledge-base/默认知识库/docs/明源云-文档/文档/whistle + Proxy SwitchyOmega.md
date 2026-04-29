介绍一些日常开发中使用`whistle + Proxy SwitchyOmega`处理问题的场景。



#### 一、数据mock
在Rules中添加对应需要mock数据的接口![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689143822826-61a3cddd-da8b-48ed-90b6-d5d31d3b65f1.png)

```plain
www.test.com/cgi-bin/get-data  resBody://{mock}
```



在Values中添加mock数据

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689143874883-5d7aa356-0c25-473b-95e4-9a47a8f594ef.png)

```plain
{
    "code": 0,
    "message": "success",
    "data": [
		{
        	name: 'test'
        }
    ]
}
```



#### 二、调试线上环境代码
一般生产上有问题时，我们需要调试代码排查问题。这时候我们可以将生产上的前端资源转发为请求本地的前端资源，这样就可以调试生产环境的前端代码。

下面中的[https://kf.myyscm.com](https://kf.myyscm.com)为前端生产站点域名， localhost:8080为本地的前端开发环境。

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689144289406-96de387e-2741-4a60-a2a1-426416948bec.png)



#### 三、模拟接口状态
在开发场景中，可能会需要验证一些接口的异常场景。这时候我们可以配置接口的返回值或响应状态来模拟。

比如下图的场景，我将这个接口的httpCode设置为了500。

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689144489846-bfef6bbf-fb23-42b5-ae80-85960b873f9c.png)



一般对于接口的状态，处理httpCode码外，还会有约定好的code，比如下面这个base-info接口，正常返回的接口errcode为0。

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689144943885-d8b01eeb-e8fd-4a1b-8095-dfc3e252c41f.png)



当我们需要模拟异常场景时，我们可以这样配置。

```plain
https://kf-api-test-kefu.myscrm.cn/retesting/bk/task/task/base-info resMerge://(errcode=1)
```

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689145013092-55bd2e10-49d5-4cbb-8312-470a5274fea6.png)

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689145104541-e3d34d54-b006-47a2-b851-1a11c675e405.png)



#### 四、App调试-vconsole.js
针对生产的App环境应用，出现问题，不好调试的场景。可以注入vconsole.js。

```plain
https://kf-test-kefu.myscrm.cn htmlAppend://{vconsole}
```



```plain
<script src="https://unpkg.com/vconsole@3.15.1/dist/vconsole.min.js"></srcipt>
```



#### 五、App调试-log
whiltle提供了一个log配置，通过配置log，可以获取APP页面的log信息。

```plain
https://kf-test-kefu.myscrm.cn log://kf
```

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689145382219-9a0e97bb-0cc1-43a1-a1f3-90bdf9cedcc9.png)



#### 六、App调试-Weinre
whiltle提供了一个Weinre配置，通过配置Weinre，可以获取APP页面的控制台继续调试操作。

```plain
https://kf-test-kefu.myscrm.cn weinre://test
```

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689145539111-5036f2f1-4230-4fd1-a58e-90f52002a198.png)

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1689145573692-d6b4b673-5afd-4c9a-8574-f1afd837f54b.png)

