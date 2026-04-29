# Object.create

```javascript
/* 
    Object.create()作用:创建一个新对象，使用现有的对象来提供新创建的对象的__proto__
    参数：
        proto：新对象的__proto__;
        propertiesObject:会成为创建对象的属性；
    返回值：
        一个对象，带着指定的原型对象和属性；
*/
 Object._create = function (proto) {
     function F () {};
     F.prototype = proto;
     return new F();
 }
```
