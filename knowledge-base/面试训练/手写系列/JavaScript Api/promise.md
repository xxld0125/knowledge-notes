### 一、Promise.all
```javascript
const a = new Promise(resolve => {
    setTimeout(() =>{
        resolve(1)
    }, 1000)
})
const b = new Promise(resolve => {
    setTimeout(() => {
        resolve(2)
    }, 500)
})

Promise._all = function (arr) {
    return new Promise(resolve => {
        const result = [];
        let index = 0;  
        for (let i = 0;i < arr.length;i++) {
            arr[i].then(res => {
                result[i] = res;
                index++;
                if (index === arr.length) {
                    resolve(result);
                }
            }).catch(err => {
                throw new Error(err)
            })
        }
    })
}
Promise._all([a, b]).then(res => {
    console.log(res)
})
```

### 二、Promise.race
```javascript
const a = new Promise(resolve => {
    setTimeout(() =>{
        resolve(1)
    }, 1000)
})
const b = new Promise(resolve => {
    setTimeout(() => {
        resolve(2)
    }, 500)
})

Promise._race = function (arr) {
    return new Promise(resolve => {
        for (let i = 0;i < arr.length;i++) {
            arr[i].then(res => {
                resolve(res)
            }).catch(err => {
                throw new Error(err)
            })
        }
    })
}
Promise._race([a, b]).then(res => {
    console.log(res)
})
Promise.race([a, b]).then(res => {
    console.log(res)
})
```

### 三、Promise.finally
```javascript
Promise.prototype._finally = function (cb) {
    const P = this.constructor;
    return P.then(
        value => P.resolve(cb).then(() => value),
        reason => P.resolve(cb).then(() => { throw new Error(reason)})
    )
}
```

### 四、Promise.allSettled
```javascript

```

### 五、Promise-polyfill
```javascript

```

