# Function.prototype.bind

```javascript
Function.prototype._bind = function (context,...args1) {
    const fn = this;
    const res = function (...args2) {
        const allArgs = args1.concat(args2);
        let res = null
        if (this instanceof res) {
            res = fn.apply(this,allArgs);
        } else {
            res = fn.apply(context, allArgs);
        }
    }
    res.prototype = Object.create(fn.prototype);
    return res;
}
```
