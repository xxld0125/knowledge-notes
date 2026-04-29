### 一、作用
<font style="color:rgb(37, 37, 37);">将值转换为数组。</font>

### 二、源码
对数据类型按照以下规则进行处理：

    - null, undefined
    - array
    - string
    - 可迭代对象
    - 其他

```javascript
export default function arrify(value) {
  // value为null 或 undefined, 返回[]
	if (value === null || value === undefined) {
		return [];
	}

  // value为数组类型, 返回value
	if (Array.isArray(value)) {
		return value;
	}
  
  // value为字符串类型, 返回[value]
	if (typeof value === 'string') {
		return [value];
	}
  
  // value为可迭代对象, 返回[...value]
	if (typeof value[Symbol.iterator] === 'function') {
		return [...value];
	}

	return [value];
}
```



**什么是可迭代对象？**

<font style="color:rgb(13, 20, 30);">简单来说就是部署了</font>`<font style="color:rgb(13, 20, 30);">Iterator</font>`<font style="color:rgb(13, 20, 30);">接口的数据结构，都可称为可迭代对象。</font>

<font style="color:rgb(13, 20, 30);">ES6 规定，默认的 </font>`<font style="color:rgb(13, 20, 30);">Iterator</font>`<font style="color:rgb(13, 20, 30);"> 接口部署在数据结构的</font>`<font style="color:rgb(13, 20, 30);">Symbol.iterator</font>`<font style="color:rgb(13, 20, 30);">属性，或者说，一个数据结构只要具有</font>`<font style="color:rgb(13, 20, 30);">Symbol.iterator</font>`<font style="color:rgb(13, 20, 30);">属性，就可以认为是“可遍历的”（</font>`<font style="color:rgb(13, 20, 30);">iterable</font>`<font style="color:rgb(13, 20, 30);">）。</font>

`<font style="color:rgb(13, 20, 30);">Symbol.itaretor</font>`<font style="color:rgb(13, 20, 30);">属性本身就是一个函数，就是当前数据结构默认的遍历器生成函数。		</font>`<font style="color:rgb(13, 20, 30);">arrify</font>`<font style="color:rgb(13, 20, 30);">源码中通过判断传入值</font>`<font style="color:rgb(13, 20, 30);">value[Symbol.iterator]</font>`<font style="color:rgb(13, 20, 30);">数据类型是否为函数来判断当前值是否为可迭代对象。</font>

<font style="color:rgb(13, 20, 30);"></font>

**<font style="color:rgb(13, 20, 30);">原生具备</font>**`**<font style="color:rgb(13, 20, 30);">Iterator</font>**`**<font style="color:rgb(13, 20, 30);">接口的数据结构</font>**

+ <font style="color:rgb(13, 20, 30);">Array</font>
+ <font style="color:rgb(13, 20, 30);">Map</font>
+ <font style="color:rgb(13, 20, 30);">Set</font>
+ <font style="color:rgb(13, 20, 30);">String</font>
+ <font style="color:rgb(13, 20, 30);">TypedArray</font>
+ <font style="color:rgb(13, 20, 30);">函数的arguments对象</font>
+ <font style="color:rgb(13, 20, 30);">Nodelist对象</font>



**可迭代对象适用扩展运算符**

<font style="color:rgb(13, 20, 30);">扩展运算符（...）会调用默认的 </font>`<font style="color:rgb(13, 20, 30);">Iterator</font>`<font style="color:rgb(13, 20, 30);"> 接口。</font>

```typescript
var str = 'arrify';
[...str] //['a', 'r', 'r', 'i', 'f', 'y']

var map = new Map;
map.set('map', '扩展运算符');
[...map]; // [['map', '扩展运算符']]

var set = new Set;
set.add('扩展运算符');
[...set]; // ['扩展运算符']

```

通过上面的代码展示，知道为什么`arrify`源码中不把`string`类型归类到可迭代对象中去处理，而是单独处理了。

### 三、测试用例
按照代码中的数据类型处理分类，对应场景的测试用例。

```javascript
import test from 'ava';
import arrify from './index.js';

test('main', t => {
	t.deepEqual(arrify('foo'), ['foo']);
	t.deepEqual(arrify(new Map([[1, 2], ['a', 'b']])), [[1, 2], ['a', 'b']]);
	t.deepEqual(arrify(new Set([1, 2])), [1, 2]);
	t.deepEqual(arrify(null), []);
	t.deepEqual(arrify(undefined), []);

	const fooArray = ['foo'];
	t.is(arrify(fooArray), fooArray);
});

```



### 四、总结
虽然本篇`arrify`源码比较简单，学习后还是有收获。对于各数据类型转为数组类型的处理。其他也了解了可迭代对象和`arrify`的测试用例。

### 参考
[https://github.com/sindresorhus/arrify](https://github.com/sindresorhus/arrify)

[https://es6.ruanyifeng.com/#docs/iterator](https://es6.ruanyifeng.com/#docs/iterator)

[https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/iterator](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/iterator)

[https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Iterators_and_Generators](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Iterators_and_Generators)

