# Leetcode javascript 环境

### 一、支持ES6+的新特性
我们在力扣提交的代码是放到力扣后台运行的， 而 JS 代码在力扣后台是在 node 中以 `--harmony` 方式运行的。

```bash
node --harmony  index.js
```



### 二、支持lodash库
在 LeetCode 中 [lodash](https://lodash.com/docs/) 默认可直接通过 `_` 访问。



### 三、支持队列、堆(优先队列)
为了弥补 JS 内置数据结构的缺失。除了 JS 内置数据结构之外，LeetCode 平台还对 JS 提供了两种额外的数据结构，它们分别是:

+ `queue`
+ `<font style="color:rgb(33, 37, 41);">priority-queue</font>`

<font style="color:rgb(33, 37, 41);"></font>

#### <font style="color:rgb(33, 37, 41);">queue</font>
LeetCode 提供了 JS 对队列的支持。详细用法见[https://github.com/datastructures-js/queue](https://github.com/datastructures-js/queue)

```javascript
// empty queue
const queue = new Queue();

// from an array
const queue = new Queue([1, 2, 3]);
```

<font style="color:rgb(33, 37, 41);"></font>

<font style="color:rgb(33, 37, 41);">其中 </font>`<font style="color:rgb(33, 37, 41);">queue</font>`<font style="color:rgb(33, 37, 41);"> 的实现也是使用数组模拟。不过不是直接使用 </font>`<font style="color:rgb(33, 37, 41);">shift</font>`<font style="color:rgb(33, 37, 41);"> 来删除头部元素，因为直接使用 </font>`<font style="color:rgb(33, 37, 41);">shift</font>`<font style="color:rgb(33, 37, 41);"> 删除最坏情况时间复杂度是 </font>`<font style="color:rgb(33, 37, 41);">$O(n)$</font>`<font style="color:rgb(33, 37, 41);">。这里它使用了一种标记技巧，即每次删除头部元素并不是真的移除，而是标记其已经被移除。</font>

<font style="color:rgb(33, 37, 41);">这种做法时间复杂度可以降低到 </font>`<font style="color:rgb(33, 37, 41);">$O(1)$</font>`<font style="color:rgb(33, 37, 41);">。只不过如果不停入队和出队，空间复杂度会很高，因为会保留所有的已经出队的元素。因此它会在每次出队超过一半的时候执行一次</font>**<font style="color:rgb(33, 37, 41);">缩容</font>**<font style="color:rgb(33, 37, 41);">（类似于数组扩容）。这样时间复杂度会增大到 </font>`<font style="color:rgb(33, 37, 41);">$O(logn)$</font>`<font style="color:rgb(33, 37, 41);">，但是空间会省。</font>

<font style="color:rgb(33, 37, 41);"></font>

#### <font style="color:rgb(33, 37, 41);">priority-queue</font>
详细用法见：[https://github.com/datastructures-js/priority-queue](https://github.com/datastructures-js/priority-queue)

```javascript
// empty queue with default priority the element value itself.
const numbersQueue = new MinPriorityQueue();

// empty queue, will provide priority in .enqueue
const patientsQueue = new MinPriorityQueue();

// empty queue with priority returned from a prop of the queued object
const biddersQueue = new MaxPriorityQueue({ priority: (bid) => bid.value });
```
