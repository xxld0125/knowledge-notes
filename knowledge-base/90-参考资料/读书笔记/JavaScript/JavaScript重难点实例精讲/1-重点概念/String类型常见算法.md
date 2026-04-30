# 字符串逆序输出
字符串的逆序输出就是将一个字符串以相反的顺序进行输出。

## 题目
给定一个字符串'abcdefg'，执行一定的算法后，输出的结果为'gfedcba'。



## 解法
### 
主要思想是借助数组的`reverse()`函数。

首先将字符串转换为字符数组，然后通过调用数组原生的`reverse()`函数进行逆序，得到逆序数组后再通过调用`join()`函数得到逆序字符串。

```javascript
function reverseString1(str) {
   return str.split('').reverse().join('');
}
```



### 
主要思想是利用字符串本身的`charAt()`函数。

从尾部开始遍历字符串，然后利用`charAt()`函数获取字符并逐个拼接，得到最终的结果。`charAt()`函数接收一个索引数字，返回该索引位置对应的字符。

```javascript
function reverseString2(str) {
   var result = '';
   for(var i = str.length - 1; i >= 0; i--){
       result += str.charAt(i);
   }
   return result;
}
```



### 
主要思想是通过递归实现逆序输出，与`charAt`的处理类似。

递归从字符串最后一个位置索引开始，通过`charAt()`函数获取一个字符，并拼接到结果字符串中，递归结束的条件是位置索引小于0。

```javascript
function reverseString3(strIn,pos,strOut){
   if(pos<0)
      return strOut;
   strOut += strIn.charAt(pos--);
   return reverseString3(strIn,pos,strOut);
}
```



### 
主要思想是通过`call()`函数来改变`slice()`函数的执行主体。

调用`call()`函数后，可以让字符串具有数组的特性，在调用未传入参数的`slice()`函数后，得到的是一个与自身相等的数组，从而可以直接调用`reverse()`函数，最后再通过调用`join()`函数，得到逆序字符串。

```javascript
function reverseString4(str) {
   // 改变slice()函数的执行主体，得到一个数组
   var arr = Array.prototype.slice.call(str);
   // 调用reverse()函数逆序数组
   return arr.reverse().join('');
}
```



### 
主要思想是借助栈的先进后出原则。

由于JavaScript并未提供栈的实现，我们首先需要实现一个栈的数据结构，然后在栈中添加插入和弹出的函数，利用插入和弹出方法的函数字符串逆序。

```javascript
// 栈
function Stack() {
   this.data = []; // 保存栈内元素
   this.top = 0;   // 记录栈顶位置
}
// 原型链增加出栈、入栈方法
Stack.prototype = {
   // 入栈:先在栈顶添加元素，然后元素个数加1
   push: function push(element) {
       this.data[this.top++] = element;
   },
   // 出栈：先返回栈顶元素，然后元素个数减1
   pop: function pop() {
       return this.data[--this.top];
   },
   // 返回栈内的元素个数，即长度
   length: function () {
       return this.top;
   }
};
```

```javascript
// 算法5：自定义栈实现
function reverseString5(str) {
   //创建一个栈的实例
   var s = new Stack();
   //将字符串转成数组
   var arr = str.split('');
   var len = arr.length;
   var result = '';
   //将元素压入栈内
   for(var i = 0; i < len; i++){
      s.push(arr[i]);
   }
   //输出栈内元素
   for(var j = 0; j < len; j++){
      result += s.pop(j);
   }
   return result;
}
```



# 统计字符串中出现次数最多的字符及出现的次数
## 题目
假如存在一个字符串`'helloJavascripthellohtmlhellocss'`，其中出现次数最多的字符是`l`，出现的次数是7次。



## 解法
### 
主要思想是通过`key-value`形式的对象来存储字符串以及字符串出现的次数，然后逐个判断出现次数最大值，同时获取对应的字符。

+ 首先通过`key-value`形式的对象来存储数据，`key`表示不重复出现的字符，`value`表示该字符出现的次数。
+ 然后遍历字符串的每个字符，判断是否出现在`key`中。如果在，直接将对应的`value`值加1；如果不在，则直接新增一组`key-value`，`value`值为1。
+ 得到`key-value`对象后，遍历该对象，逐个比较`value`值的大小，找出其中最大的值并记录`key-value`，即获得最终想要的结果。





```javascript
// 算法1
function getMaxCount(str) {
   var json = {};
   // 遍历str的每一个字符得到key-value形式的对象
   for (var i = 0; i < str.length; i++) {
       // 判断json中是否有当前str的值
       if (!json[str.charAt(i)]) {
           // 如果不存在，就将当前值添加到json中去
           json[str.charAt(i)] = 1;
       } else {
           // 如果存在，则让value值加1
           json[str.charAt(i)]++;
       }
   }
   // 存储出现次数最多的值和出现次数
   var maxCountChar = '';
   var maxCount = 0;
   // 遍历json对象，找出出现次数最大的值
  for (var key in json) {
      // 如果当前项大于下一项
      if (json[key] > maxCount) {
          // 就让当前值更改为出现最多次数的值
          maxCount = json[key];
          maxCountChar = key;
      }
   }
   //最终返回出现最多的值以及出现次数
   return '出现最多的值是' + maxCountChar + '，出现次数为' + maxCount;
}
var str = 'helloJavaScripthellohtmlhellocss';
getMaxCount(str); // '出现最多的值是l，出现次数为7'
```



### 
借助于`key-value`形式的对象来存储字符与字符出现的次数，但是在运算上有所差别。

+ 首先通过`key-value`形式的对象来存储数据，`key`表示不重复出现的字符，`value`表示该字符出现的次数。
+ 然后将字符串处理成数组，通过`forEach()`函数遍历每个字符。在处理之前需要先判断当前处理的字符是否已经在`key-value`对象中，如果已经存在则表示已经处理过相同的字符，则无须处理；如果不存在，则会处理该字符item。
+ 通过`split()`函数传入待处理字符，可以得到一个数组，该数组长度减1即为该字符出现的次数。
+ 获取字符出现的次数后，立即与表示出现最大次数和最大次数对应的字符变量`maxCount`和`maxCountChar`相比，如果比`maxCount`大，则将值写入`key-value`对象中，并动态更新`maxCount`和`maxCountChar`的值，直到最后一个字符处理完成。
+ 最后得到的结果即`maxCount`和`maxCountChar`两个值。



```javascript
// 算法2
function getMaxCount2(str) {
   var json = {};
   var maxCount = 0, maxCountChar = '';
   str.split('').forEach(function (item) {
       // 判断json对象中是否有对应的key
       if (!json.hasOwnProperty(item)) {
           // 当前字符出现的次数
           var number = str.split(item).length - 1;
           // 直接与出现次数最大值比较，并进行更新
           if(number > maxCount) {
               // 写入json对象
               json[item] = number;
               // 更新maxCount与maxCountChar的值
               maxCount = number;
               maxCountChar = item;
           }
       }
   });

   return '出现最多的值是' + maxCountChar + '，出现次数为' + maxCount;
}

var str = 'helloJavaScripthellohtmlhellocss';
getMaxCount2(str); // '出现最多的值是l，出现次数为7'
```



### 
主要思想是对字符串进行排序，然后通过`lastIndexOf()`函数获取索引值后，判断索引值的大小以获取出现的最大次数。

+ 首先将字符串处理成数组，调用`sort()`函数进行排序，处理成字符串。
+ 然后遍历每个字符，通过调用`lastIndexOf()`函数，确定每个字符出现的最后位置，然后减去当前遍历的索引，就可以确定该字符出现的次数。
+ 确定字符出现的次数后，直接与次数最大值变量`maxCount`进行比较，如果比`maxCount`大，则直接更新`maxCount`的值，并同步更新`maxCountChar`的值；如果比`maxCount`小，则不做任何处理。
+ 计算完成后，将索引值设置为字符串出现的最后位置，进行下一轮计算，直到处理完所有字符。



```javascript
// 算法3
function getMaxCount3(str) {
   // 定义两个变量，分别表示出现最大次数和对应的字符
   var maxCount = 0, maxCountChar = '';
   // 先处理成数组，调用sort()函数排序,再处理成字符串
   str = str.split('').sort().join('');
   for (var i = 0, j = str.length; i < j; i++) {
       var char = str[i];
       // 计算每个字符串出现的次数
       var charCount = str.lastIndexOf(char) - i + 1;
       // 与次数最大值作比较
       if (charCount > maxCount) {
           // 更新maxCount和maxCountChar的值
           maxCount = charCount;
           maxCountChar = char;
       }
       // 变更索引为字符出现的最后位置
       i = str.lastIndexOf(char);
   }
   return '出现最多的值是' + maxCountChar + '，出现次数为' + maxCount;
}

var str = 'helloJavaScripthellohtmlhellocss';
getMaxCount3(str);  // '出现最多的值是l，出现次数为7'
```



### 
主要思想是将字符串进行排序，然后通过正则表达式将字符串进行匹配拆分，将相同字符组合在一起，最后判断字符出现的次数。

+ 首先将字符串处理成数组，调用`sort()`函数进行排序，处理成字符串。
+ 然后设置正则表达式`reg`，对字符串使用`match()`函数进行匹配，得到一个数组，数组中的每个成员是相同的字符构成的字符串。
+ 遍历数组，依次将成员字符串长度值与`maxCount`值进行比较，动态更新`maxCount`与`maxCountChar`的值，直到数组所有元素处理完成。



```javascript
// 算法4
function getMaxCount4(str) {
   // 定义两个变量，分别表示出现最大次数和对应的字符
   var maxCount = 0, maxCountChar = '';
   // 先处理成数组，调用sort()函数排序,再处理成字符串
   str = str.split('').sort().join('');
   // 通过正则表达式将字符串处理成数组(数组每个元素为相同字符构成的字符串)
   var arr = str.match(/(\w)\1+/g);
   for (var i = 0; i < arr.length; i++) {
       // length表示字符串出现的次数
       var length = arr[i].length;
       // 与次数最大值作比较
       if (length > maxCount) {
           // 更新maxCount和maxCountChar
           maxCount = length;
           maxCountChar = arr[i][0];
       }
   }
   return '出现最多的值是' + maxCountChar + '，出现次数为' + maxCount;
}

var str = 'helloJavaScripthellohtmlhellocss';
getMaxCount4(str);  // '出现最多的值是l，出现次数为7'
```



### 
主要思想是借助`replace()`函数，主要实现方式如下。



+ 通过`while`循环处理，跳出`while`循环的条件是字符串长度为0。
+ 在`while`循环中，记录原始字符串的长度`originCount`，用于后面做长度计算处理。
+ 获取字符串第一个字符`char`，通过`replace()`函数将`char`替换为空字符串''，得到一个新的字符串，它的长度`remainCount`相比于`originCount`会小，其中的差值`originCount - remainCount`即为该字符出现的次数。
+ 确定字符出现的次数后，直接与`maxCount`进行比较，如果比`maxCount`大，则直接更新`maxCount`的值，并同步更新`maxCountChar`的值；如果比`maxCount`小，则不做任何处理。
+ 处理至跳出`while`循环，得到最终结果。



```javascript
// 算法5
function getMaxCount5(str) {
   // 定义两个变量，分别表示出现最大次数和对应的字符
   var maxCount = 0, maxCountChar = '';
   while (str) {
       // 记录原始字符串的长度
       var originCount = str.length;
       // 当前处理的字符
       var char = str[0];
       var reg = new RegExp(char, 'g');
       // 使用replace()函数替换处理的字符为空字符串
       str = str.replace(reg, '');
       var remainCount = str.length;
       // 当前字符出现的次数
       var charCount = originCount - remainCount;
       // 与次数最大值作比较
       if (charCount > maxCount) {
          // 更新maxCount和maxCountChar的值
          maxCount = charCount;
          maxCountChar = char;
       }
   }
   return '出现最多的值是' + maxCountChar + '，出现次数为' + maxCount;
}

var str = 'helloJavaScripthellohtmlhellocss';
getMaxCount5(str);  // '出现最多的值是l，出现次数为7'
```



# 去除字符串中重复的字符
## 题目
假如存在一个字符串`'helloJavaScripthellohtmlhellocss'`，其中存在大量的重复字符，例如h、e、l等，去除重复的字符，只保留一个，得到的结果应该是`'heloJavscriptm'`。



## 解法
### 
主要思想是使用`key-value`类型的对象存储，`key`表示唯一的字符，处理完后将所有的`key`拼接在一起即可得到去重后的结果。

+  首先通过`key-value`形式的对象来存储数据，`key`表示不重复出现的字符，`value`为`boolean`类型的值，为`true`则表示字符出现过。
+ 然后遍历字符串，判断当前处理的字符是否在对象中，如果在，则不处理；如果不在，则将该字符添加到结果数组中。
+ 处理完字符串后，得到一个数组，转换为字符串后即可获得最终需要的结果。



```javascript
function removeDuplicateChar1(str) {
   // 结果数组
   var result = [];
   // key-value形式的对象
   var json = {};
   for (var i = 0; i < str.length; i++) {
       // 当前处理的字符
       var char = str[i];
       // 判断是否在对象中
       if(!json[char]) {
           // value值设置为false
           json[char] = true;
           // 添加至结果数组中
           result.push(char);
       }
   }
   return result.join('');
}

var str = 'helloJavaScripthellohtmlhellocss';
removeDuplicateChar1(str);  // 'heloJavscriptm'
```



### 
主要思想是借助数组的`filter()`函数，然后在`filter()`函数中使用`indexOf()`函数判断。

+  通过`call()`函数改变`filter()`函数的执行体，让字符串可以直接执行`filter()`函数。
+ 在自定义的`filter()`函数回调中，通过`indexOf()`函数判断其第一次出现的索引位置`，如果与filter()`函数中的`index`一样，则表示第一次出现，符合条件则`return`出去。这就表示只有第一次出现的字符会被成功过滤出来，而其他重复出现的字符会被忽略掉。
+ `filter()`函数返回的结果便是已经去重的字符数组，将其转换为字符串输出即为最终需要的结果。

```javascript
function removeDuplicateChar2(str) {
   // 使用call()函数改变ﬁlter函数的执行主体
   let result = Array.prototype.ﬁlter.call(str, function (char, index, arr) {
      // 通过indexOf()函数与index的比较，判断是否是第一次出现的字符
      return arr.indexOf(char) === index;
   });
   return result.join('');
}

var str = 'helloJavaScripthellohtmlhellocss';
removeDuplicateChar2(str);  // 'heloJavscriptm'
```



### 
主要思想是借助ES6中的`Set`数据结构，`Set`具有自动去重的特性，可以直接将数组元素去重。

+  将字符串处理成数组，然后作为参数传递给Set的构造函数，通过new运算符生成一个Set的实例。
+ 将Set通过扩展运算符（...）转换成数组形式，最终转换成字符串获得需要的结果。



```javascript
function removeDuplicateChar3(str) {
   // 字符串转换的数组作为参数，生成Set的实例
   let set = new Set(str.split(''));
    // 将set重新处理为数组，然后转换成字符串
   return [...set].join('');
}

var str = 'helloJavaScripthellohtmlhellocss';
removeDuplicateChar3(str);  // 'heloJavscriptm'
```



# 判断一个字符串是否为回文字符串
## 题目
回文字符串是指一个字符串正序和倒序是相同的，例如字符串'abcdcba'是一个回文字符串，而字符串'abcedba'则不是一个回文字符串。需要注意的是，这里不区分字符大小写，即a与A在判断时是相等的。

真实的场景如下。给定两个字符串'abcdcba'和'abcedba'，经过一定的算法处理，分别会返回“true”和“false”。



## 解法
### 
主要思想是将字符串按从前往后顺序的字符与按从后往前顺序的字符逐个进行比较，如果遇到不一样的值则直接返回“false”，否则返回“true”。

```javascript
// 算法1
function isPalindromicStr1(str) {
   // 空字符则直接返回“true”
   if (!str.length) {
       return true;
   }
   // 统一转换成小写，同时转换成数组
   str = str.toLowerCase().split('');
   var start = 0, end = str.length - 1;
   // 通过while循环判断正序和倒序的字母
   while(start < end) {
      // 如果相等则更改比较的索引
      if(str[start] === str[end]) {
          start++;
          end--;
      } else {
          return false;
      }
   }
   return true;
}

var str1 = 'abcdcba';
var str2 = 'abcedba';

isPalindromicStr1(str1);  // true
isPalindromicStr1(str2);  // false
```



### 
将正序和倒序的字符逐个进行比较，与算法1不同的是，算法2采用递归的形式实现。

```javascript
// 算法2
function isPalindromicStr2(str) {
   // 字符串处理完成，则返回“true”
   if(!str.length) {
      return true;
   }
   // 字符串统一转换成小写
   str = str.toLowerCase();
   let end = str.length - 1;
   // 当首字符和尾字符不同，直接返回“false”
   if(str[0] !== str[end]) {
      return false;
   }
   // 删掉字符串首尾字符，进行递归处理
   return isPalindromicStr2(str.slice(1, end));
}

var str1 = 'abcdcba';
var str2 = 'abcedba';

isPalindromicStr2(str1);  // true
isPalindromicStr2(str2);  // false
```



### 
主要思想是将字符串进行逆序处理，然后与原来的字符串进行比较，如果相等则表示是回文字符串，否则不是回文字符串。

```javascript
// 算法3
function isPalindromicStr3(str) {
   // 字符串统一转换成小写
   str = str.toLowerCase();
   // 将字符串转换成数组
   var arr = str.split('');
   // 将数组逆序并转换成字符串
    var reverseStr = arr.reverse().join('');
    return str === reverseStr;
}

var str1 = 'abcdcba';
var str2 = 'abcedba';

isPalindromicStr3(str1);  // true
isPalindromicStr3(str2);  // false
```

