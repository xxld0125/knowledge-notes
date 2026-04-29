#### 一、官方文档
+ [中英文档](https://www.nestjs.com.cn/)
+ [英文文档](https://nestjs.com/)
+ [中文文档](https://docs.nestjs.cn/)



#### 二、nestjs设计模式
`IOC`(`Inversion of Control`)字面意思是控制翻转, 具体定义是高层模块不应该依赖低层模块, 二者都应该依赖其抽象;抽象不应该依赖细节;细节应该依赖抽象。

`DI`(`Dependency Injection`:依赖注入)其实和`IoC`原本是一个东西.



未使用控制反转和依赖注入的代码。

```typescript
class A {
    name: string;
    constructor(name: string) {
        this.name = name;
    }
}

class B {
    age: number
    entity: A
    constructor(age: number) {
        this.age = age;
        this.entity = new A('test-name');
    }
}

const c = new B(18);

console.log(c.entity.name);
```



上面的代码中 B依赖A, 耦合度高,随着业务逻辑复杂程度的增加, 维护成本与代码可读性都会随着增加，并且很难再多引入额外的模块进行功能拓展。

尝试引入IOC容器解决。



```typescript
class A {
    name: string
    constructor(name: string) {
        this.name = name;
    }
}

class C {
    name: string
    constructor(name: string) {
        this.name = name;
    }
}

// 中间件用途解耦
class Container {
    modules: any
    constructor() {
        this.modules = {};
    }
    provide(key: string, modules: any) {
        this.modules[key] = modules;
    }
    get(key: string) {
        return this.modules[key];
    }
}

const mo = new Container();
mo.provide('a', new A('test-name1'));
mo.provide('c', new C('test-name2'));


class B {
    a: any
    c: any
    constructor(container: Container) {
        this.a = container.get('a');
        this.c = container.get('c');
    }
}

const b = new B(mo);

console.log(b.a.name);
```

在引入IOC容器container之后, B 与 A 的代码逻辑已经解耦, 可以单独扩展其他功能, 也可以方便加入其他模块C。所以在面对复杂的业务逻辑时, 引入IOC可以见底组件之间的耦合度, 实现系统各层之间的解耦, 减少维护和理解成本。

#### 三、装饰器
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669001820767-fe812f36-5b72-4824-9115-efe6c4b2e5fe.png)

##### 1、类装饰器
```typescript
@decorator
class A {}

// 等同于

class A {}
A = decorator(A) || A;

function decorator(target) {
	// target: 被装饰的类: A
}

// 装饰器也可以接受参数
function testable(isTestable: boolean) {
    return function(target: any) {
        // 给被装饰的类添加静态属性;
        target.isTestable = isTestable;
        // 给被装饰的类添加实例属性, 操作类的原型;
        target.prototype.isTestable = isTestable;
    }
}

@testable(true)
class MyTestableClass {}

declare type ClassDecorator = <TFunction extends Function>(
  target: TFunction
) => TFunction | void;
```



##### 2、方法装饰器
```typescript
class C {
  @trace
  toString() {
    return 'C';
  }
}

// 相当于
C.prototype.toString = trace(C.prototype.toString);

declare type MethodDecorator = <T>(
  target: Object,
  propertyKey: string | symbol,
  descriptor: TypedPropertyDescriptor<T>
) => TypedPropertyDescriptor<T> | void;

interface TypedPropertyDescriptor<T> {
    enumerable?: boolean;
    configurable?: boolean;
    writable?: boolean;
    value?: T;
    get?: () => T;
    set?: (value: T) => void;
}
```



##### 3、属性装饰器
```typescript
function logged(value, { kind, name }) {
  if (kind === "field") {
    return function (initialValue) {
      console.log(`initializing ${name} with value ${initialValue}`);
      return initialValue;
    };
  }

  // ...
}

class C {
  @logged x = 1;
}

new C();
// initializing x with value 1

declare type PropertyDecorator = (
  target: Object,
  propertyKey: string | symbol
) => void;
```

##### 4、参数装饰器
```typescript
const currency: ParameterDecorator = (target: any, key: string | symbol, index: number) => {
    console.log(target, key, index);
}

class Person {
    public name: string;
    constructor(name : string) {
        this.name = name;
    }
    getName(@currency age: number) {
        return this.name;
    }
}

declare type ParameterDecorator = (
  target: Object,
  propertyKey: string | symbol,
  parameterIndex: number
) => void;
```





##### eg: 通过装饰器实现nestjs底层GET
```typescript
import axios from 'axios';

const Get = (url: string): MethodDecorator => {
    return (target, key, descriptor: PropertyDescriptor) => {
        const fn = descriptor.value;
        console.log('descriptor', descriptor);
        axios.get(url).then(res => {
            fn(res, {
                status: 200,
            })
        }).catch(e => {
            fn(e, {
                status: 500,
            })
        })
    }
}

class Controller {
    constrctor() {}

    @Get('https://api.apiopen.top/api/getHaoKanVideo?page=0&size=10')
    getList(res: any, status: any) {
        console.log(res.data.result.list, status);
    }
}
```



#### 四、nestjs-cli
##### 1、通过nestjs-cli快速创建nestjs项目
`npm install -g @nestjs/cli`

`nest new [项目名称]`

<font style="color:rgb(77, 77, 77);">启动项目 我们需要热更新 就启动</font>`<font style="color:rgb(77, 77, 77);">npm run start:dev</font>`<font style="color:rgb(77, 77, 77);">就可以了</font>

```json
"start": "nest start",
"start:dev": "nest start --watch",
"start:debug": "nest start --debug --watch",
"start:prod": "node dist/main",
```



##### 2、目录
1. `<font style="color:rgb(77, 77, 77);">main.ts</font>`<font style="color:rgb(77, 77, 77);"> 入口文件主文件 类似于</font>`<font style="color:rgb(77, 77, 77);">vue</font>`<font style="color:rgb(77, 77, 77);"> 的</font>`<font style="color:rgb(77, 77, 77);">main.ts</font>`

<font style="color:rgb(77, 77, 77);">通过 </font>`<font style="color:rgb(77, 77, 77);">NestFactory.create(AppModule)</font>`<font style="color:rgb(77, 77, 77);"> 创建一个</font>`<font style="color:rgb(77, 77, 77);">app</font>`<font style="color:rgb(77, 77, 77);">  就是类似于绑定一个根组件</font>`<font style="color:rgb(77, 77, 77);">App.vue</font>`<font style="color:rgb(77, 77, 77);"> </font>`<font style="color:rgb(77, 77, 77);">app.listen(3000)</font>`<font style="color:rgb(77, 77, 77);">; 监听一个端口。</font>

<font style="color:rgb(77, 77, 77);"></font>

2. `<font style="color:rgb(77, 77, 77);">Controller.ts</font>`<font style="color:rgb(77, 77, 77);"> 控制器</font>

<font style="color:rgb(77, 77, 77);">你可以理解成vue 的路由</font>

`<font style="color:rgb(77, 77, 77);">private readonly appService: AppService</font>`<font style="color:rgb(77, 77, 77);"> 这一行代码就是依赖注入不需要实例化  </font>`<font style="color:rgb(77, 77, 77);">appService</font>`<font style="color:rgb(77, 77, 77);"> 它内部会自己实例化的我们主需要放上去就可以了。</font>

```typescript
import { Controller, Get } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}
```

<font style="color:rgb(77, 77, 77);"></font>

3. <font style="color:rgb(77, 77, 77);">app.service.ts</font>

<font style="color:rgb(77, 77, 77);">这个文件主要实现业务逻辑的 当然Controller可以实现逻辑，但是就是单一的无法复用，放到app.service有别的模块也需要就可以实现复用。</font>

```typescript
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```



##### 3、nestjs-cli常用命令
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669014490808-7dfc25f4-8160-4119-804e-c619bddef420.png)



1. <font style="color:rgb(79, 79, 79);"> 生成</font>`<font style="color:rgb(79, 79, 79);">controller.ts</font>`

`nest g co user`



2. <font style="color:rgb(79, 79, 79);">生成</font>`<font style="color:rgb(79, 79, 79);">module.ts</font>`

`nest g mo user`



3. <font style="color:rgb(79, 79, 79);">生成</font>`<font style="color:rgb(79, 79, 79);">service.ts</font>`

`nest g s user`



4. 生成完整的模块

以上步骤一个一个生成的太慢了我们可以直接使用一个命令生成`CURD`(<font style="color:rgb(51, 51, 51);">CURD 定义了用于处理数据的基本</font>原子操作<font style="color:rgb(51, 51, 51);">：创建（Create）、更新（Update）、读取（Read）和删除（Delete）操作</font>)。

`nest g resource  user`

<font style="color:rgb(77, 77, 77);"> 第一次使用这个命令的时候，除了生成文件之外还会自动使用 </font>`<font style="color:rgb(77, 77, 77);">npm</font>`<font style="color:rgb(77, 77, 77);"> 帮我们更新资源，安装一些额外的插件，后续再次使用就不会更新了。</font>

<font style="color:rgb(77, 77, 77);"> 生成了一套标准的</font>`<font style="color:rgb(77, 77, 77);">CURD</font>`<font style="color:rgb(77, 77, 77);"> 模板.</font>



#### 五、RESTful风格设计
`<font style="color:rgb(77, 77, 77);">REST</font>`<font style="color:rgb(77, 77, 77);"> 指的是一组架构约束条件和原则。满足这些约束条件和原则的应用程序或设计就是 </font>`<font style="color:rgb(77, 77, 77);">RESTful</font>`<font style="color:rgb(77, 77, 77);">。</font>

`<font style="color:rgb(77, 77, 77);">RESTFUL</font>`<font style="color:rgb(77, 77, 77);">特点包括：</font>

**<font style="color:rgb(77, 77, 77);">1、每一个URI代表1种资源；</font>**

<font style="color:rgb(77, 77, 77);">2、</font>**<font style="color:rgb(77, 77, 77);">客户端使用</font>**`**<font style="color:rgb(77, 77, 77);">GET</font>**`**<font style="color:rgb(77, 77, 77);">、</font>**`**<font style="color:rgb(77, 77, 77);">POST</font>**`**<font style="color:rgb(77, 77, 77);">、</font>**`**<font style="color:rgb(77, 77, 77);">PUT</font>**`**<font style="color:rgb(77, 77, 77);">、</font>**`**<font style="color:rgb(77, 77, 77);">DELETE</font>**`**<font style="color:rgb(77, 77, 77);">4个表示操作方式的动词对服务端资源进行操作：</font>**`**<font style="color:rgb(77, 77, 77);">GET</font>**`**<font style="color:rgb(77, 77, 77);">用来获取资源，</font>**`**<font style="color:rgb(77, 77, 77);">POST</font>**`**<font style="color:rgb(77, 77, 77);">用来新建资源（也可以用于更新资源），</font>**`**<font style="color:rgb(77, 77, 77);">PUT</font>**`**<font style="color:rgb(77, 77, 77);">用来更新资源，</font>**`**<font style="color:rgb(77, 77, 77);">DELETE</font>**`**<font style="color:rgb(77, 77, 77);">用来删除资源；</font>**

<font style="color:rgb(77, 77, 77);">3、通过操作资源的表现形式来操作资源；</font>

<font style="color:rgb(77, 77, 77);">4、资源的表现形式是</font>`<font style="color:rgb(77, 77, 77);">XML</font>`<font style="color:rgb(77, 77, 77);">或者</font>`<font style="color:rgb(77, 77, 77);">HTML</font>`<font style="color:rgb(77, 77, 77);">；</font>

<font style="color:rgb(77, 77, 77);">5、客户端与服务端之间的交互在请求之间是无状态的，从客户端到服务端的每个请求都必须包含理解请求所必需的信息。 </font>

<font style="color:rgb(77, 77, 77);"></font>

**传统接口与**`**RESTful**`**接口对比**

传统接口

`http://localhost:8080/api/get_list?id=1`

`http://localhost:8080/api/delete_list?id=1`

`http://localhost:8080/api/update_list?id=1`



`RESTful`接口

`http://localhost:8080/api/get_list/1` 支持 查询 删除 更新

`RESTful` 风格一个接口就会完成 增删改差 他是通过不同的请求方式来区分的。

查询 `GET`

提交 `POST`

更新 `PUT` `PATCH`

删除 `DELETE`

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669015436722-2a12df27-3910-48bf-b741-2450ae976096.png)



#### 六、code码规范
+ 200 OK
+ 304 `Not Modified` 协商缓存了
+ 400 `Bad Request` 参数错误
+ 401 `Unauthorized token`错误
+ 403 `Forbidden referer origin` 验证失败
+ 404 `Not Found` 接口不存在
+ 500 `Internal Server Error` 服务端错误
+ 502 `Bad Gateway` 上游接口有问题或者服务器问题



#### 七、Provider
`<font style="color:rgb(77, 77, 77);">Providers</font>`<font style="color:rgb(77, 77, 77);"> 是 </font>`Nest`<font style="color:rgb(77, 77, 77);"> 的一个基本概念。许多基本的 </font>`Nest`<font style="color:rgb(77, 77, 77);"> 类可能被视为 </font>`<font style="color:rgb(77, 77, 77);">provider - </font>service`<font style="color:rgb(77, 77, 77);">,</font> `repository`<font style="color:rgb(77, 77, 77);">, </font>`factory`<font style="color:rgb(77, 77, 77);">, </font>`helper`<font style="color:rgb(77, 77, 77);"> 等等。 他们都可以通过 </font>`constructor`<font style="color:rgb(77, 77, 77);"> </font>注入<font style="color:rgb(77, 77, 77);">依赖关系。 这意味着对象可以彼此创建各种关系，并且“连接”对象实例的功能在很大程度上可以委托给 </font>Nest<font style="color:rgb(77, 77, 77);">运行时系统。 </font>`<font style="color:rgb(77, 77, 77);">Provider</font>`<font style="color:rgb(77, 77, 77);"> 只是一个用 </font>`@Injectable()`<font style="color:rgb(77, 77, 77);">装饰器注释的类。</font>

##### 1、基本用法
1. `<font style="color:rgb(77, 77, 77);">module</font>`<font style="color:rgb(77, 77, 77);">引入</font>`<font style="color:rgb(77, 77, 77);">service</font>`<font style="color:rgb(77, 77, 77);">, 并在</font>`<font style="color:rgb(77, 77, 77);">providers</font>`<font style="color:rgb(77, 77, 77);">中注入 </font>

```typescript
import { Module } from '@nestjs/common';
import { UserService } from './user.service';
import { UserController } from './user.controller';

@Module({
  controllers: [UserController],
  providers: [UserService],
})
export class UserModule {}

```



2. <font style="color:rgb(77, 77, 77);">在</font>`<font style="color:rgb(77, 77, 77);">controller</font>`<font style="color:rgb(77, 77, 77);">就可以使用注入好的</font>`<font style="color:rgb(77, 77, 77);">service</font>`

```typescript
import { Controller } from '@nestjs/common';
import { UserService } from './user.service';

@Controller('user')
export class UserController {
  constructor(private readonly userService: UserService) {}
}

```



##### 2、自定义用法
```typescript
import { Module } from '@nestjs/common';
import { UserService } from './user.service';
import { UserController } from './user.controller';

@Module({
  controllers: [UserController],
  providers: [
    {
      provide: 'TestProvideName',
      useClass: UserService,
    },
    {
      provide: 'JD',
      useValue: ['TB', 'PDD', 'JD'],
    },
  ],
})
export class UserModule {}

```



<font style="color:rgb(77, 77, 77);">自定义名称之后 需要用对应的</font>`<font style="color:rgb(77, 77, 77);">Inject</font>`<font style="color:rgb(77, 77, 77);"> 取 不然会找不到的。</font>

```typescript
import { Controller, Inject } from '@nestjs/common';
import { UserService } from './user.service';

@Controller('user')
export class UserController {
  constructor(
    @Inject('TestProvideName') private readonly userService: UserService,
    @Inject('JD') private shopList: string[],
  ) {}

  @Get()
  findAll() {
    return {
      code: 200,
      data: this.shopList,
    };
  }
}

```



##### 3、工厂模式
类似于函数模式的服务类, 也可依赖别的类。

也支持异步模式, `<font style="color:rgb(77, 77, 77);">useFactory</font>`<font style="color:rgb(77, 77, 77);"> 返回一个</font>`<font style="color:rgb(77, 77, 77);">promise</font>`<font style="color:rgb(77, 77, 77);"> 或者其他异步操作。</font>

```typescript
import { Module } from '@nestjs/common';
import { UserService } from './user.service';
import { UserService2 } from './user.service2';
import { UserService3 } from './user.service3';
import { UserController } from './user.controller';
 
@Module({
  controllers: [UserController],
  providers: [{
      provide: "Xiaoman",
      useClass: UserService
    }, {
      provide: "JD",
      useValue: ['TB', 'PDD', 'JD']
    },
      UserService2,
    {
      provide: "Test",
      inject: [UserService2],
      useFactory(UserService2: UserService2) {
        return new UserService3(UserService2)
      }
    },
    {
      provide: "sync",
      async useFactory() {
        return await  new Promise((r) => {
          setTimeout(() => {
            r('sync')
          }, 3000)
        })
      }
    }
  ]
})
export class UserModule { }
```



#### 八、模块
<font style="color:rgb(77, 77, 77);">模块是具有 </font>`@Module()`<font style="color:rgb(77, 77, 77);">装饰器的类。 </font>`@Module()`<font style="color:rgb(77, 77, 77);">装饰器提供了元数据，</font>`<font style="color:rgb(77, 77, 77);">Nest</font>`<font style="color:rgb(77, 77, 77);"> 用它来组织应用程序结构。</font>

<font style="color:rgb(77, 77, 77);">每个 </font>`<font style="color:rgb(77, 77, 77);">Nest</font>`<font style="color:rgb(77, 77, 77);"> 应用程序至少有一个模块，即根模块。根模块是 </font>`<font style="color:rgb(77, 77, 77);">Nest</font>`<font style="color:rgb(77, 77, 77);"> 开始安排应用程序树的地方。事实上，根模块可能是应用程序中唯一的模块，特别是当应用程序很小时，但是对于大型程序来说这是没有意义的。在大多数情况下，您将拥有多个模块，每个模块都有一组紧密相关的</font>**功能**<font style="color:rgb(77, 77, 77);">。</font>



##### 1、基本用法
我们创建了`UserModule.ts`文件，同时需要将这个模块导入根模块`ApplicationModule`。

```typescript
import { Module } from '@nestjs/common';
import { UserController } from './user.controller';
import { UserService } from './user.service';

@Module({
  controllers: [UserController],
  providers: [UserService],
})
export class UserModule {}

```

```typescript
import { Module } from '@nestjs/common';
import { UserModule } from './cats/cats.module';

@Module({
  imports: [UserModule],
})
export class ApplicationModule {}

```



##### 2、共享模块
<font style="color:rgb(77, 77, 77);">当 </font>`<font style="color:rgb(77, 77, 77);">user</font>`<font style="color:rgb(77, 77, 77);"> 的 </font>`<font style="color:rgb(77, 77, 77);">Service</font>`<font style="color:rgb(77, 77, 77);"> 想暴露给 其他模块使用就可以使用 </font>`exports`<font style="color:rgb(77, 77, 77);"> 导出该服务。每个导入 </font>`CatsModule`<font style="color:rgb(77, 77, 77);"> 的模块都可以访问 </font>`CatsService`<font style="color:rgb(77, 77, 77);"> ，并且它们将共享相同的 </font>`CatsService`<font style="color:rgb(77, 77, 77);"> 实例。</font>

```typescript
import { Module } from '@nestjs/common';
import { UserController } from './user.controller';
import { UserService } from './user.service';

@Module({
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService],
})
export class UserModule {}

```



##### 3、全局模块
`@Global`<font style="color:rgb(77, 77, 77);"> 装饰器使模块成为全局作用域。 全局模块应该只注册一次，最好由根或核心模块注册。 在上面的例子中，</font>`UserService`<font style="color:rgb(77, 77, 77);"> 组件将无处不在，而想要使用 </font>`UserService`<font style="color:rgb(77, 77, 77);"> 的模块则不需要在 </font>`imports`<font style="color:rgb(77, 77, 77);"> 数组中导入 </font>`UserService`<font style="color:rgb(77, 77, 77);">。</font>

```typescript
import { Module, Global } from '@nestjs/common';
import { UserController } from './user.controller';
import { UserService } from './user.service';

@Global()
@Module({
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService],
})
export class UserModule {}

```



##### 4、动态模块
<font style="color:rgb(77, 77, 77);">动态模块主要就是为了给模块传递参数 可以给该模块添加一个静态方法 用来接受</font><font style="color:rgb(77, 77, 77);">参数。</font>

```typescript
import { Module, Global, DynamicModule } from '@nestjs/common';

interface Options {
  path: string;
}

@Global()
@Module({})
export class DymicModule {
  static forRoot(options: Options): DynamicModule {
    return {
      module: DymicModule,
      providers: [
        {
          provide: 'Config',
          useValue: { baseApi: '/api' + options.path },
        },
      ],
      exports: [
        {
          provide: 'Config',
          useValue: { baseApi: '/api' + options.path },
        },
      ],
    };
  }
}

```

<font style="color:rgb(77, 77, 77);"></font>

在使用的`module`中`import`, 并在对应的`controller`使用。

```typescript
import { Module } from '@nestjs/common';
import { ListService } from './list.service';
import { ListController } from './list.controller';
import { DymicModule } from '../dymic/dymic.module';

@Module({
  imports: [
    DymicModule.forRoot({
      path: '/dymic',
    }),
  ],
  controllers: [ListController],
  providers: [ListService],
  exports: [ListService],
})
export class ListModule {}

```

<font style="color:rgb(77, 77, 77);"></font>

```typescript
import {
  Controller,
  Get,
  Inject,
} from '@nestjs/common';
import { ConfigService } from '../config/config.service';

@Controller('list')
export class ListController {
  constructor(
    @Inject('Config') private readonly base: any,
  ) {}

  @Get()
  findAll() {
    return this.base;
  }
}

```





#### 参考文档
[https://xiaoman.blog.csdn.net/article/details/126150815?spm=1001.2014.3001.5502](https://xiaoman.blog.csdn.net/article/details/126150815?spm=1001.2014.3001.5502)

