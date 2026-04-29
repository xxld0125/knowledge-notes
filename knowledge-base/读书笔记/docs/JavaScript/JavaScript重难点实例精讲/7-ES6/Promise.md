Promise是在ES6中新增的一种用于解决异步编程的方案



# 诞生的原因
Promise诞生以前，在处理一个异步请求时，我们通常是在回调函数中做处理

```javascript
$.ajax({
    url: 'testUrl',
    success: function () {
        // 回调函数
    }
});
```



假如在一个行为中，需要执行多个异步请求，每一个请求又需要依赖上一个请求的结果，按照回调函数的处理方法，代码如下所示

```javascript
// 第一个请求
$.ajax({
    url: 'url1',
    success: function () {
        // 第二个请求
        $.ajax({
            url: 'url2',
            success: function () {
                // 第三个请求
                $.ajax({
                    url: 'url3',
                    success: function () {
                        // 第四个请求
                        $.ajax({
                            url: 'url4',
                            success: function () {
                                // 成功地回调
                            }
                        })
                    }
                })
            }
        })
    }
})
```



事实上，一个行为所产生的异步请求可能比这个还要多，这就会导致代码的嵌套太深，引发“回调地狱”。





“回调地狱”存在以下几个问题。

+ 代码臃肿，可读性差
+  代码耦合度高，可维护性差，难以复用
+ 回调函数都是匿名函数，不方便调试



# 生命周期
每一个Promise对象都有3种状态，即pending（进行中）、fulfilled（已成功）和rejected（已失败）。



Promise在创建时处于pending状态，状态的改变只有两种可能，一种是在Promise执行成功时，由pending状态改变为fulfilled状态；另一种是在Promise执行失败时，由pending状态改变为rejected状态。



状态一旦改变，就不能再改变，状态改变一次后得到的就是Promise的终态



# 基本用法
Promise对象本身是一个构造函数，可以通过new操作符生成Promise的实例

```javascript
const promise = new Promise((resolve, reject) => {
    // 异步请求处理
    if(/ 异步请求标识 /) {
        resolve();
    } else {
        reject();
    }
});
```



Promise执行的过程是：在接收的函数中处理异步请求，然后判断异步请求的结果，如果结果为“true”，则表示异步请求执行成功，调用resolve()函数，resolve()函数一旦执行，Promise的状态就从pending变为fulfilled；如果结果为“false”，则表示异步请求执行失败，调用reject()函数，reject()函数一旦执行，Promise的状态就从pending变为rejected。



resolve()函数和reject()函数可以传递参数，作为后续.then()函数或者.catch()函数执行时的数据源。



需要注意的是Promise在创建后会立即调用，然后等待执行resolve()函数或者reject()函数来确定Promise的最终状态。

```javascript
let promise = new Promise(function(resolve, reject) {
    console.log('Promise');
    resolve();
});
promise.then(function() {
    console.log('resolved');
});
console.log('Hello');
```



## then()
Promise在原型属性上添加了一个then()函数，表示在Promise实例状态改变时执行的回调。

它接收两个函数作为参数，第一个参数表示的是Promise在执行成功后（即调用了resolve()函数），所需要执行的回调函数，函数参数就是通过resolve()函数传递的参数。第二个参数是可选的，表示的是Promise在执行失败后（即调用了reject()函数或抛出了异常），执行的回调函数。



在Promise的then()函数或者catch()函数中，接收的是一个函数，函数的参数是resolve()函数或者reject()函数的返回值。而如果传入的值是非函数，那么就会产生值穿透现象。



## catch()
catch()函数与then()函数是成对存在的，then()函数是Promise执行成功之后的回调，而catch()函数是Promise执行失败之后的回调，它所接收的参数就是执行reject()函数时传递的参数。

因为promise实例在创建后会立即执行，所以进入try语句后会抛出一个异常，从而被catch()函数捕获到，在catch()函数中调用reject()函数，并传递Error信息。一旦reject()函数被执行，就会触发promise实例的catch()函数，从而能在catch()函数的回调函数中输出err的信息。

<font style="color:#DF2A3F;"></font>

<font style="color:#DF2A3F;">需要注意的是，如果一个Promise的状态已经变成fulfilled成功状态，再去抛出异常，是无法触发catch()函数的。这是因为Promise的状态一旦改变，就会永久保持该状态，不会再次改变。</font>

<font style="color:#DF2A3F;"></font>

## Promise.all()
用于将多个Promise实例包装成一个新的Promise实例

```javascript
const p = Promise.all([p1, p2, p3]);
```

返回的新Promise实例p的状态由3个Promise实例p1、p2、p3共同决定，总共会出现以下两种情况

+ 只有p1、p2、p3全部的状态都变为fulfilled成功状态，p的状态才会变为fulfilled状态，此时p1、p2、p3的返回值组成一个数组，作为p的then()函数的回调函数的参数
+  只要p1、p2、p3中有任意一个状态变为rejected失败状态，p的状态就变为rejected状态，此时第一个被reject的实例的返回值会作为p的catch()函数的回调函数的参数



需要注意的是，作为参数的Promise实例p1、p2、p3，如果已经定义了catch()函数，那么当其中一个Promise状态变为rejected时，并不会触发Promise.all()函数的catch()函数



## Promise.race()
Promise.race()函数作用于多个Promise实例上，返回一个新的Promise实例，表示的是如果多个Promise实例中有任何一个实例的状态发生改变，那么这个新实例的状态就随之改变，而最先改变的那个Promise实例的返回值将作为新实例的回调函数的参数



## Promise.resolve()
它等价于在Promise函数体内调用resolve()函数

Promise.resolve()函数执行后，Promise的状态会立即变为fulfilled，然后进入then()函数中做处理

在Promise.resolve(param)函数中传递的参数param，会作为后续then()函数的回调函数接收的参数



## Promise.reject()
用于返回一个状态为rejected的Promise实例，函数在执行后Promise的状态会立即变为rejected，从而会立即进入catch()函数中做处理，等价于在Promise函数体内调用reject()函数

在Promise.reject(param)函数中传递的参数param，会作为后续catch()函数的回调函数接收的参数



# 用法实例


