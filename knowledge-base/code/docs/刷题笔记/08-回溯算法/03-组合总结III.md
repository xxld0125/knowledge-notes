### 一、[216. 组合总和 III](https://leetcode.cn/problems/combination-sum-iii/)
<font style="color:rgb(44, 62, 80);">找出所有相加之和为 n 的 k 个数的组合。组合中只允许含有 1 - 9 的正整数，并且每种组合中不存在重复的数字。</font>

<font style="color:rgb(44, 62, 80);">说明：</font>

+ <font style="color:rgb(44, 62, 80);">所有数字都是正整数。</font>
+ <font style="color:rgb(44, 62, 80);">解集不能包含重复的组合。</font>

<font style="color:rgb(44, 62, 80);">示例 1: 输入: k = 3, n = 7 输出: [[1,2,4]]</font>

<font style="color:rgb(44, 62, 80);">示例 2: 输入: k = 3, n = 9 输出: [[1,2,6], [1,3,5], [2,3,4]]</font>

<font style="color:rgb(44, 62, 80);"></font>

#### 思路
<font style="color:rgb(44, 62, 80);">本题就是在[1,2,3,4,5,6,7,8,9]这个集合中找到和为n的k个数的组合。</font>

<font style="color:rgb(44, 62, 80);">相对于</font>[02-组合问题](https://www.yuque.com/u25370234/kb/lggt90)<font style="color:rgb(44, 62, 80);">，无非就是多了一个限制，本题是要找到和为n的k个数的组合，而整个集合已经是固定的了[1,...,9]。</font>

<font style="color:rgb(44, 62, 80);">本题k相当于了树的深度，9（因为整个集合就是9个数）就是树的宽度。</font>

<font style="color:rgb(44, 62, 80);"></font>

<font style="color:rgb(44, 62, 80);">例如 k = 2，n = 4的话，就是在集合[1,2,3,4,5,6,7,8,9]中求 k（个数） = 2, n（和） = 4的组合。</font>

<font style="color:rgb(44, 62, 80);">选取过程如图：</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1660028490494-c1ec9026-26bf-4e79-bb69-af80999dbc38.png)

<font style="color:rgb(44, 62, 80);">图中，可以看出，只有最后取到集合（1，3）和为4 符合条件。</font>

<font style="color:rgb(44, 62, 80);"></font>

#### 回溯三部曲
##### <font style="color:rgb(44, 62, 80);">确定递归函数参数</font>
和[02-组合问题](https://www.yuque.com/u25370234/kb/lggt90)<font style="color:rgb(44, 62, 80);">一样，依然需要一维数组path来存放符合条件的结果，二维数组result来存放结果集。</font>

<font style="color:rgb(44, 62, 80);">这里依然定义path 和 result为全局变量。</font>

```javascript
const result = []; // 存放结果集
const path = []; // 符合条件的结果
```

<font style="color:rgb(44, 62, 80);">接下来还需要如下参数：</font>

+ <font style="color:rgb(44, 62, 80);">targetSum：目标和，也就是题目中的n。</font>
+ <font style="color:rgb(44, 62, 80);">k：就是题目中要求k个数的集合。</font>
+ <font style="color:rgb(44, 62, 80);">sum：为已经收集的元素的总和，也就是path里元素的总和。</font>
+ <font style="color:rgb(44, 62, 80);">startIndex：为下一层for循环搜索的起始位置。</font>

<font style="color:rgb(44, 62, 80);">所以代码如下：</font>

```javascript
const result = []; // 存放结果集
const path = []; // 符合条件的结果

function backtracking(targetSum, k, sum, startIndex) {

}
```

<font style="color:rgb(44, 62, 80);">其实这里sum这个参数也可以省略，每次targetSum减去选取的元素数值，然后判断如果targetSum为0了，说明收集到符合条件的结果了，我这里为了直观便于理解，还是加一个sum参数。</font>

<font style="color:rgb(44, 62, 80);">还要强调一下，回溯法中递归函数参数很难一次性确定下来，一般先写逻辑，需要啥参数了，填什么参数。</font>

<font style="color:rgb(44, 62, 80);"></font>

##### 确定终止条件
<font style="color:rgb(44, 62, 80);">在上面已经说了，k其实就已经限制树的深度，因为就取k个元素，树再往下深了没有意义。</font>

<font style="color:rgb(44, 62, 80);">所以如果path.size() 和 k相等了，就终止。</font>

<font style="color:rgb(44, 62, 80);">如果此时path里收集到的元素和（sum） 和targetSum（就是题目描述的n）相同了，就用result收集当前的结果。</font>

<font style="color:rgb(44, 62, 80);">所以 终止代码如下：</font>

```javascript
if (path.length === k) {
  if (sum === targetSum) {
    result.push(path);
  }
  return;
}
```



##### 单层搜索过程
<font style="color:rgb(44, 62, 80);">本题和</font>[02-组合问题](https://www.yuque.com/u25370234/kb/lggt90)<font style="color:rgb(44, 62, 80);">区别之一就是集合固定的就是9个数[1,...,9]，所以for循环固定i<=9</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1660029349771-46c57ee0-b743-482e-b157-1f20401faaac.png)

<font style="color:rgb(44, 62, 80);">处理过程就是 path收集每次选取的元素，相当于树型结构里的边，sum来统计path里元素的总和。</font>

代码如下：

```javascript
for (let i = startIndex;i <= 9;i++) {
  sum += i;
  path.push(i);
  backtracking(targetSum, k, sum, i + 1);
  sum -= i;
  path.pop();
}
```



完整代码：

```javascript
function combinationSum3(k, n) {
  const result = []; // 存放结果集
  const path = []; // 符合条件的结果
  
  const backtracking = function(targetSum, k, sum, startIndex) {
    if (path.length === k) {
      if (sum === targetSum) result.push(path);
      return;
    }
    
    for (let i = startIndex;i <= 9;i++) {
      sum += i;
      path.push(i);
      backtracking(targetSum, k, sum, i + 1); // 注意i+1调整startIndex
      sum -= i; // 回溯
      path.pop(); // 回溯
    }
  }
  
  backtracking(n, k, 0, 1);
  return result;
}
```



#### 剪枝
<font style="color:rgb(44, 62, 80);">这道题目，剪枝操作其实是很容易想到了，想必大家看上面的树形图的时候已经想到了。</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1660030490566-823281f7-17ed-4dad-af1b-348e35416168.png)

<font style="color:rgb(44, 62, 80);">已选元素总和如果已经大于n（图中数值为4）了，那么往后遍历就没有意义了，直接剪掉。</font>

<font style="color:rgb(44, 62, 80);">那么剪枝的地方一定是在递归终止的地方剪，剪枝代码如下：</font>

<font style="color:rgb(44, 62, 80);"></font>

```javascript
if (sum > targetSum) {
  return;
}
```



完整代码

```javascript
function combinationSum3(k, n) {
  const result = []; // 存放结果集
  const path = []; // 符合条件的结果
  
  const backtracking = function(targetSum, k, sum, startIndex) {
    if (sum > targetSum) { // 剪枝操作
      return;
    }
    
    if (path.length === k) {
      if (sum === targetSum) result.push(path);
      return;
    }
    
    for (let i = startIndex;i <= 9 - (k - path.length);i++) { // 剪枝
      sum += i;
      path.push(i);
      backtracking(targetSum, k, sum, i + 1); // 注意i+1调整startIndex
      sum -= i; // 回溯
      path.pop(); // 回溯
    }
  }
  
  backtracking(n, k, 0, 1);
  return result;
}
```





#### 写法二
```javascript
function combinationSum3(k, n) {
  const result = []; // 存放结果集
  const path = []; // 符合条件的结果
  
  const backtracking = function(startIndex) {
    const l = path.length;
    if (l === k) {
      const sum = path.reduce((a, b) => a + b);
      if (sum === n) {
        res.push([...path]);
      }
      return;
    }
    
    if (path.length === k) {
      if (sum === targetSum) result.push(path);
      return;
    }
    
    for (let i = startIndex;i <= 9 - (k - l);i++) {
      path.push(i);
      backtracking(i + 1);
      path.pop();
    }
  }
  
  backtracking(1);
  return result;
}
```



#### 总结
<font style="color:rgb(44, 62, 80);">开篇就介绍了本题与</font>[02-组合问题](https://www.yuque.com/u25370234/kb/lggt90)<font style="color:rgb(44, 62, 80);">的区别，相对来说加了元素总和的限制，如果做完</font>[02-组合问题](https://www.yuque.com/u25370234/kb/lggt90)<font style="color:rgb(44, 62, 80);">再做本题在合适不过。</font>

<font style="color:rgb(44, 62, 80);">分析完区别，依然把问题抽象为树形结构，按照回溯三部曲进行讲解，最后给出剪枝的优化。</font>

<font style="color:rgb(44, 62, 80);"></font>

  


