`nextTick`接收一个回调函数作为参数，它的作用是将回调延迟到下次DOM更新周期之后执行。它与全局方法`Vue.nextTick`一样，不同的是回调的`this`自动绑定到调用它的实例上。如果没有提供回调且在支持`Promise`的环境中，则返回一个`Promise`。

当更新了状态（数据）后，需要对新DOM做一些操作，但是这时我们其实获取不到更新后的DOM，因为还没有重新渲染。这个时候我们需要使用`nextTick`方法。



## DOM 更新周期
在Vue.js中，当状态发生变化时，`watcher`会得到通知，然后触发虚拟DOM的渲染流程。而`watcher`触发渲染这个操作并不是同步的，而是异步的。Vue.js中有一个队列，每当需要渲染时，会将`watcher`推送到这个队列中，在下一次事件循环中再让`watcher`触发渲染的流程。



## 为什么Vue.js使用异步更新队列
我们知道Vue.js 2.0开始使用虚拟DOM进行渲染，变化侦测的通知只发送到组件，组件内用到的所有状态的变化都会通知到同一个`watcher`，然后虚拟DOM会对整个组件进行“比对（diff）”并更改DOM。也就是说，如果在同一轮事件循环中有两个数据发生了变化，那么组件的`watcher`会收到两份通知，从而进行两次渲染。事实上，并不需要渲染两次，虚拟DOM会对整个组件进行渲染，所以只需要等所有状态都修改完毕后，一次性将整个组件的DOM渲染到最新即可。

要解决这个问题，Vue.js的实现方式是将收到通知的`watcher`实例添加到队列中缓存起来，并且在添加到队列之前检查其中是否已经存在相同的`watcher`，只有不存在时，才将`watcher`实例添加到队列中。然后在下一次事件循环（`eventloop`）中，Vue.js会让队列中的`watcher`触发渲染流程并清空队列。这样就可以保证即便在同一事件循环中有两个状态发生改变，`watcher`最后也只执行一次渲染流程。



## 事件循环
我们都知道JavaScript是一门单线程且非阻塞的脚本语言，这意味着JavaScript代码在执行的任何时候都只有一个主线程来处理所有任务。而非阻塞是指当代码需要处理异步任务时，主线程会挂起（pending）这个任务，当异步任务处理完毕后，主线程再根据一定规则去执行相应回调。

事实上，当任务处理完毕后，JavaScript会将这个事件加入一个队列中，我们称这个队列为事件队列。被放入事件队列中的事件不会立刻执行其回调，而是等待当前执行栈中的所有任务执行完毕后，主线程会去查找事件队列中是否有任务。

异步任务有两种类型：微任务（microtask）和宏任务（macrotask）。不同类型的任务会被分配到不同的任务队列中。

当执行栈中的所有任务都执行完毕后，会去检查微任务队列中是否有事件存在，如果存在，则会依次执行微任务队列中事件对应的回调，直到为空。然后去宏任务队列中取出一个事件，把对应的回调加入当前执行栈，当执行栈中的所有任务都执行完毕后，检查微任务队列中是否有事件存在。无限重复此过程，就形成了一个无限循环，这个循环就叫作事件循环。



## 异步任务类型
属于微任务的事件包括但不限于以下几种：

+ Promise.then
+ MutationObserver
+ Object.observe
+ process.nextTick

属于宏任务的事件包括但不限于以下几种：

+ setTimeout
+ setInterval
+ setImmediate
+ MessageChannel
+ requestAnimationFrame
+ I/O
+ UI交互事件



## 执行栈
当我们执行一个方法时，JavaScript会生成一个与这个方法对应的执行环境（context），又叫执行上下文。这个执行环境中有这个方法的私有作用域、上层作用域的指向、方法的参数、私有作用域中定义的变量以及this对象。这个执行环境会被添加到一个栈中，这个栈就是执行栈。

如果在这个方法的代码中执行到了一行函数调用语句，那么JavaScript会生成这个函数的执行环境并将其添加到执行栈中，然后进入这个执行环境继续执行其中的代码。执行完毕并返回结果后，JavaScript会退出执行环境并把这个执行环境从栈中销毁，回到上一个方法的执行环境。这个过程反复进行，直到执行栈中的代码全部执行完毕。这个执行环境的栈就是执行栈。



“下次DOM更新周期”的意思其实是下次微任务执行时更新DOM。而`vm.$nextTick`其实是将回调添加到微任务中。只有在特殊情况下才会降级成宏任务，默认会添加到微任务中。

因此，如果使用`vm.$nextTick`来获取更新后的DOM，则需要注意顺序的问题。因为不论是更新DOM的回调还是使用`vm.$nextTick`注册的回调，都是向微任务队列中添加任务，所以哪个任务先添加到队列中，就先执行哪个任务。



**<font style="color:#DF2A3F;">因此，如果使用</font>**`**<font style="color:#DF2A3F;">vm.$nextTick</font>**`**<font style="color:#DF2A3F;">来获取更新后的DOM，则需要注意顺序的问题。因为不论是更新DOM的回调还是使用</font>**`**<font style="color:#DF2A3F;">vm.$nextTick</font>**`**<font style="color:#DF2A3F;">注册的回调，都是向微任务队列中添加任务，所以哪个任务先添加到队列中，就先执行哪个任务。</font>**

```javascript
new Vue({
  // ……
  methods: {
    // ……
    example: function () {
      setTimeout(function () {
        // DOM更新了

        // setTimeout属于宏任务，使用它注册的回调会加入到宏任务中。
        // 宏任务的执行要比微任务晚，所以即便是先注册，
        // 也是先更新DOM后执行setTimeout中设置的回调。
      })
      
      nextTick(function () {
        // DOM没更新
      })

      // 修改数据
      this.message = 'changed'
      
      this.$nextTick(function () {
        // DO在更新了
      })
    }
  }
})
```



## 实现方式
由于`vm.$nextTick`会将回调添加到任务队列中延迟执行，所以在回调执行前，如果反复调用`vm.$nextTick`，Vue.js并不会反复将回调添加到任务队列中，只会向任务队列中添加一个任务。

Vue.js内部有一个列表用来存储`vm.$nextTick`参数中提供的回调。在一轮事件循环中，`vm.$nextTick`只会向任务队列添加一个任务，多次使用`vm.$nextTick`只会将回调添加到回调列表中缓存起来。当任务触发时，依次执行列表中的所有回调并清空列表。



```javascript
import { noop } from "shared/util";
import { handleError } from "./error";
import { isIE, isIOS, isNative } from "./env";

// 标记是否使用微任务
export let isUsingMicroTask = false;

// 存储所有待执行的回调函数
const callbacks = [];
// 标记是否有等待执行的回调队列
let pending = false;

/**
 * 清空回调队列的函数
 * 复制当前队列，重置原队列，然后按顺序执行复制出来的队列中的所有回调
 */
function flushCallbacks() {
  pending = false;
  // 创建 callbacks 的副本
  const copies = callbacks.slice(0);
  // 清空原始数组，允许在回调执行期间注册新的回调
  callbacks.length = 0;
  // 按顺序执行所有回调
  for (let i = 0; i < copies.length; i++) {
    copies[i]();
  }
}

// 这里我们使用微任务包装异步延迟执行。
// 在 Vue 2.5 中，我们曾使用宏任务（结合微任务）。
// 但这在状态改变后立即重绘时会有微妙问题（例如 #6813，out-in 过渡）。
// 此外，在事件处理函数中使用宏任务会导致一些无法规避的奇怪行为
// （例如 #7109，#7153，#7546，#7834，#8109）。
// 所以我们现在再次全面使用微任务。
// 这种折衷方案的一个主要缺点是：在某些场景下，
// 微任务的优先级太高，会在本应连续的事件之间触发
// （例如 #4521，#6690，这些问题有变通解决方案）
// 甚至在同一事件的冒泡过程中触发（#6566）。
let timerFunc;

// nextTick 行为利用了微任务队列，可以通过以下方式访问：
// 原生 Promise.then 或 MutationObserver。
// MutationObserver 有更广泛的支持，但在 iOS >= 9.3.3 的 UIWebView 中，
// 当在触摸事件处理程序中触发时，它存在严重 bug。
// 触发几次后完全停止工作...因此，如果原生 Promise 可用，我们将使用它：
/* istanbul ignore next, $flow-disable-line */
if (typeof Promise !== "undefined" && isNative(Promise)) {
  // 使用 Promise.resolve() 创建一个已解决的 Promise
  const p = Promise.resolve();
  timerFunc = () => {
    // 使用 Promise 微任务来执行回调队列
    p.then(flushCallbacks);
    // 在有问题的 UIWebViews 中，Promise.then 不会完全崩溃，但可能陷入怪异状态：
    // 回调被推入微任务队列但队列未被刷新，直到浏览器需要执行其他工作（如处理定时器）
    // 因此，我们可以通过添加空定时器来"强制"刷新微任务队列
    if (isIOS) setTimeout(noop);
  };
  isUsingMicroTask = true;
} else if (
  !isIE &&
  typeof MutationObserver !== "undefined" &&
  (isNative(MutationObserver) ||
    // PhantomJS 和 iOS 7.x
    MutationObserver.toString() === "[object MutationObserverConstructor]")
) {
  // 在原生 Promise 不可用的环境中使用 MutationObserver
  // 例如 PhantomJS、iOS7、Android 4.4
  // (#6466 MutationObserver 在 IE11 中不可靠)
  let counter = 1;
  // 创建 MutationObserver 实例，观察到变化时执行回调队列
  const observer = new MutationObserver(flushCallbacks);
  // 创建文本节点作为观察目标
  const textNode = document.createTextNode(String(counter));
  // 观察文本节点的字符数据变化
  observer.observe(textNode, {
    characterData: true,
  });
  // 通过修改文本节点内容来触发回调
  timerFunc = () => {
    counter = (counter + 1) % 2;
    textNode.data = String(counter);
  };
  isUsingMicroTask = true;
} else if (typeof setImmediate !== "undefined" && isNative(setImmediate)) {
  // 降级使用 setImmediate
  // 技术上它利用的是（宏）任务队列，
  // 但它仍然比 setTimeout 更好
  timerFunc = () => {
    setImmediate(flushCallbacks);
  };
} else {
  // 最后降级使用 setTimeout
  timerFunc = () => {
    setTimeout(flushCallbacks, 0);
  };
}

/**
 * nextTick 是 Vue 中一个重要的工具函数，它允许在 DOM 更新后执行回调函数
 * @param {Function} [cb] 需要延迟执行的回调函数
 * @param {Object} [ctx] 回调函数的上下文（this 指向）
 * @return {Promise} 如果没有提供回调且 Promise 可用，则返回一个 Promise
 */
export function nextTick(cb?: Function, ctx?: Object) {
  let _resolve;
  // 将回调函数包装后添加到回调队列
  callbacks.push(() => {
    if (cb) {
      // 如果提供了回调函数，则尝试调用它
      try {
        cb.call(ctx);
      } catch (e) {
        // 处理回调中可能出现的错误
        handleError(e, ctx, "nextTick");
      }
    } else if (_resolve) {
      // 如果没有提供回调但需要返回 Promise，则执行 Promise 的 resolve
      _resolve(ctx);
    }
  });
  // 如果还没有等待执行的回调队列，则启动一个
  if (!pending) {
    pending = true;
    timerFunc();
  }
  // 如果没有提供回调但 Promise 可用，则返回 Promise
  // $flow-disable-line
  if (!cb && typeof Promise !== "undefined") {
    return new Promise((resolve) => {
      _resolve = resolve;
    });
  }
}

```

	

## 运行流程图
![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748571780148-b14535ff-77ef-49a9-ad54-c7009d509bdb.png)





