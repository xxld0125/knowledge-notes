Node是JavaScript与底层操作系统绑定的结合，因而可以让JavaScript程序读写文件、执行子进程，以及实现网络通信。为此，Node得到了广泛应用：

+ 首先是替代命令行脚本，因为它没有bash及其他Unix终端那样神秘的语法；
+ 其次是作为运行受信程序的通用编程语言，没有浏览器那种运行不受信代码带来的安全限制；
+ 最后它也是编写高效、高并发Web服务器的流行环境。



Node的典型特点是由其默认异步的API赋能的单线程基于事件的并发能力。



#### 一、Node编程基础
##### 1.1 控制台输出
如果你习惯于为浏览器编写JavaScript代码，那么切换到Node编程时，要知道`console.log()`不仅可以用于调试，也是Node向用户显示消息的最简单方式，或者更宽泛地讲，是向标准输出流（stdout）发送输出的一种主要方式。

在浏览器中，`console.log()`、`console.warn()`和`console.error()`通常会在控制台中输出内容的前面显示一个小图标，表示不同类型的日志消息。

Node不会显示图标，但`console.error()`显示的输出与`console.log()`显示的输出仍然有区别，因为`console.error()`写入的是标准错误流（stderr）。如果你写的Node程序要把标准输出重定向到一个文件或管道，可以使用`console.error()`在控制台显示用户可以看到的文本，而`console.log()`打印的文本是不可见的。



##### 1.2 命令行参数和环境变量
Node遵循了这些Unix惯例，Unix风格的程序的输入首先是从命令行参数获取，其次是从环境变量中获取的。Node程序可以从字符串数组`process.argv`中读取其命令行参数。这个数组的第一个元素始终是Node可执行文件的路径。第二个参数是Node执行的JavaScript代码文件的路径。数组中剩下的所有元素都是你在调用Node时，通过命令行传给它的空格分隔的参数。



执行这个程序并看到类似下面的输出：

```javascript
$ node --trace-uncaught argv.js --arg1 --arg2 filename
[
  '/usr/local/bin/node',
  '/private/tmp/argv.js',
  '--arg1',
  '--arg2',
  'filename'
]
```



+ `process.argv`的第一和第二个元素是Node可执行文件和被执行JavaScript文件的完全限定的文件系统路径，无论你是否这样输入它们。
+ 有意提供给Node可执行文件且由它解释的命令行参数会被Node可执行文件使用，不会出现在process.argv中（前面例子中的命令行参数`--trace-uncaught`实际上没什么用，这里只是用来演示它不会出现在输出中）。出现在JavaScript文件名之后的任何参数（如`--arg1`和`filename`）都会出现在`process.argv`中。



Node程序也会从Unix风格的环境变量中获取输入。Node把这些变量保存在`process.env`对象中使用。这个对象的属性名是环境变量的属性名，而属性值（始终是字符串）是对应变量的值。



##### 1.3 程序生命期
Node程序通常是异步的，并且基于回调和事件处理程序。Node程序在运行完初始文件、调用完所有回调、不再有未决事件之前不会退出。基于Node的服务器程序监听到来的网络连接，理论上会永远运行，因为它始终要等待下一个事件。

程序通过调用`process.exit()`可以强制自己退出。用户通常需 在终端窗口中按`Ctrl + C`来终止运行中的Node程序。程序通过使用`process.on("SIGINT", ()=>{})`注册信号处理函数可以忽略`Ctrl + C`。

如果程序中的代码抛出异常，也没有catch子句捕获该异常，程序会打印栈追踪信息并退出。由于Node天生异步，发生在回调或事件处理程序中的异常必须局部处理，否则根本得不到处理。这意味着处理异步逻辑中的异常是一件麻烦事。如果你不想让这些异常导致程序崩溃，可以注册一个全局处理程序，以备调用，防止崩溃：

```javascript
process.setUncaughtExceptionCaptureCallback(e => {
  console.error("Uncaught exception:", e);
});
```

类似地，如果你的程序创建的一个Promise被拒绝，而且没有`.catch()`调用处理它，也会遇到这种问题。到Node 13为止，这还不是导致你的程序退出的致命错误，但仍然会在控制台打印出大量错误消息。在Node某个未来的版本中，未处理的promise拒绝有可能变成致命错误。如果你不希望出现未处理的拒绝，或者打印错误消息，甚至终止程序，那就要注册一个全局处理程序：

```javascript
process.on("unhandleRejection", (reason, promise) => {
  // reason是会传给.catch()函数的拒接理由
  // promise是被拒接的promise对象
})
```



##### 1.4 Node模块
JavaScript模块系统，包括Node模块和ES6模块。因为Node是在JavaScript有模块系统之前创造的，所以它必须自己创造一个模块系统。Node的模块系统使用`require()`函数向模块中导入值，使用`exports`对象或`module.exports`属性从模块中导出值。这些都是Node编程模型的基础。

Node 13增加了对标准ES6模块的支持，同时支持基于`require()`的模块（Node称其为“CommonJS模块”）。这两个模块系统并非完全兼容，因此两者并存有些棘手。Node在加载模块前，需要知道该模块会使用`require()`和`module.exports`，还是`import`和`export`。Node在把一个JavaScript文件加载为CommonJS模块时，会自动定义`require()`函数以及标识符`exports`和`module`，不会启用`import`和 `export`关键字。另外，在把一个文件加载为ES6模块时，它必须启用`import`和`export`声明，同时必须不定义`require`、`module`和`exports`等额外的标识符。

告诉Node它要加载的是什么模块的最简单方式，就是将信息编码到不同的扩展名中。如果你把JavaScript代码保存在`.mjs`结尾的文件中，那么Node始终会将它作为一个ES6模块来加载，假设其中使用了import和export，并且不提供`require()`函数。如果把代码保存在`.cjs`结尾的文件中，那么Node始终会将它作为一个CommonJS模块来对待，会提供`require()`函数，而如果其中使用了`import`或`export`声明，则会抛出SyntaxError。

对于没有明确给出`mjs`或`cjs`扩展名的文件，Node会在同级目录及所有包含目录中查找一个名为`package.json`的文件。一旦找到最近的`package.json`文件，Node会检查其中JSON对象的顶级`type`属性。如果这个type属性的值是`module`，Node将该文件按ES6模块来加载。如果这个属性的值是`commonjs`，那么Node就按CommonJS模块来加载该文件。注意，运行Node程序并不需要有`package.json`文件。 如果没有找到这个文件（或找到该文件但它没有type属性），Node默认会使用`CommonJS`模块。这个`package.json`的招术只有你想在Node中使用ES6模块，但又不希望使用`.mjs`扩展名时才是必需的。

因为大量现有的Node代码使用的都是CommonJS模块格式，Node允许ES6模块使用`import`关键字加载CommonJS模块。但反之则不可以：CommonJS模块不能使用`require()`加载ES6模块。



##### 1.5 Node包管理器
你在安装Node的同时，也会得到一个名为npm的程序。这个程序就是Node的包管理器，它可以帮你下载和管理程序的依赖库。npm通过位于程序根目录下的`package.json`文件跟踪依赖（以及与程序相关的其他信息）。这个`package.json`文件是由npm创建的，如果你想在项目中使用ES6模块，需要在其中添加`"type":"module"`。



#### 二、Node默认异步
JavaScript是一门通用的编程语言，因此完全可能用于计算大型矩阵乘法或执行复杂统计分析等占用CPU的程序。然而，Node是针对I/O密集型程序（如网络服务器）进行设计和优化的。特别地，Node的设计让实现高并发（同时处理大量请求的）服务器非常容易。

不过，与很多编程语言不同，Node并不是通过线程来实现并发的。众所周知，多线程程序很难保证不出问题，而且难以调试。另外，线程也是相对较重的抽象，如果你的服务器需要并发处理几百个请求，使用几百个线程可能占用过多内存。为此，Node采用了Web使用的单线程JavaScript编程模型，使得创建网络服务器变得极其简单，只需常规操作，没有神秘可言。



#### 三、缓冲区
Node中有一个比较常用的数据类型就是`Buffer`，常用于从文件或网络读取数据。Buffer类（或称缓冲区）非常类似字符串，只不过它是字节序列而非字符序列。Node是在核心JavaScript支持定型数组之前诞生的，因此没有表示无符号字节的`Uint8Array`。Node的`Buffer`类就是为了满足这个需求而设计的。在JavaScript语言支持`Uint8Array`之后，Node的`Buffer`类就成为`Uint8Array`的子类。

`Buffer`与其超类`Uint8Array`的区别在于，它是设计用来操作`JavaScript`字符串的。因此缓冲区里的字节可以从字符串初始化而来，也可以转换为字符串。字符编码将某个字符集中的每个字符映射为一个整数。只要有字符串和字符编码，就可以将该字符串中的字符编码为字节序列。而只要有（正确编码的）字节序列和字符编码，就可以将这些字节解码为字符串。Node的`Buffer`类有执行编码和解码的方法，这些方法都接收一个encoding参数，用于指定要使用的编码。

Node中的编码是通过名字来指定的（指定为字符串）。以下是支持的编码。

+ utf8

这是不指定编码时的默认值，也是你最可能使用的Unicode编码。

+ utf16le

双字节Unicode字符，使用小端字节序。\uffff以上的码点会编码为双字节序列。"ucs2"是这种编码的别名。

+ latinl

每字符单字节的ISO-8859-1编码，定义了适用于很多西欧语言的字符集。因为latin-1字符与字节是一对一的映射关系，因此这种编码也被称为"binary"。

+ ascii

7比特仅限英文的ASCII编码，是"utf8"编码的严格子集。

+ hex

这种编码把每个字节转换为一对ASCII十六进制数字。

+ base64

这种编码将每3个字节的序列转换为4个ASCII字符的序列。



以下是几个代码示例，展示了如何使用Buffer，以及如何与字符串相互转换：

```javascript
let b = Buffer.from([0x41, 0x42, 0x43]); // <Buffer 41 42 43>
b.toString(); // "ABC": 默认"utf8"
b.toString("hex"); // "414243"

let computer = Buffer.from("IBM3111", "ascii"); // 把字符串转换为缓冲区
for (let i = 0; i < computer.length; i++) { // 把缓冲区作为字节数组
  computer[i]--; // 缓冲区是可修改的
}
computer.toString("ascii"); // "HAL2000"
computer.subarray(0, 3).map(x => x + 1).toString(); // "IBM"

// 使用Buffer.alloc()创建一个空缓存区
let zeros = Buffer.alloc(1024); // 1024个0
let ones = Buffer.alloc(128, 1); // 128个1
let dead = Buffer.alloc(1024, "DEADBEEF", "hex"); //重复字节模式

// 缓冲区有方法可以从或者项缓冲区
// 在任意指定偏移位置读取或写入多字节值
dead.readUInt32BE(0); // 0xDEADBEEF
dead.readUInt32BE(1); // 0xADBEEFDE
dead.readBigUInt64BE(6); // OxBEEFDEADBEEFDEADn
dead.readUInt32LE(1020); // 0xEFBEADDE
```

	如果你的Node程序会操作二进制数据，那么一定会经常使用`Buffer`类。而如果你只是操作与读取或写入文件或网络相关的文本，那么可能只会将`Buffer`作为数据的中间表示。很多Node API都可以接收或返回字符串或Buffer对象的输入或输出。一般来说，如果在使用这些API时，你传递的是字符串，或者期待返回字符串，那么都需要指定要使用的文本编码的名字。而此时，通常根本不会使用Buffer对象。

