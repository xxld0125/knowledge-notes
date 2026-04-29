### 一、[169. 多数元素](https://leetcode-cn.com/problems/majority-element/)


类似题目：

[剑指 Offer 39. 数组中出现次数超过一半的数字](https://leetcode-cn.com/problems/shu-zu-zhong-chu-xian-ci-shu-chao-guo-yi-ban-de-shu-zi-lcof/)



#### 解法一：哈希表
<font style="color:rgb(38, 38, 38);">因为数量大于一半，统计完大于一半的数据直接返回即可。</font>

```javascript
/**
 * @param {number[]} nums
 * @return {number}
 */
var majorityElement = function(nums) {
    const map = new Map();
    let n = nums.length;
    if (nums.length <= 1) {
        return nums[0];
    }

    for (let i = 0;i < n;i++) {
        if (map.has(nums[i])) {
            map.set(nums[i], map.get(nums[i]) + 1);
            if (map.get(nums[i]) > n / 2) {
                return nums[i]
            }
        } else {
            map.set(nums[i], 1);
        }
    }
};
```



#### 解法二：排序法
<font style="color:rgb(38, 38, 38);">首先对数组进行升序，因为题意中指出多数元素一定存在且出现的次数大于 n/2 次，所以返回中间元素即可。</font>

```javascript
/**
 * @param {number[]} nums
 * @return {number}
 */
var majorityElement = function(nums) {
    nums.sort((a,b) => a - b);
    return nums[Math.floor(nums.length / 2)];
};
```



#### 解法三：摩尔投票法
题目求多数元素，有点类似古代两军对战，

两军领导说我们一对一火拼，人多的哪怕多一个人就胜利了

A军B军火力值相同（人数相同）的情况下，我们假设让A军做胜利的候选者

来了一个兵，问这个兵你是站队A军还是不站队A军，如果站队A军的话，A军火力值加1

如果不站队A军，那A军火力值减1

最后人数最多的军队胜出

```javascript
/**
 * @param {number[]} nums
 * @return {number}
 */
var majorityElement = function(nums) {
    let count = 1;
    let pre = nums[0];

    for (let i = 1;i < nums.length;i++) {
        if (!count) {
            pre = nums[i];
            count = 1;
        } else if (pre === nums[i]) {
            count++;
        } else if (pre !== nums[i]) {
            count--;
        }
    }
    return pre;
};
```



### 二、[205. 同构字符串](https://leetcode-cn.com/problems/isomorphic-strings/)
类似题目：

[290. 单词规律](https://leetcode-cn.com/problems/word-pattern/)

#### 解法一：哈希表-双射
**思路：**需要我们判断 ss 和 tt 每个位置上的字符是否都一一对应，即 ss 的任意一个字符被 tt 中唯一的字符对应，同时 tt 的任意一个字符被 ss 中唯一的字符对应。这也被称为「双射」的关系。故此，我们要维护两张哈希表，存储映射关系。

```javascript
/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
var isIsomorphic = function(s, t) {

    const smap = new Map();
    const tmap = new Map();
    for (let i = 0;i < s.length;i++) {
        if (smap.has(s[i]) && smap.get(s[i]) !== t[i] || tmap.has(t[i]) && tmap.get(t[i]) !== s[i]) {
            return false;
        }
        smap.set(s[i], t[i]);
        tmap.set(t[i], s[i]);
    }

    return true;
};
```

### 
#### 解法二：索引
**思路：**同构字符串，没字符首次出现、最后出现、指定位出现索引始终相同

```javascript
/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
var isIsomorphic = function(s, t) {
    for (let i = 0;i < s.length;i++) {
        if (s.indexOf(s[i]) !== t.indexOf(t[i])) return false;
    }
    return true
};
```

#### [  
](https://leetcode-cn.com/problems/happy-number/)解法三：元组
**思路：**同构字符串、分别去重与每位两两组合去重后长度相等

```javascript
/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
var isIsomorphic = function(s, t) {
    const n = s.length;
    const arr = new Array(n);
    for (let i = 0;i < n;i++) {
        arr[i] = s[i] + ',' + t[i];
    }

    const c = new Set(arr).size;
    return c === new Set(s).size && c === new Set(t).size;
};
```



#### 解法四、双哈希-索引
**思路：**与方法一相比,此方法哈希表存储的是索引, 因为同构字符串,每个字符上次出现索引始终相同.

```javascript
/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
var isIsomorphic = function(s, t) {
    const smap = new Map, tmap = new Map;
    for (let i = 0;i < s.length;i++) {
        if (smap.get(s[i]) !== tmap.get(t[i])) {
            return false;
        }
        smap.set(s[i], i);
        tmap.set(t[i], i);
    }
    return true;
};
```





### 三、[1002. 查找共用字符](https://leetcode-cn.com/problems/find-common-characters/)
#### 解法一：
思路：判断每个单词是否包含当前字符，是的话则将当前字符推入结果栈， 并将每个单词中的该字符置空，接着循环首个单词，即可得到所有的共用字符。

```javascript
/**
 * @param {string[]} words
 * @return {string[]}
 */
var commonChars = function(words) {
    const res = [], word = words[0];
    for (let s of word) {
        if (words.every(v => v.includes(s))) {
            words = words.map(k => k.replace(s, ''));
            res.push(s);
        }
    }
    return res;
};
```

### 
#### 解法二
思路：将首个单词根据出现次数，存入字典表。再遍历所有的单词，对每个单词创建字典表，再与首单词的字典表对比，取出现次数小的值。循环后得到的就是所有的共用字符。

```javascript
/**
 * @param {string[]} words
 * @return {string[]}
 */
var commonChars = function(words) {
    const map = new Map;

    for (let n of words[0]) {
        map.set(n, (map.get(n) || 0) + 1);
    }

    for (let i = 1;i < words.length;i++) {
        const tmp = new Map;

        for (let n of words[i]) {
            tmp.set(n, (tmp.get(n) || 0) + 1);
        }

        map.forEach((v, k) => {
            let count = v;

            if (tmp.has(k)) {
                if (v > tmp.get(k)) {
                    count = tmp.get(k);
                }
            } else {
                count = 0;
            }

            map.set(k, count);
        })
    }

    const res = [];

    map.forEach((v, k) => {
        let i = v;
        if (i > 0) {
            while (i--) {
                res.push(k);
            }
        }
    })
    return res;
};
```

