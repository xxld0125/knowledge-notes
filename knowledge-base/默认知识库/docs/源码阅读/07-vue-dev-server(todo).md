### 前言


### 一、how it works
以下是`git`中`readme`文档中的介绍

+ <font style="color:rgb(36, 41, 47);">Imports are requested by the browser as native ES module imports - there's no bundling.</font>
+ <font style="color:rgb(36, 41, 47);">The server intercepts requests to</font><font style="color:rgb(36, 41, 47);"> </font><font style="color:rgb(36, 41, 47);">*.vue</font><font style="color:rgb(36, 41, 47);"> </font><font style="color:rgb(36, 41, 47);">files, compiles them on the fly, and sends them back as JavaScript.</font>
+ <font style="color:rgb(36, 41, 47);">For libraries that provide ES modules builds that work in browsers, just directly import them from a CDN.</font>
+ <font style="color:rgb(36, 41, 47);">Imports to npm packages inside </font><font style="color:rgb(36, 41, 47);">.js</font><font style="color:rgb(36, 41, 47);"> files (package name only) are re-written on the fly to point to locally installed files. Currently, only </font><font style="color:rgb(36, 41, 47);">vue</font><font style="color:rgb(36, 41, 47);"> is supported as a special case. Other packages will likely need to be transformed to be exposed as a native browser-targeting ES module.</font>

<font style="color:rgb(36, 41, 47);"></font>

+ <font style="color:rgb(37, 37, 37);">浏览器请求导入作为原生 ES 模块导入-没有捆绑。</font>
+ <font style="color:rgb(37, 37, 37);">服务器拦截对 *.vue 文件的请求，即时编译它们，并将它们作为 JavaScript 发送回来。</font>
+ <font style="color:rgb(37, 37, 37);">对于提供在浏览器中工作的 ES 模块构建的库，直接从 CDN 导入它们。</font>
+ <font style="color:rgb(37, 37, 37);">对 .js 文件中的 npm 包的导入（仅包名）被动态重写以指向本地安装的文件，目前仅支持 vue 作为特例，其他包可能需要进行转换才能作为本地浏览器目标 ES 模块公开。</font>

<font style="color:rgb(37, 37, 37);"></font>

<font style="color:rgb(37, 37, 37);"></font>

需要待熟悉node express框架后，在阅读

<font style="color:rgb(37, 37, 37);"></font>

