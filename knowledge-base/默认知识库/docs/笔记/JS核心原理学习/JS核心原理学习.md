#### 一、数据类型
##### 1、数据类型概念
基础类型存储在栈内存，被引用或拷贝时，会创建一个完全相等的变量。

引用类型存储在堆内存，存储的是地址，多个引用指向同一个地址。



##### 2、数据类型检测
+ `typeof`：可以正确判断基础数据类型(`null`除外),但是引用数据类型中，只能判断`function`类型。
+ `instanceof`：可以准确判断复杂引用数据类型，但不能正确判断基础数据类型。
+ `Object.prototype.toString`：可以正确判断基础数据类型和复杂引用数据类型。

封装通用判断数据类型方法：

```javascript
function getType(obj) {
	let type = typeof obj;
  // 先进行typeof判断，如果是基础数据，就直接返回。
  if (type !== 'object') {
    return type;
  }
	// 对于typeof返回的是object的，再进行如下判断。
  return Object.prototype.toString.call(obj).replace(/^\[object (\S+)\]$/, '$1');
}
```



##### 3、数据类型转换
+ 强制数据类型转换
    - `Number`
        * `boolean`：`true` 和 `false` 转化为 1 和 0
        * `number`：返回自身
        * `null`：返回 0
        * `undefined`：返回`NaN`
        * `string`：
            + 字符串只包含数字，则将其转换成十进制
            + 字符串包含有效的浮点格式，将其转化成浮点数值
            + 空字符串，将其转化成0
            + 非以上格式，均返回`NaN`
        * `symbol`：抛出错误
        * `object`：进行`object`的隐式转换。
    - 
    - `Boolean`：除`undefined`、`null`、`""`、`0`（包括+0, -0）、`NaN`转换出来的都是`false`,其他都是`true`。
    - `parseFloat`
    - `toString`
    - `String`
    - `parseInt`
    - 。。。
+ 隐式类型转换
    - `==`
        * 两个操作值类型相同：无需转换
        * 其中一个操作值是`null`或`undefined`：另一个操作符必须为`null`或`undefined`才会返回`true`，否则都返回`false`
        * 其中一个是`Symbol`类型：返回`false`
        * 两个操作值都为`string`和`number`类型：字符串转化为`number`
        * 其中一个操作值是`boolean`：转化为`number`
        * 其中一个操作值为`object`，且另一个为`string`、`number`、`symbol`：进行`object`的隐式转化为原始类型在进行判断 
    - `+`
        *  其中一个是`string`
            + 另一个是`string`、`undefined`、`null`或`boolean`，则调用`toString()`进行字符串拼接。
            + 另一个是纯对象、数组、正则等，则进行`object`的隐式转化为原始类型在进行拼接
        * 其中一个是`number`，
            + 另一个是`undefined`、`null`、`boolean`或`number`，则会将其转换成数字进行加法运算
            + 另一个是纯对象、数组、正则等，则进行`object`的隐式转化为原始类型在进行拼接
+ object
    - 部署了`[Symbol.toPrimitive]`方法，优先调用再返回
    - 调用`valueOf()`，如果转化为基础类型则返回
    - 调用`toString()`，如果转化为基础类型则返回
    - 如果都没有返回基础类型，则报错



#### 二、继承
##### 1、原型链继承
原型链继承是比较常见的继承方式之一，其中涉及的构造函数、原型和实例。

+ 每一个构造函数都有一个原型对象
+ 原型对象又包含一个指向构造函数的指针
+ 实例包含一个原型对象的指针

```javascript
function Parent(){
  this.name = 'parent';
  this.play = [1,2,3];
}

function Child() {
  this.type = 'child';
}

Child.prototype = new Parent();

var s1 = new Child();
var s2 = new Child();

s1.play.push(4);

console.log(s1.play, s2.play); // [1,2,3,4] [1,2,3,4]
```



**缺点：**

**内存空间是共享的,当一个发生变化的时候,另外一个也随之进行了变化。**



##### 2、构造函数继承（借助call）
```javascript
function Parent(){
  this.name = 'parent';
}

Parent.prototype.getName = function() {
  return this.name;
}

function Child(){
  Parent.call(this);
  this.type = 'child';
}

let child = new Child();
console.log(child.name); // parent
console.log(child.getName()); // 报错
```



**缺点：**

**无法继承原型上的方法。**

****

##### 3、组合继承（前两种组合）
```javascript
function Parent(){
  this.name = 'parent';
  this.play = [1,2,3];
}

function Child(){
  Parent.call(this);
  this.type = 'child';
}

Child.prototype = new Parent();
Child.prototype.constructor = Child;

var s1 = new Child();
var s2 = new Child();

s1.play.push(4);

console.log(s1.play, s2.play); //[1,2,3,4] [1,2,3]
console.log(s1.getName()); // 正常输出parent
console.log(s2.getName()); // 正常输出parent

```



##### 4、原型式继承
```javascript
const parent = {
  name: 'parent',
  friends: ['p1','p2','p3'],
  getName: function(){
    return this.name;
  }
}
let person1 = Object.create(parent);
person1.name = 'tom';
person1.friends.push('p4');

let person2 = Object.create(parent);
person2.friends.push('p5');

console.log(person1.name); // tom
console.log(person1.name === person1.getName()); // true
console.log(person2.name); // parent
console.log(person1.friends); // ['p1','p2','p3', 'p4', 'p5']
console.log(person2.friends); // ['p1','p2','p3', 'p4', 'p5']
```



**缺点：**

**内存空间是共享的,当一个发生变化的时候,另外一个也随之进行了变化。**



##### 5、寄生式继承
寄生式继承相比于原型式，还是在父类基础上添加了更多的方法。

```javascript
let parent = {
	name: 'parent',
  friends: ['p1', 'p2', 'p3'],
  getName: function() {
    return this.name;
  }
}

function clone(original) {
	let clone = Object.create(original);
  clone.getFriends = function() {
    returm this.friends;
  }
}

let person = clone(parent);

console.log(person.getName()); // parent
console.log(person.getFriends()); // ['p1', 'p2', 'p3']
```



##### 6、寄生组合式继承
```javascript
function clone(parent, child) {
  child.prototype = Object.create(parent.prototype);
  child.prototype.constructor = child;
}

function Parent() {
  this.name = 'parent';
  this.play = [1,2,3];
}

Parent.prototype.getName = function() {
  return this.name;
}

function Child() {
  Parent.call(this);
  this.friends = 'p1';
}

clone(Parent, Child);

Child.prototype.getFriends = function() {
  return this.friends;
}

let person = new Child();
console.log(person);
console.log(person.getName); // parent
console.log(person.getFriends); // p1

```

##### 7、extends
```javascript
class Person {
  constructor(name) {
    this.name = name;
  }
	getName() {
    console.log('Person:', this.name);
  }
}

class Gamer extends Person {
	constructor(name, age) {
    // 子类中存在构造函数，则需要在使用this之前首先调用super()
    super(name);
    this.age = age;
  }
}

const asuna = new Gamer('Asuna', 20)
asuna.getName(); 
```





```javascript
function _possibleConstructorReturn(self, call) {
  return call && (typeof call === 'object' || typeof call === 'function') ? call : self;
}

function _inherits(subClass, superClass) {

  subClass.prototype = Object.create(superClass && superClass.prototype, {
    constructor: {
      value: subClass,
      enumerable: false,
      writable: true,
      configurable: true,
    }
  });

  if(superClass) 
    Object.serPrototypeOf
      ? Object.setPrototypeOf(subClass, superClass)
      : subClass.__proto__ = superClass;
}

var Parent = function Parent() {
  // 验证是否是Parent构造出来的this
  _classCallCheck(this, Parent);
}

var Child = (function(_Parent) {
  _inherits(Child, _Parent);

  function Child() {
    _classCallCheck(this, Child);
    return _possibleConstructorReturn(this, (
      Child.__proto__ || Object.getPrototypeOf(Child).apply(this, arguments)
    ));
  }
}(Parent));
```



##### 8、总结
![画板](https://cdn.nlark.com/yuque/0/2023/jpeg/25743026/1676807627642-f7ac5d72-0e34-4996-90e0-da10766503ef.jpeg)



#### 三、继承进阶
##### 1、new
new的作用就是执行一个构造函数、返回一个实例对象，根据构造函数的情况，来确定是否可以接受参数的传递。



具体作用：

1. 创建一个新对象
2. 将构造函数的作用于赋给新对象(this指向新对象)
3. 执行构造函数中的代码(为这个新对象添加属性)
4. 返回新对象



##### 2、call、apply、bind
应用场景：

1. 判断数据类型

```javascript
function getType(obj) {
	let type = typeof obj;
  if (type !== 'object') {
    return type;
  }
  return Object.prototype.toString.call(obj).replace(/^$/, '$1');
}
```



2. 类数组借用方法

类数组因为不是真正的数组，所有没有数组类型上自带的方法，可以利用一些方法去**借用**数组的方法。

```javascript
var arrayLike = {
  0: 'java',
  1: 'script',
  length: 2
}

Array.prototype.push.call(arrayLike, 'jack', 'lily');
console.log(typeof arrayLike); // object
console.log(arrayLike);
// {0: 'java',1: 'script',2: 'jack',3: 'lily',length: 4}
```



3. 获取数组的最大/小值

用`apply`来实现数组中判断最大/小值，`apply`直接传递数组作为调用方法的参数，也可以减少一步展开数组。

```javascript
let arr = [13,6,10,11,16];
const max = Math.max.apply(Math, arr);
const min = Math.min.apply(Math, arr);

console.log(max); // 16
console.log(min); // 6
```



4. 继承

```javascript
function Parent() {
  this.name = 'parent';
  this.play = [1,2,3];
}
Parent.prototype.getName = function() {
  return this.name;
}
function Child() {
  Parent.call(this);
  this.type = 'child';
}
Child.prototype = new Parent();
Child.prototype.constructor = Child;
var s = new Child();
console.log(s.getName()); // parent;
```



##### 3、new的实现
new 被调用后大致做了哪几件事情

1. 让实例可以访问到私有属性
2. 让实例可以访问构造函数原型(`constructor.prototype`)所在原型链上的属性
3. 构造函数返回的最后结果是引用数据类型



```javascript
function _new(ctor, ...args){
  if (typeof ctor !== 'function'){
    throw 'ctor must be a function';
  }
  let obj = new Object();
  obj.__proto__ = Object.create(ctor.prototype);
  let res = ctor.apply(obj, args);

  let isObject = typeof res === 'object' && typeof res !== null;
  let isFunction = typeof res === 'function';

  return isObject || isFunction ? res : obj;
}
```



#####  4、apply和call的实现
直接返回执行结果

```javascript
Function.prototype.call = function(context, ...args) {
	var context = context || window;
  context.fn = this;
  var result = eval('context.fn(...args)');
  delete context.fn;
  return result;
}

Function.prototype.apply = function(context, args) {
  let context = context || window;
  context.fn = this;
  let result = eval('context.fn(...args)');
  delete context.fn;
  return result;
}
```



##### 5、bind实现
```javascript
Function.prototype.bind = function(context, ...args) {
  if (typeof this !== 'function') {
    throw new Error('this must be a function');
  }
  var self = this;
  var fbound = function() {
    self.apply(
      this instanceof self ? this : context,
      args.concat(Array.prototype.slice.call(arguments))
    );
  }
  if (this.prototype) {
    fbound.prototype = Object.create(this.prototype);
  }
  return fbound;
}
```



#### 四、闭包
#####  1、作用域
指变量能够被访问到的范围。

+ 全局作用域
+ 函数作用域
+ 块级作用域(ES6)



##### 2、闭包
闭包是指有权访问另一个函数作用域中的变量的函数。



##### 3、作用域链
当访问一个变量时，代码解释器会首先在当前的作用域查找，如果没有找到就会去父级作用域去查找，直到找到该变量或者不存在父级作用域中。



##### 4、应用场景
+ 返回一个函数
+ 在定时器、事件监听、ajax请求、web workers或者任何异步中，只要使用了回调函数，实际上就是在使用闭包
+ 作为函数参数传递的形式

```javascript
var a = 1;
function foo() {
  var a = 2;
  function baz() {
    console.log(a);
  }
  bar(baz);
}

function bar(fn) {
  // 这就是闭包
  fn();
}

foo(); // 2
```

+ IIFE(立即执行函数)，创建了闭包

保存了全局作用于(`window`)和当前函数的作用域，因此可以输出全局的变量。

```javascript
var a = 2;
(function IIFE() {
  console.log(a); // 2
})()
```

