### 一、this定义：
`this`绑定的对象即函数执行的上下文环境（`context`）。



### 二、this指向的优先级
1. `new`运算符；
2. `bind`、`call`、`apply`(`bind`处理后的方法，再使用`call`或`apply`，`this`还是指向`bind`对应的对象)；
3. 对象调用；
4. 默认绑定：



### 三、call、apply、bind；


1. `call`和`bind`传递的参数无限制，写在绑定的对象后，`apply`传递的参数需要写成数组形式，放在绑定的对象后
2. `call`和`apply`处理的函数调用，会立即执行；`bind`处理的函数调用，会延时执行
3. `bind`会返回与原函数相同的函数，`call`和`apply`会返回函数的返回值
4. `call`和`apply`处理的函数调用，会临时改变函数内`this`的指向；`bind`处理的函数调用，会永久改变函数内this的指向；



### 四、箭头函数：
箭头函数内的`this`指向父作用域的`this`；



