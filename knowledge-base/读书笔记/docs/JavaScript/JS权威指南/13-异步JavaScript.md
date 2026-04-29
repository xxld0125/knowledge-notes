#### 一、使用回调的异步编程
在最基本的层面上，JavaScript异步编程是使用回调实现的。回调就是函数，可以传给其他函数。而其他函数会在满足某个条件或发生某个（异步）事件时调用（“回调”）这个函数。回调函数被调用，相当于通知你满足了某个条件或发生了某个事件，有时这个调用还会包含函数参数，能够提供更多细节。通过具体的示例会更容易理解这些，接下来的几个小节将演示几种不同形式的基于回调的异步编程，包括客户端JavaScript和Node。



##### 1.1 定时器
一种最简单的异步操作就是在一定时间过后运行某些代码。

```javascript
setTimeout(function() { console.log("定时器") }, 1000);
```



##### 1.2 事件
客户端JavaScript编程几乎全都是事件驱动的。也就是说，不是运行某些预定义的计算，而是等待用户做一些事，然后响应用户的动作。用户在按下键盘按键、移动鼠标、单击鼠标或轻点触摸屏设备时，浏览器会生成事件。事件驱动的`JavaScript`程序在特定上下文中为特定类型的事件注册回调函数，而浏览器在指定的事件发生时调用这些函数。

```javascript
// 要求浏览器返回一个对象, 表示与下面的
// CSS选择符匹配的 HTML <botton> 元素
let okay = document.querySelector('#confirmUpdateDialog botton.okay');

// 接下来注册一个回调函数, 当用户单击该按钮时会被调用
okay.addEventListener('click', applyUpdate);
```



##### 1.3 网络事件
JavaScript编程中另一个常见的异步操作来源是网络请求。浏览器中运行的JavaScript可以通过类似下面的代码从Web服务器获取数据：

```javascript
function getCurrentVersionNumber(versionCallback) {
  // 通过脚本向后端版本API发送一个HTTP请求
  let request = new XMLHttpRequest();
  request.open("GET", "http://www.example.com/api/version");
  request.send();

  // 注册一个将在响应到达时调用的回调
  request.onload = function() {
    if (request.status === 200) {
      // 如果HTTP状态码没问题, 则取得版本号并调用回调
      let currentVersion = parseFloat(request.responseText);
      versionCallback(null, currentVersion);
    } else {
      // 否则, 通过回调报告错误
      versionCallback(response.statusText, null);
    }
  };

  request.onerror = request.ontimeout = function(e) {
    versionCallback(e.type, null):
  }
}
```



##### 1.4 Node中的回调与事件
Node.js服务器端JavaScript环境底层就是异步的，定义了很多使用回调和事件的API。例如，读取文件内容的默认API就是异步的，会在读取文件内容后调用一个回调函数：

```javascript
const fs = require("fs");
let options = {};

// 读取配置文件, 然后调用回调函数
fs.readFile("config.json", "utf-8", (err, text) => {
  if (err) {
    console.warn("Could not read config file:", err);
  } else {
  	// 否则, 解析文件内容并赋值给选项对象
    Object.assign(options, JSON.parse(text));
  }

  // 无论是什么情况, 都会启动运行程序
  startProgram(options);
})


```

	

Node也定义一些基于事件的API。下面这个函数展示了在Node中如何通过HTTP请求获取URL的内容。它包含两层处理事件监听器的异步代码。注意，Node使用on()方法而非addEventListener()注册事件监听器：

```javascript
const https = require("https");

// 读取URL的文本内容, 将其异步传给回调
function getText(url, callback) {
  // 对URL发送一个HTTP GET请求
  request = https.get(url);

  // 注册一个函数处理 response 事件
	request.on("response", response => {
    // 这个响应事件意味着收到了响应头
    let httpStatus = response.statusCode;

    // 此时并没有收到HTTP响应体
    // 因此还要再注册几个事件处理程序, 以便收到响应体时被调用
    response.setEncoding("utf-8");
    let body = "";

    // 每个响应体块就绪时都会调用这个事件处理程序
    response.on("data", chunk => { body += chunk; });

    // 响应完成时会调用这个事件处理程序
    response.on("end", () => {
      if (httpStatus === 200) {
        callback(null, body);
      } else {
        callback(httpStatus, null);
      }
    });
  })

// 这里也为底层网络错误注册了一个事件处理程序
  request.on("error", (err) => {
    callback(err, null);
  });
}
```



#### 二、Promise
##### 2.1 使用Promise
```javascript
getJSON(url).then(jsonData => {
  // 这是一个回调函数, 它会在解析得到JSON值之后被异步调用, 并接受该JSON值作为参数
})

function displayUserProfile(profile) {};

getJSON("/api/user/profile").then(displayUserProfile);

// 使用promise处理错误
getJSON("/api/user/profile").then(displayUserProfile, handleProfileError);

// 更符合传统的错误处理方法
getJSON("/api/user/profile").then(displayUserProfile).catch(handleProfileError);
```



##### 2.2 期约链
Promise有一个最重要的优点，就是以线性`then()`方法调用链的形式表达一连串异步操作，而无须把每个操作嵌套在前一个操作的回调内部。

```javascript
fetch("/api/user/profile").then(response => {
	response.json().then(profile => {
    displayUserProfile(profile);
  })
})
```



说这是使用Promise的幼稚方式，是因为我们像嵌套回调一样嵌套了它们，而这违背了Promise的初衷。使用Promise的首选方式是像以下代码这样写成一串Promise链：

```javascript
fetch("/api/user/profile")
  .then(response => {
  	return response.json();
	})
	.then(profile => {
    displayUserProfile(profile);
  })
```



像这样在一个表达式中调用多个方法，我们称其为方法链。我们知道，`fetch()`函数返回一个Promise对象，而这个链上的第一个`.then()`调用了返回的Promise对象上的一个方法。不过链中还有第二个`.then()`，这意味着第一个`then()`方法调用本身必须返回一个期约。



##### 2.3 解决Promise
下面我们再重写一次抓取URL的代码，这一次使用冗余和非惯用方法，以便回调和Promise更加明显：

```javascript
function c1(response) {
  let p4 = response.json();
  return p4;
}

function c2(profile) {
  displayUserProfile(profile);
}

let p1 = fetch("/api/user/profile");
let p2 = p1.then(c1);
let p3 = p2.then(c2);
```



##### 2.4 再谈Promise 和 错误
期约的`.catch()`方法实际上是对以`null`为第一个参数、以错误处理回调为第二个参数的`.then()`调用的简写。对于任何Promise`p`和错误回调`c`，以下两行代码是等价的：

```javascript
p.then(null, c);
p.catch(c);
```

	之所以应该首选`.catch()`简写形式，一方面是因为它更简单，另一方面是因为它的名字对应`try/catch`异常处理语句的`catch`子句。



在ES2018中，期约对象还定义了一个`.finally()`方法，其用途类似`try/catch/finally`语句的`finally`子句。如果你在期约链中添加一个`.finally()`调用，那么传给`.finally()`的回调会在期约落定 时被调用。无论这个期约是兑现还是被拒绝，你的回调都会被调用，而且调用时不会给它传任何参数，因此你也无法知晓期约是兑现了还是被拒绝了。

但假如你需要在任何情况下都运行一些清理代码（如关闭打开的文件或网络连接），那么`.finally()`回调是做这件事的理想方式。

与`.then()`和`.catch()`一样，`.finally()`也返回一 个新Promise对象。但`.finally()`回调的返回值通常会被忽略，而解决或拒绝调用`finally()`的Promise的值一般也会用来解决或拒绝`.finally()`返回的Promise。不过，如果`.finally()`回调抛出异常，就会用这个错误值拒绝`.finally()`返回的Promise。

```javascript
fetch("/api/user/profile")
	.then(response => {
    if (!response.of) { // 如果遇到404 Not Found获类似的错误
      return null;
    }

  	// 检查头部以确保服务器发送给我们的是JSON
		// 如果不是, 说明服务器坏了, 这是一个严重错误
    let type = response.headers.get("content-Type");
    if (type !== "application/json") {
      throw new TypeError(`Expected JSON, got ${type}`);
    }

    // 如果到这里说明状态码是2xx, 内容类型也是JSON
  	return response.json();
  })
	.then(profile => { // 调用时传入解析后的响应体或null
    if (profile) {
      displayUserProfile(profile);
    } else {
      // 如果遇到了404错误并返回null
      displayLoggedOutProfilePage();
    }
  })
	.catch(e => {
    if (e instanceof NetworkError) {
      // fetch()在互联网链接故障时
      displayErrorMessage("Check your internet connection.");
    } else if (e instanceof TypeError) {
      // 在上面抛出TypeError时
      diaplayErrorMessage("Something is wrong with our sercer!");
    } else {
      // 发生了意料之外的错误
      console.error(e);
    }
  })
```

	

+ 传给`.catch()`的回调只会在上一环的回调抛出错误时才会被调用。
+ 如果该回调正常返回，那么这个`.catch()`回调就会被跳过，之前回调返回的值会成为下一个`.then()`回调的输入。
+ `.catch()`回调不仅仅可以用于报告错误，还可以处理错误并从错误中恢复。一个错误只要传给了`.catch()`回调，就会停止在Promise链中向下传播。`.catch()`回调可以抛出新错误，但如果正常返回， 那这个返回值就会用于解决或兑现与之关联的Promise，从而停止错误传播。



现在假设瞬间网络负载问题会导致这个查询有1%的失败概率。一个简单的解决方案是通过`.catch()`调用来重新发送请求：

```javascript
queryDatabase()
	.catch(e => wait(500).then(queryDatabase)) // 如果失败, 等待并重试
	.then(displayTable)
	.catch(displayDatabaseError);
```

	如果我们假想的失败真是随机的，那么加上这行代码应该可以把错误率从1%降到0.01%。



在Promise链中，一个环节返回（或抛出）的值会成为下一个环节的输入。因此每个环节返回什么至关重要。

```javascript
.catch(e => wait(500).then(queryDatabase));

.catch(e => { wait(500).then(queryDatabase) });
```

箭头函数加上了大括号, 就无返回值。现在这个函数返回的是undefined, 而非Promise。这意味着Promise下一环节的回调会接受到undefined参数，而不是重试查询的结果。



##### 2.5 并行Promise
我们已经花了很多时间讨论Promise链，但主要针对的是顺序运行一个较大异步操作的多个异步环节。然而有时候，我们希望并行执行多个异步操作。函数`Promise.all()`可以做到这一点。

`Promise.all()`接收一个Promise对象的数组作为输入，返回一个期约。如果输入Promise中的任意一个拒绝，返回的Promise也将拒绝；否则，返回的Promise会以每个输入Promise返回值的数组返回。

```javascript
// 先定义一个URL数组
const urls = [/* 0或多个URL */];
// 将他转换为一个Promise对象的数组
promises = urls.map(url => fetch(url).then(r => r.text()));
Promise.all(promises)
	.then(bodies => {/* 处理得到的字符串数组 */})
	.catch(e => console.error(e));
```



`Promise.all()`实际上比刚才描述的稍微更灵活一些。其输入数组可以包含Promise对象和非Promise值。如果这个数组的某个元素不是Promise，那么它就会被当成一个已兑现Promise的值，被原封不动地复制到输出数组中。

由`Promise.all()`返回的Promise会在任何一个输入Promise被拒绝时拒绝。这会在第一个拒绝发生时立即发生，此时其他Promise的状态可能还是待定。

与`Promise.all()`一样。但是，`Promise.allSettled()`永远不拒绝返回的Promise，而是会等所有输入Promise全部落定后兑现。这个返回的Promise解决为一个对象数组，其中每个对象都对应一个输入Promise，且都有一个`status`属性，值为`fulfilled`或`rejected`。如果status属性值为`fulfilled`，那么该对象还会有一个`value`属性，包含兑现的值。而如果`status`属性值为`rejected`，那么该对象还会有一个`reason`属性，包含对应Promise的错误或拒绝理由：

```javascript
Promise.allSettled([Promise.resolve(1), Promise.reject(2), 3]).then(results => {
  results[0]; // { status: "fulfilled", value: 1 }
  results[1]; // { status: "rejected", reason: 2 }
  results[2]; // { status: "fulfilled", value: 3 }
})
```

	

你可能偶尔想同时运行多个Promise，但只关心第一个兑现的值。此时，可以使用`Promise.race()`而不是`Promise.all()`。`Promise.race()`返回一个Promise，这个Promise会在输入数组中的Promise有一个兑现或拒绝时马上兑现或拒绝（或者，如果输入数组中有非Promise值，则直接返回其中第一个非Promise值）。



##### 2.6 创建Promise
+ 基于其他Promise的Promise

如果有其他返回Promise的函数，那么基于这个函数写一个返回Promise的函数很容易。给定一个Promise，调用`.then()`就可以创建（并返回）一个新Promise。因此，如果以已有的`fetch()`函数为起点，可以像下面这样实现getJSON()：

```javascript
function getJSON(url) {
  return fetch(url).then(response => response.json());
}
```



+ 基于同步值的Promise

有时候，我们可能需要实现一个已有的基于Promise的API，并从一个函数返回Promise，尽管要执行的计算实际上并不涉及异步操作。在这种情况下，静态方法`Promise.resolve()`和`Promise.reject()`可以帮你达成目的。

`Promise.resolve()`接收一个值作为参数，并返回一个会立即（但异步）以该值兑现的Promise。

类似地，`Promise.reject()`也接收一个参数，并返回一个以该参数作为理由拒绝的Promise（明确一下：这两个静态方法返回的Promise在被返回时并未兑现或拒绝，但它们会在当前同步代码块运行结束后立即兑现或拒绝。通常，这会在几毫秒之后发生，除非有很多待定的异步任务待运行）。

写一个基于Promise的函数，其中值是同步计算得到的，但使用`Promise.resolve()`异步返回是可能的，但不常见。不过在一个异步函数中包含同步执行的代码，通过`Promise.resolve()`和`Promise.reject()`来处理这些同步操作的值倒是相当常见。特别地，如果在开始异步操作前检测错误条件（如坏参数值），那可以通过返回`Promise.reject()`创建的Promise来报告该错误（这种情况下也可以同步抛出一个错误，但这种做法并不推荐，因为这样一来，函数的调用者为了处理错误既要写同步的`catch`子句，还要使用异步的`.catch()`方法）。最后，`Promise.resolve()`有时候也可以用来创建一个Promise链的第一个期约。



+ 从头开始创建Promise

使用`Promise()`构造函数来创建一个新Promise对象，而且可以完全控制这个新Promise。

```javascript
function wait(duration) {
  // 创建并返回新Promise
  return new Promise((resolve, reject) => {
    if (duration < 0) {
      reject(new Error("Time travel not yet implemented"));
    }

    setTimeout(resolve, duration);
  });
}
```

	注意，用来控制`Promise()`构造函数创建的Promise命运的那对函数叫`resolve()`和`reject()`，不是`fulfill()`和`reject()`。如果把一个Promise传给`resolve()`，返回的Promise将会解决为该新Promise。不过，通常在这里都会传一个非Promise值，这个值会兑现返回的Promise。



```javascript
const http = require("http");

function getJSON(url) {
  // 创建并返回一个Promise
  return new Promise((resolve, reject) => {
    request = http.get(url, response => {
      if (response.statusCode !== 200) {
        reject(new Error(`HTTP status ${response.statusCode}`));
        response.resume(); // 这样不会导致内存泄漏
      } else if (response.headers["content-type"] !== "application/json") {
        reject(new Error("Invalid content-type"));
        response.resume(); // 不会造成内存泄漏
      } else {
        let body = "";
        response.setEncoding("utf-8");
        response.on("data", chunk => { body += chunk; });
        response.on("end", () => {
          try {
            let parsed = JSON.parse(body);
            resolve(parsed);
          } catch(e) {
            reject(e);
          }
        });
      }
    });

    request.on("error", error => {
      reject(error);
    })
  })
}
```



##### 2.7 串行Promise
```javascript
function fetchSequentially(urls) {
  // 抓取URL时, 要把响应体保存在这里
  const bodies = [];

  // 这个函数返回一个Promise, 它只抓取一个URL响应体
  function fetchOne(url) {
    return fetch(url)
            .then(response => response.text())
            .then(body => {
              bodies.push(body);
            });
  }

  // 从一个立即(以undefined值)兑现的Promise开始
  let p = Promise.resolve(undefined);

  // 现在循环目标URL, 构建任意长度的Promise链
  for (url of urls) {
    p = p.then(() => fetchOne(url));
  }

  // Promise链的最后一个Promise兑现后, 响应体数组(bodies)
  // 也已经就绪。因此, 可以将这个bodies数组通过Promise返回
  return p.then(() => bodies);
}
```

有了这个`fetchSequentially()`函数定义，就可以像使用前面演示的`Promise.all()`并行抓取一样，按顺序依次抓取每个URL：

```javascript
fetchSequentially(urls)
	.then(bodies => { /* 处理抓到的字符串数组 */ })
	.catch(e => console.error(e));
```

	

还有一种（可能更简练）的实现方式。不是事先创建Promise，而是让每个Promise的回调创建并返回下一个期Promise。换句话说，不是创建并连缀一串Promise，而是创建解决为其他Promise的Promise。这种方式创建 的就不是多米诺骨牌形式的Promise链了，而是像俄罗斯套娃那样一系列相互嵌套的Promise。

```javascript
// 这个函数接受一个输入值数组和一个promiseMaker函数
// 对输入数组中的任何值, promiseMaker(x)都应该返回
// 一个兑现为输出值的promise。这个函数返回一个promise,
// 该promise最终会兑现为一个包含计算得到的输出值的数组

// promiseSequence()不是一次创建所有promise然后让它们并行运行,
// 而是每次只运行一个promise,直到上一个promise兑现之后,
// 才会调用promiseMaker()计算下一个值
function promiseSequence(inputs, promiseMaker) {
  // 为数组创建一个可以修改的私有副本
  inputs = [...inputs];

  function handleNextInput(outputs) {
    // 如果没有输入值, 则返回输出值的数组
    if (inputs.length === 0) {
      return outputs;
    } else {
      // 如果还有要处理的输入值, 那会返回一个Promise对象
      // 将当前的Promise解决为一个来自新Promise的未来值
      let nextInput = inputs.shift(); // 取得下一个输入值
      return promiseMaker(nextInput); // 计算下一个输出值
      				// 然后用这个新输出值创建一个新输出值的数组
              .then(output => output.concat(output))
              // 然后递归, 传入新的输出值数组
              .then(handleNextInput);
    }
  }

  return Promise.resolve([]).then(handleNextInput);
}

// 传入一个URL, 返回一个以该URL的响应体文本对象的Promise
function fetchBody(url) { return fetch(url).then(r => r.text(); }

// 使用它依次抓取一批URL的响应体
promiseSequence(urls, fetchBody)
	.then(bodies => { /* 处理字符串数组 */ } 
  .catch(e => console.error(e));
```



#### 三、async 和 await
##### 3.1 await 表达式
await关键字接收一个Promise并将其转换为一个返回值或一个抛出的异常。给定一个Promise p，表达式`await p`会一直等到p落定。如果p兑现，那么`await p`的值就是兑现p的值。如果p被拒绝，那么`await p`表达式就会抛出拒绝p的值。我们通常并不会使用await来接收一个保存期约的变量，更多的是把它放在一个会返回期约的函数调用前面：

```javascript
let response = await fetch("/api/user/profile");
let profile = await response.json();
```

	这里的关键是要明白，await关键字并不会导致你的程序阻塞或者在指定的Promise落定前什么都不做。你的代码仍然是异步的，而await只是掩盖了这个事实。这意味着任何使用await的代码本身都是异步的。



##### 3.2 async 函数
因为任何使用await的代码都是异步的，所以有一条重要的规则：只能在以async关键字声明的函数内部使用await关键字。以下是使用async和await将本章前面的getHighScore()函数重写之后的样子：

```javascript
async function getHeightScore() {
  let response = await fetch("/api/user/profile");
  let profile = await response.json();
  return profile.highScope;
}
```

	把函数声明为async意味着该函数的返回值将是一个Promise，即便函数体中不出现Promise相关的代码。如果async函数会正常返回，那么作为该函数真正返回值的Promise对象将解决为这个明显的返回值。如果async函数会抛出异常，那么它返回的Promise对象将以该异常被拒绝。

这个getHighScore()函数前面加了async，因此它会返回一个Promise。由于它返回Promise，所以我们可以对它使用await关键字：

```javascript
displayHighScore(await getHighScore());
```



不过要记住，这行代码只有在它位于另一个async函数内部时才能运行！你可以在async函数中嵌套await表达式，多深都没关系。但如果是在顶级或因为某种原因在一个非async函数内部，那么就不能使用await关键字，而是必须以常规方式来处理返回的期约：

```javascript
getHighScore().then(displayHighScore).catch(e => console.error(e));
```



##### 3.3 等候多个Promise
假设我们使用async写重写了getJSON()函数:

```javascript
async function getJSON(url) {
  let response = await fetch(url);
  let body = await response.json();
  return body;
}
```

	再假设我们想使用这个函数抓取两个JSON值：

```javascript
let value1 = await getJSON(url1); 
let value2 = await getJSON(url2); 
```

	

以上代码的问题在于它不必顺序执行。这样写就意味着必须等到抓取第一个URL的结果之后才会开始抓取第二个URL的值。如果第二个URL并不依赖从第一个URL抓取的值，那么应该可以尝试同时抓取两个值。这个示例显示了async函数本质上是基于Promise的。要等候一组并发执行的async函数，可以像使用Promise一样直接使用 `Promise.all()`：

```javascript
let [value1, value2] = await Promise.all([getJSON(url1), getJSON(url2)]);
```



##### 3.4 实现细节
假设你写了一个这样的async函数：

```javascript
async function f(x) { /* 函数体 */ }
```



可以把这个函数想象成一个返回期约的包装函数，它包装了你原始函数的函数体:

```javascript
function f(x) {
  return new Promise(function(resolve, reject) => {
    try {
      resolve((function(x) { /* 函数体 */ })(x));
    } catch (e) {
      reject(e);
    }
  })
}
```

	

像这样以语法转换的形式解释await关键字比较困难。但可以把await关键字想象成分隔代码体的记号，它们把函数体分隔成相对独立的同步代码块。ES2017解释器可以把函数体分割成一系列独立的子函数，每个子函数都将被传给位于它前面的以await标记的那个Promise的then()方法。



#### 四、异步迭代
##### 4.1 for/await 循环
Node 12的可读流实现了异步可迭代。这意味着可以像下面这样使用`for/await`循环从一个流中读取连续的数据块：

```javascript
const fs = require("fs");

async function parseFile(filename) {
  let stream = fs.createReadStream(filename, { encoding: "utf-8" });
  for await (let chunk of stream) {
    parseChunk(chunk);
  }
}
```

	

与常规的await表达式类似，`for/await`循环也是基于Promise的。 大体上说，这里的异步迭代器会产生一个Promise，而`for/await`循环等待该Promise兑现，将兑现值赋给循环变量，然后再运行循环体。之后再从头开始，从迭代器取得另一个Promise并等待这个新Promise兑现。



我们可以使用`Promise.all()`来等待数组中的所有Promise兑现。但假设我们希望第一次抓取的结果尽快可用，不想因此而等待抓取其他URL（当然，也许第一次抓取的时间是最长的，因此这样不一定比使用`Promise.all()`更快）。数组是可迭代的，因此我们可以使用常规的`for/of`循环来迭代这个Promise数组：

```javascript
for (const promise of promises) {
  response = await promise;
  handle(response);
}
```

	

这个示例代码使用了常规的`for/of`循环和一个常规迭代器。但由于这个迭代器返回Promise，所以我们也可以使用新的`for/await`循环让代码更简单：

```javascript
for await (const response of promises) {
  handle(response);
}
```

	

这里的`for/await`循环只是把`await`调用内置在循环中，从而让代码稍微简洁了一点。但这两个示例做的事情是一样的。关键在于，这两个示例都只能在以async声明的函数内部才能使用。从这方面来说，`for/await`循环与常规的`await`表达式没什么不同。 不过，最重要的是应该知道，在这个示例中我们是对一个常规的迭代器使用了`for/await`。如果是完全异步的迭代器，那么还会更有意思。



##### 4.2 异步迭代器
可迭代对象是可以在`for/of`循环中使用的对象。它以一个符号名字`Symbol.iterator`定义了一个方法，该方法返回一个迭代器对象。这个迭代器对象有一个`next()`方法，可以反复调用它获取可迭代对象的值。迭代器对象的这个`next()`方法返回迭代结果对象。迭代结果对象有一个value属性或一个done属性。

异步迭代器与常规迭代器非常相似，但有两个重要区别。第一，异步可迭代对象以符号名字`Symbol.asyncIterator`而非`Symbol.iterator`实现了一个方法（如前所示，`for/await`与常规迭代器兼容，但它更适合异步可迭代对象，因此会在尝试`Symbol.iterator`法前先尝试`Symbol.asyncIterator`方法）。第二，异步迭代器的`next()`方法返回一个Promise，解决为一个迭代器结果对象，而不是直接返回一个迭代器结果对象。

当我们对一个常规同步可迭代的Promise数组使用`for/await`时，操作的是同步迭代器结果对象。其中，value属性是一个Promise对象，但done属性是一个同步值。真正的异步迭代器返回的是迭代结果对象的Promise，其中value和done都是异步值。两者的区别很微妙：对于异步迭代器，关于迭代何时结束的选择可以异步实现。



##### 4.3 异步生成器
实现迭代器的最简单方式通常是使用生成器。同理，对于异步迭代器也是如此，我们可以使用声明为async的生成器函数来实现它。声明为async的异步生成器同时具有异步函数和生成器的特性，即可以像在常规异步函数中一样使用await，也可以像在常规生成器中一样使用yield。但通过yield生成的值会自动包装到Promise中。就连异步生成器的语法也是`async function`和`function *`的组合：`async function *`。下面这个示例展示了使用异步生成器和`for/await`循环，通过循环代码而非`setInterval()`回调函数实现以固定的时间间隔重复运行代码：

```javascript
// 一个基于Promise的包装函数, 包装setTimeout()以实现等待
// 返回一个Promise, 这个Promise会在指定的毫秒数之后兑现
function elapsedTime(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 一个异步迭代器函数, 按照固定的时间间隔
// 度增并生成指定(或无穷)个数的计数器
async function* clock(interval, max = Infinity) {
  for (let count = 1; count <= max; count++) {
    await elapsedTime(interval);
    yield count;
  }
}

// 一个测试函数, 使用异步迭代器和for/await
async function test() {
  for await (let tick of clock(300, 100)) { // 循环100次, 每次间隔300ms
    console.log(tick);
  }
}
```



##### 4.4 实现异步迭代器
除了使用异步生成器实现异步迭代器，还可以直接实现异步迭代器。这需要定义一个包含`Symbol.asyncIterator()`方法的对象，该方法要返回一个包含`next()`方法的对象，而这个`next()`方法要返回解决为一个迭代器结果对象的期约。在下面的代码中，我们重新实现了前面示例中的`clock()`函数。但它在这里并不是一个生成器，只是会返回一个异步可迭代对象。注意这个示例中的`next()`方法，它并没有显式返回Promise，我们只是把它声明为了async next()：

```javascript
function clock(interval, max = Infinity) {
  // 一个setTimeout的Promise版, 可以实现等待
  // 注意参数是一个绝对时间而非时间间隔
  function until(time) {
    return new Promise(resolve => setTimeout(resolve, time - Date.now()));
  }

  // 返回一个异步可迭代对象
  return {
    startTime: Date.now(), // 记住开始时间
    count: 1, // 记住第几次迭代
    async next() { // 方法使其成为迭代器
      if (this.count > max) {
        // 表示结束的迭代结果
        return { done: true };
      }
      // 计算下次迭代什么时间开始
      let targetTime = this.startTime + this.count * interval;
    	// 等待该时间到来
      await until(targetTime);
			// 在迭代结果对象中返回计数器的值
      return { value: this.count++ };
    },
    // 这个方法意味着这个迭代器对象同时也是一个可迭代对象
    [Symbol.asyncIterator]() { return this; }
  }
}
```

	

这个基于迭代器的clock()函数修复了基于生成器版本的一个缺陷。注意，在这个更新的代码中，我们使用的是每次迭代应该开始的绝对时间减去当前时间，得到要传给setTimeout()的时间间隔。如果在for/await循环中使用clock()，这个版本会更精确地按照指定的时间间隔运行循环迭代。因为这个时间间隔包含了循环体运行的时间。不过这个修复并不仅仅与计时精度有关。for/await循环在开始下一次迭代之前，总会等待一次迭代返回的Promise兑现。但如果不是在for/await循环中使用异步迭代器，那你可以在任何时候调用next()方法。对于基于生成器的clock()版本，如果你连续调用3次next()方法，就可以得到3个Promise，而这3个Promise将几乎同时兑现， 而这可能并非你想要的。在这里实现的这个基于迭代器的版本则没有这个问题。

异步迭代器的优点的是它允许我们表示异步事件流或数据流。前面讨论的clock()函数写起来相当简单，因为其中的异步性源于由我们决定的setTimeout()调用。但是，在面对其他异步源时，比如事件处理程序的触发，要实现异步迭代器就会困难很多。因为通常我们只有一个事件处理程序响应事件，但每次调用迭代器的next()方法都必须返回一个独一无二的期约对象，而在第一个Promise解决之前很有可能出现多次调用next()的情况。这意味着任何异步迭代器方法都必须能在内部维护一个Promise队列，让这些Promise按照异步事件发生的顺序依次解决。如果把这个Promise队列的逻辑封装到一个AsyncQueue类中，再基于这个类编写异步迭代器就会简单多了。



```javascript
/* 
	一个异步可迭代队列类, 使用enqueue()添加值
  使用dequeue()移除值, dequeue()返回一个Promise
  这意味着, 值可以在入队之前出队, 这个类实现了
  [Symbol.asyncIterator]和next(), 因而可以
  与for/await循环一起配合使用(这个循环在调用close()方法前不会终止)
*/
class AsyncQueue {
  constrcutor() {
    // 已经入队尚未出队的值保存在这里
    this.value = [];
    // 如果Promise出队时它们对应的值尚未入队
    // 就把那些Promise的解决方法保存在这里
    this.resolvers = [];
    // 一旦关闭, 任何值都不会再入队, 也不会再返回任何未兑现的Promise
    this.closed = false;
  }

  enqueue(value) {
    if (this.closed) {
      throw new Error("Async closed");
    }
    if (this.resolvers.length > 0) {
      // 如果这个值已经有对应的Promise, 则解决该Promise
      const resolve = this.resolvers.shift();
      resolve(value);
    } else {
    	// 否则排队
      this.values.push(value);
    }
  }

  dequeue() {
    if (this.values.length > 0) {
    	// 如果有一个排队的值, 为它返回一个解决Promise
      const value = this.values.shift();
      return Promise.resolve(value);
    } else if (this.closed) {
      // 如果没有排队的值, 而且队列已经关闭
      // 返回一个解决为EQS(流终止)标记的Promise
      return Promise.resolve(AsyncQueue.EQS);
    } else {
      // 否则返回一个未解决的Promise
      // 将解决方法排队, 以便后面使用
      return new Promise((resolve) => { this.resolvers.push(resolve); });
    }
  }

  close() {
    // 一旦关闭, 任何值都不能再入队
    // 因此以EQS标记解决所有待决Promise
    while (this.resolvers.length > 0) {
      this.resolvers.shift()(AsyncQueue.EQS);
    }
    this.closed = true;
  }

  // 定义这个方法, 让这个类成为异步可迭代对象
  [Symbol.asyncIterator]() { return this; }

  // 定义这个方法, 让这个类成为异步迭代器
  // dequeue()返回的Promise会解决为一个值
  // 或者在关闭时解决为EQS标记。这里, 我们需要返回一个解决为迭代器结果对象的Promise
  next() {
    return this.dequeue().then(value => (value === AsyncQueue.EQS)
                                ? { value: undefined, done: true }
                                : { value: value, done: false }
  }
}

// dequeue()方法返回的标记, 在关闭时表示"流终止"
AsyncQueue.EQS = Symbol("end-of-stream");
```

	

因为这个AsyncQueue类定义了异步迭代的基础，所以我们可以创建更有意思的异步迭代器，只要简单地对值异步排队即可。下面这个示例使用AsyncQueue产生了一个浏览器事件流，可以通过for/await循环来处理：

```javascript
// 把指定文档元素上指定类型的事件推入一个AsyncQueue对象,
// 然后返回这个队列, 以便将其作为事件流来使用
function eventStream(elt, type) {
  const q = new AsyncQueue(); // 创建一个队列
  elt.addEventListener(type, e => q.enqueue(e)); // 入队事件
  return q;
}

async function handleKeys() {
  // 取得一个keypress事件流, 对每个事件都要执行一次循环
  for await (const event of eventStream(document, "keypress")) {
    console.log(event.key);
  }
}
```

