### 一、Promise并发限制实现
```javascript

```

### 二、Promise实现每秒输出123
```javascript
// 方法一：
for (let i = 1;i <= 3;i++) {
    setTimeout(() => {
        console.log(i)
    }, i * 1000)
}

// 方法二、
const arr = [1, 2, 3];
arr.reduce((prev, next) => {
    return prev.then(res => {
        return new Promise(resolve => {
            setTimeout(() => {
                console.log(next)
                resolve();
            }, 1000)
        }) 
    })
}, Promise.resolve())
```



### 三、promise.resolve()的作用；


### 四、promise.then()如何实现链式调用；


### 五、promise.then()不返回promise还能继续then吗；


### 六、promise.finally()的作用；


### promise做题总结
1. `Promise.all().then()` 结果中的数组的顺序和 `Promise.all()` 接收到的数组的顺序一致，并不会因为 `setTimeout` 的输出而改变。
2. `Promise.all()` 和 `Promise.then()` 碰到会抛出异常的情况，都只会抛出最先出现问题的那个，被 `.then()` 的第二个参数或者 `.catch()` 捕获，但是不会影响数组中其他的异步任务的执行。
3. `finally` 方法用于指定不管 `Promise` 对象最后状态如何，都会执行的操作，同时，`.finally()` 方法的回调函数是不接受任何参数的，因为它是强制执行，不需要依赖 `Promise` 的执行结果。它本质上就是 `.then()` 方法的特例。
4. 在 `await` 后面的，会等当前宏任务里面所有微任务执行完毕，方且执行；
5. 正常情况下， `async` 中的 `await `命令是一个 `Promise `对象，返回该对象的结果，但如果不是 `Promise `对象的话，就会直接返回对应的值，相当于 `Promise.resolve()`;
6. 在 `await `后面的 `Promise `没有返回值，`await `会一直等待；
7. `Promise`对象多次链式调用时，状态一直不变，但是其值由最后一个链式调用的返回值决定，无返回值则为`undefined`；







