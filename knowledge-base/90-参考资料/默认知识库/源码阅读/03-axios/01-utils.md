#### 概览


`axios`源码中`util`部分代码,相对还是比较简单的



```javascript
axios/lib/utils.js

module.exports = {
  isArray: isArray,
  isArrayBuffer: isArrayBuffer,
  isBuffer: isBuffer,
  isFormData: isFormData,
  isArrayBufferView: isArrayBufferView,
  isString: isString,
  isNumber: isNumber,
  isObject: isObject,
  isPlainObject: isPlainObject,
  isUndefined: isUndefined,
  isDate: isDate,
  isFile: isFile,
  isBlob: isBlob,
  isFunction: isFunction,
  isStream: isStream,
  isURLSearchParams: isURLSearchParams,
  isStandardBrowserEnv: isStandardBrowserEnv,
  forEach: forEach,
  merge: merge,
  extend: extend,
  trim: trim,
  stripBOM: stripBOM
};
```



按照上面的方法,主要可以分为三类方法:判断数据类型、操作数据、环境判断.



#### 一、判断数据类型方法


```javascript
axios/lib/utils.js

// 获取 Object 原型上的 toString 方法;
var toString = Object.prototype.toString;

// 是否为数组
function isArray(val) {
  return Array.isArray(val);
}

// 是否为 undefined
function isUndefined(val) {
  return typeof val === 'undefined';
}

// 是否为 buffer 类型
function isBuffer(val) {
  return val !== null && !isUndefined(val) && val.constructor !== null && !isUndefined(val.constructor)
    && typeof val.constructor.isBuffer === 'function' && val.constructor.isBuffer(val);
}

// 是否为 ArrayBuffer 类型
function isArrayBuffer(val) {
  return toString.call(val) === '[object ArrayBuffer]';
}

// 是否为 FormData 类型
function isFormData(val) {
  return toString.call(val) === '[object FormData]';
}

// 是否为 ArrayBuffer 的视图实例
function isArrayBufferView(val) {
  var result;
  if ((typeof ArrayBuffer !== 'undefined') && (ArrayBuffer.isView)) {
    result = ArrayBuffer.isView(val);
  } else {
    result = (val) && (val.buffer) && (isArrayBuffer(val.buffer));
  }
  return result;
}

// 判断是否为字符串
function isString(val) {
  return typeof val === 'string';
}

// 判断是否为对象
function isObject(val) {
  return val !== null && typeof val === 'object';
}

// 判断是否为纯对象
function isPlainObject(val) {
  if (toString.call(val) !== '[object Object]') {
    return false;
  }

  var prototype = Object.getPrototypeOf(val); // Obeject.getPrototypeOf():获取对象的原型
  return prototype === null || prototype === Object.prototype;
}

// 判断是否为日期对象
function isDate(val) {
  return toString.call(val) === '[object Date]';
}

// 判断是否为文件对象
function isFile(val) {
  return toString.call(val) === '[object File]';
}

// 判断是否为 blob 类型
function isBlob(val) {
  return toString.call(val) === '[object Blob]';
}

// 判断是否为函数
function isFunction(val) {
  return toString.call(val) === '[object Function]';
}

// 判断是否为 Stream 类型
function isStream(val) {
  return isObject(val) && isFunction(val.pipe);
}

// 判断是否为 URLSearchParams 类型
function isURLSearchParams(val) {
  return toString.call(val) === '[object URLSearchParams]';
}
```



上述数据类型判断方法主要依赖以下三个方法:



+ `Object.prototype.toString.call()`:	返回`[object type]`, 其中`type`是对象的类型,该方法可以准确判断数据类型,人称万能方法;
+ `typeof`:	可以准确检测基础数据类型(`undefined`, `number`,`string`,`boolean`,`symbol`),但是遇到`null`和`Array`、`Object`等引用类型(`Function`除外),均输出`object`,无法准确判断;
+ `Array.isArray`: 	该方法为ES6新增方法,用于判断是否为数组类型;



判断数据类型,除了上面几个,还有:



+  `constructor`:	原型对象上的属性，指向构造函数;  
1、`undefined`和`null`没有`constructor`属性,无法检测`undefined`、`null`；  
2、当被检测的数据的原型指向另一个实例时，使用`constructor`检测的是这个实例的数据类型；不是被检测数据的数据类型； 
+  `instanceof`:    判断一个对象是否在其原型链原型构造函数的属性;  
1、无法检测`undefiend`,`null`;  
2、当通过直接字面量创建基本类型数据时，无法通过`instanceof`检测数据类型；  
3、当检测数据的类存在原型的继承时，检测也未必准确；(原理同`constructor`); 



总结:



		建议开发中使用`Object.prototype.toString.call()`、`Array.isArray`及`typeof`(需要区分情况)等方法,不建议使用`constructor`及instanceof.



上述提到的`buffer`简单介绍:



+  作用:  
Buffer对象是Node处理二进制数据的一个接口。它是Node原生提供的全局对象，可以直接使用，不需要`require('buffer')`。JavaScript比较擅长处理字符串，对于处理二进制数据（比如TCP数据流），就不太擅长。`Buffer`对象就是为了解决这个问题而设计的。它是一个构造函数，生成的实例代表了V8引擎分配的一段内存，是一个类似数组的对象，成员都为0到255的整数值，即一个8位的字节。 
+  使用场景: 
    1. 可用于处理大量二进制数据
    2. 处理图片、文件接收上传、网络协议等等
+  优势  
在网络传输中，性能提升  
大部分网络传输的时候会使用通过使用字符串，这难免需要转换成Buffer，以二进制方式进行数据传输。如果我们直接预先转换为Buffer 再进行传输，那么在传输过程中无需做额外的转换，也避免了损耗，使性能得到提升。 



#### 二、数据操作方法


```javascript
axios/libs/helpers/bind.js

function bind(fn, thisArg) {
  return function wrap() {
    var args = new Array(arguments.length);
    for (var i = 0; i < args.length; i++) {
      args[i] = arguments[i];
    }
    return fn.apply(thisArg, args);
  };
}

axios/lib/utils.js

// trim方法不存在,就使用正则,删除字符串两端空格
function trim(str) {
  return str.trim ? str.trim() : str.replace(/^\s+|\s+$/g, '');
}

// 遍历数组及对象
function forEach(obj, fn) {
  // 若无值,则不处理
  if (obj === null || typeof obj === 'undefined') {
    return;
  }

  // 数据不是对象类型,则加工为数组;
  if (typeof obj !== 'object') {
    obj = [obj];
  }
	
  if (isArray(obj)) {
    // 使用for循环遍历数组下标
    for (var i = 0, l = obj.length; i < l; i++) {
      fn.call(null, obj[i], i, obj);
    }
  } else {
    // 使用for in 循环,遍历对象私有属性key
    for (var key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        fn.call(null, obj[key], key, obj);
      }
    }
  }
}

// 合并多个对象,存在相同键时,后面的对象优先,并返回一个合并后的对象
function merge(/* obj1, obj2, obj3, ... */) {
  // 返回的对象
  var result = {};
  function assignValue(val, key) {
    if (isPlainObject(result[key]) && isPlainObject(val)) {
      result[key] = merge(result[key], val);
    } else if (isPlainObject(val)) {
      result[key] = merge({}, val);
    } else if (isArray(val)) {
      result[key] = val.slice();
    } else {
      result[key] = val;
    }
  }
	
  // 遍历入参,合并对象
  for (var i = 0, l = arguments.length; i < l; i++) {
    forEach(arguments[i], assignValue);
  }
  return result;
}

// 将b对象的属性添加到a对象对象上,并可指定b对象上的方法绑定的对象
function extend(a, b, thisArg) {
  forEach(b, function assignValue(val, key) {
    if (thisArg && typeof val === 'function') {
      a[key] = bind(val, thisArg);
    } else {
      a[key] = val;
    }
  });
  return a;
}

// 删除UTF-8编码中BOM
function stripBOM(content) {
  if (content.charCodeAt(0) === 0xFEFF) {
    content = content.slice(1);
  }
  return content;
}
```



所谓 `BOM`，全称是`Byte Order Mark`，它是一个`Unicode`字符，通常出现在文本的开头，用来标识字节序。`UTF-8`主要的优点是可以兼容`ASCII`，但如果使用`BOM`的话，这个好处就荡然无存了。



#### 三、环境相关


```javascript
// 判断是否为标准浏览器环境
function isStandardBrowserEnv() {
  if (typeof navigator !== 'undefined' && (navigator.product === 'ReactNative' ||
                                           navigator.product === 'NativeScript' ||
                                           navigator.product === 'NS')) {
    return false;
  }
  return (
    typeof window !== 'undefined' &&
    typeof document !== 'undefined'
  );
}
```



#### 四、总结


	这部分axios源码相对不难,都是些常用且实用的工具方法,经过这次学习,后续也可以应用到自己开发的项目当中去!



#### 参考资料


[聊聊JS的二进制家族：Blob、ArrayBuffer和Buffer](https://zhuanlan.zhihu.com/p/97768916)

