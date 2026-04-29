### <font style="color:rgb(23, 43, 77);">一、项目现状</font>
+ <font style="color:rgb(23, 43, 77);">项目现技术栈vue版本：2.6.11 ，</font>`<font style="color:rgb(23, 43, 77);">vue-cli</font>`<font style="color:rgb(23, 43, 77);">对应的</font>`<font style="color:rgb(23, 43, 77);">webpack</font>`<font style="color:rgb(23, 43, 77);">版本： 4.46.0。</font>
+ <font style="color:rgb(23, 43, 77);">当前项目开发环境首次构建时间：81s+， 热更新时间：2s+（</font>`<font style="color:rgb(23, 43, 77);">mac m1,</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">在</font>`<font style="color:rgb(23, 43, 77);">windows</font>`<font style="color:rgb(23, 43, 77);">上时间会更长）。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066479929-d8d2567d-2f6e-452a-9b58-4689aa202ee7.png)

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066485598-16ff4351-134e-4dea-a9ce-1910ff48735c.png)

<font style="color:rgb(23, 43, 77);"></font>

<font style="color:rgb(23, 43, 77);">现在项目首次构建时间较长，影响开发效率。</font>

### <font style="color:rgb(23, 43, 77);">二、对比使用webpack进行开发</font>
#### <font style="color:rgb(23, 43, 77);">1、开发环境</font>
<font style="color:rgb(23, 43, 77);">开发环境相较于</font>`<font style="color:rgb(23, 43, 77);">webpack</font>`<font style="color:rgb(23, 43, 77);">,</font>`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">使用原生</font>`<font style="color:rgb(23, 43, 77);">ES</font>`<font style="color:rgb(23, 43, 77);">模块.</font>

<font style="color:rgb(23, 43, 77);">使用</font>`<font style="color:rgb(23, 43, 77);">webpack</font>`<font style="color:rgb(23, 43, 77);">启动本地服务时, 必须优先抓取并构建整个应用,然后才能提供服务.</font>

`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">则在一开始就将应用中的模块区分为 依赖 和 源码 两类.</font>

    - <font style="color:rgb(23, 43, 77);">依赖 大多为在开发时不会变动的纯</font>`<font style="color:rgb(23, 43, 77);">JavaScript</font>`<font style="color:rgb(23, 43, 77);">. 一些较大的依赖处理的代价也很高.依赖也通常会存在多种模块化格式(</font>`<font style="color:rgb(23, 43, 77);">ESM</font>`<font style="color:rgb(23, 43, 77);">或</font>`<font style="color:rgb(23, 43, 77);">CommosJS</font>`<font style="color:rgb(23, 43, 77);">).</font>

`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">使用</font>`<font style="color:rgb(23, 43, 77);">esbuild</font>`<font style="color:rgb(23, 43, 77);">预构建依赖.</font>`<font style="color:rgb(23, 43, 77);">Esbuild</font>`<font style="color:rgb(23, 43, 77);">使用</font>`<font style="color:rgb(23, 43, 77);">Go</font>`<font style="color:rgb(23, 43, 77);">编写,比</font>`<font style="color:rgb(23, 43, 77);">JavaScipt</font>`<font style="color:rgb(23, 43, 77);">编写的打包器预构建依赖快10-100倍.</font>

    - <font style="color:rgb(23, 43, 77);">源码 通常包含一些并非直接是</font>`<font style="color:rgb(23, 43, 77);">JavaScript</font>`<font style="color:rgb(23, 43, 77);">的文件.需要转化(例如</font>`<font style="color:rgb(23, 43, 77);">JSX</font>`<font style="color:rgb(23, 43, 77);">, CSS</font>`<font style="color:rgb(23, 43, 77);">或</font>``<font style="color:rgb(23, 43, 77);">Vue/Svelte</font>`<font style="color:rgb(23, 43, 77);">组件), 时常会被编辑. 同时, 并不是所有源码都需要同时被加载(例如基于路由拆分的代码模块).</font>

`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">以原生的ESM方式提供源码. 这实际上是让浏览器接管了打包程序的部分工作:</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">只需要在浏览器请求源码时进行转换并按需提供源码. 根据情景动态导入代码, 即只在当前屏幕上实际使用时才会被处理.</font>

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066505055-6b589fb3-4dca-475c-8dca-6eb6392d11b1.png)

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066510665-6483b7f3-0450-48a2-96a3-8e0e231ff333.png)

<font style="color:rgb(23, 43, 77);">  
</font>

**<font style="color:rgb(23, 43, 77);">热更新</font>**

<font style="color:rgb(23, 43, 77);">基于打包器启动时, 重建整个包的效率很低. 更新速度会随着应用体积增长而直线下降.</font>

<font style="color:rgb(23, 43, 77);">一些打包器将构建内容存入内存, 这样他们只需要在文件更改时使模块图的一部分失活, 但是仍需要整个重新构建并重载页面.这样的代价很高,并且重新加载页面会消除应用的当前状态, 所以打包器支持了动态模块热重载: 允许一个模块"热替换"它自己, 而不会影响页面其他部分.但是即使采用</font>`<font style="color:rgb(23, 43, 77);">HMR</font>`<font style="color:rgb(23, 43, 77);">模式, 其热更新速度也会随着应用规模的增长而显著下降.</font>

<font style="color:rgb(23, 43, 77);">在</font>`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">中,</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">HMR</font>`<font style="color:rgb(23, 43, 77);">也是基于</font>`<font style="color:rgb(23, 43, 77);">ESM</font>`<font style="color:rgb(23, 43, 77);">上执行的. 当编辑一个文件时,</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">只需要精确地使已编辑的模块与其最近的</font>`<font style="color:rgb(23, 43, 77);">HMR</font>`<font style="color:rgb(23, 43, 77);">边界之间的链失活(大多数时候只是模块本身). 使得无论应用大小如何, HMR始终能保持快速更新</font>

`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">同时利用</font>`<font style="color:rgb(23, 43, 77);">HTTP</font>`<font style="color:rgb(23, 43, 77);">头来加速整个页面的重新加载, 源码模块的请求会根据</font>`<font style="color:rgb(23, 43, 77);">304 Not Modified</font>`<font style="color:rgb(23, 43, 77);">来进行协商缓存, 而依赖模块则会通过</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">Cache-Control: max-age = 31536000, immutable</font>`<font style="color:rgb(23, 43, 77);">进行强缓存, 一旦被缓存将不需要再重新请求.</font>

<font style="color:rgb(23, 43, 77);">  
</font>

#### <font style="color:rgb(23, 43, 77);">2、生产环境</font>
<font style="color:rgb(23, 43, 77);">此次接入方案暂未考虑使用</font>`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">进行生产的打包。主要是因为尽管原生</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">ESM</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">现在得到了广泛支持，但由于嵌套导入会导致额外的网络往返，在生产环境中发布未打包的</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">ESM</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">仍然效率低下（即使使用</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">HTTP/2</font>`<font style="color:rgb(23, 43, 77);">）。为了在生产环境中获得最佳的加载性能，最好还是将代码进行</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">tree-shaking</font>`<font style="color:rgb(23, 43, 77);">、懒加载和</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">chunk</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">分割（以获得更好的缓存）。这样和使用</font>`<font style="color:rgb(23, 43, 77);">webpack</font>`<font style="color:rgb(23, 43, 77);">进行生产环境打包优化不大，且生产环境还是要以稳定为主。</font>

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">注：以上对比资料来自</font>[<font style="color:rgb(0, 82, 204);">vite官方文档</font>](https://cn.vitejs.dev/)<font style="color:rgb(23, 43, 77);">。</font>

<font style="color:rgb(23, 43, 77);">  
</font>

### <font style="color:rgb(23, 43, 77);">三、改动点</font>
#### <font style="color:rgb(23, 43, 77);">1、</font>`<font style="color:rgb(23, 43, 77);">vite.config.js</font>`
<font style="color:rgb(23, 43, 77);">新增</font>`<font style="color:rgb(23, 43, 77);">vite.config.js</font>`<font style="color:rgb(23, 43, 77);">配置文件</font>

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

#### <font style="color:rgb(23, 43, 77);">2、</font>`<font style="color:rgb(23, 43, 77);">index.html</font>`
<font style="color:rgb(23, 43, 77);">在根目录新增</font>`<font style="color:rgb(23, 43, 77);">index.html</font>`<font style="color:rgb(23, 43, 77);">文件。</font>

`<font style="color:rgb(23, 43, 77);">index.html</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">在项目最外层而不是在</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">public</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">文件夹内。这是有意而为之的：在开发期间</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">Vite</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">是一个服务器，而</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">index.html</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">是该</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">Vite</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">项目的入口文件。</font>

```javascript
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

<font style="color:rgb(23, 43, 77);">  
</font>

#### <font style="color:rgb(23, 43, 77);">3、</font>`<font style="color:rgb(23, 43, 77);">/deep/</font>`<font style="color:rgb(23, 43, 77);">改成</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">::v-deep</font>`
<font style="color:rgb(23, 43, 77);">使用</font>`<font style="color:rgb(23, 43, 77);">vscode</font>`<font style="color:rgb(23, 43, 77);">的全局替换即可。</font>

<font style="color:rgb(23, 43, 77);"></font>

#### <font style="color:rgb(23, 43, 77);">4、处理</font>`<font style="color:rgb(23, 43, 77);">require</font>`
`<font style="color:rgb(23, 43, 77);">require</font>`<font style="color:rgb(23, 43, 77);">是</font>`<font style="color:rgb(23, 43, 77);">Commonjs</font>`<font style="color:rgb(23, 43, 77);">的语法，</font>`<font style="color:rgb(23, 43, 77);">ESM</font>`<font style="color:rgb(23, 43, 77);">不支持，需要处理成</font>`<font style="color:rgb(23, 43, 77);">ESM</font>`<font style="color:rgb(23, 43, 77);">识别的语法。</font>

+ `<font style="color:rgb(23, 43, 77);">import</font>`

```javascript
require(../xx/xx.png);
 
=>>
   
import xxxx from '../xx/xx.png';
```

  


+ `**<font style="color:rgb(68, 68, 68);">import</font>**<font style="color:rgb(68, 68, 68);">.meta.url</font>`

`<font style="color:rgb(23, 43, 77);">import.meta.url</font>`<font style="color:rgb(23, 43, 77);">是一个 ESM 的原生功能，会暴露当前模块的</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">URL</font>`<font style="color:rgb(23, 43, 77);">。将它与原生的</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">URL</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">构造器 组合使用，在一个</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">JavaScript</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">模块中，通过相对路径我们就能得到一个被完整解析的静态资源</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">URL</font>`<font style="color:rgb(23, 43, 77);">：</font>

```javascript
const imgUrl = new URL('./img.png', import.meta.url).href
document.getElementById('hero-img').src = imgUrl
```

<font style="color:rgb(23, 43, 77);"></font>

<font style="color:rgb(23, 43, 77);">所以我们可以封装一个方法,然后把它变成全局，以便我们不需引入就可以直接调用：</font>

```javascript
export const getImgFromAssets = path => {\
  return new URL(`../assets/images/${path}`, import.meta.url).href;
}
// 兼容template的场景
Vue.prototype.$getImgFromAssets = getImgFromAssets
// 兼容js里面的场景
window.getImgFromAssets = getImgFromAssets
```

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">具体用法参考：</font>[<font style="color:rgb(0, 82, 204);">wepack快速迁移到vite</font>](https://confluence.mysre.cn/pages/viewpage.action?pageId=53855529)<font style="color:rgb(23, 43, 77);">。</font>

<font style="color:rgb(23, 43, 77);">  
</font>

+ <font style="color:rgb(23, 43, 77);">插件方案：</font>

<font style="color:rgb(23, 43, 77);">可以使用插件，将</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">CommonJs</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">转化成</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">ESModule</font>`<font style="color:rgb(51, 51, 51);">。</font>

```javascript
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

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">三种方法对比来看，方法一和方法二对于旧项目来说，改动量及改动范围太大，且webpack目前不支持</font>`<font style="color:rgb(23, 43, 77);">import.meta.url</font>`<font style="color:rgb(23, 43, 77);">语法，因生产还未引入</font>`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">，所以暂不适用。方案三的改动量最小，但是在实际开发中，少数场景的</font>`<font style="color:rgb(23, 43, 77);">require</font>`<font style="color:rgb(23, 43, 77);">无法处理，需要结合方案一特殊处理。</font>

<font style="color:rgb(23, 43, 77);">  
</font>

#### <font style="color:rgb(23, 43, 77);">5、处理</font>`<font style="color:rgb(23, 43, 77);">require.context</font>`
1. `<font style="color:rgb(23, 43, 77);">import.meta.globEager</font>`

<font style="color:rgb(23, 43, 77);">vite支持使用</font>`<font style="color:rgb(44, 62, 80);"> </font><font style="color:rgb(23, 43, 77);">import.meta.glob</font><font style="color:rgb(44, 62, 80);"> </font>`<font style="color:rgb(44, 62, 80);">函数从文件系统导入多个模块，也支持使用</font><font style="color:rgb(44, 62, 80);"> </font>`<font style="color:rgb(23, 43, 77);">import.meta.globEager</font>`<font style="color:rgb(44, 62, 80);">引入所有的模块。</font>

<font style="color:rgb(44, 62, 80);">当前项目使用到</font>`<font style="color:rgb(23, 43, 77);">require.context</font>`<font style="color:rgb(23, 43, 77);">场景可以用</font>`<font style="color:rgb(23, 43, 77);">import.meta.globEager</font>`<font style="color:rgb(23, 43, 77);">处理。</font>

```javascript
const moduleFiles = require.context('./modules', false, /\.js$/);
 
==>>
   
const files= import.meta.globEager('./modules/*.js')
```

<font style="color:rgb(23, 43, 77);">  
</font>

1. <font style="color:rgb(23, 43, 77);">插件方案</font>

<font style="color:rgb(23, 43, 77);">可以使用插件，在</font>`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">中支持</font>`<font style="color:rgb(23, 43, 77);">require.context</font>`<font style="color:rgb(23, 43, 77);">。</font>

```plain

npm i @originjs/vite-plugin-require-context -D
```



```plain

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

<font style="color:rgb(23, 43, 77);">因</font>`<font style="color:rgb(23, 43, 77);">import.meta.globEager</font>`<font style="color:rgb(23, 43, 77);">只支持在</font>`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">环境， 故当前方案采用插件方案，目前使用正常。</font>

<font style="color:rgb(23, 43, 77);">  
</font>

#### <font style="color:rgb(23, 43, 77);">6、vite相关依赖</font>
```plain
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

<font style="color:rgb(23, 43, 77);">  
</font>

#### <font style="color:rgb(23, 43, 77);">7、完整</font>`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">配置</font>
```plain
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



### <font style="color:rgb(23, 43, 77);">四、遇到的问题:</font>
#### <font style="color:rgb(23, 43, 77);">1、</font>`<font style="color:rgb(23, 43, 77);">jsx</font>`<font style="color:rgb(23, 43, 77);">报错</font>
![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066749803-952eba40-730c-4a98-bb31-c3eba2edbcbc.png)

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">解决方法:</font>

```plain
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

#### <font style="color:rgb(23, 43, 77);">2、</font><font style="color:rgb(23, 43, 77);">main.js</font>
![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066783775-20a6ab6a-0e7d-40d3-ab1a-55d12040c8ab.png)<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">解决方案：</font>



```plain
new Vue({
  router,
  store,
  components: { App },
  render: h => h(App)
}).$mount('#app');
```

<font style="color:rgb(23, 43, 77);"></font>

#### <font style="color:rgb(23, 43, 77);">3、缓存问题</font>
<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">以下问题主要是因为：vite会在浏览器解析后的依赖请求会以</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">HTTP</font>`<font style="color:rgb(23, 43, 77);"> </font><font style="color:rgb(23, 43, 77);">头</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">max-age=31536000,immutable</font><font style="color:rgb(23, 43, 77);"> </font>`<font style="color:rgb(23, 43, 77);">强缓存，以提高在开发时的页面重载性能。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066816666-80214e06-34a3-46ab-82a1-e36639611686.png)

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">解决方案:</font>

<font style="color:rgb(23, 43, 77);">出现该问题是，关闭浏览器缓存，并刷新当前页面。</font>

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">参考：</font>

[<font style="color:rgb(0, 82, 204);">https://cn.vitejs.dev/guide/dep-pre-bundling.html#caching</font>](https://cn.vitejs.dev/guide/dep-pre-bundling.html#caching)

[<font style="color:rgb(0, 82, 204);">https://github.com/vitejs/vite/issues/108</font>](https://github.com/vitejs/vite/issues/108)

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">  
</font>

#### <font style="color:rgb(23, 43, 77);">4、从public文件夹下导入文件时出现警告</font>
![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066828137-1a234896-9f63-4f4e-b100-a7ed6a9b3312.png)

`<font style="color:rgb(23, 43, 77);">vite</font>`<font style="color:rgb(23, 43, 77);">官方不建议从</font>`<font style="color:rgb(23, 43, 77);">public</font>`<font style="color:rgb(23, 43, 77);">目录导入文件，建议移入</font>`<font style="color:rgb(23, 43, 77);">src</font>`<font style="color:rgb(23, 43, 77);">目录下，但当前项目场景不适合。可以设置增加下面的配置，隐藏警告信息。  
</font>

```plain
// vite.config.js
publicDir: false,
```

<font style="color:rgb(23, 43, 77);">参考：</font>[<font style="color:rgb(0, 82, 204);">https://github.com/vitejs/vite/issues/6700</font>](https://github.com/vitejs/vite/issues/6700)

<font style="color:rgb(23, 43, 77);">  
</font>

#### <font style="color:rgb(23, 43, 77);">5、异步导入代码警告</font>
![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066849372-2c802dbf-d43d-4fd0-bb57-c49dc26fc38c.png)

<font style="color:rgb(23, 43, 77);">解决方法：</font>

1. <font style="color:rgb(23, 43, 77);">按照上面的提示方法，添加注释来隐藏该警告</font>

<font style="color:rgb(23, 43, 77);">  
</font>

```plain
import(/* @vite-ignore */../components/${this.curShowComponent}${path ?/${path}: ''});
```

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">备注： 此方法虽然不会再显示警告，但会引起另一个问题。但我们再修改动态导入的组件时，热更新会报错 。</font>

<font style="color:rgb(23, 43, 77);">  
</font>

1. <font style="color:rgb(23, 43, 77);">根据要求的异步导入路径规范，进行修改（推荐方法）</font>

```plain

import(../components/${this.curShowComponent} + (path ? /${path} : '') + '/index.vue');
```

<font style="color:rgb(23, 43, 77);">  
</font>

<font style="color:rgb(23, 43, 77);">上面动态导入的路径问题是无文件后缀名。  
</font><font style="color:rgb(23, 43, 77);">此方法，消除了报错， 也解决了上面的热更新异常的问题。</font>



#### <font style="color:rgb(23, 43, 77);">6、使用代理页面会自动刷新，且热更新不生效</font>
`<font style="color:rgb(23, 43, 77);">vite.config.js</font>`<font style="color:rgb(23, 43, 77);">增加以下配置</font>

```plain
server: {
  hmr: {
    protocol: 'ws',
    host: '127.0.0.1'
  }
}
```

<font style="color:rgb(23, 43, 77);">参考：</font>[<font style="color:rgb(0, 82, 204);">https://github.com/vitejs/vite/issues/2968</font>](https://github.com/vitejs/vite/issues/2968)

### <font style="color:rgb(23, 43, 77);">五、优化效果</font>
<font style="color:rgb(23, 43, 77);">迁移vite后开发环境的首次构建速度为0.5s左右，提速效果显著，大大提高了开发效率。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/25743026/1769066910696-57700eb9-4ec0-4e83-ac22-6a756ba501d9.png)

