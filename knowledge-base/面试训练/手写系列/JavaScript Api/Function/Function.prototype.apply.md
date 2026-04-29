# Function.prototype.apply

```javascript
 Function.prototype._apply = function (context = globalThis, arr) {
    context.fn = this;
    let res = null;
    if (arr) {
        res = context.fn(...arr);
    } else {
        res = context.fn();
    }
    delete context.fn;
    return res;
}
```
