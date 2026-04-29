### 一、例题-[28. 实现 strStr()](https://leetcode.cn/problems/implement-strstr/)


<font style="color:rgb(44, 62, 80);">实现 strStr() 函数。</font>

<font style="color:rgb(44, 62, 80);">给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1。</font>

<font style="color:rgb(44, 62, 80);"></font>

<font style="color:rgb(44, 62, 80);">示例 1: 输入: haystack = "hello", needle = "ll" 输出: 2</font>

<font style="color:rgb(44, 62, 80);">示例 2: 输入: haystack = "aaaaa", needle = "bba" 输出: -1</font>

<font style="color:rgb(44, 62, 80);"></font>

<font style="color:rgb(44, 62, 80);">说明: 当 needle 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。 对于本题而言，当 needle 是空字符串时我们应当返回 0 。这与C语言的 strstr() 以及 Java的 indexOf() 定义相符。</font>

<font style="color:rgb(44, 62, 80);"></font>

####   
思路
<font style="color:rgb(44, 62, 80);">本题是KMP 经典题目。KMP主要应用在字符串匹配上。</font>

<font style="color:rgb(44, 62, 80);"></font>

<font style="color:rgb(44, 62, 80);">KMP的经典思想就是:</font>**<font style="color:rgb(44, 62, 80);">当出现字符串不匹配时，可以记录一部分之前已经匹配的文本内容，利用这些信息避免从头再去做匹配。</font>**

**<font style="color:rgb(44, 62, 80);"></font>**

**<font style="color:rgb(44, 62, 80);">什么是KMP,可看这篇介绍</font>**[什么是KMP](https://www.programmercarl.com/0028.%E5%AE%9E%E7%8E%B0strStr.html)**<font style="color:rgb(44, 62, 80);">。</font>**

**<font style="color:rgb(44, 62, 80);"></font>**

#### 解法一: 前缀表统一减一
```javascript
var strStr = function (haystack, needle) {
  if (needle.length === 0) return 0;
  
  const getNext = (needle) => {
    let next = [];
    let j = -1;
    next.push(j);
    
    for (let i = 1;i < needle.length;i++) {
      while (j >= 0 && needle[i] !== needle[j + 1]) {
        j = next[j];
      }
      if (needle[i] === needle[j + 1]) {
        j++;
      }
      
      next.push(j);
    }
    return next;
  }
  
  let next = getNext(needle);
  
  let j = -1;
  
  for (let i = 0;i < haystack.length;i++) {
    while (j >= 0 && haystack[i] !== needle[j + 1]) {
      j = next[j];
    }
    if (haystack[i] === needle[j + 1]) j++;
    if (j === needle.length - 1) {
      return i  - needle.length + 1;
    }
  }
  
  return -1;
}
```

**<font style="color:rgb(44, 62, 80);"></font>**

#### 解法二: 前缀表统一不减一
```javascript
/**
 * @param {string} haystack
 * @param {string} needle
 * @return {number}
 */
var strStr = function (haystack, needle) {
    if (needle.length === 0)
        return 0;

    const getNext = (needle) => {
        let next = [];
        let j = 0;
        next.push(j);

        for (let i = 1; i < needle.length; ++i) {
            while (j > 0 && needle[i] !== needle[j])
                j = next[j - 1];
            if (needle[i] === needle[j])
                j++;
            next.push(j);
        }

        return next;
    }

    let next = getNext(needle);
    let j = 0;
    for (let i = 0; i < haystack.length; ++i) {
        while (j > 0 && haystack[i] !== needle[j])
            j = next[j - 1];
        if (haystack[i] === needle[j])
            j++;
        if (j === needle.length)
            return (i - needle.length + 1);
    }

    return -1;
};
```

  


