主要记录项目的各功能模块。

#### 项目初始化
**Mars**：[https://mars.myscrm.cn/applications/detail/3139?oid=1](https://mars.myscrm.cn/applications/detail/3139?oid=1)

**Git**：[https://git.myscrm.cn/kefu/bff-kefu-demo](https://git.myscrm.cn/kefu/bff-kefu-demo)

**Apollo**：[https://apollo-test-kefu.myscrm.cn/config.html?#/appid=bff-kefu-demo](https://apollo-test-kefu.myscrm.cn/config.html?#/appid=bff-kefu-demo)

**MiddleMan**：[https://api.myscrm.cn/project/17734/interface/api/master](https://api.myscrm.cn/project/17734/interface/api/master)



#### 云客镜像源地址:
```bash
// 设置淘宝源
npm config set registry https://registry.npmmirror.com

// @yunke 前缀包设置云客 npm 源 
npm config set @yunke:registry https://registry-npm.myscrm.cn/repository/yunke/

// 设置grpc镜像源
npm config set grpc-node-binary-host-mirror https://registry-npm.myscrm.cn/repository/mirrors
```

#### 
#### 一、node版本
采用[公司推荐alinode](https://confluence.myscrm.cn/pages/viewpage.action?pageId=27358773)<font style="color:rgb(23, 43, 77);">为基础镜像: </font>[yunke-registry.cn-hangzhou.cr.aliyuncs.com/yued/alinode:v2-14.18.1-1.24.6](http://yunke-registry.cn-hangzhou.cr.aliyuncs.com/yued/alinode:v2-14.18.1-1.24.6)

+ `v<font style="color:rgb(23, 43, 77);">2</font>`<font style="color:rgb(23, 43, 77);"> 表示云客 </font>`<font style="color:rgb(23, 43, 77);">bff node</font>`<font style="color:rgb(23, 43, 77);">镜像第二个版本</font>
+ `<font style="color:rgb(23, 43, 77);">14.18.1</font>`<font style="color:rgb(23, 43, 77);"> 表示</font>`<font style="color:rgb(23, 43, 77);">node</font>`<font style="color:rgb(23, 43, 77);">版本</font>
+ `<font style="color:rgb(23, 43, 77);">1.24.6</font>`<font style="color:rgb(23, 43, 77);"> 表示镜像内</font>`<font style="color:rgb(23, 43, 77);">grpc</font>`<font style="color:rgb(23, 43, 77);">版本</font>



#### 二、接口返回格式定义
返回格式要求与`kfbacked`保持一致。

```json
{
	"data": {
    "value": "1"
  },
  "errcode": 0,
  "errmsg": "ok"
}
```

+ data:业务数据
+ errcode: 错误码
    - 0: 接口正常
    - 500: token失效，重新登录
+ errmsg: 报错信息



```typescript
  // 返回处理
  config.response = {
    enable: true,

    /* This config will customize the success status code.（Optional） */
    // succCode: 0,

    /* Customize your response fn.（Optional） */
    customResponse: async (ctx: Context, next: (err?: any) => Promise<any>) => {
      const { body: data, message: errmsg, status } = ctx.response;

      const errcode = status === 200 ? 0 : status;

      ctx.response.body = {
        errcode,
        errmsg,
        data,
      };
      await next();
    },
  };
```



#### 四、日志
1. <font style="color:rgb(28, 30, 33);">记录常规业务需求日志的 </font>`<font style="color:rgb(28, 30, 33);">business.log</font>`<font style="color:rgb(28, 30, 33);"> 日志</font>

```typescript
console.log
console.info
console.warn
console.trace
console.debug
```

2. <font style="color:rgb(28, 30, 33);">记录错误信息的 </font>`<font style="color:rgb(28, 30, 33);">error.log</font>`<font style="color:rgb(28, 30, 33);"> 日志</font>

```typescript
console.error
```

3. <font style="color:rgb(28, 30, 33);">记录框架请求链路的 </font>`<font style="color:rgb(28, 30, 33);">access.log</font>`<font style="color:rgb(28, 30, 33);"> 日志</font>

```typescript
console.access
```



<font style="color:rgb(28, 30, 33);">生产环境错误日志在</font>**<font style="color:rgb(28, 30, 33);">贾维斯</font>**<font style="color:rgb(28, 30, 33);">中进行查看，具体的查看方式为：</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1672131689203-88483f9b-3966-471c-ab82-df56da8add00.png)



#### 五、鉴权




#### 六、grpc
查看开发环境各服务端口：[http://10.10.4.36:32379/v2/keys](http://10.10.4.36:32379/v2/keys)



