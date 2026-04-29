### 一、DOM常用API


```html
// 获取元素
getElementById(id);
getElementsByName(elementName); // 标签：name属性值
document.getElementsByTagName(elementName);

querySelector(".class|#id|name");
querySelectorAll(".class|#id|name");


// 创建元素
document.createElement(name); // 创建一个具体的元素
createDocumentFragment()    //创建一个DOM片段
createTextNode()   //创建一个文本节点

// 添加元素
document.body.appendChild(heading);

// 删除元素
document.body.removeChild(node);


<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>DOM 操作</title>
    <style>
      div {
        border: 1px solid #ccc;
        padding: 50px;
        width: 100px;
      }
    </style>
  </head>
  <body>
    <div id="dom1">元素 1</div>
    <div class="dom2">元素 2</div>
    
    <button class="btn">点我</button>
    
    <script>
      (function() {
        const btn = document.querySelector('.btn');
        
        // 注册点击事件
        btn.onclick = function() {
          const dom1 = document.getElementById('dom1');
          
          // 第一种添加元素
          const newDom1 = document.createElement('p');
          newDom1.innerHTML = '<a href="https://github.com/LiangJunrong/document-library">jsliang 的文档库</a>';
          dom1.appendChild(newDom1);
          
          // 第二种添加元素
          const newDom2 = document.createElement('ul');
          newDom2.innerHTML = `
          <li>aaa</li>
          <li>bbb</li>
          `;
          document.body.appendChild(newDom2);
          
          // 移除元素
          const dom2 = document.querySelector('.dom2');
          document.body.removeChild(dom2);
        }
      })()
    </script>
  </body>
</html>
```



### 二、null和undefined的区别


+ `null` 表示 `无` 的对象，也就是此处不应该有值；而 `undefined` 表示未定义。
+ 在转换数字的时候，`Number(null)` 为 `0`，而 `Number(undefined)` 为 `NaN`。



使用场景细分如下：



+ `null`：



1. 作为函数的参数，表示该函数的参数不是对象。
2. 作为对象原型链的终点。`Object.prototype.__proto__ === null`



+ `undefined`：



1. 变量被声明但是没有赋值，等于 `undefined`。
2. 调用函数时，对应的参数没有提供，也是 `undefined`。
3. 对象没有赋值，这个属性的值为 `undefined`。
4. 函数没有返回值，默认返回 `undefined`。



### 三、常用的原型检测方法：


+ 对象.`prototype`:设置构造函数的原型对象;
+ `_proto_`查看对象的原型对象
+ 属性 `in` 指定对象 ： 查看指定对象是否在某对象的原型链上；
+ 对象.`hasOwnProperty`(属性),判断某对象是否有指定的私有属性 （返回布尔值）；
+ 对象 `instanceof` 指定对象 ： 判断指定对象的原型是否在对象的原型链上；
+ 指定对象 `isPrototyOf` 对象 ： 判断对象是否在指定对象的原型链上（指定该对象带prototype）



### 五、this


#### 5.1定义：
this绑定的对象即函数执行的上下文环境（context）。



#### 5.2this指向：
1、当this所在的函数时箭头函数时，this的指向与箭头函数所在作用域的this指向同一个对象；

2、当this所在函数的调用，通过call、apply或bind处理后，this指向call、apply或bind的第一个参数；

3、当this所在的函数通过new处理后，函数内的this指向new生成的实例对象；







#### 5.3特殊情况的this的指向：
1、call和bind传递的参数无限制，写在绑定的对象后，apply传递的参数需要写成数组形式，放在绑定的对象后；

2、call和apply处理的函数调用，会立即执行；bind处理的函数调用，会延时执行；

3、bind会返回与原函数相同的函数，call和apply会返回函数的返回值；

4、call和apply处理的函数调用，会临时改变函数内this的指向；bind处理的函数调用，会永久改变函数内this的指向；



### 六、JS 位置


+ `clientHeight`：表示可视区域的高度，不包含 `border` 和滚动条
+ `offsetHeight`：表示可视区域的高度，包含了 `border` 和滚动条
+ `scrollHeight`：表示了所有区域的高度，包含了因为滚动被隐藏的部分
+ `clientTop`：表示边框 `border` 的厚度，在未指定的情况下一般为 `0`
+ `scrollTop`：滚动后被隐藏的高度，获取对象相对于由 `offsetParent` 属性指定的父坐标（CSS 定位的元素或 `body` 元素）距离顶端的高度。



### 七、JS拖拽


+ 通过 `mousedown`、`mousemove`、`mouseup` 方法实现
+ 通过 HTML5 的 `Drag` 和 `Drop` 实现



### 八、setTimeout实现setInterval


这算另类知识点吧，本来打算归类手写源码系列的，但是想想太 `low` 了，没牌面，入基础系列吧：



```javascript
const say = () => {
  // do something
  setTimeout(say, 200);
};

setTimeout(say, 200);
```



清除这个定时器：



```javascript
let i = 0;

const timeList = [];

const say = () => {
  // do something
  console.log(i++);
  timeList.push(setTimeout(say, 200));
};

setTimeout(say, 200);

setTimeout(() => {
  for (let i = 0; i < timeList.length; i++) {
    clearTimeout(timeList[i]);
  }
}, 1000);
```



### 九、实现sleep


如下，实现 `1000` 毫秒后执行其他内容：



```javascript
const sleep = time => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(time);
    }, time);
  });
};

sleep(1000).then((res) => {
  console.log(res);
});
```



### 十、执行上下文


#### 10.1 执行上下文类型


JavaScript 中有 3 种执行上下文类型：



+ **全局执行上下文**：这是默认或者说基础的上下文，任何不在函数内部的代码都在全局上下文中。它会执行两件事：创建一个全局的 `window` 对象（浏览器的情况下），并且设置 `this` 的值等于这个全局对象。一个程序中只会有一个全局执行上下文。
+ **函数执行上下文**：每当一个函数被调用时, 都会为该函数创建一个新的上下文。每个函数都有它自己的执行上下文，不过是在函数被调用时创建的。函数上下文可以有任意多个。每当一个新的执行上下文被创建，它会按定义的顺序执行一系列步骤。
+ **Eval 函数执行上下文**：执行在 `eval` 函数内部的代码也会有它属于自己的执行上下文，但由于 JavaScript 开发者并不经常使用 `eval`，所以在这里我不会讨论它。



#### 10.2 执行栈


执行栈，也就是在其它编程语言中所说的 “调用栈”，是一种拥有 `LIFO`（后进先出）数据结构的栈，被用来存储代码运行时创建的所有执行上下文。



当 JavaScript 引擎第一次遇到你的脚本时，它会创建一个全局的执行上下文并且压入当前执行栈。每当引擎遇到一个函数调用，它会为该函数创建一个新的执行上下文并压入栈的顶部。



引擎会执行那些执行上下文位于栈顶的函数。当该函数执行结束时，执行上下文从栈中弹出，控制流程到达当前栈中的下一个上下文。



```javascript
let a = 'Hello World!';

function first() {
  console.log('Inside first function');
  second();
  console.log('Again inside first function');
}

function second() {
  console.log('Inside second function');
}

first();
console.log('Inside Global Execution Context');
```



![](https://mmbiz.qpic.cn/mmbiz_jpg/P8CbrweAZpDqlETOsGJnShvC62Epm8eJGQ6gd3hZwp6HpOwxo5Z1ZHeQTx5nWS6dOlFdqRdPTU0VozoHibub3FQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



### 十一、函数式编程


函数式编程（Functional Programming，简称 FP）。



函数式编程：通过对面向对象式编程代码的拆分，将各个功能独立出来，从而达到功能独立、易复用等目的。



举例：代码转换



```javascript
['john-reese', 'harold-finch', 'sameen-shaw'] 
// 转换成 
[{name: 'John Reese'}, {name: 'Harold Finch'}, {name: 'Sameen Shaw'}]
```



对上面代码进行转换。



```javascript
const arr = ['john-reese', 'harold-finch', 'sameen-shaw'];
const newArr = [];
for (let i = 0, len = arr.length; i < len ; i++) {
  let name = arr[i];
  let names = name.split('-');
  let newName = [];
  for (let j = 0, naemLen = names.length; j < naemLen; j++) {
    let nameItem = names[j][0].toUpperCase() + names[j].slice(1);
    newName.push(nameItem);
  }
  newArr.push({ name : newName.join(' ') });
}
return newArr;
```



这份代码中，有 2 个部分：



1. 拆分数组中字符串，将字符串变成人名。`john-reese -> John Reese`
2. 将数组转换成对象。`['John Reese'] -> [{ name: 'John Reese' }]`



所以我们直接可以改动：



```javascript
/**
* @name 改变人名展示方式
* @param {array} arr 需要改变的数组
* @param {string} type 支持不同格式的人名
*/
const changeName = (arr, type) => {
  return arr.map(item => item.split(type).map(name => name[0].toUpperCase() + name.slice(1)).join(' '));
};

/**
* @name 数组改变成对象
* @param {array} arr 需要改变的数组
* @param {string} key 对应变成什么字段
* @return {object} 返回改变后的对象
*/
const arrToObj = (arr, key) => {
  return arr.map(item => ({ [key]: item }));
};

const result = arrToObj(changeName(['john-reese', 'harold-finch', 'sameen-shaw'], '-'), 'name');
console.log(result); // [ { name: 'John Reese' }, { name: 'Harold Finch' }, { name: 'Sameen Shaw' } ]
```



嗨，这不就是对功能封装吗？一般来说工作中出现 2 次以上的代码才进行封装。



函数式编程就是对可以抽离的功能都进行抽取封装。



> 到这里仿佛掌握了真理，**jsliang** 也没详细了解定义撒，希望没误导。
>



#### 11.1 函数式编程特点


1. **函数是一等公民**。可以利用这点让它支持抽取到外部。
2. **声明做某件时间**。函数式编程大多数声明某个函数需要做什么，而不是它怎么做的。
3. **便于垃圾回收**。函数内部的变量方便垃圾回收，不会产生太多的变量，用户不需要大量的定义。
4. **数据不可变**。函数式编程要求所有的数据都是不可变的，如果需要修改某个对象，应该新建后再修改，而不是污染原本的数据。
5. **无状态**。不管什么时候运行，同一个函数对相同的输入返回相同的输出，而不依赖外部状态的变化。
6. **无副作用**。功能 A 应该仅仅为了完成它的实现，而不会随着外部的改变而改变，这样当它执行完毕之后，就可以将其内部数据进行回收。并且它不会修改传入的参数。



注重引用值（Object、Array）的传递，尽可能不要污染传入的数据。



#### 11.2 纯函数


纯函数的概念有 2 点：



1. **不依赖外部状态（无状态）**：函数的运行结果不依赖全局变量，`this` 指针，`IO` 操作等。
2. **没有副作用（数据不变）**：不修改全局变量，不修改入参。



优点：



+ 便于测试和优化
+ 可缓存性
+ 自文档化
+ 更少 Bug



### 十二、渐进式网络应用


渐进式网络应用（PWA）是谷歌在 2015 年底提出的概念。基本上算是 Web 应用程序，但在外观和感觉上与原生 App 类似。支持 PWA 的网站可以提供脱机工作、推送通知和设备硬件访问等功能。



#### 12.1 优点


+ **更小更快**: 渐进式的 Web 应用程序比原生应用程序小得多。他们甚至不需要安装。这是他们没有浪费磁盘空间和加载速度非常快。
+ **响应式界面**: PWA 支持的网页能够自动适应各种屏幕大小。它可以是手机、平板、台式机或笔记本。
+ **无需更新**: 大多数移动应用程序需要每周定期更新。与普通网站一样，每当用户交互发生且不需要应用程序或游戏商店批准时，PWA 总是加载最新更新版本。
+ **高性价比**：原生移动应用需要分别为 Android 和 iOS 设备开发，开发成本非常高。另一方面，PWA 有着相同的功能，但只是先前价格的一小部分，开发成本低。
+ **SEO 优势**：搜索引擎可以发现 PWA，并且加载速度非常快。就像其他网站一样，它们的链接也可以共享。提供良好的用户体验和结果，在 SEO 排名提高。
+ **脱机功能**：由于 Service Worker API 的支持，可以在脱机或低internet连接中访问PWAs。
+ **安全性**：PWA 通过 HTTPS 连接传递，并在每次交互中保护用户数据。
+ **推送通知**：通过推送通知的支持，PWA 轻松地与用户进行交互，提供非常棒的用户体验。
+ **绕过应用商店**：原生 App 如果需要任何新的更新，需要应用商店几天的审批，且有被拒绝或禁止的可能性，对于这方面来说，PWA 有它独特的优势，不需要 App Store 支持。更新版本可以直接从 Web 服务器加载，无需 App Store 批准。
+ **零安装**：在浏览过程中，PWA 会在手机和平板电脑上有自己的图标，就像移动应用程序一样，但不需要经过冗长的安装过程。



#### 12.2 缺点


+ **对系统功能的访问权限较低**：目前 PWA 对本机系统功能的访问权限比原生 App 有限。而且，所有的浏览器都不支持它的全部功能，但可能在不久的将来，它将成为新的开发标准。
+ **多数 Android，少数 iOS**：目前更多的支持来自 Android。iOS 系统只提供了部分。
+ **没有审查标准**：PWA 不需要任何适用于应用商店中本机应用的审查，这可能会加快进程，但缺乏从应用程序商店中获取推广效益。



### 十三、规范化


`CommonJS` 规范、`AMD` 规范、`CMD` 规范、`ES6 Modules` 规范这 4 者都是前端规范化的内容，那么它们之间区别是啥呢？



在没有这些之前，我们通过：



+ 一个函数就是一个模块。`function fn() {}`
+ 一个对象就是一个模块。`let obj = new Object({ ... })`
+ 立即执行函数（IIFE）。`(function() {})()`



#### 13.1 CommonJS 规范


这之后，就有了 `CommonJS` 规范，其实 `CommonJS` 我们见得不少，就是 `Node` 的那套：



+ 导出：`module.exports = {}`、`exports.xxx = 'xxx'`
+ 导入：`require(./index.js)`
+ 查找方式：查找当前目录是否具有文件，没有则查找当前目录的 `node_modules` 文件。再没有，冒泡查询，一直往系统中的 `npm` 目录查找。



它的特点：



1. 所有代码在模块作用域内运行，不会污染其他文件
2. `require` 得到的值是值的拷贝，即你引用其他 JS 文件的变量，修改操作了也不会影响其他文件



它也有自己的缺陷：



1. 应用层面。在 `index.html` 中做 `var index = require('./index.js')` 操作报错，因为它最终是后台执行的，只能是 `index.js` 引用 `index2.js` 这种方式。
2. 同步加载问题。`CommonJS` 规范中模块是同步加载的，即在 `index.js` 中加载 `index2.js`，如果 `index2.js` 卡住了，那就要等很久。



#### 13.2 AMD 规范


为什么有 `AMD` 规范？



答：`CommonJS` 规范不中用：



1. 适用客户端
2. 等待加载（同步加载问题）。



所以它做了啥？



可以采用异步方式加载模块。`AMD` 是 `Asynchronous Module Definition` 的缩写，也就是 “异步模块定义”，记住这个 `async` 就知道它是异步的了。



#### 13.3 CMD 规范


CMD (Common Module Definition), 是 seajs 推崇的规范，CMD 则是依赖就近，用的时候再 `require`。



AMD 和 CMD 最大的区别是对依赖模块的执行时机处理不同，注意不是加载的时机或者方式不同，二者皆为异步加载模块。



#### 13.4 ES6 Modules 规范


+ 导出：



1. `export a`
2. `export { a }`
3. `export { a as jsliang }`
4. `export default function() {}`



+ 导入：



1. `import './index'`
2. `import { a } from './index.js'`
3. `import { a as jsliang } from './index.js'`
4. `import * as index from './index.js'`



特点：



1. `export` 命令和 `import` 命令可以出现在模块的任何位置，只要处于模块顶层就可以。如果处于块级作用域内，就会报错，这是因为处于条件代码块之中，就没法做静态优化了，违背了 ES6 模块的设计初衷。
2. `import` 命令具有提升效果，会提升到整个模块的头部，首先执行。



和 `CommonJS` 区别：



+ `CommonJS` 模块是运行时加载，`ES6 Modules` 是编译时输出接口
+ `CommonJS` 输出是值的拷贝；`ES6 Modules` 输出的是值的引用，被输出模块的内部的改变会影响引用的改变
+ `CommonJs` 导入的模块路径可以是一个表达式，因为它使用的是 `require()` 方法；而 `ES6 Modules` 只能是字符串
+ `CommonJS this` 指向当前模块，`ES6 Modules` 的 `this` 指向 `undefined`
+ `ES6 Modules` 中没有这些顶层变量：`arguments`、`require`、`module`、`exports`、`__filename`、`__dirname`



### 十四、babel编译原理


+ `babylon` 将 `ES6/ES7` 代码解析成 `AST`
+ `babel-traverse` 对 `AST` 进行遍历转译，得到新的 `AST`
+ 新 `AST` 通过 `babel-generator` 转换成 `ES5`



这一块的话 **jsliang** 并没有过分深究，单纯理解的话还是容易理解的：



1. 黑白七巧板组成的形状，拆分出来得到零件（`ES6/ES7` 解析成 `AST`）
2. 将这些零件换成彩色的（`AST` 编译得到新 `AST`）
3. 将彩色零件拼装成新的形状（`AST` 转换为 `ES5`）



### 十五、题集


#### 15.1 数组常见 API


+ `push`：数组尾部添加元素
+ `unshift`：数组头部添加元素
+ `pop`：数组尾部移除元素
+ `shift`：数组头部移除元素
+ `splice`：删除数组元素
+ `slice`：截取数组元素
+ `indexOf`：查找某元素第一次出现的位置
+ `lastIndexof`：查找某元素最后一次出现的位置
+ `findIndex`：查找元素第一次出现的位置
+ `forEach`：遍历元素
+ `map`：遍历元素
+ `filter`：过滤元素
+ `some`：包含某元素
+ `every`：所有元素和某元素一致
+ `includes`：查看是否包含某元素
+ `concat`：合并元素
+ `join`：合并元素，变成字符串
+ `toString`：变成字符串
+ `sort`：元素排序



#### 15.3 数组去重


数组去重是个经常提及的点：



```javascript
const arr = [1, 1, 2, 3, 3];
// 期望得到：[1, 2, 3]

// 方法一：for 配合新数组截取
const newArr1 = [];
for (let i = 0; i < arr.length; i++) {
  if (!newArr1.includes(arr[i])) {
    newArr1.push(arr[i]); 
  }
}
console.log('newArr1：', newArr1);

// 方法二：使用 Set
const newArr2 = [...new Set(arr)];
console.log('newArr2：', newArr2);

// 方法三：使用 filter
const newArr3 = arr.filter((item, index) => arr.lastIndexOf(item) === index);
console.log('newArr3：', newArr3);
```



有一次面试碰到的有意思的提问是：不使用数组 `API` 进行去重。



> 注意：不能使用 `push`、`indexOf` 等 `API`
>



#### 15.4 数字化金额


+ **方法一：暴力遍历**



```javascript
const num = String(1234567890);
let result = '';

for (let i = num.length - 1; i >= 0; i--) {
  if (i !== num.length - 1 && i % 3 === 0) {
    result = num[i] + ',' + result;
  } else {
    result = num[i] + result;
  }
}

console.log(result);
```



+ **方法二：API 技巧**



```javascript
console.log(
  String(1234567890).split('').reverse().reduce((prev, next, index) => (index % 3) === 0 ? next + ',' + prev : next + prev)
);
```



+ **方法三：API技巧**



```javascript
console.log(
  (1234567890).toLocaleString('en-US')
);
```



+ **方法四：正则表达式**



```javascript
String(1234567890).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
```



#### 15.5 遍历问题


以下代码执行后，array 的结果是？



```javascript
let array = [ , 1, , 2, , 3];
array = array.map((i) => ++i)
```



+ A：`[ , 2, , 3, , 4]`
+ B：`[NaN, 2, NaN, 3, NaN, 4]`
+ C：`[1, 2, 1, 3, 1, 4]`
+ D：`[null, 2, null, 3, null, 4]`

---

答案：A



解释：



1. `forEach()`、`filter()`、`reduce()`、`every()` 和 `some()` 都会跳过空位。
2. `map()` 会跳过空位，但会保留这个值
3. `join()` 和 `toString()` 会将空位视为 `undefined`，而 `undefined` 和 `null` 会被处理成空字符串。



#### 15.6 setTimeout


```javascript
for (var i = 0; i < 5; i++) {
  setTimeout(() => {
    console.log(i);
  }, 1000);
}
```



以上代码执行结果？



+ A：5 5 5 5 5
+ B：0 0 0 0 0
+ C：0 1 2 3 4
+ D：1 2 3 4 5

---

答案：A



解析：



1. `var i` 在 `for` 中使用，会造成变量污染，从而导致全局有一个遍历 `i`，这个 `i` 运行到最后，就是 `5`
2. `setTimeout` 是宏任务，在 `script` 这个宏任务执行完毕后才执行，所以搜集到的 `i` 是 `5`
3. 最终输出 5 个 `5`



#### 15.7 requestAnimationFrame


```javascript
for (let i = 0; i < 5; i++) {
  requestAnimationFrame(() => {
    console.log(i);
  });
}
```



以上代码执行结果：



+ A：1 2 3 4 5
+ B：0 1 2 3 4
+ C：4 4 4 4 4
+ D：5 5 5 5 5

---

答案：B



解析：



1. `let i` 使 `for` 形成块级作用域。
2. `requestAnimationFrame` 类似于 `setTimeout`，但是它可以当成一个微任务来看，是在微任务队列执行完毕后，执行 UI 渲染前，调用的一个方法。
3. 因此，这道题并不是指 `requestAnimationFrame` 会收集 `i`，而是 `let` 形成了块级作用域的问题，如果改成 `var i`，照样输出 5 个 `5`。



#### 15.8 暂时性死区


1、下面代码输出什么？



```javascript
let a = 1;
let test = function() {
  console.log(a);
  a++;
}
test();
```



2、下面代码输出什么？



```javascript
let a = 1;
let test = function() {
  console.log(a);
  let a = 2;
  a++;
}
test();
```

---

答案：



第一道题输出：`1`



第二道题输出：`Uncaught ReferenceError: Cannot access 'a' before initialization`



解析：



其原因是在同一个 `block` 中，`let` 在后面重新定义的，那么就不能在之前引用该变量。同时，也不能取嵌套外层的值。



#### 15.9 输出打印结果


```javascript
function sayHi() {
  console.log(name);
  console.log(age);
  var name = "Lydia";
  let age = 21;
}

sayHi();
```



上面代码输出结果？

---

答案：undefined、报错



解析：



这道题转变一下就看明白了：



```javascript
function sayHi() {
  var name; // 变量提升 - 变量声明
  console.log(name); // undefined
  console.log(age); // let 存在暂时性死区，不会变量提升
  name = "Lydia"; // 变量提升 - 变量赋值
  let age = 21;
}

sayHi();
```



#### 15.10 输出打印结果


```javascript
function myFunc() {
  console.log(a);
  console.log(func());
  
  var a = 1;
  function func() {
    return 2;
  }
}

myFunc();
```



请问输出啥？

---

答案：`undefined` `2`



解析：不难，不解析了



#### 15.11 Event Loop


```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 1);
}

for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 1);
}
```



上面代码输出结果？

---

答案和解析：



第一道题目：`var` 在 `for` 中存在变量污染，同步代码 `for` 执行完毕之后，再执行宏任务 `setTimeout`，发现当前 `i` 都成为 `3` 了，所以输出 `3、3、3`



第二道题目：`let` 在 `for` 中会形成块级作用域，每次迭代的时候 `i` 都是一个新值，并且每个值都存在于循环内的块级作用域，所以输出 `0、1、2`



#### 15.12 输出打印结果


```javascript
let date = new Date();

for (var i = 0; i < 5; i++) {
  setTimeout(function() {
    console.log(new Date - date, i); // 1
  }, 1000);
}

console.log(new Date - date, i); // 2
```



请问输出啥？

---

答案：



```javascript
0 5
1001 5
1004 5
1005 5
1006 5
1007 5
```



解析：题目先走宏任务 `script`，所以定义了 `date` 之后，执行注释为 2 这行的 `console`。



然后 5 个宏任务，都是定时器 `setTimeout`，所以会在之后执行，输出：`1000 5`，但是定时器也不一定准时的，所以有可能是 `1001`、`1002` 或者其他的。



#### 15.13 使 a == 1 && a == 2 成立


尝试编码，使：`if(a == 1 && a == 2 && a == 3) {}` 这种情况成立。



+ **方法一**



在类型转换的时候，我们知道了对象如何转换成原始数据类型。如果部署了 `[Symbol.toPrimitive]`，那么返回的就是 `Symbol.toPrimitive` 的返回值。



当然，我们也可以把此函数部署在 `valueOf` 或者是 `toString` 接口上，效果相同。



```javascript
//利用闭包延长作用域的特性
let a = {
  [Symbol.toPrimitive]: (function () {
    let i = 1;
    return function () {
      return i++;
    }
  })()
}
```



+ **方法二**



利用 `Object.defineProperty` 在 `window/global` 上定义 `a` 属性，获取 `a` 属性时，会调用 `get`



```javascript
let val = 1;
Object.defineProperty(window, 'a', {
  get: function() {
    return val++;
  }
});
```



+ **方法三**



```javascript
var a = [1, 2, 3];
a.join = a.shift;
```



数组的 `toString` 方法返回一个字符串，该字符串由数组中的每个元素的 `toString()` 返回值经调用 `join()` 方法连接（由逗号隔开）组成。



因此，我们可以重新 `join` 方法。返回第一个元素，并将其删除。



### 16、各数据类型的常用方法


#### 16.1 Number


#### 16.2 String


#### 16.3 Boolean


#### 16.4 Array


#### 16.5 Object


#### 16.6 Function


### 17、对象属性的四种基本描述


+ value；
+ writable；
+ enumerable；
+ configurable；
+ getOwnPropertyDescriptor；



### 18、闭包


+  js高级程序设计内的解释：  
有权访问另一个函数作用域中的变量的函数 
+  闭包的形成机制：  
当前函数执行，形成一个私有的上下文，函数执行完成之后， 若当前私有上下文中的某些内容，被上下文以外的内容占用，那么当前上下文就不能被释放。 
+  闭包的作用： 
    - 保护私有上下文中的变量不受干扰；
    - 保存私有上下文中的变量；
    - 实现柯里化；
+  闭包的缺点： 
    - 内存消耗，闭包产生的变量无法销毁；
    - 性能问题，由于闭包内部变量优先级高于外部变量，所以需要多查找作用域的一个层次，一定层度影响查找速度；
+  闭包的原理：垃圾回收机制  
1、原理： 找出不再继续使用的变量，然后释放其占用的内存；

2、实现方法：  



### 19、原型与原型链


#### 19.1原型链定义：
JavaScript是面向对象的，每个实例对象都有一个`_proto_`属性，该属性指向他的原型，这个实例的构造函数由一个原型属性`prototype`，与实例的 `_proto_`属性指向同一个对象。当一个对象查找一个属性或方法时，自身没有就会根据_`proto`_向他的原型进行查找，如果都没有就向他的原型的原型继续查找，知道查找到`Object.prototype._proto_`为 `null`，这样也就形成了原型链







#### 19.2实现方法：


##### 1、借助构造函数，经典继承：


+ 思路：在子类构造函数中，调用父类的构造函数，通过 `call`和 `apply`改变父类构造函数中this指向子类实例
+ 缺点：无法复用父组件的方法；



##### 2、原型继承：


+ 思路：将子类的原型设置为父类的实例，子类实例可以使用父类原型的公有方法；
+ 缺点：无法获取父组件的私有属性，且父类创建实例时，会默认调用一个父类的构造函数，浪费性能；



##### 3、组合继承：


+ 思路：将原型链与借助构造函数的技术进行组合，实现子类继承父类的私有属性和公有方法的效果；
+ 缺点：父类创建实例时，会默认调用一个父类的构造函数，浪费性能；



##### 4、寄生继承：


+ 思路：将一个父类的原型赋值给一个空函数的原型，通过将子类的原型设置为空函数的实例，继承父类原型的公有方法；
+ 缺点：无法获取父类的私有方法



##### 5、寄生组合继承：


+ 思路：将寄生继承和借用构造函数方法组合，实现子类继承父类的私有属性和公有方法；
+ 优点：理想方法；



##### 6、ES6继承方法：


+ 思路：使用 `extends`继承父类原型的共有方法，使用 `super`关键字继承父类的私有属性；
+ 缺点：ES6不同浏览器的兼容问题；



#### 19.3prototype、**proto**、constructor的关系


+ 构造函数的 `prototype`指向构造函数的原型对象；
+ 实例的 `_proto_`指向实例的构造函数的原型对象；
+ 实例.`_proto_.constructor`指向实例的构造函数  

| 特点 | 指向 | 作用 | |
| --- | --- | --- | --- |
| **prototype** | **函数**独有 | 函数–>对象 | 含义是**函数的原型对象**，可以给函数的所有实例添加共享的属性和方法 （函数在创建的时候，就会默认创建其prototype对象） |
| _ _**proto**_ _ | **对象**独有 | 对象–>对象 | 当访问对象的属性的时候，如果没有，就会去 _ _**proto**_ _所指向的对象中去找， 找不到的话再往上层 _ _**proto**_ _去找，直到找到**null**为止。 |
| **constructor** | **对象**独有 | 对象–>函数 | 含义是**指向该对象的构造函数**，其中**constructor**可以从 _ _**proto**_ _中继承而来 |




### 20、变量声明


#### 20.1变量声明的几种方法：


+ const（声明常量）
+ let（声明变量）
+ var（声明变量）
+ function（声明函数）



#### 20.2注意点：


+ const声明时，声明和赋值必须同时进行，否则会报错；
+ var可重复声明同一个变量、let无法重复声明同一个变量；
+ var声明的变量会在预解析阶段进行变量提升、let无变量提升；
+ var声明的变量不会识别块级作用域、let声明的变量会识别块级作用域；
+ var声明的全局变量会变成window的属性、let声明的变量不会；



#### 20.3暂时性死区：
只要在块级作用域内存在let/const命令，它所声明的变量就会绑定这个区域，不再受外部的影响。



### 21、数据类型的检测


+  `typeof` ：数据检测缺点；无法检测 `Array`、`Object`、Null几个数据类型，这几个类型均为Object；  
`typeof` 会对 `null` 显示错误是个历史 Bug，`typeof null` 输出的是 `object`，因为 JavaScript 早起版本是 32 位系统，为了性能考虑使用低位存储变量的类型信息，`000` 开头代表是对象然而 `null` 表示为全零，所以它错误判断为 `object`。 
+  `Object.prototype.toString.call()`：万能的数据检测方法； 
+  `instanceof` ：  
缺点：  
1、无法检测`undefiend`,`null`;  
2、当通过直接字面量创建基本类型数据时，无法通过`instanceof`检测数据类型；  
3、当检测数据的类存在原型的继承时，检测也未必准确；(原理同`constructor`) 
+  `constructor`:  
缺点：  
1、无法检测`undefined`、`null`；  
2、当被检测的数据的原型指向另一个实例时，使用`constructor`检测的是这个实例的数据类型；不是被检测				数据的数据类型； 
+  `ES6`新增的数据检测方法:  
1、`Aray.isArray()`判断数据是否为数据类型 



### 22、异步操作与同步操作的执行顺序


#### 22.1原理：
工作栈工作时，先执行同步操作、在执行异步操作中的微任务、最后执行异步操作中的宏任务；







#### 22.2常见的异步模式：


+ 回调函数：缺点：1、回调地狱、2、不能捕获错误、不能return。 
+ 事件监听、
+ 发布/订阅模式、
+  promise：  
优点：解决了回调地狱 ：  
缺点：无法取消promise，错误需要通过回调函数获取； 

##### 
+  Generator(ES6)：

优点：可以控制函数执行 

+  async/await(ES7，async/await是Generator的语法糖)  
优点：处理了回调地狱、也不用像promise写链式 ；  
缺点： 如果多个异步操作没有依赖性而使用await，会导致性能降低，无法并发发送多个请求； 



#### 22.3前端使用的场景：


+ 定时任务
+ ajax请求
+ 事件绑定
+ 回调函数



#### 22.4同步操作与异步操作的区别：
同步会阻塞代码执行，异步不会



#### 22.5注意点：


+ promise是同步操作，链式调用的then是异步操作；
+ async是同步造操作，当await后面的是promise对象时，await后面的为异步操作



### 23、事件对象


#### 23.1事件流


+ 定义： 
    - 事件流会沿着DOM树的节点进行传递
    - JS高级程序设计：
+ `DOM2`级事件流包括下面几个阶段 
    - 事件捕获阶段
    - 处于目标阶段
    - 事件冒泡阶段
+ 如何让事件先冒泡后捕获：



在 `DOM` 标准事件模型中，是先捕获后冒泡。但是如果要实现先冒泡后捕获的效果，对于同一个事件，监听捕获和冒泡，分别对应相应的处理函数，监听到捕获事件，先暂缓执行，直到冒泡事件被捕获后再执行捕获之间。



#### 23.2事件处理机制


当一个元素被点击，首先是事件捕获阶段，`window` 最先接收事件，然后一层一层往下捕获，最后由具体元素接收；之后再由具体元素再一层一层往上冒泡，到 `window` 接收事件。



+   事件冒泡（ **IE** ）：
    - 当一个元素接受到事件时，会将接受到事件传递给自己的父元素
    - 原生JS阻止事件冒泡 ：stopPropagation()
    - vue使用.stop修饰符阻止事件冒泡
+   事件捕获（网景）:事件流从上往下传递
+   事件委托（事件代理）：
    - 原理: 
        * 简单易懂版：利用事件冒泡的事件传递机制，当子元素的事件触发时，传递给父元素处理;
        * 严谨版：利用事件冒泡，只指定一个事件处理对象，就可以管理某一类型的所有事件；
    - 优缺点: 
        * 提高性能;
        * 新添加的元素还会有之前的事件；



#### 23.3事件绑定与解绑


+  事件绑定 
    -  利用事件属性添加事件； 
    -  利用js对象的on属性添加事件（一个事件，只能绑定一个句柄）； 
    -  利用addEvevtlistener绑定事件（一个事件可以绑定多个句柄）；  
备注：`addEventListener` 的第三个参数涉及到冒泡和捕获，为 `true` 时是捕获，为 `false` 时是冒泡。 
+  事件解绑 
    - removeEventListener



#### 23.4事件循环(Event Loop)


JavaScript 从 `script` 开始读取，然后不断循环，从 “任务队列” 中读取执行事件的过程，就是**事件循环（Event Loop）**。



+ 当任务进入执行栈的时候，同步任务和异步任务会进入不同的执行场所，同步进入主线程，异步进入event table并注册函数(宏任务进入宏任务队列，微任务进入微任务队列)；
+ 当指定的事情完成后，event table会将这个函数转移到event queue(事件队列)；
+ 主线程的任务执行完毕后，回去event queue读取对应的函数，进入主线程执行；
+ 上述过程不断重复，就是事件循环；



注：事件循环中异步队列有两种，宏任务队列和微任务队列。



宏任务队列可以有多个，微任务队列只有一个；



其中宏任务包括：



+ script;
+ setTimeout;
+ setTimeInterval;
+ setImmediate;
+ I/O;
+ UI rendering ;



微任务包括：



+ MutationObserver;
+ Promise.then()/catch;
+ 以Promise为基础开发的其他技术，例如fetch、Axios;
+ V8的垃圾回收过程；
+ Node独有的process.nextTick



#### 23.5 onmouseover 和 onmouseenter 区别


![](https://mmbiz.qpic.cn/mmbiz_png/P8CbrweAZpDqlETOsGJnShvC62Epm8eJaFdGaQ64duIaib8z0xqmlD7GcQA6Ueq8p3ZrcbAzibElmOxp918W3e4A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



这两者都是移入的时候触发，但是 `onmouseover` 会触发多次，而 `onmouseenter` 只在进去的时候才触发。



#### 23.6 科普


并不是所有的事件都有冒泡，例如：



+ `onblur`
+ `onfocus`
+ `onmouseenter`
+ `onmouseleave`



### 24、前端模块化


前端模块化方法：require和import



#### 24.1作用：
require和import是不同模块化规范下引入模块的语句



#### 24.2不同点：


+ require是运行时动态加载，import是静态编译；
+ require输出的是一个值的拷贝、import输出的是值的引用



### 25、call、apply和bind的区别


+ call和bind传递的参数无限制，写在绑定的对象后，apply传递的参数需要写成数组形式，放在绑定的对象后；
+ call和apply处理的函数调用，会立即执行；bind处理的函数调用，会延时执行；
+ bind会返回与原函数相同的函数，call和apply会返回函数的返回值；
+ call和apply处理的函数调用，会临时改变函数内this的指向；bind处理的函数调用，会永久变函数内this的指向；



### 26、new


+ 让构造函数返回一个实例；
+ 让构造函数内的this指向实例；
+ 实例默认继承构造函数类的原型



备注：运算符的优级(从上往下)



+ new带参数列表(new后面的表达式带（）)
+ 点运算符
+ new不带参数列表(new后面的表达式不带（）)
+ 函数调用；



### 27、防抖节流


#### 27.1定义：


+ 防抖：原理是维护一个定时器，规定在delay时间后触发函数，但是在delay时间内再次触发的话，就会取消之前的计时器而重新设置； 这样就只有最后一次操作能被触发；
+ 节流：使得一定时间内只触发一次函数，原理是通过判断是否到达一定时间，来触发函数；



#### 27.2区别：


+ 节流是不管时间触发多么频繁，都会保证在规定时间内一定会执行一次真正的事件处理函数；
+ 防抖是在最后一次事件后才触发一次函数；



27.3应用场景：



+ 防抖： 
    - window触发resize时，不断调整浏览器窗口大小会不断触发这个事件，采用防抖让其只触发一次；
    - 页面滚动特定距离，显示[返回顶部按钮]；
+ 节流： 
    - 监听滚动事件，滚动到底部自动加载更多内容，单位事件只触发一次；
    - 刷新按钮，单位时间只触发一次



### 28、面向对象


### 29、BOM


#### 29.1BOM的对象：


+ Window
+ Location
+ History
+ Navigator
+ Screemn
+ document



29.2BOM的方法:



+ Alert()(弹出框)
+ confirm()(确认框)
+ Prompt(用户输入框)
+ Open(打开页面)
+ Close(关闭页面)



### 30、JS常用内置对象


+ Arguments；函数参数集合
+ Date；日期对象
+ Error： 异常对象
+ Math ：数学对象
+ RegExp： 正则表达式对象
+ Array；
+ Boolean
+ Object：基础对象
+ String



### 31、数据拷贝


#### 31.1对象


##### 深拷贝：


+ JSON
+ 递归加for-in循环



##### 浅拷贝：


+ assign
+ 展开扩展符
+ for-in循环



#### 31.2数组


##### 深拷贝：


+ JSON
+ 递归加遍历



##### 浅拷贝：


+ slice
+ concat
+ 遍历
+ 展开运算符



### 32、柯里化


#### 1、定义：
柯里化( Currying) 是把接受多个参数的函数转变为单一参数的函数，并返回接受余下的参数且返回结果的新函数的技术。

简单来说就是：通过闭包管理，支持链式调用，每次运行返回一个function



即：通过将多个参数转化为一个参数，每次运行返回新函数的技术；



#### 2、柯里化的好处：


+ 参数复用；
+ 提前确认；
+ 延迟运行



### 33、Promice


#### 33.1  JS的异步方案的演进：


```plain
CallBack   ->  Promise  ->  generator   ->   async/await。
```



#### 33.2  promise的方法


+ promise.all():提供了并行执行异步操作的能力，并且在所有异步操作执行完成后才执行回调； 
    - 只有所有的请求状态都变成fulfilled,promise的状态才会变成fulfilled，此时所有请求的返回值组成一个数组，传递给promise的回调函数；
    - 只要之中有一个氢气球被rejected，promise的状态就会变成reject，此时第一个被reject的实例的返回值，会传递给promise的回调；
    - 注：使用场景：需要预先加载多种图片、静态文件；
+ promise.race()返回第一个完成请求的返回值给promise的回调；



#### 33.3 promise的做题总结点


1. `Promise.all().then()` 结果中的数组的顺序和 `Promise.all()` 接收到的数组的顺序一致，并不会因为 `setTimeout` 的输出而改变。
2. `Promise.all()` 和 `Promise.then()` 碰到会抛出异常的情况，都只会抛出最先出现问题的那个，被 `.then()` 的第二个参数或者 `.catch()` 捕获，但是不会影响数组中其他的异步任务的执行。
3. `finally` 方法用于指定不管 `Promise` 对象最后状态如何，都会执行的操作，同时，`.finally()` 方法的回调函数是不接受任何参数的，因为它是强制执行，不需要依赖 `Promise` 的执行结果。它本质上就是 `.then()` 方法的特例。
4. 在 `await` 后面的，会等当前宏任务里面所有微任务执行完毕，方且执行；
5. 正常情况下， async 中的 await 命令是一个 Promise 对象，返回该对象的结果，但如果不是 Promise 对象的话，就会直接返回对应的值，相当于 Promise.resolve();；
6. 在 await 后面的 Promise 没有返回值，await 会一直等待；
7. Promise对象多次链式调用时，状态一直不变，但是其值由最后一个链式调用的返回值决定，无返回值则为undefined；



#### 33.4大厂题


1、使用Promise实现每个一秒输出1,2,3



### 34、XML和JSON的区别：


1. 数据体积方面。  
JSON相对于XML来讲，数据的体积小，传递的速度更快些。
2. 数据交互方面。  
JSON与JavaScript的交互更加方便，更容易解析处理，更好的数据交互。
3. 数据描述方面。  
JSON对数据的描述性比XML较差。
4. 传输速度方面。  
JSON的速度要远远快于XML。



### 35、常见兼容性问题：


+  png24位的图片在iE6浏览器上出现背景，解决方案是做成PNG8.也可以引用一段脚本处理. 
+  浏览器默认的margin和padding不同。解决方案是加一个全局的*{margin:0;padding:0;}来统一。 
+  IE6双边距bug:块属性标签float后，又有横行的margin情况下，在ie6显示margin比设置的大。  
浮动ie产生的双倍距离（IE6双边距问题：在IE6下，如果对元素设置了浮动，同时又设置了margin-left或margin-right，margin值会加倍。）  
_#box{ float:left; width:10px; margin:0 0 0 100px;}_ 
+  这种情况之下IE会产生20px的距离，解决方案是在float的标签样式控制中加入 ——_display:inline;将其转化为行内属性。(_这个符号只有ie6会识别) 
+  进识别的方式，从总体中逐渐排除局部。  
首先，巧妙的使用“\9”这一标记，将IE游览器从所有情况中分离出来。  
接着，再次使用“+”将IE8和IE7、IE6分离开来，这样IE8已经独立识别。  
css  
.bb{  
background-color:_#f1ee18;/*所有识别*/_  
.background-color:_#00deff\9; /*IE6、7、8识别*/_  
+background-color:_#a200ff;/*IE6、7识别*/_  
_background-color:*#1e0bd1;/*IE6识别*/*  
} 
+  IE下,可以使用获取常规属性的方法来获取自定义属性,  
也可以使用getAttribute()获取自定义属性;  
Firefox下,只能使用getAttribute()获取自定义属性.  
解决方法:统一通过getAttribute()获取自定义属性. 
+  IE下,event对象有x,y属性,但是没有pageX,pageY属性;  
Firefox下,event对象有pageX,pageY属性,但是没有x,y属性. 
+  Chrome 中文界面下默认会将小于 12px 的文本强制按照 12px 显示,  
可通过加入 CSS 属性 -webkit-text-size-adjust: none; 解决. 
+  超链接访问过后hover样式就不出现了 被点击访问过的超链接样式不在具有hover和active了解决方法是改变CSS属性的排列顺序:  
L-V-H-A : a:link {} a:visited {} a:hover {} a:active {} 
+  怪异模式问题：漏写DTD声明，Firefox仍然会按照标准模式来解析网页，但在IE中会触发怪异模式。为避免怪异模式给我们带来不必要的麻烦，最好养成书写DTD声明的好习惯。现在可以使用[html5](http://www.w3.org/TR/html5/single-page.html)推荐的写法：`<doctype html>` 
+  上下margin重合问题  
ie和ff都存在，相邻的两个div的margin-left和margin-right不会重合，但是margin-top和margin-bottom却会发生重合。  
解决方法，养成良好的代码编写习惯，同时采用margin-top或者同时采用margin-bottom。 
+  ie6对png图片格式支持不好(引用一段脚本处理) 



### 36、时间相关


#### 1、获取精度更高的时间


浏览器使用 `performance.now()` 可以获取到 `performance.timing.navigationStart` 到当前时间之间的微秒数



#### 2、获取首屏事件


1.  H5如果页面首屏有图片：  
首屏时间 = 首屏图片全部加载完毕的时刻 - performance.timing.navigationStart 
2.  如何页面首屏没有图片：  
首屏时间 = performance.timing.domContentLoadedEventStart - performance.timing.navigationStart 



#### 3、介绍原型鸡生蛋、蛋生鸡的问题


Object instanceof Function  
Function instanceof Object



Object instanceof Object  
Function instanceof Function



**结果都是 true**



### 37、ES6及ES6+等能力集，做常用的有哪些，其中最有用的，都解决了什么问题；


#### 1、let 和 const;


新增加了两种声明变量的方法，let、const与var声明变量的差异



#### 2、解构赋值


1. 设置默认值；
2. 字符串、数组、对象、函数参数解构赋值；
3. 交换变量；
4. 提取模块；



#### 3、字符串、数值、正则、数组、函数、对象等方法扩展


1. 字符串：模板字符串；
2. 数值：isFinite、isNaN、parseInt、parseFloat、isInteger、指数运算符(**)等等;
3. 函数：函数参数默认值、rest参数、严格模式、name属性、箭头函数、toString；
4. 数组：扩展运算符、Array.from、Array.of、copyWithin、find、findIndex、fill、entries、keys、values、includes、flat、flatMap、sort；
5. 对象：简洁写法、属性名表达式、name属性、super、扩展运算符、链式运算符(?.)、null运算符(??)、Object.is、Object.assign、Object.getOwnPropertyDescriptors、**proto**、Object.setPrototypeOf、Object.getPrototypeOf、Object.entries、Object.keys、Object.values、Object.fromEntries(Object.entries的逆运算)



#### 4、新增数据类型：Symbol、BigInt


1.  symbol： 
    1. 创造独一无二的变量，防止变量命名冲突；
    2. 对象symbol属性不会被普通遍历方法获取，可以模拟私有属性；
    3. [Symbol.Iterator]给不可迭代对象，提供迭代器;
2.  BigInt:  
实现大数运算； 



#### 5、新增数据结构：Set、Map


1. Set：Set的元素不可重复
2. Map：类似于对象，元素为键值对，但对象的键必须为字符串、Map的键可为任意类型



#### 6、Proxy、Reflect


#### 7、Promise、Generator、async/await


以上均为异步的解决方法



#### 8、Iterator和for-of


遍历器



#### 9、Class和继承


#### 10、ES6Module


### 38、JS内置对象类型
+ `Arguments`函数参数集合
+  `Date`日期对象
+ `Error`异常对象
+ `Math `数学对象
+ `RegExp`正则表达式对象
+ `Array`
+ `Boolean`
+ `Object`基础对象
+ `String`



### 39、渐进式网络应用
  
	渐进式网络应用（`PWA`）是谷歌在 2015 年底提出的概念。基本上算是 `Web` 应用程序，但在外观和感觉上与原生 `App `类似。支持 `PWA `的网站可以提供脱机工作、推送通知和设备硬件访问等功能。

1. 优点：
+ 更小更快: 渐进式的 Web 应用程序比原生应用程序小得多。他们甚至不需要安装。这是他们没有浪费磁盘空间和加载速度非常快。
+ 响应式界面: `PWA` 支持的网页能够自动适应各种屏幕大小。它可以是手机、平板、台式机或笔记本。
+ 无需更新: 大多数移动应用程序需要每周定期更新。与普通网站一样，每当用户交互发生且不需要应用程序或游戏商店批准时，`PWA `总是加载最新更新版本。
+ 高性价比：原生移动应用需要分别为 `Android `和 `iOS `设备开发，开发成本非常高。另一方面，`PWA `有着相同的功能，但只是先前价格的一小部分，开发成本低。
+ `SEO `优势：搜索引擎可以发现 `PWA`，并且加载速度非常快。就像其他网站一样，它们的链接也可以共享。提供良好的用户体验和结果，在 `SEO `排名提高。
+ 脱机功能：由于 `Service Worker API` 的支持，可以在脱机或低`internet`连接中访问`PWAs`。
+ 安全性：`PWA `通过 `HTTPS `连接传递，并在每次交互中保护用户数据。
+ 推送通知：通过推送通知的支持，PWA 轻松地与用户进行交互，提供非常棒的用户体验。
+ 绕过应用商店：原生 `App `如果需要任何新的更新，需要应用商店几天的审批，且有被拒绝或禁止的可能性，对于这方面来说，`PWA` 有它独特的优势，不需要 `App Store` 支持。更新版本可以直接从 `Web `服务器加载，无需 `App Store` 批准。
+ 零安装：在浏览过程中，`PWA` 会在手机和平板电脑上有自己的图标，就像移动应用程序一样，但不需要经过冗长的安装过程。



2. 缺点：
+ 对系统功能的访问权限较低：目前 `PWA `对本机系统功能的访问权限比原生 `App` 有限。而且，所有的浏览器都不支持它的全部功能，但可能在不久的将来，它将成为新的开发标准。
+ 多数 `Android`，少数 `iOS`：目前更多的支持来自 `Android`。`iOS `系统只提供了部分。
+ 没有审查标准：`PWA `不需要任何适用于应用商店中本机应用的审查，这可能会加快进程，但缺乏从应用程序商店中获取推广效益。



### 40、箭头函数与普通函数的区别
+ 更简洁的语法 
+ 没有`this`
+ 不能使用`new `构造函数
+ 不绑定`arguments`，可用`rest`参数...解决
+ 使用`call()`和`apply()`调用
+ 捕获其所在上下文的 `this `值，作为自己的 this 值
+ 箭头函数没有原型属性(即`__proto__`属性)
+ 不能简单返回对象字面量
+ 箭头函数不能当做`Generator`函数,不能使用yield关键字
+ 箭头函数不能换行



### 41、变量声明
1. `let`、`var`、`const`、`function`的区别对比
+ `const`声明时，声明和赋值必须同时进行，否则会报错；
+ `var`可重复声明同一个变量、`let`无法重复声明同一个变量；
+ `var`声明的变量会在预解析阶段进行变量提升、`let`无变量提升；
+ `var`声明的变量不会识别块级作用域、`let`声明的变量会识别块级作用域；
+ `var`声明的全局变量会变成window的属性、`let`声明的变量不会；



2. `ES3`实现`let`和`const`



3. 暂时性死区

只要在块级作用域内存在`let`/`const`命令，它所声明的变量就会绑定这个区域，不再受外部的影响。在声明变量时，提前使用变量会报错。

