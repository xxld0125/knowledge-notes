#### 前言


remote-git-tags包功能:从git远程仓库获取tag.



#### 一、引入模块介绍


```javascript
import {promisify} from 'node:util'; 

import childProcess from 'node:child_process';

const execFile = promisify(childProcess.execFile);
```



##### 1、node:前缀


[nodejs文档](https://nodejs.org/dist/latest-v16.x/docs/api/modules.html)介绍:



_Core modules are always preferentially loaded if their identifier is passed to _`_require()_`_. For instance, _`_require('http')_`_ will always return the built in HTTP module, even if there is a file by that name._



_Core modules can also be identified using the _`_node:_`_ prefix, in which case it bypasses the _`_require_`_ cache. For instance, _`_require('node:http')_`_ will always return the built in HTTP module, even if there is _`_require.cache_`_ entry by that name._



引用node原生库,除require()外,还可以在使用增加node: 前缀的方式.



##### 2、node:util


util是nodejs的一大核心模块，用来提供常用函数的集合;



其中上面用到的promisify方法:



[nodejs文档](http://nodejs.cn/api/util.html#utilpromisifyoriginal)介绍:



_Takes a function following the common error-first callback style, i.e. taking an _`_(err, value) => ..._`_ callback as the last argument, and returns a version that returns promises._



简单来说就是将回调函数的异步处理转化为promise形式.



##### 3.node:child_progress


child_process: 子进程模块



Nodejs 是以单线程的模式运行的，但它使用的是事件驱动来处理并发，这样有助于我们在多核 cpu 的系统上创建多个子进程，从而提高性能



默认情况下，Nodejs 的父进程与衍生的子进程之间会建立 stdin、stdout 和 stderr 的管道。 数据能以非阻塞的方式在管道中流通



Node 提供了 child_process 模块来创建子进程，方法有：



1.  exec:  
`child_process.exec(command[, options][, callback])`  
使用子进程执行命令，缓存子进程的输出，并将子进程的输出以回调函数参数的形式返回。 
2.  execFile:  
`child_process.execFile(command[, options][, callback])`  
child_process.execFile()与child_process.exec()类似,不同之处在于它默认不衍生 shell。 而是，指定的可执行文件 `file` 直接作为新进程衍生，使其比child_process.exec()更有效率 
3.  spawn:  
`child_process.spawn(command[, args][, options])`  
使用指定的命令行参数创建新进程。 
4.  fork:  
`child_process.fork(modulePath[, args][, options])`  
是 spawn()的特殊形式，用于在子进程中运行的模块，如 fork('/haha.js') 相当于 spawn('node', ['/haha.js']) 。与spawn方法不同的是，fork会在父进程与子进程之间，建立一个通信管道，用于进程之间的通信。  
每个函数都返回 ChildProcess 实例。 这些实例实现了 Node.js EventEmitter API，允许父进程注册监听器函数，在子进程生命周期期间，当特定的事件发生时会调用这些函数。 



#### 二、remoteGitTags方法


使用`Node.js`的子进程 `child_process` 模块的`execFile`方法执行 `git ls-remote --tags repoUrl` 获取所有 `tags` 和 `tags` 对应 `hash` 值 存放在 `Map` 对象。



```javascript
export default async function remoteGitTags(repoUrl) {
	const {stdout} = await execFile('git', ['ls-remote', '--tags', repoUrl]);
	const tags = new Map();

	for (const line of stdout.trim().split('\n')) {
		const [hash, tagReference] = line.split('\t');

		// Strip off the indicator of dereferenced tags so we can override the
		// previous entry which points at the tag hash and not the commit hash
		// `refs/tags/v9.6.0^{}` → `v9.6.0`
		const tagName = tagReference.replace(/^refs\/tags\//, '').replace(/\^{}$/, '');

		tags.set(tagName, hash);
	}

	return tags;
}
```



#### 三、promisify


		在上面我们介绍到promisfy方法的作用是将回调函数的异步处理转化为promise形式.



		在学习promisify源码前, 我们先看看如何使用js加载图片







```javascript
const imgSrc = 'https://www.themealdb.com/images/ingredients/Lime.png';


function loadImage(src, cb) {
  	const img = document.createElement('img');
  	img.src = src;
  	img.onload = () => cb(null, img);
  	img.onerror = () => cb(new Error('图片加载失败'));
  	document.body.append(img')
}

loadImage(imgSrc, function (err, content) {
  	if(err) {
      console.log(err);
      return;
    }
  	console.log(content);
})
```



上面的异步处理是使用了回调函数, 接下来我们使用promise进行优化;



```javascript
function loadImagePromise(src) {
  	return new Promise((resolve, reject) => {
      	loadImage(src, function(err, image) {
          	if (err) {
								reject(err);
              	return;
            }
          	resolve(image);
        })
    })
}

loadImagePromise(imgSrc).then(res => {
  	console.log(res);
}).catch(err => {
  	console.log(err);
})
```



上面的方法是根据loadImage方法改造不通用, 接下来将其改造成通用的promise方法;



```javascript
function promisify(original) {
		function fn(...args) {
      	return new Promise((resolve, reject) => {
          	args.push((err, ...values) => {
              	if (err) {
                  	return reject(err);
                }
              	resolve(values);
            })
          	original.apply(this, args);
        })
    }
	  return fn;
}

const loadImagePromise = promisify(loadImage);

async load (src) {
  	try {
    		const res = await loadImagePromise(src);
  	} catch (err) {
      	console.log(err);
    }
}

load(imgSrc);
```



上面的promisify方法与node.utils中promisify方法处理逻辑一致, 此处不再赘述.



#### 四、总结


		通过学习本篇内容, 了解到以下几个知识点:



+ 引入node库时, 可以使用加node前缀的方式引入对应库;
+ 学习node.utils库中promisify方法的作用, 及源码实现;
+ 了解node的child_progress模块及常用方法;
+ 学习remote-git-tags 包作用及其实现原理;



其中重点就是学习promisify的实现, 可使用在日常的项目开发当中.



#### 五、参考文档
[从22行有趣的源码库中，我学到了 callback promisify 化的 Node.js 源码实现](https://juejin.cn/post/7028731182216904740#heading-9)

