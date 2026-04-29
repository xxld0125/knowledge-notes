# instanceof

```javascript
function instanceOf (a,b) {
    // 通过 typeof 判断基本类型
    if (typeof a !== 'object' || b === null){
        return false
    }

    // getPrototypeOf 是Object自带的一个方法，可以拿到参数的原型对象
    let proto = Object.getPrototypeOf(a);
    const prototype = b.prototype;

    // 从当前 __proto__ 开始查找
    while (proto) {
        if(proto === null){
            return false
        }

        // 如果a.__proto__.xx ===b.prototype,返回true
        if(proto === prototype){
            return true
        }

        proto = protp.__proto__
    }

}
```
