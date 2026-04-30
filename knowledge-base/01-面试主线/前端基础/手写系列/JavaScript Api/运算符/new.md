```javascript
// new 的作用是： 
// 1、第一个参数必须是函数；
// 2、创建一个新对象；
// 3、构造函数内的this指向这个对象；
// 4、对象继承构造函数的原型；
// 5、如果函数返回的是引用类型，则返回运行后的结果，否则返回新创建的对象；
function myNew (func,...args) {
   // 判断第一个参数是否为函数；
   if (typeof func !== 'function') {
       throw '第一个参数必须为函数体';
   }
   // 新建一个对象；
   const obj = {};
   // 对象继承函数的原型；
   obj.__proto__ = Object.create(func.prototype);
   // 函数执行的结果赋值给result
   const result = func.apply(obj,args);

   const isObject = typeof result === 'Object' && obj !== null;
   const isFunction = typeof result === 'function';
   return isObject || isFunction ? result : obj
}
```

