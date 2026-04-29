#### 一、概念
`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 全称为 </font>`<font style="color:rgb(0, 0, 0);">JavaScript Object Notation</font>`<font style="color:rgb(0, 0, 0);">，是一种轻量级的数据交换格式。它是 </font>`<font style="color:rgb(0, 0, 0);">JavaScript</font>`<font style="color:rgb(0, 0, 0);"> 中用于描述对象数据的语法的扩展。不过并不限于与 </font>`<font style="color:rgb(0, 0, 0);">JavaScript</font>`<font style="color:rgb(0, 0, 0);"> 一起使用。它采用完全独立于语言的文本格式，这些特性使 </font>`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 成为理想的数据交换格式。易于阅读和编写，同时也易于机器解析和生成。所有现代编程语言都支持这些数据结构，使 </font>`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 完全独立于语言。</font>

<font style="color:rgb(0, 0, 0);"></font>

`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 的官方媒体类型是 </font>`application/json`<font style="color:rgb(0, 0, 0);">，JSON 文件名使用扩展名 </font>`.json`<font style="color:rgb(0, 0, 0);">。</font>

<font style="color:rgb(0, 0, 0);"></font>

`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 的流行正是因为网站和移动应用程序需要更快捷、有效地将数据从一个系统传输到另一个系统。</font>`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 可以通过多种方式共享数据、存储设置以及与系统交互。它的简单性和灵活性使其适用于许多不同的情况。</font>

`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 最常见的用法是通过网络连接交换序列化数据。</font>`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 的其他常见用途包括公共、前端或内部 </font>`<font style="color:rgb(0, 0, 0);">API</font>`<font style="color:rgb(0, 0, 0);">、</font>`<font style="color:rgb(0, 0, 0);">NoSQL</font>`<font style="color:rgb(0, 0, 0);"> 数据库、模式描述、配置文件、公共数据或数据导出。</font>

`JSON` 的特点如下：

+ **紧凑、高效的格式**：`JSON` 语法提供了简单的数据解析和更快的实现；
+ 易于**阅读**：人类和计算机都可以快速解释语法且错误最少；
+ **广泛支持**：大多数语言、操作系统和浏览器都可以使用开箱即用的 `JSON`，这允许使用 `JSON` 而不存在兼容性问题；
+ **自我描述**：很容易区分数据类型，并且更容易解释数据，而无需提前知道会发生什么；
+ **格式灵活**：`JSON` 支持多种数据类型，可以组合起来表达大多数数据的结构。



#### 二、JSON结构
`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 数据类型的完整列表：</font>

+ `<font style="color:rgb(1, 1, 1);">string</font>`<font style="color:rgb(1, 1, 1);">：用引号括起来的文字。</font>
+ `<font style="color:rgb(1, 1, 1);">number</font>`<font style="color:rgb(1, 1, 1);">：正整数或负整数或浮点数。</font>
+ `<font style="color:rgb(1, 1, 1);">object</font>`<font style="color:rgb(1, 1, 1);">：用花括号括起来的键值对</font>
+ `<font style="color:rgb(1, 1, 1);">array</font>`<font style="color:rgb(1, 1, 1);">：一个或多个 </font>`<font style="color:rgb(1, 1, 1);">JSON</font>`<font style="color:rgb(1, 1, 1);"> 对象的集合。</font>
+ `<font style="color:rgb(1, 1, 1);">boolean</font>`<font style="color:rgb(1, 1, 1);">：不带引号的 </font>`<font style="color:rgb(1, 1, 1);">true</font>`<font style="color:rgb(1, 1, 1);"> 或 </font>`<font style="color:rgb(1, 1, 1);">false</font>`<font style="color:rgb(1, 1, 1);"> 值。</font>
+ `<font style="color:rgb(1, 1, 1);">null</font>`<font style="color:rgb(1, 1, 1);">：表示键值对没有数据，表示为</font>`<font style="color:rgb(1, 1, 1);">null</font>`<font style="color:rgb(1, 1, 1);">，不带引号。</font>

<font style="color:rgb(0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);">下面是一个包含这些数据类型的 JSON 对象示例：</font>

```json
{
  "name": "zhangsan",
  "age": 28,
  "badperson":true,
  "child": {
    "name": "zhangxiaosan",
    "age": 8
  },
  "job": ["React", "JavaScript"],
  "wages": null,
}
```



#### 三、`JSON`解析与序列化
`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 内置了两种方法：</font>

+ `JSON.parse()` <font style="color:rgb(1, 1, 1);">：将数据转换为 </font>`<font style="color:rgb(1, 1, 1);">JavaScript</font>`<font style="color:rgb(1, 1, 1);"> 对象。</font>
+ `JSON.stringify() `<font style="color:rgb(1, 1, 1);">：将 </font>`<font style="color:rgb(1, 1, 1);">JavaScript</font>`<font style="color:rgb(1, 1, 1);"> 对象转换为字符串。</font>

<font style="color:rgb(1, 1, 1);"></font>

##### <font style="color:rgb(1, 1, 1);">1、</font>JSON.parse()
用法：`JSON.parse(text[, reviver])`

    - `text`：<font style="color:rgb(27, 27, 27);">要被解析成 </font>`<font style="color:rgb(27, 27, 27);">JavaScript</font>`<font style="color:rgb(27, 27, 27);"> 值的字符串</font>
    - `reviver`：<font style="color:rgb(27, 27, 27);">转换器，如果传入该参数 (函数)，可以用来修改解析生成的原始值，调用时机在 </font>`<font style="color:rgb(27, 27, 27);">parse</font>`<font style="color:rgb(27, 27, 27);"> 函数返回之前。</font>



```javascript
JSON.parse(text, reviver);
// text： 必需， 一个有效的 JSON 字符串。
// reviver：可选，一个转换结果的函数， 将为对象的每个成员调用此函数。

const json = '{"name": "zhangsan", "age": 18, "city": "beijing"}';

const myJSON = JSON.parse(json);
 
console.log(myJSON.name, myJSON.age);  // zhangsan 18
```



我们可以启用 `JSON.parse` 的第二个参数 `reviver`，一个转换结果的函数，对象的每个成员都会调用此函数：

```javascript
const json = '{"name": "zhangsan", "age": 18, "city": "beijing"}';

const myJSON = JSON.parse(json, (key, value) => {
  if(typeof value === "number") {
     return String(value).padStart(3, "0");
  }
  return value;
});
 
console.log(myJSON.name, myJSON.age);  // zhangsan 018
```



##### 2、JSON.stringify()
用法：`JSON.stringify(value[, replacer [, space]])`

    - `value`：将要序列化成 一个 `JSON` 字符串的值。
    - `replacer`：
        * 如果该参数是一个函数，则在序列化过程中，被序列化的值的每个属性都会经过该函数的转换和处理
        * 如果该参数是一个数组，则只有包含在这个数组中的属性名才会被序列化到最终的 JSON 字符串中
        * 如果该参数为 null 或者未提供，则对象所有的属性都会被序列化。
    - `space`：指定缩进用的空白字符串，用于美化输出（`pretty-print`）；
        * 如果参数是个数字，它代表有多少的空格；上限为 10。该值若小于 1，则意味着没有空格
        * 如果该参数为字符串（当字符串长度超过 10 个字母，取其前 10 个字母），该字符串将被作为空格
        * 如果该参数没有提供（或者为 null），将没有空格。



```javascript
JSON.stringify(value, replacer, space);
// value： 必需， 要转换的 JavaScript 值（通常为对象或数组）。
// replacer： 可选。用于转换结果的函数或数组。如果 replacer 为函数，则 JSON.stringify 将调用该函数，并传入每个成员的键和值。使用返回值而不是原始值。如果此函数返回 undefined，则排除成员。根对象的键是一个空字符串：""。如果 replacer 是一个数组，则仅转换该数组中具有键值的成员。成员的转换顺序与键在数组中的顺序一样。当 value 参数也为数组时，将忽略 replacer 数组。
// space： 可选，文本添加缩进、空格和换行符，如果 space 是一个数字，则返回值文本在每个级别缩进指定数目的空格，如果 space 大于 10，则文本缩进 10 个空格。space 也可以使用非数字，如：\t。

const json = {"name": "zhangsan", "age": 18, "city": "beijing"};

const myJSON = JSON.stringify(json);
 
console.log(myJSON);  // {"name":"zhangsan","age":18,"city":"beijing"}
```



##### 3、异常处理
那如果 `JSON` 无效怎么办呢？比如缺少了逗号，引号等，上面的两种方法都会抛出异常。建议在使用这两个方法时使用`try...catch`来包裹，也可以将其封装成一个函数。

```javascript
let myJSON = {}
const json = '{"name": "zhangsan", "age": 18, "city": "beijing"}';

try {
  myJSON = JSON.parse(json);
} catch (e){
  console.error(e.message)
}
console.log(myJSON.name, myJSON.age);  // zhangsan 18
```

<font style="color:rgb(0, 0, 0);">如果 </font>`<font style="color:rgb(0, 0, 0);">JSON</font>`<font style="color:rgb(0, 0, 0);"> 操作时出现问题，这样就能确保应用程序不会因此中断。</font>

<font style="color:rgb(0, 0, 0);"></font>

#### 四、使用技巧
##### 1、格式化
上面提到，可以使用`JSON.stringify()`来将 `JSON` 对象转换为字符串。它支持第二、三个参数。我们可以借助第二三个参数来格式化 `JSON` 字符串。正常情况下，格式化后的字符串长这样:

```javascript
const json = {"name": "zhangsan", "age": 18, "city": "beijing"};

const myJSON = JSON.stringify(json);
 
console.log(myJSON);  // {"name":"zhangsan","age":18,"city":"beijing"}
```



<font style="color:rgb(0, 0, 0);">添加第二三个参数：</font>

```javascript
const json = {"name": "zhangsan", "age": 18, "city": "beijing"};

const myJSON = JSON.stringify(json, null, 2);
 
console.log(myJSON);  
```

	

<font style="color:rgb(0, 0, 0);">生成的字符串格式如下：</font>

```json
{
  "name": "zhangsan",
  "age": 18,
  "city": "beijing"
}
```

	

<font style="color:rgb(0, 0, 0);">这里的 2 其实就是为返回值文本在每个级别缩进 2 个空格。</font>

<font style="color:rgb(0, 0, 0);">如果缩进是一个字符串而不是空格，就可以传入需要缩进的填充字符串：</font>

```javascript
const json = {"name": "zhangsan", "age": 18, "city": "beijing"};

const myJSON = JSON.stringify(json, null, "--");

console.log(myJSON);  
```



<font style="color:rgb(0, 0, 0);">输出结果如下：</font>

```json

{
  --"name": "zhangsan",
  --"age": 18,
  --"city": "beijing"
}
```



##### 2、<font style="color:rgb(0, 0, 0);">隐藏属性</font>
我们知道`JSON.stringify()`支持第二个参数，用来处理 `JSON` 中的数据：

```javascript
const user = {
  "name": "John",
  "password": "12345",
  "age": 30
};

console.log(JSON.stringify(user, (key, value) => {
  if (key === "password") {
    return;
  }
  return value;
}));

// 输出结果：{"name":"John","age":30}
```



##### 3、过滤结果
当 `JSON` 中的内容很多时，想要查看指定字段是比较困难的。可以借助`JSON.stringify()`的第二个属性来获取指定值，只需传入指定一个包含要查看的属性 `key` 的数组即可：

```javascript
const user = {
    "name": "John",
    "password": "12345",
    "age": 30
}

console.log(JSON.stringify(user, ['name', 'age']))

// 输出结果：{"name":"John","age":30}
```



#### 五、手写JSON方法
##### 1、JSON.stringify
各种数据类型及边界情况，特别注意循环引用场景，会报错。

| ******JSON.stringify** | **输入** | **输出** |
| :---: | :---: | --- |
| **基础数据类型** | **undefined** | **undefined** |
| | **boolean** | **"true"/"false"** |
| | **string** | **string** |
| | **number** | **字符串类型的数组** |
| | **symbol** | **undefined** |
| | **null** | **"null"** |
| | **NaN和Ininity** | **"null"** |
| | **BigInit** | **<font style="color:rgb(37, 41, 51);">抛出TypeError错误</font>** |
| **引用数据类型** | **function** | **undefined** |
| | **Array中除undefined、function或symbol外的数据** | **string** |
| | **Array中的undefined、function或symbol** | **都转化为"null"** |
| | **RegExp/Error** | **"{}"** |
| | **Date** | **Date的toJson()字符串值，同****<font style="color:rgb(27, 27, 27);">Date.toISOString()方法</font>** |
| | **普通object** | **1、如果有toJson()方法，那么序列化toJson()的返回值** |
| | | **2、如果属性中出现undefined、任意函数或symbol值，则忽略** |
| | | **3、所有以symbol为属性键的属性都会被完全忽略掉** |
| | | **4、忽略不可遍历属性enumerable** |


```javascript
function jsonStringify(data){
  let result = '';
  var type = typeof data;
  if(type !== 'object' || data === null ){
    // 基础类型在此处理
    result = data;
    if(type == 'number' &&(Number.isNaN(data) || !Number.isFinite(data))){
      // 规则8:NaN 和 Infinity格式的数值会被当做 null。
      result = "null";
    }else if(type == 'function' || type == 'undefined' || type == 'symbol'){
      // 规则4:函数、undefined 被单独转换时，会返回 undefined，
      result = "undefined";
    }else if(type == 'string'){
      result = `"${data}"`
    }
    result = String(result);
  }else{
    if(data.toJSON && typeof data.toJSON =='function'){
      //规则1:转换值如果有 toJSON() 方法，该方法定义什么值将被序列化。
      result+=jsonStringify(data.toJSON())
    }else if(data instanceof Array){
      result = [];
      data.forEach((item,index)=>{
        let itemType = typeof item;
        // 规则4:undefined、任意的函数以及 symbol 值，出现在数组中时,被转换成 null
        if(itemType == 'undefined' || itemType =='function' || itemType =='symbol'){
          result[index]="null";
        }else{
          result[index]=jsonStringify(item);
        }
      })
      result = `[${result}]`
    }else{
      result = [];
      Object.keys(data).forEach((item,index)=>{
        // 规则6:所有以 symbol 为属性键的属性都会被完全忽略掉，Object.keys返回包括对象自身的（不含继承的）所有可枚举属性（不含 Symbol 属性）的键名。
        let valueType = typeof data[item];
        if(valueType == 'undefined' || valueType =='function' || valueType =='symbol'){
          // 规则4:undefined、任意的函数以及 symbol 值，在序列化过程中会被忽略（出现在非数组对象的属性值中时）
        }else if(data[item] == data){
          // 规则5:对包含循环引用的对象（对象之间相互引用，形成无限循环）执行此方法，会抛出错误。
          throw "cycling";
        }else{
          result.push(`"${item}":${jsonStringify(data[item])}`);
        }
      })
      result = `{${result}}`
    }
  }
  return result;
}
```



##### 2、JSON.parse


