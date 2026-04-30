

`middleman`地址：[https://api.myscrm.cn/group/10561](https://api.myscrm.cn/group/10561)

`middleman`文档地址：[https://tools.myscrm.cn/middleman-doc/#/](https://tools.myscrm.cn/middleman-doc/#/)



#### 一、文档配置
##### 1、安装依赖
```bash
yarn add @yunke/yundoc --dev
```



##### 2、`yundoc.config.js`
```javascript
/**
 * yundoc 生成api文档配置项
*/
const path = require('path');
module.exports = {
  controllers: [path.join(process.cwd(), "./src/controller/*")],
  filterFiles: [],
  requiredType: 'typescript', // typescript | routing-controllers
  servers: [
    {
      url: 'http://127.0.0.1:46122',
      description: '开发环境域名前缀',
    }
  ],
  // 此参数在 --push 下生效
  middleman: {

  },
  //   // 是否根据生成结果生成前端请求代码和类型定义
  //   // 此参数在 --api 下生效
  //   genApi: {
  //     // 输出目录，一般指向 bff 对应的前端项目 src/api 这样的目录
  //     outputDir: path.join(__dirname, './api'),
  //     // 支持自定义 axios，必须使用 export default 导出 axios 或其实例
  //     // axiosFilePath: path.join(__dirname, './utils/request'),
  //     // 是否需要生成 header 相关参数（默认不开启，header 推荐在 axios 拦截器全局处理）
  //     header: false,
  //     // 是否需要生成 cookie 相关参数（默认不开启，cookie 推荐在 axios 拦截器全局处理）
  //     cookie: false,
  //     // prettier 配置文件，用于格式化生成结果
  //     // prettierConfig: path.join(__dirname, '../xxx/.prettierrc')
  //   },
  // 自定义 response 返回结构
  // 若不需要自定义外层数据结构则屏蔽此参数
  responseSchema: {
    type: 'object',
    properties: {
      code: {
        type: "number",
        description: "接口返回code码字段,成功是1",
      },
      // data配置必填，格式固定请不要更改
      data: {
        $ref: "#Response",
      },
      message: {
        type: "string",
        description: "接口返回信息字段，一般指代错误message",
      }
    },
    required: [
      "code",
      "data",
    ]
  }
}

```



##### 3、`.gitignore`文件增加屏蔽`openapi`文件夹


#### 二、接口文档自动同步
##### 1、增加script命令
```json
// 本地生成openapi数据的同时上传到middleman
"yundoc": "yundoc --push",
```



##### 2、增加自动push配置
```javascript
  middleman: {
    // 项目ID 打开 middleman项目 => 设置 => 项目配置 => 项目ID
    projectId: '2354',
    // 打开 middleman项目 => 设置 => token配置
    token: 'e80e5837eb00420d97ba',
    // add和update，add为新增模式，update为更新模式，新增模式下会跳过已存在的接口，更新模式下相同接口路径的用例会导入并覆盖数据，默认为update
    mport_mode: 'update',
    // 对没有默认分类的接口设置分类，默认为"公共分类"
    category_name: '公共分类',
    // 需要同步接口的分支名
    branch: 'f-20220217-operation-flow',
  },
```



##### 3、运行`yarn yundoc --push`命令
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1672385401004-b8296b5e-18b4-4ac8-a8a3-420a9d14a428.png)



查看`middleman`中自动生成的接口文档。

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1672385441517-f178238c-0ab2-42a2-acd7-f26a93f8ac8f.png)

#### 三、接口文档手动同步
##### 1、增加script命令
```json
// 仅仅本地生成openapi文档数据
"yundoc": "yundoc",
```



##### 2、运行`yundoc`命令, 生成`openapi`文件
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669708916825-816bb33e-9143-4004-99c9-fc9f7399511e.png)

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669708904355-b677bf48-ba6a-4013-b43a-86fcdac42052.png)



##### 3、导入middleman
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669708999590-7c9cdfce-2323-419b-b35c-22ad1c9fbec3.png)

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669709246073-c20b1ce6-0513-431e-b1e9-24961df9c0a3.png)

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669709373031-ddb4bc6a-9d03-498d-8141-4fc447d120b7.png)



#### 四、api文档注释规范
参考文档：

+ [https://github.com/yunke-yunfly/routing-controllers-to-openapi](https://github.com/yunke-yunfly/routing-controllers-to-openapi)
+ [注释支持说明](https://github.com/yunke-yunfly/routing-controllers-to-openapi/blob/master/DOCS.md#%E6%B3%A8%E9%87%8A%E6%94%AF%E6%8C%81%E8%AF%B4%E6%98%8E)

##### 1、interface
```typescript
interface AAA {
    // 姓名
    name: string;
    /**
     * 年龄
    */
    age: number;
}

interface AAA {
    // @param {string} [name='zane'] 姓名
    name: string;
    /**
     * 年龄
     * @param {number} [age=25]
     */
    age: number;
}
```

##### 2、方法
```typescript
// -----简单注释----------

/**
 * 获得用户信息（方法名注释）
 * @description 方法级别的描述信息
 * @param {string} name 姓名
 * @param {number} age 年龄
 */
@Get('/test')
async getUserInfo(
    @QueryParam("name") name: string,
    @QueryParam("age") age: number,
): Promise<{name: string}> {}
```



