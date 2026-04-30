#### 一、基础类型
```typescript
// 1、布尔
let isDone: boolean = false;

// 2、数字
let decLiteral: number = 6;

// 3、字符串(支持模版字符串)
let firstName: string = "bob";

// 4、数组
let list1: number[] = [1, 2, 3];

// 数组泛型 Array<元素类型>
let list2: Array<number> = [4, 5, 6];

// 5、元组: 表示一个已知元素数量和类型的数组，各元素的类型不必相同
let x: [string, number] = ['hello', 10];

// 6、枚举: 默认情况下，从0开始为元素编号; 也可以手动置顶成员数值
enum Color {Red, Green = 2, Blue};
let c: Color = Color.Green;

// 7、Any: 不清楚类型的变量时使用
let notSure: any = 4;
notSure = false; // okay, definitely a boolean

// 8、Void: 表示没有任何类型, 当一个函数没有返回值时, 你通常会见到其返回值类型是 void
function warnUser(): void {
  console.error('This is my warning message');
}

// 9、Null & Undefined:
let u: undefined = undefined;
let n: null = null;

// 10、Never: 表示的是那些永不存在的值的类型(抛出异常或根本就不会有返回值的函数表达式或箭头函数表达式的返回值类型)
function error(message: string): never {
  throw new Error(message);
}

// 11、Object: 表示非原始类型，也就是除number，string，boolean，symbol，null或undefined之外的类型。
declare function create(o: object | null): void;

create({prop: 0}); // ok
create(null); // ok

create(42); // Error

```



#### 二、接口




#### 三、TS开发环境搭建
全局安装typescript: `npm i -g typescript`



#### 四、联合类型




#### 五、类型断言




#### 六、编译<u>选项</u>
##### 1、自动编译ts文件
`tsc xx.ts -w`：对单个文件监听改动，并自动编译成js文件。



##### 2、项目自动编译ts文件
`tsc`：可对当前项目下的ts文件进行编译。

`tsc -w`：可对当前项目下的ts文件进行监控, 并自动编译成js文件。

但前提是当前项目存在`tsconfig.json`。



##### 3、tsconfig.json
`tsconfig.json`是ts编译器的配置文件, ts编译器根据配置信息进行编译。

```json
{
  // 一、基础配置
	"include": [ // 需要编译的ts文件
    "./src/**/*" // ** 表示任意目录, * 表示任意文件
  ],
  "exclude": [], 
  "extends": "./configs/base", 继承置顶路径的tsconfig.json文件
  "files": [], // 指定需要编译的ts文件（不常用）

 
  // 二、常用配置
  "compilerOptions": { // 编译器选项
    "target": "ES3", // 用来指定ts被编译为的ES版本
    "module": "commonjs", // 指定生成哪个模块系统代码
    "lib": ["ES2015"], // 指定项目中编译过程中需要引入的库文件的列表
    "outdir": "./dist/", // 指定编译后的文件目录
    "outFile": "./dist/app.js", // 将输出文件合并为一个文件
    "allowJs": true, // 允许编译javascript文件
    "checkJs": true, // 检查js代码是否符合规范
    "removeComments": true, // 删除所有注释
  	"noEmit": true, // 不生成输出文件
    "noEmitOnError": true, // 报错时不生成输出文件
    "alwaysStrict": true, // 以严格模式解析并为每个源文件生成
    "noImplicitAny": true, // 在表达式和声明上有隐含的 any类型时报错
    "noImplicitThis": true, // 当 this表达式的值为 any类型的时候，生成一个错误
  	"strictNullChecks": true, // 在严格的 null检查模式下， null和 undefined值不包含在任何类型里，只允许用它们自己和 any来赋值
  }
}
```





#### 七、wepback打包ts








#### 八、ts面向对象
##### 1、抽象类 & 抽象方法
以`abstract`开头的类是抽象类, 抽象类和其他类的区别不大, 只是不能用来创建实例。

抽象类就是专门用来继承的。



抽象方法使用`abstract`开头, 没有方法体。

抽象方法只能定义在抽象类中，子类必须对抽象方法进行重写。

```typescript
abstract class Animal {
    move(distanceInMeters: number = 0) {
        console.log(`${this.name} moved ${distanceInMeters}m.`);
    }
  	abstract sayHello(): void;
}
```





##### 2、<font style="color:rgb(21, 39, 64);">公共，私有与受保护的修饰符</font>
+ public

默认为 public

```typescript
  class Animal {
      public name: string;
      public constructor(theName: string) { this.name = theName; }
      public move(distanceInMeters: number) {
          console.log(`${this.name} moved ${distanceInMeters}m.`);
      }
  }

```

+ private

当成员被标记成 private时，它就不能在声明它的类的外部访问

```typescript
class Animal {
    private name: string;
    constructor(theName: string) { this.name = theName; }
}

new Animal("Cat").name; // 错误: 'name' 是私有的.
```



+ protected

protected修饰符与 private修饰符的行为很相似，但有一点不同， protected成员在派生类中仍然可以访问。

```typescript
  class Person {
      protected name: string;
      protected constructor(name: string) { this.name = name; }
  }

  class Employee extends Person {
      private department: string;

      constructor(name: string, department: string) {
          super(name)
          this.department = department;
      }

      public getElevatorPitch() {
          return `Hello, my name is ${this.name} and I work in ${this.department}.`;
      }
  }

  let howard = new Employee("Howard", "Sales");
  console.log(howard.getElevatorPitch());
  console.log(howard.name); // 错误

  let john = new Person("John"); // 错误: 'Person' 的构造函数是被保护的.
```





#### 九、泛型


