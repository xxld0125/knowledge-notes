# Function.prototype.call

```javascript
Function.prototype._call = function (context = globalThis){
    context.fn = this;
    let args = Array.from(arguments).slice(1);
    const res = context.fn(...args);
    delete context.fn;
    return res;
}
```
