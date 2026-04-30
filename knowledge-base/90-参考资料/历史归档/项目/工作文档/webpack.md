#### 一、了解vue.config.js
注：查看vue.config.js对应的webpack配置文件：`vue inspect > [文件名]

1. `vue-cli`默认做了哪些优化？
    - `vue-cli`的出现，让我们省掉了配置webpack的时间。让我们能直接上手开发。注：例如提前配置好file-loader、url-loader;
    - **「性能方面」**，`vue-cli`默认尽可能多的帮我们做了优化，比如cache-loader会在项目中预先做了配置。
2. 在cli的基础上我们又能做哪些优化？》
3. `vue.config.js`中如何配置一些常用的`plugin`和`loader`

二、优化实践

1. 检测当前项目的打包后的大小，速度，各chunk的大小（分析的依据）；kffrontend:构建速度： 52.3s![](C:\Users\xulf01\AppData\Roaming\Typora\typora-user-images\image-20211211142847433.png)构建体积33.87MB、3.43MB(GZIP)![](C:\Users\xulf01\AppData\Roaming\Typora\typora-user-images\image-20211211142935022.png)
2. vue inspect => 查看当前项目vue.config.js对应的webpack.config.js的配置项；
3. 针对上面的分析依据，进行对应的优化；

#### 二、页面分析
1. 调试工具network中的几个参数
    - `DOMContentLoaded``DOM`树构建完成；
    - `Finish`页面加载完毕，包括DOM树构建和请求css、图片等外部资源；
    - `Load`页面上所有http请求发送到响应完成的时间。注：`HTTP1.0/1.1` 协议限定，单个域名的请求并发量是 6 个，即 Finish 是所有请求（不只是`XHR`请求，还包括`DOC`，`img`，`js`，`css`等资源的请求）在并发量为6的限制下完成的时间
2. Waterfall参数解析
    - 浅灰：查询中；
    - 深灰：停滞，代理转发，请求发送；
    - 橙色：初始连接；
    - 绿色：等待中；
    - 蓝色：内容下载。
3. 优化方向
    - 减少瀑布宽度，即减少资源的加载时间；
    - 减少瀑布的高度，即减少请求的数量；
    - 将绿色的”开始渲染“线向左移动，即通过优化资源请求顺序来加快渲染时间。
4. 

#### 三、优化方案
1. 代码分割
    - 公共代码分割
2. source-map现在的生产设置为sourcemap  ： source-map; js文件：44.1M;生产不设置sourcemap  => js文件大小：11.5M左右；cheap-module-source-map: 11.7M左右
3. 多进程打包
    - thread-loader
    - 
4. 压缩代码
    - gzip（需要调研当前项目是否启用gzip，并且需要后端支持，且设置Nginx）（待处理）[https://www.jianshu.com/p/fcfa1945db23](https://www.jianshu.com/p/fcfa1945db23)
    - 
5. 路由懒加载不使用路由懒加载的话，会在一开始就下载完所有路由对应的组件文件。
6. 关闭预加载模块

```javascript
// vue.config.js
chainWebpack: config => {
    // 去掉预检请求处理
    config.plugins.delete('prefetch');
    // 移除 preload 插件，避免加载多余的资源
    config.plugins.delete('preload');
}
```

注：Preload 是一个新的控制特定资源如何被加载的新的 Web 标准，这是已经在 2016 年 1 月废弃的 subresource prefetch 的升级版。这个指令可以在 中使用，比如 。一般来说，最好使用 preload 来加载你最重要的资源，比如图像，CSS，JavaScript 和字体文件。这不要与浏览器预加载混淆，浏览器预加载只预先加载在HTML中声明的资源。preload 指令事实上克服了这个限制并且允许预加载在 CSS 和JavaScript 中定义的资源，并允许决定何时应用每个资源。Prefetch 是一个低优先级的资源提示，允许浏览器在后台（空闲时）获取将来可能用得到的资源，并且将他们存储在浏览器的缓存中。一旦一个页面加载完毕就会开始下载其他的资源，然后当用户点击了一个带有 prefetched 的连接，它将可以立刻从缓存中加载内容。有三种不同的 prefetch 的类型，link，DNS 和 prerendering。

7. CDN引入劣势：CDN请求资源数多，会影响首屏加载速度；
8. 
9. 按需加载
    - lodash处理前 531KB => 处理后的 后的25KB![](C:\Users\xulf01\AppData\Roaming\Typora\typora-user-images\image-20211211175805553.png)![](C:\Users\xulf01\AppData\Roaming\Typora\typora-user-images\image-20211211175849573.png)

```plain
npm install lodash-webpack-plugin --save-dev
```

 在`babel.config.js`设置

```plain
module.exports = {
  plugins: [
    "lodash",
  ]
}
```

在`vue.config.js`设置

```plain
const LodashModuleReplacementPlugin = require("lodash-webpack-plugin");

chainWebpack: config => {
    config
    .plugin("loadshReplace")
    .use(new LodashModuleReplacementPlugin());
}
```

    - css:    mini-css-extract-plugin先生产css资源：1.05M;
    - 图片：image-webpack-loader
    - element-ui按需加载（待处理）
    - echarts（需要处理项目中已使用的echart类型-待处理）

```latex
    npm install babel-plugin-equire -D
```

在项目中创建 `echarts.js`:

```latex
// eslint-disable-next-line
  const echarts = equire([
    // 写上你需要的 echarts api
    "tooltip",
    "line"
  ]);

  export default echarts;
```

在 `babel.config.js`里面：

```latex
module.exports = {
  presets: [
    '@vue/app'
  ],
  plugins: [
    [
      "component",
      {
        libraryName: "element-ui",
        styleLibraryName: "theme-chalk"
      }
    ],
    "equire"
  ]
}
```

具体页面应用：

```plain
import echarts from '@/lib/util/echarts.js' 

 this.myChart = echarts.init(this.$refs.chart) 
```

        1. 安装 `babel-plugin-equire` 插件：
    - momentjs按需加载在vue.config.js里面

```plain
const webpack = require('webpack')
export default = {
  ......
  configureWebpack: config => {
    const plugins = [];
    plugins.push(
      new webpack.ContextReplacementPlugin(/moment[/\\]locale$/, /zh-cn/)
    );
    config.plugins = [...config.plugins, ...plugins];
  }
}
```

处理前的672kb ==> 处理后的169KB![](C:\Users\xulf01\AppData\Roaming\Typora\typora-user-images\image-20211211173847041.png)![](C:\Users\xulf01\AppData\Roaming\Typora\typora-user-images\image-20211211173913036.png)



#### 四、优化配置文件
```javascript
'use strict';
const path = require('path');
// 体积分析插件
// const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
// 速度分析插件
// const SpeedMeasureWebpackPlugin = require('speed-measure-webpack-plugin');
// gzip压缩插件
// const CompressionWebpackPlugin = require('compression-webpack-plugin');

const LodashModuleReplacementPlugin = require("lodash-webpack-plugin");

// const productionGzipExtensions = /\.(js|css)(\?.*)?$/i; // 开启gzip压缩， 按需写入

const UglifyJsWebpackPlugin = require("uglifyjs-webpack-plugin");

const webpack = require('webpack');

function resolve(dir) {
  return path.join(__dirname, dir);
}
const baseConfig = {
  //vue-baidu-map,vue-upload-component在ie会报错，需要babel编译一下
  transpileDependencies: [/vue-baidu-map/, /vue-upload-component/],
  configureWebpack: config => {
    config.resolve.alias = Object.assign({}, config.resolve.alias, {
      vue$: 'vue/dist/vue.esm.js',
      '@': resolve('src')
    });

    // 开启gzip压缩(需要后端配合设置ngix)
    // if (process.env.NODE_ENV === 'production') {
    //   config.plugins.push(
    //     new CompressionWebpackPlugin(
    //       {
    //         filename: info => {
    //           return `${info.path}.gz${info.query}`
    //         },
    //         algorithm: 'gzip',
    //         threshold: 10240, // 只有大小大于该值的资源会被处理 10240
    //         test: productionGzipExtensions,
    //         minRatio: 0.8, // 只有压缩率小于这个值的资源才会被处理
    //         deleteOriginalAssets: false // 删除原文件
    //       }
    //     )
    //   )
    // }

    // 压缩代码配置
    config.optimization.minimizer = [
      new UglifyJsWebpackPlugin({
       uglifyOptions: {
        compress: {
         drop_console: true,
        },
        sourceMap: false,
        parallel: true, //默认并发运行数：os.cpus().length - 1
       }
      })
     ]

    // jq采用CDN引入
    // config.externals = {
    //   jquery: 'jQuery'
    // }

    // 不解析三方库
    // config.module.noParse = /^(lodash|moment)$/;

    // momentjs按需加载
    config.plugins.push(
      new webpack.ContextReplacementPlugin(/moment[/\\]locale$/, /zh-cn/)
    );

    // sourcemap类型
    config.devtool = process.env.NODE_ENV === 'development' ? 'source-map' : undefined;

  },

  // 仅作用于生产构建
  parallel: require("os").cpus().length > 1,

  css: {
    // Enable CSS source maps.
    // sourceMap: true,
    // loaderOptions: {
    //   sass: {
    //     prependData: `@import "@src/assets/styles/variable.scss";`,
    //   },
    // },
    // extract: true,
  },
  // Configure Webpack's dev server.
  // https://github.com/vuejs/vue-cli/blob/dev/docs/cli-service.md
  devServer: {
    port: '8080',
    disableHostCheck: true,
    // 代理没生效的话，去 apiMap.js 文件里修改，接口已改造成动态域名方案
    proxy: {
      '/apis': {
        // target: 'https://kefu-liaoyg.myyscm.com',
        target: 'https://kefu-songzw.dev.myyscm.com',
        changeOrigin: true,
        pathRewrite: {
          '^/apis': '' //重写接口
        }
      }
    }
  },

  productionSourceMap: process.env.NODE_ENV === 'development',

  chainWebpack: config => {
    // 去掉预检请求处理
    config.plugins.delete('prefetch');

    // 移除 preload 插件，避免加载多余的资源
    // config.plugins.delete('preload');

    // 体积分析插件
    // config
    //   .plugin('webpack-bundle-analyzer')
    //   .use(BundleAnalyzerPlugin);

    // 打包速度分析插件
    // config.plugin('speed')
    //   .use(SpeedMeasureWebpackPlugin);

    // // 按需加载loadsh
    config
      .plugin("loadshReplace")
      .use(new LodashModuleReplacementPlugin());

    // css按需加载
    config.when(process.env.NODE_ENV !== 'development', config => {
      config.plugin('extract-css').tap(options => {
        options[0].filename = 'static/css/[name].[hash:8].css';
        return options;
      })
    })

    // 图片按需加载
    config.module.rule('images')
      .test(/\.(png|jpe?g|gif|webp)(\?.*)?$/)
      .use('image-webpack-loader')
      .loader('image-webpack-loader')
      .options({
        bypassOnDebug: true
      })
      .end();

  }
};

if (process.env.VUE_APP_MODE === 'docs') {
  console.log('====> 构建 docs 模块');
  const _chainWebpack = baseConfig.chainWebpack;
  Object.assign(baseConfig, {
    chainWebpack: config => {
      _chainWebpack && _chainWebpack(config);
      // docs 文档目录的编译
      config.module
        .rule('md-loader')
        .test(/\.md$/)
        .use('vue-loader')
        .loader('vue-loader')
        .options({
          compilerOptions: {
            preserveWhitespace: false
          }
        })
        .end()
        .use('md-enhance-vue')
        .loader('md-enhance-vue')
        .options({
          // 缓存文件目录，不设置的话默认以 md 文件所在目录
          cacheDir: resolve('node_modules')
          // lineNumbers: false,
          // toc: {},
          // anchor: {
          //   permalinkSymbol: "#"
          // }
        })
        .end();

      // 修改 doc 入口文件
      config
        .entry('app')
        .clear()
        .add('./src/docs/doc.main.js')
        .end();
    },
    publicPath: './',
    devServer: {
      port: '8079',
      disableHostCheck: true
    }
  });
}

module.exports = baseConfig;

```

