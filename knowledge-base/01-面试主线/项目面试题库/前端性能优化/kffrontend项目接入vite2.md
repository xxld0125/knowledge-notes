### 一、项目现状
+ 项目现技术栈vue版本：2.6.11 ，`vue-cli`对应的`webpack`版本： 4.46.0。
+ 当前项目开发环境首次构建时间：81s+， 热更新时间：2s+（`mac m1,` 在`windows`上时间会更长）。

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649758519809-230cddba-c20a-4f58-91d2-15718413fcfa.png)

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1651028558927-6631ec8d-dcc5-41e0-a25b-14d1ee417ef7.png)



现在项目首次构建时间较长，影响开发效率。



### 二、对比使用webpack进行开发
#### 1、开发环境
开发环境相较于`webpack`,`vite`使用原生`ES`模块.

使用`webpack`启动本地服务时, 必须优先抓取并构建整个应用,然后才能提供服务.

`vite`则在一开始就将应用中的模块区分为 依赖 和 源码 两类.

    - 依赖 大多为在开发时不会变动的纯`JavaScript`. 一些较大的依赖处理的代价也很高.依赖也通常会存在多种模块化格式(`ESM`或`CommosJS`).

`vite`使用`esbuild`预构建依赖.`Esbuild`使用`Go`编写,比`JavaScipt`编写的打包器预构建依赖快10-100倍.

    - 源码 通常包含一些并非直接是`JavaScript`的文件.需要转化(例如`JSX`, CSS`或``Vue/Svelte`组件), 时常会被编辑. 同时, 并不是所有源码都需要同时被加载(例如基于路由拆分的代码模块).

`vite`以原生的ESM方式提供源码. 这实际上是让浏览器接管了打包程序的部分工作: `vite` 只需要在浏览器请求源码时进行转换并按需提供源码. 根据情景动态导入代码, 即只在当前屏幕上实际使用时才会被处理.

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649913341269-03bfe44e-b905-4623-8851-fe5b6a0b963c.png)

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649913371609-4d95bf0b-412c-41df-bf8a-5b089ed35482.png)

**热更新**

基于打包器启动时, 重建整个包的效率很低. 更新速度会随着应用体积增长而直线下降.

一些打包器将构建内容存入内存, 这样他们只需要在文件更改时使模块图的一部分失活, 但是仍需要整个重新构建并重载页面.这样的代价很高,并且重新加载页面会消除应用的当前状态, 所以打包器支持了动态模块热重载: 允许一个模块"热替换"它自己, 而不会影响页面其他部分.但是即使采用`HMR`模式, 其热更新速度也会随着应用规模的增长而显著下降.

在`vite`中, `HMR`也是基于`ESM`上执行的. 当编辑一个文件时, `vite`只需要精确地使已编辑的模块与其最近的`HMR`边界之间的链失活(大多数时候只是模块本身). 使得无论应用大小如何, HMR始终能保持快速更新

`vite`同时利用`HTTP`头来加速整个页面的重新加载, 源码模块的请求会根据`304 Not Modified`来进行协商缓存, 而依赖模块则会通过 `Cache-Control: max-age = 31536000, immutable`进行强缓存, 一旦被缓存将不需要再重新请求.



#### 2、生产环境
此次接入方案暂未考虑使用`vite`进行生产的打包。主要是因为尽管原生 `ESM` 现在得到了广泛支持，但由于嵌套导入会导致额外的网络往返，在生产环境中发布未打包的 `ESM` 仍然效率低下（即使使用 `HTTP/2`）。为了在生产环境中获得最佳的加载性能，最好还是将代码进行 `tree-shaking`、懒加载和 `chunk` 分割（以获得更好的缓存）。这样和使用`webpack`进行生产环境打包优化不大，且生产环境还是要以稳定为主。



注：以上对比资料来自[vite官方文档](https://cn.vitejs.dev/)。



### 三、改动点
#### 1、`vite.config.js`
新增`vite.config.js`配置文件

```javascript
import { defineConfig } from 'vite';
import { createVuePlugin } from 'vite-plugin-vue2';
import legacy from '@vitejs/plugin-legacy';
import path from 'path';

const resolve = dir => {
  return path.resolve(__dirname, dir);
};

export default defineConfig({
  plugins: [
    createVuePlugin({}), // 如果要兼容vue2.x就需要引入此插件
    legacy({
      // 此插件主要用于生产打包使用，打包出兼容老浏览器的代码
      targets: ['defaults', 'not IE 11']
    }),
  ],
  resolve: {
    alias: {
      '@': resolve('src'),
      '~@': resolve('src')
    },
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'] //默认不处理vue文件
  },
});

```

#### 
#### 2、`index.html`
在根目录新增`index.html`文件。

`index.html `在项目最外层而不是在 `public` 文件夹内。这是有意而为之的：在开发期间 `Vite` 是一个服务器，而 `index.html` 是该 `Vite` 项目的入口文件。



```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0" />
    <meta
          name="viewport"
          content="width=device-width, initial-scale=1.0, maximum-scale=1.0,
                   user-scalable=no"
          />
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```



#### 3、`/deep/`改成 `::v-deep`
使用`vscode`的全局替换即可。



#### 4、处理`require`
`require`是`Commonjs`的语法，`ESM`不支持，需要处理成`ESM`识别的语法。

+ `import`

```javascript
require(../xx/xx.png);

=>>
  
import xxxx from '../xx/xx.png';
```



+ `**<font style="color:rgb(68, 68, 68);">import</font>**<font style="color:rgb(68, 68, 68);background-color:rgb(240, 240, 240);">.meta.url</font>`

`import.meta.url`是一个 ESM 的原生功能，会暴露当前模块的 `URL`。将它与原生的 `URL` 构造器 组合使用，在一个 `JavaScript` 模块中，通过相对路径我们就能得到一个被完整解析的静态资源 `URL`：

```javascript
const imgUrl = new URL('./img.png', import.meta.url).href
document.getElementById('hero-img').src = imgUrl 
```



所以我们可以封装一个方法,然后把它变成全局，以便我们不需引入就可以直接调用：

```javascript
export const getImgFromAssets = path => {\
  return new URL(`../assets/images/${path}`, import.meta.url).href;
}
// 兼容template的场景
Vue.prototype.$getImgFromAssets = getImgFromAssets
// 兼容js里面的场景
window.getImgFromAssets = getImgFromAssets
```

具体用法参考：[wepack快速迁移到vite](https://confluence.mysre.cn/pages/viewpage.action?pageId=53855529)。



+ 插件方案：

可以使用插件，将<font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">CommonJs</font>`<font style="color:rgb(51, 51, 51);"> 转化成 </font>`<font style="color:rgb(51, 51, 51);">ESModule</font>`<font style="color:rgb(51, 51, 51);">。</font>

```bash
npm i vite-plugin-commonjs -D
```

```javascript
import { defineConfig } from 'vite';
import { vitePluginCommonjs } from 'vite-plugin-commonjs;
// ...

export default defineConfig({
  // ...
  plugins: [
    vitePluginCommonjs(),
  ],
  // ...
});

```



三种方法对比来看，方法一和方法二对于旧项目来说，改动量及改动范围太大，且webpack目前不支持`import.meta.url`语法，因生产还未引入`vite`，所以暂不适用。方案三的改动量最小，但是在实际开发中，少数场景的`require`无法处理，需要结合方案一特殊处理。



#### 5、处理`require.context`
1. `import.meta.globEager`

vite支持使用`<font style="color:rgb(44, 62, 80);"> </font>import.meta.glob<font style="color:rgb(44, 62, 80);"> </font>`<font style="color:rgb(44, 62, 80);">函数从文件系统导入多个模块，也支持使用 </font>`import.meta.globEager`<font style="color:rgb(44, 62, 80);">引入所有的模块。</font>

<font style="color:rgb(44, 62, 80);">当前项目使用到</font>`require.context`场景可以用`import.meta.globEager`处理。

```javascript
const moduleFiles = require.context('./modules', false, /\.js$/);

==>>
  
const files= import.meta.globEager('./modules/*.js')
```



2. 插件方案

可以使用插件，在`vite`中支持`require.context`。

```bash
npm i @originjs/vite-plugin-require-context -D
```

```javascript
import { defineConfig } from 'vite';
import viteRequireContext from '@originjs/vite-plugin-require-context';
// ...

export default defineConfig({
  // ...
  plugins: [
    viteRequireContext()
  ]
  // ...
});
```

因`import.meta.globEager`只支持在`vite`环境， 故当前方案采用插件方案，目前使用正常。



#### 6、vite相关依赖
```json
{
  "scripts": {
    "vite": "VITE_NODE_ENV=dev vite"
  },
  "devDependencies": {
    "@originjs/vite-plugin-require-context": "^1.0.9",
    "@vitejs/plugin-legacy": "^1.6.4",
    "dotenv": "^16.0.0",
    "sass": "^1.44.0",
    "vite": "^2.6.4",
    "vite-plugin-commonjs": "^0.2.6",
    "vite-plugin-html": "^3.0.6",
    "vite-plugin-importer": "0.2.5",
    "vite-plugin-vue2": "latest",
    "vue-loader": "^14.2.2",
  }
}
```



#### 7、完整`vite`配置
```javascript
import { defineConfig } from 'vite';
import { createVuePlugin } from 'vite-plugin-vue2';
import legacy from '@vitejs/plugin-legacy';
import path from 'path';
import { vitePluginCommonjs } from 'vite-plugin-commonjs';
import viteRequireContext from '@originjs/vite-plugin-require-context';

const resolve = dir => {
  return path.resolve(__dirname, dir);
};

export default defineConfig({
  root: './', // 项目根目录（index.html 文件所在的位置）可以是一个绝对路径，或者一个相对于该配置文件本身的相对路径。
  publicDir: false, // 作为静态资源服务的文件夹.该值可以是文件系统的绝对路径，也可以是相对于项目的根目录的相对路径。
  base: './', // 公共基础路径。改值可以是绝对路径或空字符串
  plugins: [
    createVuePlugin({
      jsx: true
    }), // 如果要兼容vue2.x就需要引入此插件
    legacy({
      // 此插件主要用于生产打包使用，打包出兼容老浏览器的代码
      targets: ['defaults', 'not IE 11']
    }),
    vitePluginCommonjs(),
    viteRequireContext()
  ],
  resolve: {
    alias: {
      '@': resolve('src'),
      '~@': resolve('src')
    },
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'] //默认不处理vue文件
  },
  server: {
    host: '0.0.0.0',
    open: false,
    port: 3100,
    proxy: {},
    hmr: {
      protocol: 'ws',
      host: '127.0.0.1'
    }
  }
});

```



### 四、遇到的问题:
#### 1、使用`jsx`报错


![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649333972556-7b7882e7-9484-4111-865c-84951418a5ee.png)



解决方法:



```javascript
// .vue
<script lang="jsx">
  //...
</script>


// vite.config.js

import { createVuePlugin } from 'vite-plugin-vue2';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    createVuePlugin({
      jsx: true
    }),
  ],
});
```



#### 2、`main.js`
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1651063286997-c6bde878-4a31-4eed-838e-4dafbbeaefc0.png)

解决方案：

```javascript
new Vue({
  router,
  store,
  components: { App },
  render: h => h(App)
}).$mount('#app');
```



#### 3、缓存问题
以下问题主要是因为：vite会在浏览器解析后的依赖请求会以 `HTTP` 头 `max-age=31536000,immutable `强缓存，以提高在开发时的页面重载性能。

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1649334090184-24f05106-06f3-4d91-8e72-10e43d2a4d4f.png)



解决方案:

出现该问题是，关闭浏览器缓存，并刷新当前页面。



参考资料：

[https://cn.vitejs.dev/guide/dep-pre-bundling.html#caching](https://cn.vitejs.dev/guide/dep-pre-bundling.html#caching)

[https://github.com/vitejs/vite/issues/108](https://github.com/vitejs/vite/issues/108)



#### 4、从public文件夹下导入文件时出现警告
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1651065604521-89e3fcfe-7ec8-4b99-80bf-0c762c286819.png)

`vite`官方不建议从`public`目录导入文件，建议移入`src`目录下，但当前项目场景不适合。可以设置增加下面的配置，隐藏警告信息。

```javascript
// vite.config.js
publicDir: false,
```



参考资料：

[https://github.com/vitejs/vite/issues/6700](https://github.com/vitejs/vite/issues/6700)



#### 5、异步导入代码警告
#### ![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1651067053614-9b1d4742-72eb-421c-b52f-f2d424bb6d87.png)解决方法：
1.  按照上面的提示方法，添加注释来隐藏该警告

```javascript
import(/* @vite-ignore */../components/${this.curShowComponent}${path ?/${path}: ''});
```

  
备注： 此方法虽然不会再显示警告，但会引起另一个问题。但我们再修改动态导入的组件时，热更新会报错 。



2.  根据要求的异步导入路径规范，进行修改（推荐方法）

```javascript
import(../components/${this.curShowComponent} + (path ? /${path} : '') + '/index.vue');
```

  
上面动态导入的路径问题是无文件后缀名。  
此方法，消除了报错， 也解决了上面的热更新异常的问题。



#### 6、使用代理页面会自动刷新，且热更新不生效
`vite.config.js`增加以下配置

```git
server: {
  hmr: {
    protocol: 'ws',
    host: '127.0.0.1'
  }
}
```

参考资料：

[https://cloud.tencent.com/developer/article/1945422](https://cloud.tencent.com/developer/article/1945422)

[https://github.com/vitejs/vite/issues/2968](https://github.com/vitejs/vite/issues/2968)



### 五、优化效果
迁移vite后开发环境的首次构建速度为0.5s左右，提速效果显著，大大提高了开发效率。

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1651027149071-0a22dfe1-62e5-40c5-beb1-b00b3f995f9d.png)

