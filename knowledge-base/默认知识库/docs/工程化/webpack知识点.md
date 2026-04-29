### 一、babel


#### 1、AST


	抽象语法树（Abstract Syntax Tree，AST），或简称语法树（Syntax tree），是源代码语法结构的一种抽象表示。



它以树状的形式表现编程语言的语法结构，树上的每个节点都表示源代码中的一种结构。



之所以说语法是 “抽象”的，是因为这里的语法并不会表示出真实语法中出现的每个细节。





转换成 AST 的目的就是将我们书写的字符串文件转换成计算机更容易识别的数据结构，这样更容易提取其中的关键信息，而这棵树在计算机上的表现形式，其实就是一个单纯的 `Object`。





比如 `if(false){}` 编译成 AST 代码，我们是知道这段不执行的，就删除这个语法。



+ [AST Explorer](https://astexplorer.net/)



#### 2、Babel原理


大多数 JavaScript `Parser` 遵循 `estree` 规范，`Babel` 最初基于 `acorn` 项目（轻量级现代 JavaScript 解析器）



`Babel` 大概分为三大部分：



+ 解析：将代码转换成AST 
    - **词法分析**：将代码（字符串）分割为 `token` 流，即语法单元成的数组
    - **语法分析**：分析 token 流（上面生成的数组）并生成 `AST`
+ 转换：访问AST的节点进行变换操作生产新的AST 
    - `Taro` 就是利用 `babel` 完成的小程序语法转换
+ **生成**：以新的 `AST` 为基础生成代码



#### 二、Webpack


#### 1、Webpack是什么


	Webpack 是一个现代 JavaScript 应用程序的静态模块打包器（`module bundler`）。



当 Webpack 处理应用程序时，它会递归地构建一个依赖关系图（`dependency graph`），其中包含应用程序需要的每个模块，然后将所有这些模块打包成一个或多个 `bundle`。



所以，它的本质是一个模块打包器，其工作是将每个模块打包成相应的 `bundle`。



#### 2、核心概念


+  `mode`：模式。对应有开发模式、生产模式等 
+  `entry`：指示 webpack 以哪个文件为入口起点开始打包，分析构建内部依赖图。 
+  `output`：指示 webpack 打包后的资源 bundles 输出到哪里去，以及如何命名。 
+  `loader`：模块转换器，让 webpack 能 够 去 处 理 那 些 非 JavaScript 文 件 (webpack 自 身 只 理 解  
JavaScript和json文件)。Webpack 对于 `.jpg`、`.txt` 等内容无法处理，就需要 `file-loader`、`url-loader` 等进行协助处理。 
+  `plugins`：扩展插件，在 Webpack 构建流程中的特定时机注入拓展逻辑来改变构建结果或者做其他你想做的事情。 



#### 3、Webpack构建流程


Webpack 就像一条生产线，要经过一系列处理流程后才能将源文件转换成输出结果。



这条生产线上的每个处理流程的职责都是单一的，多个流程之间有存在依赖关系，只有完成当前处理后才能交给下一个流程去处理。



`Webpack` 的运行流程是一个串行的过程，从启动到结束会依次执行以下流程：



+ **初始化参数**：从配置文件和 `Shell` 语句中读取与合并参数，得出最终的参数
+ **开始编译**：用上一步得到的参数初始化 `Compiler` 对象，加载所有配置的插件，执行对象的 `run` 方法开始执行编译
+ **确定入口**：根据配置中的 `entry` 找出所有的入口文件
+ **编译模块**：从入口文件出发，调用所有配置的 `Loader` 对模块进行翻译，再找出该模块依赖的模块，再递归本步骤直到所有入口依赖的文件都经过了本步骤的处理
+ **完成模块编译**：在经过第 4 步使用 `Loader` 翻译完所有模块后，得到了每个模块被翻译后的最终内容以及它们之间的依赖关系
+ **输出资源**：根据入口和模块之间的依赖关系，组装成一个个包含多个模块的 `Chunk`，再把每个 `Chunk` 转换成一个单独的文件加入到输出列表，这步是可以修改输出内容的最后机会
+ **输出完成**：在确定好输出内容后，根据配置确定输出的路径和文件名，把文件内容写入到文件系统



简单来说：



+ **初始化**：启动构建，读取与合并配置参数，加载 `Plugin`，实例化 `Compiler`（钩子）
+ **编译**：从 `Entry` 出发，针对每个 `Module`（模块）串行调用对应的 `Loader` 去翻译文件的内容，再找到该 `Module` 依赖的 `Module`，递归地进行编译处理
+ **输出**：将编译后的 `Module` 组合成 `Chunk`，将 `Chunk` 转换成文件，输出到文件系统中（`Chunk` 就是打包过程中，入口模块引用其他模块，模块再引用模块，这个关系链连接的 `Module` 就形成了 `Chunk`）



在这个过程中，`Webpack` 会在特定的时间点广播出特定的事件，插件在监听到感兴趣的事件后会执行特定的逻辑，并且插件可以调用 `Webpack` 提供的 `API` 改变 `Webpack` 的运行结果。



#### 4、entry


	指定打包⼊口文件，有三种不同的形式：`string | object | array`。



	一对一：一个入口、一个打包文件



```plain
module.exports = {
  entry: './src/index.js'
}
```



	多对一：多个入口、一个打包文件



```plain
module.exports = {
  entry: [
    './src/index1.js',
    './src/index2.js',
  ]
}
```



	多对多：多个入口、多打包文件



```plain
module.exports = {
  entry: {
    'index1': "./src/index1.js",
    'index2': "./src/index2.js"
  }
}
```



#### 5、output


	打包后的文件位置



```javascript
module.exports = {
  ...,
  output: {// 文件名称（指定名称+目录）
    filename: 'js/[name].js',
    // 输出文件目录（将来所有资源输出的公共目录）
    path: resolve(__dirname, 'build'),
    // 所有资源引入公共路径前缀 --> 'imgs/a.jpg' --> '/imgs/a.jpg'
    publicPath: '/',
    chunkFilename: 'js/[name]_chunk.js', // 非入口chunk的名称
    // library: '[name]', // 整个库向外暴露的变量名
    // libraryTarget: 'window' // 变量名添加到哪个上 browser
    // libraryTarget: 'global' // 变量名添加到哪个上 node
    // libraryTarget: 'commonjs'
  }
}
```



+ 可以指定一个固定的文件名称，如果是多入口多出口（`entry` 为对象），则不能使用单文件出口，需要使用下面的方式
+ 通过 `Webpack` 内置的变量占位符：`[name]`



#### 6、loader


`loader` 的执行顺序是从右向左执行的，也就是后面的 `loader` 先执行。



假如有配置：



```plain
// webpack.config.js
module.exports = {
  //...
  module: {
    rules: [
      {
        test: /\.(le|c)ss$/,
        use: ['style-loader', 'css-loader', 'less-loader'],
        exclude: /node_modules/,
      },
    ],
  },
};
```



那就是先处理 `less-loader`，再处理 `css-loader`，最后处理 `style-loader`。



1.  **关于文件处理的常见loader** 
    - `file-loader`：当引入的文件是 `.png`、`.txt` 等时，可以通过 `file-loader` 解析项目中的 `url` 引入。根据配置将文件拷贝到相应的路径，并修改打包后文件的引入路径，让它指向正确的文件。
    - `url-loader`：`url-loader` 封装了 `file-loader` 且可以不依赖于 `file-loader` 单独使用，并且可以配置 `limit`。对小于 `limit` 大小的图片转换成 `Base64`，大于 `limit` 的时候使用 `file-loader` 里的方法。
2.  **关于语法检查常见loader** 
    - `tslint-loader`：通过 TSLint 检查 TypeScript 代码
    - `eslint-loader`：通过 ESLint 检查 JavaScript 代码
3.  **关于HTML代码常见处理的loader** 
    - `html-loader`：处理 HTML 中的图片
4.  **关于CSS代码处理常见loader** 
    - `style-loader`：动态创建 `style` 标签，将 CSS 代码插入到 `head` 中。
    - `css-loader`：负责处理 `@import`、`url` 等语句。例如 `import css from 'file.css'`、`url(image.png)`。
    - `postcss-loader`：负责进一步处理 CSS 文件，比如添加浏览器前缀，压缩 CSS 等。
    - `less-loader`：将 `.less` 文件内容转换成 CSS。
    - `sass-loader`：将 `.sass` 文件内容转换成 CSS。
5.  **关于JS代码处理常见的loader** 
    - `babel-loader`：将 JS 代码向低版本转换，我们需要使用 `babel-loader`。
    - `ts-loader`：将 TypeScript 转换成 JavaScript
6.  关于Vue单文件组件的loader  
	vue loader 



#### 7、plugin


1. **常见plugin** 
    - `clean-webpack-plugin`：打包前自动清理 `dist` 目录，防止文件残留。
    - `copy-webpack-plugin`：将单个文件或者整个目录复制到构建目录
    - `mini-css-extract-plugin`：将 CSS 抽离出来单独打包并且通过配置可以设置是否压缩。
    - `html-webpack-plugin`：这个插件可以配置生成一个 HTML5 文件，其中 `script` 标签包含所有 Webpack 包。如果你设置多个入口点，你可以据此实现多页面应用打包。
2. **提高效率的plugin** 
    - `webpack-dashboard`：可以更友好的展示相关打包信息。
    - `webpack-merge`：提取公共配置，减少重复配置代码
    - `speed-measure-webpack-plugin`：简称 SMP，分析出 Webpack 打包过程中 Loader 和 Plugin 的耗时，有助于找到构建过程中的性能瓶颈。
    - `size-plugin`：监控资源体积变化，尽早发现问题
    - `HotModuleReplacementPlugin`：模块热替换



#### 8、loader和plugin的区别


+  Loader  
`Loader` 本质上就是一个函数，对接收到的内容进行转换，返回转换后的结果。  
因为 `Webpack` 只认识 JavaScript，所以 `Loader` 就成了翻译官，对不同类型的资源进行处理。  
就好比 `file-loader` 或者 `url-loader`，配置之后就可以正确引用 `png` 等格式的图片、`txt` 等格式文件。  
又好比 `style-loader` 以及 `css-loader`，引用后就可以对 CSS 内容进行预编译处理。 
+  Plugin  
`Plugin` 就是插件，`Plugin` 拓展了 `Webpack` 的功能。`Plugin` 就是在 `Webpack` 的生命周期中进行各种操作，从而达到使用者目的插件。就好比 `html-webpack-plugin`，配合多入口形式使用之后，就可以实现多页面应用的功能。又好比 `clean-webpack-plugin` 实现打包之前清空 `dist` 目录，`copy-webpack-plugin` 可以将单个文件或者整个目录复制到构建目录。 



#### 9、resolve


`resolve` 配置 Webpack 如何寻找模块所对应的文件。



Webpack 内置 JavaScript 模块化语法解析功能，默认会采用模块化标准里约定好的规则去寻找，但你可以根据自己的需要修改默认的规则。



```javascript
// webpack.config.js
module.exports = {
   // 解析模块的规则
  resolve: {
    // 配置解析模块路径别名: 优点简写路径 缺点路径没有提示
    alias: {
      $css: resolve(__dirname, 'src/css')
    },
    // 配置省略文件路径的后缀名
    extensions: ['.js', '.json', '.jsx', '.css'],
    // 告诉 webpack 解析模块是去找哪个目录
    modules: [resolve(__dirname, '../../node_modules'), 'node_modules']
  }
}
```



+ `resolve.modules`：配置 Webpack 去哪些目录下寻找第三方模块，默认情况下，只会去 `node_modules` 下寻找，如果你在项目中某个文件夹下的模块经常被导入，不希望写很长的路径，那么就可以通过配置 `resolve.modules` 来简化。
+ `resolve.alias`：配置项通过别名把原导入路径映射成一个新的导入路径。
+ `resolve.extensions`：适配多端的项目中，可能会出现 `.web.js`, `.wx.js`，例如在转 Web 的项目中，我们希望首先找 `.web.js`，如果没有，再找 `.js`。`extensions: ['web.js', '.js']`。



#### 10、dev server


```plain
module.exports = {
	devServer: {
    // 运行代码的目录
    contentBase: resolve(__dirname, 'build'),
    // 监视 contentBase 目录下的所有文件，一旦文件变化就会 reload
    watchContentBase: true,
    watchOptions: {
      // 忽略文件
      ignored: /node_modules/
    },
    // 启动gzip压缩
    compress: true,
    // 端口号
    port: 5000,
    // 域名
    host: 'localhost',
    // 自动打开浏览器
    open: true,
    // 开启HMR功能
    hot: true,
    // 不要显示启动服务器日志信息
    clientLogLevel: 'none',
    // 除了一些基本启动信息以外，其他内容都不要显示
    quiet: true,
    // 如果出错了，不要全屏提示~
    overlay: false,
    // 服务器代理 --> 解决开发环境跨域问题
    proxy: {
      // 一旦devServer(5000)服务器接受到 /api/xxx 的请求，就会把请求转发到另外一个服务器(3000)
      '/api': {
        target: 'http://localhost:3000',
        // 发送请求时，请求路径重写：将 /api/xxx --> /xxx （去掉/api）
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  }
}
```



#### 11、optimization


```plain
module.exports = {
optimization: {
    splitChunks: {
      chunks: 'all'
      // 默认值，可以不写~
      /* minSize: 30 * 1024, // 分割的chunk最小为30kb
      maxSiza: 0, // 最大没有限制
      minChunks: 1, // 要提取的chunk最少被引用1次
      maxAsyncRequests: 5, // 按需加载时并行加载的文件的最大数量
      maxInitialRequests: 3, // 入口js文件最大并行请求数量
      automaticNameDelimiter: '~', // 名称连接符
      name: true, // 可以使用命名规则
      cacheGroups: {
        // 分割chunk的组
        // node_modules文件会被打包到 vendors 组的chunk中。--> vendors~xxx.js
        // 满足上面的公共规则，如：大小超过30kb，至少被引用一次。
        vendors: {
          test: /[\\/]node_modules[\\/]/,
          // 优先级
          priority: -10
        },
        default: {
          // 要提取的chunk最少被引用2次
          minChunks: 2,
          // 优先级
          priority: -20,
          // 如果当前要打包的模块，和之前已经被提取的模块是同一个，就会复用，而不是重新打包模块
          reuseExistingChunk: true
        } 
      }*/
    },
    // 将当前模块的记录其他模块的hash单独打包为一个文件 runtime
    // 解决：修改a文件导致b文件的contenthash变化
    runtimeChunk: {
      name: entrypoint => `runtime-${entrypoint.name}`
    },
    minimizer: [
      // 配置生产环境的压缩方案：js和css
      new TerserWebpackPlugin({
        // 开启缓存
        cache: true,
        // 开启多进程打包
        parallel: true,
        // 启动source-map
        sourceMap: true
      })
    ]
  }
 }
```



#### 12、从 0 开始配置 Webpack


如何从 0 开始配置一个属于自己的 Webpack 脚手架呢？那就涉及到选型问题。



1.  **技术选型** 
    - 移动端 || PC
    - MPA || SPA
    - HTML || 模板引擎
    - CSS || 预处理器
    - JavaScript ES5 || ES6
    - 本地发布服务（数据模拟）
    - React || Vue
    - 多人项目 || 单人项目
    - 语法规范 Eslint
    - 单元测试
    - 提交规范
2.  **Loader配置 - 处理CSS、Less** 
    - use: `['style-loader', 'css-loader', 'postcss-loader', 'less-loader']`
    - `less less-loader`：解析 `.less` 文件
    - `postcss-loader autoprefixer`：对 `flex` 布局等进行前缀补充
3.  **Loader配置 - 处理图片** 
    - `file-loader`：解析 `.txt`、`.png`、`.md` 等格式文件
    - `url-loader`：`limit: 1024`，判断大小是否处理成 `base64` 格式
4.  **Loader配置 - 处理字体** 
    - `url-loader`
5.  **Loader配置 -  MPA多页面打包通用方案** 
    - 安装 `glob`
    - 将 `entry` 和 `htmlwebpackplugin` 动态生成
6.  **SourceMap** 
    - 开发环境配置：`eval-source-map`
    - 线上生成配置：`source-map`
7.  **WebpackDevServer** 
    - 安装
    - 配置：`devServer`
    - `HMR`（热模块替换，Hot Module Replacement）
    - 开启 JS 模块的 `HMR`，需要 `Webpack` 配合
8.  **babel解析**  
js兼容性处理：安装babel-loader @babel/core; 
    1.  基本js兼容性 ： @babel/preset -env;  
问题：只能转换基本语法，如promise等高级语法不能转化； 
    2.  全部js兼容性：@babel/polyfill;  
问题，只需要解决部分兼容性问题，但是将所有兼容性代码全部引入，导致体积太大； 
    3.  需要做兼容性处理的就做-按需加载：core-js;**(最优方案) 
9.  **性能优化** 
    -  缩小 `loader` 的文件范围：`loader` 的 `include` 配置，可以指定 `src` 目录，减少检查范围。 
    -  优化 `resolve.modules` 配置：配置 `Webpack` 去哪些目录下寻找第三方模块，默认 `node_modules`。 
    -  分离 CSS：`MiniCssExtractPlugin` 
    -  hash、chunkhash、contenthash  
区别 
        * `hash` 作用域 JS、CSS，图片的 `hash` 有区别，每次打包构建都会变化一次。
        * `chunkhash` 以 `chunk` 为单位，修改了那部分就改动哪部分的 `hash`。（同时依赖的模块也会改变 `hash`）
        * `contenthash` 只有自己内容发生改变，才发生改变（区别于 `chunkhash`）。
        * 所以 JS 适用于 `chunkhash`；CSS 适用于 `contenthash`；Image 适用于 `hash`
    -  压缩 CSS：`optimize-css-assets-webpack-plugin` 和 `cssnano` 
    -  压缩 HTML：`html-webpack-plugin` 
    -  压缩图片：`img-webpack-loader` 
    -  分离 `Webpack` 配置：分离 `base.config`、`dev.config`、`mpa.config` 和 `pro.config` 4 个，通过 `merge` 进行 `config` 配置的合并 
10.   

##### 其他
    - 如何简单编写一个 `Webpack` 解析器
    - 如何编写一个 `Webpack loader`
    - 如何编写一个 `Webpack plugin`



#### 13、webpack环境配置优化方案


###### 1、开发环境性能优化：


1.  **优化打包构建速度** 
    -  HMR:  
刷新我们一般分为两种： 
        * 一种是页面刷新，不保留页面状态，就是简单粗暴，直接 `window.location.reload()`。
        * 另一种是基于 `WDS`（`Webpack-dev-server`）的模块热替换，只需要局部刷新页面上发生变化的模块，同时可以保留当前的页面状态，比如复选框的选中状态、输入框的输入等。

`Webpack` 的热更新又称热替换（`Hot Module Replacement`），缩写为 `HMR`。  
这个机制可以做到不用刷新浏览器而将新变更的模块替换掉旧的模块。 

        1.  **开启热更新**  
在 Webpack 的 `webpack.config.js` 中： 
            1. 配置 `devServer` 的 `hot` 为 `true`
            2. 在 `plugins` 中增加 `new webpack.HotModuleReplacementPlugin()`

```plain
// webpack.config.js
const webpack = require('webpack');
module.exports = {
  //....
  devServer: {
    hot: true
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin() // 热更新插件
  ]
}
```

并且在入口文件配置： 

```plain
if(module && module.hot) {
  module.hot.accept()
}
```

此时修改代码的时候，只有对应部分的内容才会相应更新。 

        2.  **热更新原理**  
`HMR` 的核心就是客户端从服务端拉去更新后的文件，准确的说是 `chunk diff`（`chunk` 需要更新的部分）。  
实际上 `webpack-dev-server`（`WDS`）与浏览器之间维护了一个 `Websocket`，当本地资源发生变化时，`WDS` 会向浏览器推送更新，并带上构建时的 `hash`，让客户端与上一次资源进行对比。  
客户端对比出差异后会向 `WDS` 发起 `Ajax` 请求来获取更改内容（文件列表、`hash`），这样客户端就可以再借助这些信息继续向 `WDS` 发起 `jsonp` 请求获取该 `chunk` 的增量更新。  
后续的部分（拿到增量更新之后如何处理？哪些状态该保留？哪些又需要更新？）由 `HotModulePlugin` 来完成，提供了相关 `API` 以供开发者针对自身场景进行处理，像 `react-hot-loader` 和 `vue-loader` 都是借助这些 `API` 实现 `HMR`。 
1.  优化代码调试 
    -  source-map：  
`source map` 是将编译、打包、压缩后的代码映射回源代码的过程。打包压缩后的代码不具备良好的可读性，想要调试源码就需要 `soucre map`。  
`map` 文件只要不打开开发者工具，浏览器是不会加载的。  
线上环境一般有三种处理方案： 
        * `hidden-source-map`：借助第三方错误监控平台 `Sentry` 使用
        * `nosources-source-map`：只会显示具体行数以及查看源代码的错误栈。安全性比 `source map` 高
        * `source map`：通过 `nginx` 设置将 `.map` 文件只对白名单开放（公司内网）

注意：避免在生产中使用 `inline-` 和 `eval-`，因为它们会增加 `bundle` 体积大小，并降低整体性能。  
一般开发环境采用eval-source-map；  
生产环境采用source-map； 



###### 2、生产环境性能优化：


1.  **优化打包构建速度** 
    -  oneOf  
正常情况下，每个文件会被每个loader进行检测处理，使用oneOf后的文件只会匹配一个loader，不会被多个loader重复检测匹配，可以提高构建速度；  
注意：oneOf内不能有多个处理同一类型文件的配置； 
    -  多进程打包  
**配置**{loader:'thread-loader',options: {worker:2 // 进程数量}}；  
**作用**：开启多进程打包；  
**使用场景**：进程开启时间 600ms，只用打包消耗时间较长的项目，才需要多进程打包； 
    -  多进程压缩  
因为自带的 `UglifyjsWebpackPlugin` 压缩插件是单线程运行的，而 `TerserWebpackPlugin` 可以并发运行压缩功能（多进程）。  
所以通过  WebpackPlugin`代替自带的`UglifyjsWebpackPlugin` 插件。 
    -  externals  
**配置**：externals:{jquery:'jQuery'};  
**作用**：externals配置内的代码库，不会被打包，可使用cdn引入； 
    -  dll  
**作用**：对某些库进行单独打包，再单独引入到项目中； 
    -  Scope Hoisting(作用域提升)  
**作用**：Webpack会将引入的JS文件"提升到"它的引入者顶部;  
**好处**： 
        * 「代码体积更小」，因为函数申明语句会产生大量代码，导致包体积增大（模块越多越明显）；
        * 代码在运行时因为创建的函数作用域更少，「内存开销也随之变小」。

**原理**：  
`Scope Hoisting` 的实现原理其实很简单：分析出模块之间的依赖关系，尽可能将打散的模块合并到一个函数中，前提是不能造成代码冗余。因此「只有那些被引用了一次的模块才能被合并」。  
由于 `Scope Hoisting` 需要分析出模块之间的依赖关系，因此源码「必须采用 `ES6` 模块化语句」，不然它将无法生效。原因和 `Tree Shaking` 中介绍的类似。 

2.  优化代码运行性能 
    -  缓存(hash-chunkhash-contenthash)  
cacheDirectory：true开始babel缓存；  
文件指纹是打包后输出的文件名的后缀，对应着 3 种 `hash`。 
        *  `hash` 是跟整个项目的构建相关，只要项目里有文件更改，整个项目构建的 `hash` 值都会更改，并且全部文件都共用相同的 `hash` 值。（整个项目）  
适用类型：图片文件  
设置file-loader的name，使用hash。  
占位符名称及含义 
            + ext     资源后缀名
            + name    文件名称
            + path    文件的相对路径
            + folder  文件所在的文件夹
            + contenthash   文件的内容hash，默认是md5生成
            + hash         文件内容的hash，默认是md5生成
            + emoji        一个随机的指代文件内容的emoj

```plain
const path = require('path');

module.exports = {
    entry: './src/index.js',
    output: {
        filename:'bundle.js',
        path:path.resolve(__dirname, 'dist')
    },
    module:{
        rules:[{
            test:/\.(png|svg|jpg|gif)$/,
            use:[{
                loader:'file-loader',
                options:{
                    name:'img/[name][hash:8].[ext]'
                }
            }]
        }]
    }
}
```

        *  `chunkhash` 是根据不同的入口进行依赖文件解析，构建对应的 `chunk`（模块），生成对应的 `hash` 值。只有被修改的 `chunk`（模块）在重新构建之后才会生成新的 `hash` 值，不会影响其它的 `chunk`。（粒度 `entry` 的每个入口文件）  
适用类型：JS文件  
设置 output 的 filename，用 chunkhash。 

```plain
module.exports = {
    entry: {
        app: './scr/app.js',
        search: './src/search.js'
    },
    output: {
        filename: '[name][chunkhash:8].js',
        path:__dirname + '/dist'
    }
}
```

 

        *  `contenthash` 是跟每个生成的文件有关，每个文件都有一个唯一的 `hash` 值。当要构建的文件内容发生改变时，就会生成新的 `hash` 值，且该文件的改变并不会影响和它同一个模块下的其它文件。（粒度每个文件的内容）  
适用类型：CSS文件  
设置 MiniCssExtractPlugin 的 filename，使用 contenthash。 

```plain
module.exports = {
    entry: {
        app: './scr/app.js',
        search: './src/search.js'
    },
    output: {
        filename: '[name][chunkhash:8].js',
        path:__dirname + '/dist'
    },
    plugins:[
        new MiniCssExtractPlugin({
            filename: `[name][contenthash:8].css`
        })
    ]
}
```

 

    -  babel缓存  
**cache-loader**  
在 `babel-loader` 开启 `cache` 后，将 `loader` 的编译结果写进硬盘缓存，再次构建如果文件没有发生变化则会直接拉取缓存。  
**uglifyjs-webpack-plugin** 
    -  tree shaking  
**作用**：去除JS上下文中的未引用代码(dead-code)；  
**前提**：1、必须使用ES6模块化；2、开启production环境；  
**副作用**：在导入时会执行特殊行为的代码，而不是仅仅暴露一个 `export` 或者多个 `export`。  
**配置**：在package.json中配置： 
        1.  sideEffects：false：所有代码都可以进行tree shaking.  
问题：可能会把css/@babel.polyfill文件干掉； 
        2.  sideEffects:["_ .css","_.less"] //配置内的文件不做处理； 
        3.  引入一个能够删除未引用代码(dead-code)的压缩工具(例如：UglifyJSPlugin),或使用webpack5 

**问题一：为什么可以实现 Tree Shaking？**ES6 模块依赖关系是确定的，和运行时的状态无关，可以进行可靠的静态分析，这就是 `Tree Shaking` 的基础。  
所谓的 **静态分析**，就是不执行代码，从字面量上对代码进行分析，ES6 之前的模块化，比如我们可以动态 `require` 一个模块，只有执行后才知道引用的什么模块，这个就不能通过静态分析去做优化。 

```plain
// demo.js
export const a = 'a';
export const b = 'b';

// test.js
import { a } from './demo.js';

// 以上代码不运行，仅仅经过扫描分析，抛弃了 const b，代码缩减了 size
// 这就是 Tree Shaking 的静态分析基本原理：有引用就保留，没有引用就抛弃
```

所以为啥 CommonJS 不能 `Tree Shaking` 就是这个缘故。  
**问题二：下面哪种情况会Tree Shaking?**

```plain
// 全部导入
import _ from 'lodash';

// 具名导入
import { debounce } from 'lodash';

// 直接导入具体模块
import debounce from 'lodash/lib/debounce';
```

上面导入中：第一种的 **全部导入** 是不支持 `Tree Shaking` 的，其他都支持。  
为什么呢？因为当你将整个库导入到单个 JavaScript 对象中时，就意味着你告诉 Webpack，你需要整个库，这样 Webpack 就不会摇它。 

    -  code-split  
**1、代码分割（**`**code splitting**`**）**  
		是指：将脚本中无需立即调用的代码在代码构建时转变为异步加载的过程。  
在 Webpack 构建时，会避免加载已声明要异步加载的代码，异步代码会被单独分离出一个文件，当代码实际调用时被加载至页面。  
代码分割技术的核心是 **异步加载资源**。  
2、**可实现代码分割的方式**： 
        * entry使用对象结构，有多少个入口，最终输出就有相应的bundle；
        * 可以设置optimization:{splitChunks: {chunk:'all'}}, 
            + 可以将node_modules中代码单独打包成一份chunk输出；
            + 自动分析多入口chunk中，有公共文件的话，则会打包成单独的chunk；
        * 使用import()动态导入语法，可以将文件单独打包；

**3、实现原理**

        1. 将需要进行懒加载的子模块单独打包成文件（`children chunk`）
        2. 借助函数来实现延迟进行子模块的加载代码（`import`）

> print.js
>

```plain
console.log('输出 1');

export default () => {
  console.log('输出 2');
};
```

> index.js
>

```plain
const btn = document.querySelector('.btn');
btn.onclick = import('./print.js').then((module) => {
  const print = module.default;
  print();
});
```

**4、Vue按需加载**		Vue 的特点就是 SPA - Single Page Application（单页应用程序）。  
只有第一次加载页面，以后的每次页面切换，只需要进行组件替换。  
它减少了请求次数，加快页面响应速度，降低对服务器压力等等。  
但是，因为 Vue 是 SPA，所以首页第一次加载时会把所有组件以及组件相关资源全部加载，从而导致网站首页打开速度变慢，降低用户体验。  
Vue 项目中，可以结合 Webpack，在 `vue-router` 通过 `import` 进行动态加载： 

```plain
const routes = [{
  path: '/',
  name: 'Home',
  component: () => import('../views/Home.vue')
}];
```

##### 
    -  懒加载/预加载  
**懒加载或者按需加载**，是一种很好的优化网页或应用的方式。  
这种方式实际上是先把你的代码在一些逻辑断点处分离开，然后在一些代码块中完成某些操作后，立即引用或即将引用另外一些新的代码块。  
这样加快了应用的初始加载速度，减轻了它的总体体积，因为某些代码块可能永远不会被加载。  
**实现方法：**使用import()导入文件；  
**正常加载**：可以认为时候并行加载(同一时间加载多个文件)；  
**预加载(prefetch）**：等待其他资源加载完毕，浏览器空闲了，再偷偷加载资源  
**实现方法：**使用import()导入文件，并添加webpackPrefech：true； 
    -  PWA  
PWA:渐进式网络开发应用程序(可以离线访问) 
    -  打包资源压缩 
        * JS 压缩：`UglifyjsWebpackPlugin`
        * HTML 压缩：`HtmlWebpackPlugin`
        * CSS 压缩：`MiniCssExtractPlugin`
        * 图片压缩：`image-webpack-loader`
        * Gzip 压缩：不包括图片



###### 3、体验优化


+ [progress-bar-webpack-plugin](https://www.npmjs.com/package/progress-bar-webpack-plugin)：在终端底部，将会有一个构建的进度条，可以让你清晰的看见构建的执行进度。
+ [webpack-build-notifier](https://www.npmjs.com/package/webpack-build-notifier)：在构建完成时，能够像微信、Lark 这样的 APP 弹出消息的方式，提示构建已经完成。
+ [webpack-dashboard](https://juejin.im/post/6844903924806189070)：对 Webpack 原始的构建输出不满意的话，也可以使用这样一款 Plugin 来优化你的输出界面。
+ [speed-measure-webpack-plugin](https://www.npmjs.com/package/speed-measure-webpack-plugin)：该插件可以测量各个插件和 `loader` 所花费的时间。
+ `webpack-bundle-analyzer`：可视化分析。通过矩阵树图的方式将包内各个模块的大小和依赖关系呈现出来。



#### 14、Webpack 打包原理


在 Webpack 简单实现中，简单的做了下如何将一份代码进行打包：



1. 利用 `babel` 完成代码转换，并生成单个文件的依赖
2. 生成依赖图谱
3. 生成最后打包代码

