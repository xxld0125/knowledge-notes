# Array.prototype.map

```javascript
/* 
  map的参数：
      callback
          生成新数组元素的函数，使用三个参数：
          currentValue
              callback 数组中正在处理的当前元素。
          index可选
              callback 数组中正在处理的当前元素的索引。
          array可选
              map 方法调用的数组。
      thisArg可选
          执行 callback 函数时值被用作this。
*/

//  1、简易版：
Array.prototype._map = function(fn, context) {
    let resArr = [];
    const me = this;
    const ctx = context ? context : me // 定义上下文
    if (typeof fn !== 'function') {
        throw new Error(`${fn} is not a function`)
    }
    me.forEach((item, index) => {
        resArr.push(fn.call(ctx, item, index, me)) // 将回调结果放入数组中
    })
    return resArr // 返回map后的数组
}
```
