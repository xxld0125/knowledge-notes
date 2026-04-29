### 1、let 和 const;
新增加了两种声明变量的方法，let、const与var声明变量的差异



### 2、解构赋值
1. 设置默认值；
2. 字符串、数组、对象、函数参数解构赋值；
3. 交换变量；
4. 提取模块；





### 3、字符串、数值、正则、数组、函数、对象等方法扩展
1. 字符串：模板字符串；
2. 数值：`isFinite`、`isNaN`、`parseInt`、`parseFloat`、`isInteger`、指数运算符(**)等等;
3. 函数：函数参数默认值、`rest`参数、严格模式、name属性、箭头函数、`toString`；
4. 数组：扩展运算符、`Array.from`、`Array.of`、`copyWithin`、`find`、`findIndex`、`fill`、`entries`、`keys`、`values`、`includes`、`flat`、`flatMap`、`sort`；
5. 对象：简洁写法、属性名表达式、`name`属性、`super`、扩展运算符、链式运算符(?.)、null运算符(??)、`Object.is`、`Object.assign`、`Object.getOwnPropertyDescriptors`、`proto`、`Object.setPrototypeOf`、`Object.getPrototypeOf`、`Object.entries`、`Object.keys`、`Object.values`、`Object.fromEntries`(`Object.entries`的逆运算)





### 4、新增数据类型：Symbol、BigInt
1.  `symbol`： 
    1. 创造独一无二的变量，防止变量命名冲突；
    2. 对象`symbol`属性不会被普通遍历方法获取，可以模拟私有属性；
    3. `[Symbol.Iterator]`给不可迭代对象，提供迭代器;
2.  `BigInt`:  
实现大数运算； 



### 5、新增数据结构：Set、Map
1. `Set`：`Set`的元素不可重复
2. `Map`：类似于对象，元素为键值对，但对象的键必须为字符串、`Map`的键可为任意类型



### 6、Proxy、Reflect


### 7、Promise、Generator、async/await
以上均为异步的解决方法





### 8、Iterator和for-of
遍历器





### 9、Class和继承


### 10、ES6Module
