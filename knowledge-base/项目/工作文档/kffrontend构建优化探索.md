#### <font style="color:rgb(23, 43, 77);">一、vue-cli</font>
<font style="color:rgb(23, 43, 77);">kffrontend项目使用的是vue官方提供的脚手架工具vue-cli.vue-cli的出现,让我们省掉了配置webpack的时间,让我们能直接上手开发.</font>

<font style="color:rgb(23, 43, 77);">下图是vue-cli的官方介绍,其核心还是基于webpack的,并在做了部分合理的默认配置(配置好file-loader,url-loader),也会默认帮我们做一些优化(cache-loader,配置one-of等配置).</font>

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066295825-9a803866-5c80-478a-8488-b18a83f0ae87.png)

#### <font style="color:rgb(23, 43, 77);">二、分析当前构建配置</font>
1. <font style="color:rgb(23, 43, 77);">因为vue-cli其基础还是webpack,所以还是需要分析当前vue.cofig.js对应的webpack.config.js</font>

```plain
// 生成对应的webpack配置文件
vue-cli-service inspect webpack.config.js
```

<font style="color:rgb(23, 43, 77);">  
</font>

2. <font style="color:rgb(23, 43, 77);">构建速度分析</font>

`<font style="color:rgb(23, 43, 77);">speed-measure-webpack-plugin</font>`<font style="color:rgb(23, 43, 77);">.</font>

<font style="color:rgb(23, 43, 77);">通过smp输出的分析可以清楚的了解到webpack构建过程中，每一阶段的loader以及plugin的工作花费的时间。</font>

```plain
// cnpm install speed-measure-webpack-plugin -D

//vue.config.js
const SpeedMeasurePlugin = require('speed-measure-webpack-plugin');

module.exports = {
  chainWebpack: config => {
    config
      .plugin('speed-measure-webpack-plugin')
      .use(SpeedMeasurePlugin)
  }
}
```

<font style="color:rgb(23, 43, 77);">  
</font>

3. <font style="color:rgb(23, 43, 77);">构建体积分析</font>

`<font style="color:rgb(23, 43, 77);">webpack-bundle-analyzer</font>`<font style="color:rgb(23, 43, 77);">.</font>

<font style="color:rgb(23, 43, 77);">用来分析webapck构建打包后的文件，如分包情况，占用体积等参数的分析。</font>

```plain
//cnpm i webpack-bundle-analyzer -D

const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  chainWebpack: config => {
    config
      .plugin('webpack-bundle-analyzer')
      .use(BundleAnalyzerPlugin);
  }
}
```

<font style="color:rgb(23, 43, 77);">或者也可使用vue-cli的分析命令:</font>`<font style="color:rgb(23, 43, 77);">npm run build -- report</font>`

#### <font style="color:rgb(23, 43, 77);">三、优化方案</font>
1. `<font style="color:rgb(23, 43, 77);">sourcemap</font>`<font style="color:rgb(23, 43, 77);">调整</font>

<font style="color:rgb(23, 43, 77);">现生产环境sourcemap配置为:source-map, js文件大小为44.1M;</font>

<font style="color:rgb(23, 43, 77);">调整为sourcemap配置为cheap-module-source-map或不设置sourcemap,js文件为11.5M左右;</font>

```plain
// vue.config.js
module.exports = {
  configureWebpack: config => {
    config.devtool = process.env.NODE_ENV === 'development' ? 'source-map' : undefined;

  },
 productionSourceMap: process.env.NODE_ENV === 'development',
}
```

<font style="color:rgb(23, 43, 77);">  
</font>

2. <font style="color:rgb(23, 43, 77);">按需加载</font>
    - <font style="color:rgb(23, 43, 77);">lodash</font>

<font style="color:rgb(23, 43, 77);">优化前 531KB</font>

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066308738-b1a753d7-3351-477c-9416-90263bfb5ab7.png)

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">优化后25KB</font>

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066321474-ec3fa949-aa10-4fce-851c-692a0a24a78d.png)

```plain
// npm install lodash-webpack-plugin --save-dev

// babel.config.js
module.exports = {
  plugins: [
   + "lodash",
  ]
}

// vue.config.js
const LodashModuleReplacementPlugin = require("lodash-webpack-plugin");

module.exports = {
  chainWebpack: config => {
      config
        .plugin("loadshReplace")
        .use(new LodashModuleReplacementPlugin());
}
```

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">momentjs</font>

<font style="color:rgb(23, 43, 77);">优化前672KB</font>

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">  
</font>

    - ![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066331539-d7b4433e-a8a7-470d-bff8-7419ed808421.png)

<font style="color:rgb(23, 43, 77);">优化169KB,(只加载中文包)</font>

<font style="color:rgb(23, 43, 77);">  
</font>

    - ![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066338073-9cc13b15-b2f4-4cd9-97e2-9a0ffb71c097.png)

```plain
// vue.config.js
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

    - <font style="color:rgb(23, 43, 77);">css</font>

```plain
// vue.config.js
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

    - <font style="color:rgb(23, 43, 77);">图片</font>

```plain
// npm install image-webpack-loader -D

//vue.config.js
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

    - <font style="color:rgb(23, 43, 77);">echarts</font>

```plain
// npm install babel-plugin-equire -D

// echarts.js
// eslint-disable-next-line
  const echarts = equire([
    // 写上你需要的 echarts api
    "tooltip",
    "line"
  ]);

  export default echarts;

//babel.config.js
module.exports = {
  plugins: [
    "equire"
  ]
}

// 应用页面
import echarts from '@/lib/util/echarts.js' 

this.myChart = echarts.init(this.$refs.chart)
```

<font style="color:rgb(23, 43, 77);">  
</font>

3. <font style="color:rgb(23, 43, 77);">压缩代码</font>

`<font style="color:rgb(23, 43, 77);">uglifyJsPlugin</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">用来对js文件进行压缩，减小js文件的大小。其会拖慢webpack的编译速度，建议开发环境时关闭，生产环境再将其打开.</font>

```plain
// npm install uglifyjs-webpack-plugin -D

// vue.config.js
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

<font style="color:rgb(23, 43, 77);">  
</font>

4. <font style="color:rgb(23, 43, 77);">关闭预加载模块</font>

```plain
// vue.config.js
module.exports = {
  chainWebpack: config => {
      // 去掉预检请求处理
      config.plugins.delete('prefetch');
      // 移除 preload 插件，避免加载多余的资源
      config.plugins.delete('preload');
  }
}
```

<font style="color:rgb(23, 43, 77);">注：Preload 是一个新的控制特定资源如何被加载的新的 Web 标准，这是已经在 2016 年 1 月废弃的 subresource prefetch 的升级版。这个指令可以在 中使用，比如 。一般来说，最好使用 preload 来加载你最重要的资源，比如图像，CSS，JavaScript 和字体文件。这不要与浏览器预加载混淆，浏览器预加载只预先加载在HTML中声明的资源。preload 指令事实上克服了这个限制并且允许预加载在 CSS 和JavaScript 中定义的资源，并允许决定何时应用每个资源。</font>

<font style="color:rgb(23, 43, 77);">Prefetch 是一个低优先级的资源提示，允许浏览器在后台（空闲时）获取将来可能用得到的资源，并且将他们存储在浏览器的缓存中。一旦一个页面加载完毕就会开始下载其他的资源，然后当用户点击了一个带有 prefetched 的连接，它将可以立刻从缓存中加载内容。有三种不同的 prefetch 的类型，link，DNS 和 prerendering。</font>

<font style="color:rgb(23, 43, 77);">  
</font>

5. <font style="color:rgb(23, 43, 77);">cdn & externals</font>

<font style="color:rgb(23, 43, 77);">externals 配置选项提供了「从输出的 bundle 中排除依赖」的方法。防止将某些 import 的包(package)打包到 bundle 中，而是在运行时(runtime)再去从外部获取这些扩展依赖。</font>

```plain
// vue.config.js
configureWebpack:{
  externals: {
      // "vue": "Vue",
      // "jquery": "jQuery",
    },
}

// public/index.html 手动cdn引入(或者用插件自动添加)
<html>
  <head>
    <!-- 引入 cdn 地址 -->
    <script src="https://cdn.bootcdn.net/ajax/libs/vue/2.5.10/vue.min.js"></script>
  <body>
    <div id="app"></div>
  </body>
</html>
```

<font style="color:rgb(23, 43, 77);">劣势：CDN请求资源数多，会影响首屏加载速度；</font>

6. <font style="color:rgb(23, 43, 77);">gzip打包</font>

```plain
// npm install compression-webpack-plugin -D

// vue.config.js
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

<font style="color:rgb(23, 43, 77);">PS:需要调研当前项目是否启用gzip，并且需要后端支持，且需要调整Nginx配置</font>

7. <font style="color:rgb(23, 43, 77);">hard-source-webpack-plugin</font>

<font style="color:rgb(23, 43, 77);">在启动项目时会针对项目生成缓存，若是项目无package或其他变化，下次就不用花费时间重新构建，直接复用缓存。</font>

```plain
// npm install hard-source-webpack-plugin -D

// vue.config.js
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

<font style="color:rgb(23, 43, 77);">PS:该优化针对开发环境的构建速度,建议引入vite优化开发环境的构建速度;</font>

8. <font style="color:rgb(23, 43, 77);">路由懒加载</font>

<font style="color:rgb(23, 43, 77);">不使用路由懒加载的话，会在一开始就下载完所有路由对应的组件文件。</font>

```plain
// router/index.js
  {
      path: 'index',
      name: 'index',
      component: () => import('@/views/test/index')
  }
```

9. <font style="color:rgb(23, 43, 77);">dll & splitChunks(待补充)</font>

#### <font style="color:rgb(23, 43, 77);">四、优化进度</font>
<font style="color:rgb(23, 43, 77);">以上的优化方案,部分方案现配置已在使用(路由懒加载等),部分方案不使用(hard-source-webpack-plugin等),及部分方案现已使用</font>

+ <font style="color:rgb(23, 43, 77);">调整sourcmap配置</font>
+ <font style="color:rgb(23, 43, 77);">压缩代码(js、css、图片等资源)</font>
+ <font style="color:rgb(23, 43, 77);">lodash、momentjs、echarts等按需加载</font>
+ <font style="color:rgb(23, 43, 77);">...</font>

<font style="color:rgb(23, 43, 77);">部分配置在需要在继续验证调试(影响点较多)</font>

+ <font style="color:rgb(23, 43, 77);">gzip</font>
+ <font style="color:rgb(23, 43, 77);">splitChunks & dll</font>
+ <font style="color:rgb(23, 43, 77);">引入vite 优化开发环境构建速度</font>

<font style="color:rgb(23, 43, 77);">dist文件大小65.1MB => 20MB;</font>

<font style="color:rgb(23, 43, 77);">优化前:</font>

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066389980-7fd35a56-50f6-47fb-b526-8400339aa21e.png)

<font style="color:rgb(23, 43, 77);">优化后:</font>

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066395221-31ce3277-46d9-4b1c-868f-71209548a0fb.png)

