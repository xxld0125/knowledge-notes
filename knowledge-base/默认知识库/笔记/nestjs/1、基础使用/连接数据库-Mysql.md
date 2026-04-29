#### 一、安装Mysql
先去[Mysql官网](https://dev.mysql.com/downloads/mysql/)下载<font style="color:rgb(77, 77, 77);">。</font>

`m1`的选择`ARM`<font style="color:rgb(77, 77, 77);">。</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669558310059-fa29d78b-b497-4377-a0e7-c4159f67c1ef.png)



<font style="color:rgb(77, 77, 77);"></font>

<font style="color:rgb(77, 77, 77);">这里可以不用登录直接选择 </font>`<font style="color:rgb(77, 77, 77);">No thanks, just start my download</font>`<font style="color:rgb(77, 77, 77);"> 即可下载。</font>





安装<font style="color:rgb(77, 77, 77);">一路点击继续即可。</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669558453931-aec18e4d-8350-4609-9ba2-56999edd822d.png)

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669558354657-11d522f8-b1f5-4b7a-8bde-34db58e70723.png)

<font style="color:rgb(77, 77, 77);">这里选择 Use Legacy Password Encryption 然后点击 Next。</font>![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669558535085-de361b5b-3008-47c9-9ad6-646d01229e00.png)



<font style="color:rgb(77, 77, 77);">安装完成后,此时可以打开系统偏好设置下方会出现一个</font>`<font style="color:rgb(77, 77, 77);">MySQL</font>`<font style="color:rgb(77, 77, 77);">的图标。</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669558670317-6d306bad-1b42-405d-a060-9efa1478a3b1.png)	



<font style="color:rgb(77, 77, 77);">点击进入可以查看到左边的两个绿色的小标意味着MySQL安装成功。</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669558719294-99e56637-1b28-4f81-85d5-12f58c95dfec.png)

#### 二、配置Mysql
安装完成之后,还需要<font style="color:rgb(77, 77, 77);">配置环境,在终端通过 vim 来编辑 .zshrc 配置文件</font>

`<font style="color:rgb(79, 79, 79);background-color:rgb(238, 240, 244);">sudo vim ~/.zshrc</font>`

<font style="color:rgb(79, 79, 79);background-color:rgb(238, 240, 244);"></font>

<font style="color:rgb(77, 77, 77);">点击 i 键，进入编辑模式，在配置文件中添加如下路径：</font>

`<font style="color:rgb(79, 79, 79);background-color:rgb(238, 240, 244);">export PATH=$PATH:/usr/local/mysql/bin</font>`



<font style="color:rgb(77, 77, 77);">然后按 esc 退出编辑模式，输入 </font>`<font style="color:rgb(77, 77, 77);">:wq</font>`<font style="color:rgb(77, 77, 77);"> 保存退出</font>

<font style="color:rgb(77, 77, 77);"></font>

<font style="color:rgb(77, 77, 77);">接着在终端执行 </font>`<font style="color:rgb(77, 77, 77);">source ~/.zshrc</font>`<font style="color:rgb(77, 77, 77);"> 使配置生效</font>

<font style="color:rgb(77, 77, 77);">此时在终端查看 mysql 版本可以看到已经可以查到我们安装的版本了，说明环境已经配好</font>

`<font style="color:rgb(79, 79, 79);background-color:rgb(238, 240, 244);">mysql --version</font>`

<font style="color:rgb(79, 79, 79);background-color:rgb(238, 240, 244);"></font>

<font style="color:rgb(77, 77, 77);"> 现在就可以在终端输入 </font>`<font style="color:rgb(77, 77, 77);">mysql -uroot -p</font>`<font style="color:rgb(77, 77, 77);"> 然后输入密码，进入</font>`<font style="color:rgb(77, 77, 77);">MySQL</font>`<font style="color:rgb(77, 77, 77);">使用了</font>

<font style="color:rgb(77, 77, 77);"></font>

#### 三、ORM框架(typeorm)
`<font style="color:rgb(77, 77, 77);">typeOrm</font>`<font style="color:rgb(77, 77, 77);"> 是 </font>`<font style="color:rgb(77, 77, 77);">TypeScript</font>`<font style="color:rgb(77, 77, 77);"> 中最成熟的对象关系映射器( </font>`<font style="color:rgb(77, 77, 77);">ORM</font>`<font style="color:rgb(77, 77, 77);"> )。因为它是用 </font>`<font style="color:rgb(77, 77, 77);">TypeScript</font>`<font style="color:rgb(77, 77, 77);"> 编写的，所以可以很好地与 </font>`<font style="color:rgb(77, 77, 77);">Nest</font>`<font style="color:rgb(77, 77, 77);"> </font>框架<font style="color:rgb(77, 77, 77);">集成</font>

<font style="color:rgb(77, 77, 77);">安装依赖</font>

```bash
npm install --save @nestjs/typeorm typeorm mysql2
```

  


<font style="color:rgb(77, 77, 77);">如果使用的是vsCode可安装数据库可视化工具 </font>`<font style="color:rgb(77, 77, 77);">Database Client</font>`

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669559130211-25356d34-6487-4189-bd62-9fc0de3152ac.png)



填写Mysql信息

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669559250700-a70217df-d9be-4ded-aa8b-2a292a42b0e0.png)

  
	新增一个库

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1669559343934-1809ed0a-d3f2-4065-9826-356db4f0151a.png)



#### 四、注册
在`app.modules.ts`注册数据库

```typescript
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'mysql', // 数据库类型
      username: 'root', // 账号
      password: '120616c.+', // 密码
      host: 'localhost', // host
      port: 3306, // 端口
      database: 'db', // 库名
      entities: [__dirname + '/**/*.entity{.ts,.js}'], // 实体文件
      synchronize: true, // 是否自动将实体类同步到数据库
      retryDelay: 500, // 重试连接数据库间隔
      retryAttempts: 10, // 充实连接数据库次数
      autoLoadEntities: true, // 如果为true,将自动加载实体forFeature()方法注册的每个实体都添加到配置对象的实体数组中
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

```



定义实体

```typescript
import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
} from 'typeorm';

@Entity()
export class Form {
  // 自增列
  @PrimaryGeneratedColumn()
  id: number;

  // 普通列
  @Column()
  name: string;

  @CreateDateColumn({ type: 'timestamp' })
  createTime: Date;
}

```



关联实体

```typescript
import { Module } from '@nestjs/common';
import { FormService } from './form.service';
import { FormController } from './form.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Form } from './entities/form.entity';

@Module({
  // 关联实体
  imports: [TypeOrmModule.forFeature([Form])],
  controllers: [FormController],
  providers: [FormService],
})
export class FormModule {}

```

