#### 目录
+ vue-cli介绍
+ 分析当前项目构建配置
+ 优化方案
+ 优化结果

---

#### 一、vue-cli介绍
kffrontend项目使用的是vue官方提供的脚手架工具`vue-cli`。`vue-cli`的出现,让我们省掉了配置`webpack`的时间,让我们能直接上手开发.

下图是`vue-cli`的官方介绍,其核心还是基于webpack的,并在做了部分合理的默认配置(配置好`file-loader`,`url-loader`),也会默认帮我们做一些优化(`cache-loader`,配置`one-of`等配置).

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649491936798-c025567c-6075-490c-aae3-d3bd96cb1866.png)

---

#### 二、分析当前构建配置
1. 因为`vue-cli`其基础还是`webpack`,所以还是需要分析当前`vue.cofig.js`对应的`webpack.config.js`

```bash
# 生成对应的webpack配置文件
vue-cli-service inspect webpack.config.js
```



2. 构建速度分析`speed-measure-webpack-plugin`。通过smp输出的分析可以清楚的了解到`webpack`构建过程中，每一阶段的`loader`以及`plugin`的工作花费的时间。

```bash
cnpm install speed-measure-webpack-plugin -D
```

```javascript
const SpeedMeasurePlugin = require('speed-measure-webpack-plugin');

module.exports = {
  chainWebpack: config => {
    config
      .plugin('speed-measure-webpack-plugin')
      .use(SpeedMeasurePlugin)
  }
}
```



3. 构建体积分析`webpack-bundle-analyzer`.用来分析`webapck`构建打包后的文件，如分包情况，占用体积等参数的分析。

```bash
cnpm i webpack-bundle-analyzer -D
```

```javascript
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  chainWebpack: config => {
    config
      .plugin('webpack-bundle-analyzer')
      .use(BundleAnalyzerPlugin);
  }
}
```



或者也可使用`vue-cli`的分析命令

```bash
npm run build -- report
```

---

#### 三、优化方案
1. `sourcemap`调整现生产环境`sourcemap`配置为`source-map`, `js`文件大小为44.1M;调整为`sourcemap`配置为`cheap-module-source-map`或不设置`sourcemap`,js文件为11.5M左右;

```javascript
module.exports = {
  configureWebpack: config => {
    config.devtool = process.env.NODE_ENV === 'development' ? 'source-map' : undefined;
    
  },
  productionSourceMap: process.env.NODE_ENV === 'development',
}
```



2. 按需加载
+ <font style="color:rgb(23, 43, 77);">lodash</font>
    - `lodash`优化前 531KB 	

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649491944437-8bf6cf9e-6c5a-46b8-b3c0-6b3c2cd2c7d8.png)

    - 优化后25KB

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649491987990-d5a96ea5-b3ef-4cc3-baa8-ab33269a3985.png)

```bash
npm install lodash-webpack-plugin --save-dev
```

```javascript
module.exports = {
  plugins: [
   + "lodash",
  ]
}
```

```javascript
const LodashModuleReplacementPlugin = require("lodash-webpack-plugin");

module.exports = {
  chainWebpack: config => {
      config
        .plugin("loadshReplace")
        .use(new LodashModuleReplacementPlugin());
}
```



+ <font style="color:rgb(23, 43, 77);">momentjs</font>
    - `momentjs`优化前672KB  
  
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649492724056-7d4e0b6a-d3d1-48ee-8986-e7cc4d89094f.png)
    - 优化后169KB,(只加载中文包)  
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649492783401-6ec7925b-f433-40ba-a1fb-9c8d15ce74ba.png)

```javascript
const webpack = require('webpack')
export default = {
  configureWebpack: config => {
    const plugins = [];
    plugins.push(
      new webpack.ContextReplacementPlugin(/moment[/\\]locale$/, /zh-cn/)
    );
    config.plugins = [...config.plugins, ...plugins];
  }
}
```



+ css

```javascript
module.exports = {
  chainWebpack: config => {
      config.when(process.env.NODE_ENV !== 'development', config => {
            config.plugin('extract-css').tap(options => {
              options[0].filename = 'static/css/[name].[hash:8].css';
              return options;
            })
          })
  }
}
```



+ 图片

```bash
npm install image-webpack-loader -D
```

```javascript
module.exports = {
  chainWebpack: config => {
    config.module.rule('images')
      .test(/\.(png|jpe?g|gif|webp)(\?.*)?$/)
      .use('image-webpack-loader')
      .loader('image-webpack-loader')
      .options({
        bypassOnDebug: true
      })
      .end();
   }
}
```

+ echarts

```bash
npm install babel-plugin-equire -D
```

```javascript
// eslint-disable-next-line
const echarts = equire([
  // 写上你需要的 echarts api
  "tooltip",
  "line"
]);

export default echarts;
```

```javascript
module.exports = {
  plugins: [
    "equire"
  ]
}
```

```javascript
import echarts from '@/lib/util/echarts.js' 

this.myChart = echarts.init(this.$refs.chart) 
```



3. 压缩代码`uglifyJsPlugin` 用来对js文件进行压缩，减小`js`文件的大小。其会拖慢`webpack`的编译速度，建议开发环境时关闭，生产环境再将其打开。

```bash
npm install uglifyjs-webpack-plugin -D
```

```javascript
const UglifyJsWebpackPlugin = require("uglifyjs-webpack-plugin");

module.exports = {
  configureWebpack: config => {
    config.optimization.minimizer = [
          new UglifyJsWebpackPlugin({
           uglifyOptions: {
            // 删除注释
            output: {
              comments: false
            },
            // 删除console debugger 删除警告(按需设置)
            compress: {
              warnings: false,
              drop_console: true, //console
              drop_debugger: false,
            }
            sourceMap: false,
            parallel: true,//使用多进程并行运行来提高构建速度。默认并发运行数：os.cpus().length - 1。
           }
          })
         ]
  }
}
```



4. 关闭预加载模块

```javascript
module.exports = {
  chainWebpack: config => {
      // 去掉预检请求处理
      config.plugins.delete('prefetch');
      // 移除 preload 插件，避免加载多余的资源
      config.plugins.delete('preload');
  }
}
```

注：`Preload` 是一个新的控制特定资源如何被加载的新的 Web 标准，这是已经在 2016 年 1 月废弃的 `subresource prefetch` 的升级版。这个指令可以在 中使用，比如 。一般来说，最好使用 `preload` 来加载你最重要的资源，比如图像，`CSS`，`JavaScript` 和字体文件。这不要与浏览器预加载混淆，浏览器预加载只预先加载在`HTML`中声明的资源。`preload` 指令事实上克服了这个限制并且允许预加载在 `CSS` 和`JavaScript` 中定义的资源，并允许决定何时应用每个资源。`Prefetch` 是一个低优先级的资源提示，允许浏览器在后台（空闲时）获取将来可能用得到的资源，并且将他们存储在浏览器的缓存中。一旦一个页面加载完毕就会开始下载其他的资源，然后当用户点击了一个带有 `prefetched` 的连接，它将可以立刻从缓存中加载内容。有三种不同的 `prefetch` 的类型，`link`，`DNS` 和 `prerendering`。



5. `cdn` & `externalsexternals` 配置选项提供了「从输出的 `bundle` 中排除依赖」的方法。防止将某些 `import` 的包(`package`)打包到 `bundle` 中，而是在运行时(`runtime`)再去从外部获取这些扩展依赖。

```javascript
configureWebpack:{
  externals: {
      "vue": "Vue",
      "jquery": "jQuery",
    },
}
```

```html
<html>
  <head>
    <!-- 引入 cdn 地址。手动cdn引入(或者用插件自动添加) -->
    
    <script src="https://cdn.bootcdn.net/ajax/libs/vue/2.5.10/vue.min.js"></script>
  <body>
    <div id="app"></div>
  </body>
</html>
```

劣势：`CDN`请求资源数多，会影响首屏加载速度；



6. `gzip`打包

```bash
npm install compression-webpack-plugin -D
```

```javascript
const CompressionWebpackPlugin = require('compression-webpack-plugin');
module.exports = {
  configureWebpack: config => {
    if (process.env.NODE_ENV === 'production') {
      config.plugins.push(
        new CompressionWebpackPlugin(
          {
            filename: info => {
              return `${info.path}.gz${info.query}`
            },
            algorithm: 'gzip',
            threshold: 10240, // 只有大小大于该值的资源会被处理 10240
            test: productionGzipExtensions,
            minRatio: 0.8, // 只有压缩率小于这个值的资源才会被处理
            deleteOriginalAssets: false // 删除原文件
          }
        )
      )
    }
  }
}
```

PS:需要调研当前项目是否启用`gzip`，并且需要后端支持，且需要调整`Nginx`配置

7. `hard-source-webpack-plugin`在启动项目时会针对项目生成缓存，若是项目无`package`或其他变化，下次就不用花费时间重新构建，直接复用缓存。

```bash
 npm install hard-source-webpack-plugin -D
```

```javascript
const HardSourceWebpackPlugin = require('hard-source-webpack-plugin')
module.exports = {
  configureWebpack: config => {
    config.plugin.push(
      // 为模块提供中间缓存，缓存路径是：node_modules/.cache/hard-source
      // solve Configuration changes are not being detected
      new HardSourceWebpackPlugin({
        root: process.cwd(),
        directories: [],
        environmentHash: {
          root: process.cwd(),
          directories: [],
          files: ['package.json', 'yarn.lock']
        }
      })
      // 配置了files的主要原因是解决配置更新，cache不生效了的问题，配置后有包的变化，plugin会重新构建一部分cache
    )
  }
}
```

PS:该优化针对开发环境的构建速度,建议引入`vite`优化开发环境的构建速度;



8. 路由懒加载不使用路由懒加载的话，会在一开始就下载完所有路由对应的组件文件。

```javascript
  {
      path: 'index',
      name: 'index',
      component: () => import('@/views/test/index')
  }
```

<font style="color:#da924a;"></font>

9. `dll` & `splitChunks`(待补充)

---

#### 四、优化进
以上的优化方案,部分方案现配置已在使用(路由懒加载等),部分方案不使用(`hard-source-webpack-plugin`等),及部分方案现已使用

+ 调整`sourcmap`配置
+ 压缩代码(`js`、`css`、图片等资源)
+ `lodash`、`momentjs`、`echarts`等按需加载
+ ...

部分配置在需要在继续验证调试(影响点较多)

+ `gzip`
+ `splitChunks` & `dll`
+ 引入`vite` 优化开发环境构建速度

`dist`文件大小65.1MB => 20MB;

优化前:

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649493406770-b975b97f-de7f-45ef-af43-de8b1107bb87.png)

优化后:

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649493413046-b19c5f7b-08d9-4692-9499-b4f711d2fc90.png)

