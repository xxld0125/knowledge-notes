### 一、DIV + CSS布局的优缺点


#### 1优点：代码精简，且结构与样式分离，易于维护


+ 代码量减少了，减少了大量的带宽，页面加载的也更快，提升了用户的体验
+ 对 SEO 搜索引擎更加友好，且 H5 又新增了许多语义化标签更是如此
+ 允许更多炫酷的页面效果，丰富了页面
+ 符合 W3C 标准，保证网站不会因为网络应用的升级而被淘汰



#### 1缺点：


+ 不同浏览器对 Web 标准默认值不同，所以更容易出现对浏览器的兼容性问题。



### 二、如何解决a标签点击后hover事件实现的问题


改变a标签CSS属性的排列问题；



`LoVe HAte `原则



link -> visited -> hover -> active



+ `a:link`：简写 `a`，未访问的样式
+ `a:visited`：已经访问的样式
+ `a:hover`：鼠标移上去时的样式
+ `a:active`：鼠标按下的样式



在 CSS 中，如果对于相同元素针对不同条件的定义，适宜将最一般的条件放在最上面，依次向下，保证最下面的是最特殊的条件（可以理解为样式覆盖）。



这样，浏览器显示元素的时候，才会从特殊到一半、逐级向上验证条件。



### 三、响应式布局和流体布局


1、**响应式**网站设计（`Responsive Web design`）是一个网站能够兼容多个终端，而不是为每一个终端做一个特定的版本。



2、**流式布局** 使用非固定像素来定义网页内容，`也就是百分比布局`，通过盒子的宽度设置成百分比来根据屏幕的宽度来进 行伸缩，不受固定像素的限制，内容向两侧填充。



基本原理是通过媒体查询（`@media`）检测不同的设备屏幕尺寸做处理。



好处：对某些数据的修改就能自动更新视图，让开发者不需要操作 DOM，有更多的时间去思考完成业务逻辑。



### 四、文档流


文档流：将窗体自上而下分成一行一行，并在每行中按从左至右一次排放元素，成为文档流，也就普通流。



脱离文档流：脱离文档流的元素，将不再在文档流占据空间，而是漂浮在文档流上方。



+ `float: left/right`：使用之后会脱离，但是其他盒子会环绕该元素的周围。
+ `position: absolute/fixed`：`absolute` 为绝对定位，脱离文档流之后还是会相对于该元素的父类（做了 `relative/absolute` 定位的父类）进行偏移。而 `fixed` 就是完全脱离文档流，相对于 HTML （整个浏览器窗口）的形式展示。



### 五、块级格式化上下文（BFC:Block Formatting Context）


#### 5.1定义：


BFC 是Block Formatting Context（块级格式化上下文）, 是指页面上一个隔离的独立容器，容器内部的子元素不会影响到外面的元素，反之外面的元素也不会影响容器里面的元素。



#### 5.2布局规则：


+ 内部的Box会在垂直方向，一个接一个地放置；
+ 同一个BFC的两个相邻Box的margin会重叠(不同BFC下的相邻元素不会发生margin重叠)；
+ 每个元素的margin box的左边，与包含块border box 的左边相接触。即使存在浮动也是如此；
+ BFC区域不会与float box 重叠(不会与外部浮动元素重叠)；
+ BFC就是页面上的一个隔离的独立容器，容器里面的子元素不会影响到外部元素，反之也如此；
+ 计算BFC的高度时，浮动元素也参与计算(闭合浮动，可以包含浮动元素)；



#### 5.3产生BFC的条件：


+ 根元素；
+ `float`属性不为none；
+ `position`为absolute或 `fixed`；
+ display为 `inline-block`、`table-cell`、`table-caption`、`flex`、`inline-flex`；
+ `overflow`不为 `visible`；



#### 5.4主要用途：


+ 解决margin叠加的问题；
+ 用于布局、BFC不会与浮动盒子叠加；
+ 用于清除浮动，给浮动元素的父元素设置；



### 六、盒子模型


`box-sizing: content-box`。标准盒子，总宽度等于：`width + 2*padding + 2*border + 2*margin`。



`box-sizing: border-box`。IE 盒子，总宽度等于：`width + margin`。IE 盒子的 `width` 包含了 `width`、`padding` 和 `border` 属性。



### 七、link和@import的区别


#### 7.1CSS 引入方式有：


+ 内联：`style` 属性（`style="color: red"`）：通常在开发的临时测试使用；
+ 内嵌：`style` 标签（`<style></style>`）：加载速度快，但改变麻烦。可以减少HTTP请求。
+ 外链：`link` 标签（`<link href="index.css">`：方便多个网页同时使用一个样式表。
+ 导入：`@import`（`@import url('index.css')` 或者 `@import 'index.css'`）：页面加载完成后，再导入样式表，会导致加载页面的前几秒页面没有样式，然后突然出现样式。



#### 7.2 `link` 和 `@import` 区别：


+ `link` 是 `XHTML` 标签，除了加载 `CSS` 外，还可以定义 `RSS` ，`rel`链接属性等作用；`@import`属于 `CSS` 范畴，只能加载 `CSS`。
+ `link` 引用 `CSS` 时，在页面载入时同时加载；`@import` 需要页面网页完全载入以后加载。
+ `link` 是 `XHTML` 标签，无兼容问题；`@import` 是在 `CSS2.1` 提出的，低版本的浏览器不支持。
+ `link` 支持使用 `Javascript` 控制 `DOM` 去改变样式；而 `@import` 不支持。



### 八、逐渐增加和优雅降级


关键的区别是他们所侧重的内容，以及这种不同造成的工作流程的差异。



+ **优雅降级**：一开始就构建完整的功能，然后再针对低版本浏览器进行兼容。
+ **渐进增强**：针对低版本浏览器进行构建页面，保证最基本的功能，然后再针对高级浏览器进行效果、交互等改进和追加功能达到更好的用户体验。



区别：



+ 优雅降级是从复杂的现状开始，并试图减少用户体验的供给
+ 渐进增强则是从一个非常基础的，能够起作用的版本开始，并不断扩充，以适应未来环境的需要
+ 降级（功能衰减）意味着往回看；而渐进增强则意味着朝前看，同时保证其根基处于安全地带



### 九、CSS实现垂直居中


+ **方法一：已知宽高-absolute**



```css
.box {
  position: relative;
}
.box-center{
  position: absolute;
  left: 50%;
  top: 50%;
  margin： -50%的height 0 0 -50%的width
}
```



+  **方法二：未知宽高-使用 transform**  
父盒子设置：`display: relative`  
div 设置： 



```css
div {
  transform: translate(-50%, -50%);
  position: absolute;
  top: 50%;
  left: 50%;
}
```



+   **方法三：Flex 布局**



```css
.box {
  display: flex;
  justify-content: center;
  align-items: center;
}
.box-center{
}
```



+  ** 方法四：table布局**



```css
.box {
  display:table-cell;
  text-align: center; // 行内元素
  vertical-align: middle;
}
.box-center{
  display: inline-block;// 行内元素
  margin ： 0 auto;// 块级元素
}
```



+   **方法五：**grid布局



```css
.box {
  display：grid;
  justify-items：center;
  align-items：center
}
.box-center{
}
```



### 十、CSS单位


+ **px**



`px` 是像素（`pixel`）的缩写，相对长度单位，是网页设计常用的基本基本单位，它是相对于显示器屏幕分辨率而言的。



+ **em**



`em` 是相对长度单位，相对于对象内文本的字体尺寸（参考物是父元素的 `font-size`。



如果当前父元素的字体元素未设置，则相对于浏览器的默认字体尺寸设置。



+ **rem**



`rem` 是相对于 HTML 根元素的字体大小（`font-size`）来计算的长度单位。



如果你没有设置 HTML 字体大小，那么以浏览器默认为主，一般为 `16px`。



+ **vw/vh**



`vw` 和 `vh` 是相对于 `viewport` - 相对视口的宽度或者高度而定的。



一般来说：`1vw = npx / 100`，即浏览器宽度为 `200px` 的时候，`1vw = 200px / 100`，即 `1vw = 2px`。



### 十一、CSS设置隐藏


+ `display: none`：彻底消失，会导致浏览器回流和重绘，不能再触发点击事件。
+ `visibility: hidden`：元素隐藏，空间仍保留，会导致重绘，但是不能再触发点击事件。
+ `opacity: 0`：设置为透明，相当于它还在那里，但是你看不到，可以触发点击事件。
+ `position + z-index`：元素存在，但是看不到，也不能再触发点击事件。



### 十二、CSS选择器


#### 12.1CSS 选择器及样式优先级：


+ 在属性后面使用 `!important` 会覆盖页面任意位置定义的元素样式
+ 作为 `style` 属性写在元素内的样式（行内样式）
+ `id` 选择器
+ 类选择器 | 伪类选择器 | 属性选择器（后面样式覆盖前面样式）
+ 标签选择器
+ 通配符选择器
+ 浏览器自定义样式或继承样式



#### 12.2权重算法：


+ `！important`：infinty
+ `行间样式`：1000
+ `id` :100
+ `class/属性/伪类`：10
+ `标签/伪标签`：1



#### 12.3属性继承：


+ **可继承的属性**:font-size,font-family,color等;
+ **不可继承的样式**：border,padding,margin,width,height等;



#### 12.4CSS3新增得到伪类


p:first-of-type 选择属于其父元素的首个元素



p:last-of-type 选择属于其父元素的最后元素  
p:only-of-type 选择属于其父元素唯一的元素  
p:only-child 选择属于其父元素的唯一子元素  
p:nth-child(2) 选择属于其父元素的第二个子元素  
:enabled :disabled 表单控件的禁用状态。  
:checked 单选框或复选框被选中。



### 十三、层叠上下文


层叠上下文（`stacking context`），是 HTML 中一个三维的概念。在 CSS2.1 规范中，每个盒模型的位置是三维的，分别是平面画布上的 X 轴，Y 轴以及表示层叠的 Z 轴。



一般情况下，元素在页面上沿 X 轴 Y 轴平铺，我们察觉不到它们在 Z 轴上的层叠关系。



而一旦元素发生堆叠，这时就能发现某个元素可能覆盖了另一个元素或者被另一个元素覆盖。



**触发条件**：



+ 根层叠上下文（`HTML`）
+ `position`
+ CSS3 属性
+  
    - `flex`
    - `transform`
    - `opacity`
    - `filter`
    - `will-change`
    - `-webkit-overflow-scrolling`



**层叠等级**：层叠上下文在 Z 轴上的排序



+ 在同一层叠上下文中，层叠等级才有意义
+ `z-index` 的优先级最高



![](https://mmbiz.qpic.cn/mmbiz/P8CbrweAZpAiaGOrntA3xS9HOGm3qbsF9g9cPr2BL2YibcTS81iaA6EcYR3YmDJwPmgnVichH1dswMQAzk647t7fpQ/640?wx_fmt=other&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



### 十四、display和position


#### 14.1 display


```css
div {
  display: none;
}
```



+ `inline`：（默认）内联
+ `none`：隐藏
+ `block`：块显示
+ `table`：表格显示
+ `inline-block`：内联块



#### 14.2 position


```css
div {
  position: absolute;
}
```



+ `static`：默认位置。不需要特别声明，不常用。
+ `relative`：相对定位。相对于元素默认的位置进行定位，设置 `top/left/right/bottom` 后的元素仍占据空间。
+ `absolute`：绝对定位。如果父元素设置了 `position: absolute/relative`，那么这个设置成立。它会根据上一个设置了 `absolute/relative` 的元素进行偏移。
+ `fixed`：固定定位。相对于整个浏览器窗口进行定位，无论页面怎么滚动。
+ `sticky`：黏性定位。屏幕范围内该元素位置不受影响，超出范围后，会变成 `fixed`，根据设置的 `left/top` 等属性成固定的效果。



### 十五、CSS3


#### 15.1 新特性


+ `RGBA` 透明度、`hsla`(h:色相”，“s：饱和度”，“l：亮度”，“a：透明度”)(不会继承给后代)
+ `background-image`、`background-origin(content-box/padding-box/border-box)`、`background-size`、`background-repeat`
+ `word-wrap`：对长的不可分割单词换行，例如 `word-wrap：break-word`
+ 文字阴影：`text-shadow: 5px 5px 5px #FF0000;`，对应水平阴影，垂直阴影，模糊距离，阴影颜色
+ `font-face` 属性：定义自己的字体
+ 圆角（边框半径）：`border-radius` 属性用于创建圆角
+ 边框图片：`border-image: url(border.png) 30 30 round`
+ 盒阴影：`box-shadow: 10px 10px 5px #888888`
+ 媒体查询：定义两套 CSS，当浏览器的尺寸变化时会采用不同的属性
+ transform(转换,适用于2D/3D转换)，translate(改变元素位置)、animation(动画)、transition(状态过渡)等
+ 怪异盒模型
+ 新增选择器
+ flex布局、grid布局
+ filter(滤镜)
+ Gredient(渐变)



#### 15.2 Flexbox 弹性盒布局模型


该布局模型的目的是提供一种更加高效的方式来对容器中的条目进行布局、对齐和分配空间。



在传统的布局方式中，`block` 布局是把块在垂直方向从上到下依次排列的；而 `inline`布局则是在水平方向来排列。



弹性盒布局并没有这样内在的方向限制，可以由开发人员自由操作。



试用场景：弹性布局适合于移动前端开发，在 Android 和 IOS 上也完美支持。



### 十六、CSS优化


+ 避免过度约束
+ 避免后代选择符
+ 避免链式选择符
+ 使用紧凑的语法
+ 避免不必要的命名空间
+ 避免不必要的重复
+ 最好使用表示语义的名字。一个好的类名应该是描述他是什么而不是像什么
+ 避免 `!important`，可以选择其他选择器
+ 尽可能的精简规则，你可以合并不同类里的重复规则



#### 16.1 CSS 匹配规则


CSS 选择器的解析是从右向左解析的。



若从左向右的匹配，发现不符合规则，需要进行回溯，会损失很多性能。



若从右向左匹配，先找到所有的最右节点，对于每一个节点，向上寻找其父节点直到找到根元素或满足条件的匹配规则，则结束这个分支的遍历。



两种匹配规则的性能差别很大，是因为从右向左的匹配在第一步就筛选掉了大量的不符合条件的最右节点（叶子节点），而从左向右的匹配规则的性能都浪费在了失败的查找上面。



#### 16.2 CSS 的 style 标签位置


页面加载自上而下，当然是先加载样式。



写在 `body` 标签后由于浏览器以逐行方式对 HTML 文档进行解析，当解析到写在尾部的样式表（外联或写在 `style` 标签）会导致浏览器停止之前的渲染，等待加载且解析样式表完成之后重新渲染，在 Windows 的 IE 下可能会出现 FOUC 现象（即样式失效导致的页面闪烁问题）。



#### 16.3减少重排和不必要的重绘


##### 1、减少重排：


重排会导致浏览器重新计算整个文档，重新构建渲染树，这一过程会降低浏览器的渲染速度。如下所示，有很多操作会触发重排，我们应该避免频繁触发这些操作。



1. 改变 `font-size`和 `font-family`
2. 改变元素的内外边距
3. 通过JS改变CSS类
4. 通过JS获取DOM元素的位置相关属性（如width/height/left等）
5. CSS伪类激活
6. 滚动滚动条或者改变窗口大小



此外，我们还可以通过[CSS Trigger](https://csstriggers.com/)15查询哪些属性会触发重排与重绘。



值得一提的是，某些CSS属性具有更好的重排性能。如使用 `Flex`时，比使用 `inline-block`和 `float`时重排更快，所以在布局时可以优先考虑 `Flex`。



##### 2、减少不必要的重绘：


当元素的外观（如color，background，visibility等属性）发生改变时，会触发重绘。在网站的使用过程中，**重绘是无法避免的**。不过，浏览器对此做了优化，它会将多次的重排、重绘操作合并为一次执行。不过我们仍需要**避免不必要的重绘**，如页面滚动时触发的hover事件，可以在滚动的时候禁用hover事件，这样页面在滚动时会更加流畅。



#### 16.4使用Link导入css，不使用@import()方法；


#### 16.5减少使用昂贵的属性
在浏览器绘制屏幕时，**所有需要浏览器进行操作或计算的属性相对而言都需要花费更大的代价**。当页面发生重绘时，它们会降低浏览器的渲染性能。所以在编写CSS时，我们应该尽量减少使用昂贵属性，如 `box-shadow`/`border-radius`/`filter`/透明度/`:nth-child`等。





#### 16.6文件压缩
webpack压缩CSS;



### 十七、float


#### 17.1浮动导致的问题：


1、父元素没有设置height时，高度由子元素撑开，当子元素浮动后，会脱离文档流,无法撑开父元素；

2、行内元素与浮动元素发生重叠，其边框，背景和内容都会显示在浮动元素之上；

3、块级元素与浮动元素发生重叠时，边框和背景会显示在浮动元素之下，内容会显示在浮动元素之上；



#### 17.2解决方法；


1. 给父元素设置高；
2. 给父元素设置`overflow`：`hidden`；
3. 给父元素设置浮动；
4. 在父元素的最后面插入一个空div。给这个div设置`clear`：`both`；
5. 给父元素的最后面设置一个伪元素，并设置以下样式：  
1、`content`:''  
2、`display`：`block`；  
3、`clear`：`both`； 



#### 17.3、浮动元素的性质；


1. 可以设置宽高；
2. 排成一排；
3. 宽高均由内容撑开；



### 十八页面布局思路


#### 18.1三栏布局


效果：两边定宽、中间自适应、中间栏在文档流中优先渲染；



+ 圣杯布局：使用一个 `div`包住左、中、右的内容；，给div设置 `padding-left`、和 `padding-right`(带下等于左右部分的宽度)；
+ 双飞翼布局：  使用一个div包住中间内容，给 `div`设置 `margin-left`和 `margin-right`(等于左右部分的宽度)



#### 18.2两栏布局


 效果：左侧栏固定，右侧栏自适应； 

+  `float`(左侧栏设置) + `margin-left`(等于左侧栏宽度)； 
+  `absolute`(左侧栏设置) + `margin-left`(等于左侧栏宽度)； 
+  `float`(左侧栏设置) + BFC(常用设置：`overflow：hidden`) 
+  父元素设置 `display:flex`，右侧元素设置 `flex-grow：1` 



#### 18.3常见布局汇总






### 十九CSS移动端


#### 19.1移动端使用的单位


+  `em`：定义字体大小时以父级的字体大小为基准；定义长度单位时以当前字体大小为基准。 
+  `rem`：以根元素的字体大小为基准。 
+  `%`：以父级的宽度为基准。 
+  `vw/vh`：基于视口的宽度和高度。 
+  `rpx`：rpx是微信小程序中css的尺寸单位，可以根据屏幕宽度进行自适配。  
规定屏幕宽度为750px，譬如iphone6，屏幕宽度为375px，共有750个物理像素，则1rpx = 0.5px。 



#### 19.2移动端布局


+ 使用 `rem` 单位。可以拷贝淘宝那份代码直接使用，简单来说就是定义 `1rem = 16px`，然后配合 `meta` 使用。
+ 通过 `position: relative/absolute` 布局（现在更推荐使用 Flex 布局）



#### 19.31px实现	


**产生的原因：**



根本原因是 `750px` 的设计稿上是 UI 设计师期待的 `1px` 物理像素，它对应实际 `375px`稿子上的 `0.5px` 设备独立像素。



而 `0.5px` 设备独立像素对于 `IOS-8` 支持，对于安卓不支持。



所以安卓会将 `0.5px` 的设备独立像素渲染成 `1px` 的设备独立像素，也就是说，安卓在 `375px` 稿子上的设备独立像素为 `1px` 时，占 `2px` 物理像素，更粗。



所以我们拿到设计稿，要按照像素比 `dpr` 换算，每次量的单位 = `单位 / dpr`，比如 `dpr` 为 2 的时候，`1px` 转换为 CSS 以后就是 `0.5px`。（我们看的页面效果是按以物理像素来说，这才是问题的关键）



方法一：利用 `::after` + `transform`



```css
div::after {
  display: block;
  content: '';
  border: 1px solid #ccc;
  transform: scaleY(0.5);
}
```



方法二：利用 `box-shadow`



```css
div: {
  box-shadow: 0 0.5px 0 0 #fff;
}
```



#### 19.4300ms点击延迟


历史原因：



首款 iPhone 发布的时候，因为手机不知道用户点击一次屏幕，是点击按钮链接，还是要进行双击缩放。



所以 IOS Safari 就等待 `300ms` 来判断用户需要哪个操作（单击还是双击），然后产品一把抄，其他手机也逐渐变成这样了。



##### 1  阐述


`300ms` 是由于首款苹果做了个双击放大的效果，为了能看到用户到底是希望单击还是双击，所以有个 `300ms` 的等待，让手机知道用户想做啥。



一开始还没啥，现在网速越来越快、手机性能越来越好，这个弊端就暴露了。



网上有很多解决方案，说的较多的是浏览器厂商提供 `viewport` 的设置，还有 `pollfill`。



但是比较有效的是 `FastClick`，它利用的原理是在 `touchend` 中绑定自定义 `click` 事件，触发该事件后直接阻止 `300ms` 后的 `click` 事件。



实现自定义事件有 3 种方法：



1. `new Event`
2. `new CustomEvent`
3. `document.createEvent('CustomEvent')`



然后通过给按钮绑定 `addEventListener(eventName, callback)` 来实现。



##### 2 浏览器开发商解决方案


+ 方法一：禁止缩放



```html
<meta name="viewport" content="user-scalable=no, initial-scale=1, maxinmum-scale=1">
```



缺陷：并不能很好解决问题，用户想看图片这些没法双击放大看了。



+ 方法二：更改默认的视口宽度



```html
<meta name="viewport" content="width=device-width">
```



+ 总结



对于方案一和方案二，`Chrome` 是率先支持的，`Firefox` 紧随其后，然而 `Safari` 令人头疼的是，它除了双击缩放还有双击滚动操作，如果采用这种两种方案，那势必连双击滚动也要一起禁用；



##### 3 JavaScript 解决方案


+ 方法一：指针事件的 `polyfill`



除了IE，其他大部分浏览器都还不支持指针事件。有一些JS库，可以让我们提前使用指针事件。比如：



1. 谷歌的Polymer
2. 微软的HandJS
3. [@Rich-Harris ](/Rich-Harris ) 的 Points 



+ 方法二：FastClick



FastClick 是 FT Labs 专门为解决移动端浏览器 300 毫秒点击延迟问题所开发的一个轻量级的库。



实现原理是检测到 `touchend` 事件的时候，通过 DOM 自定义事件模拟一个 `click` 事件，并把浏览器 `300ms` 之后的 `click` 阻止掉。



### 二十盒子模型


+ CSS 盒子模型分为标准盒子和怪异盒子；
+ 标准盒子的 `contentWidth` 等于设置的 `width`，它的 `实际总宽度 = width + padding + border + margin`
+ 怪异盒子的 `contentWidth` 等于设置的 `width + padding + border`，它的 `实际总宽度 = contentWidth + margin`
+ 建议在页面初始化的时候，设置全局 CSS 属性 `box-sizing`，统一标准。



1.  
    - `inherit` - 继承父元素的值
    - `content-box` - 指定盒子为 W3C（标准盒子）
    - `border-box` - 指定为 IE（怪异盒子）。
2.  在IE8 以下版本的浏览器中使用盒模型有什么不同；  
IE8以下浏览器的盒模型中定义的元素的宽高不包括内边距和边框； 



### 二十一Flex


**display:flex / inline-flex;**



#### 一、容器属性：


+  **flex-direction**:决定主轴方向(row,row-reverse,column,column-reverse); 
+  **flex-wrap**:换行的方式(nowrap,wrap,wrap-reverse); 
+  **flex-flow**：是flex-direction和flex-wrap属性的简写(默认值为：row nowrap)； 
+  **justify-content**：定义主轴上的对齐方式  
**flex-start**：左对齐(默认)  
**flex-end**：右对齐  
**center**：居中  
**space-between**：两端对齐，项目之间的间隔都相等  
**space-around**：每个项目两侧的间隔相等 
+  **align-items**：在交叉轴上的对齐方式  
**flex-start**:交叉轴起点对齐  
**flex-end**:交叉轴终点对齐  
**center**:交叉轴中点对齐  
**stretch**:如果项目未设置高度或设为auto，则占满整个容易的高度(默认)  
**baseline**:项目的第一行文字的基线对齐 
+  **align-content**：定义了多根轴线的对齐方式：  
**flex-start**:交叉轴起点对齐  
**flex-end**:交叉轴终点对齐  
**center**:交叉轴中点对齐  
**space-betweem**:与交叉轴两端对齐，轴线之间的间隔平均分布  
**space-around**:每根轴线两侧的间隔都相等。所以，轴线之间的间隔比轴线与边框的间隔大一倍  
**stretch**:轴线占满整个交叉轴(**默认**) 



**备注：**align-items与align-content的区别：



1. align-items适用于所有flex容器，作用是设置flex子项在每个flex行的交叉轴的默认对齐方式。
2. align-content只适用于多行的flex容器(只有当flex容器的子项不止一行时，才有效果)，作用是当flex容器在交叉轴有多余空间时，将子项作为一个整体进行对齐；



#### 二、项目属性：


+  **order**:定义项目的排列属性，越小越靠前 
+  **flex-grow**:定义项目的方法比例 
+  **flex-shrink**：定义了项目的缩小比例 
+  **flex-basis**：定义了分配多余空间之前，项目占据的主轴空间 
+  **flex**：是flex-grow,flex-shrink,flex-basis的缩写(默认值：0 1 auto) 
+  **align-self**：允许单个项目与其他项目有不同的对齐方式,可覆盖aign-items,默认值为 `auto`，表示继承父元素的 `align-items`属性，如果没有父元素，则等同于 `stretch`。  
该属性可能取6个值，除了auto，其他都与align-items属性完全一致。 

```css
 auto | flex-start | flex-end | center | baseline | stretch;
```

 



### 二十二其他布局样式方法：


#### 1、水平居中方法：


1. text-align:center:只控制行内内容相对它的块父元素居中对齐，若子元素为块级元素可使用display:inline-block/inline，也可行;
2. 设置子元素margin: 0 auto,实现块级元素水平居中;



#### 2、垂直居中：


1.  line-height值等于height值，适用于行内元素/行内块级元素;

 

2. 父元素设置:display: table,子元素设置display:table-cell,vertical-align:middle;



### 二十三grid网格布局


flex 布局虽然强大，但是只能是一维布局，如果要进行二维布局，那么我们还需要使用 grid。



grid 布局又称为“网格布局”，可以实现二维布局方式，和之前的 表格 `table`布局差不多，然而，这是使用 CSS 控制的，不是使用 HTML 控制的，同时还可以依赖于媒体查询根据不同的上下文得新定义布局。



1、使用grid布局

```css
display:grid/inline-grid/subgrid;
```



网格容器的所有子元素自动变为网格项目（grid item），然后设置列（grid-template-columns）和 行（grid-template-rows）的大小，设置 `grid-template-columns` 有多少个参数生成的 grid 列表就有多少个列。



**注：当元素设置了网格布局，column、float、clear、vertical-align属性无效。**



如果没有设置 `grid-template-columns`，那么默认只有一列，宽度为父元素的 100%



`grid-template-row` 参数就是每一列的高度（超出列数的高度无效）



**注**：



1、css fr 单位是一个自适应单位，fr单位被用于在一系列长度值中分配剩余空间，如果多个已指定了多个部分，则剩下的空间根据各自的数字按比例分配。



2、`minmax()` 函数来创建行或列的最小或最大尺寸，第一个参数定义网格轨道的最小值，第二个参数定义网格轨道的最大值。可以接受任何长度值，也接受 `auto` 值。`auto` 值允许网格轨道基于内容的尺寸拉伸或挤压。



3、`repeat()` 属性可以创建重复的网格轨道。这个适用于创建相等尺寸的网格项目和多个网格项目。



接受两个参数：第一个参数定义网格轨道应该重复的次数，第二个参数定义每个轨道的尺寸。



4、`grid-column-gap`：创建列与列之间的距离。  
`grid-row-gap`：行与行之间的距离。



`grid-gap` 是 `grid-row-gap` 和 `grid-column-gap`两个属性的缩写。



5、我们可以通过表格线行或者列来定位 grid item。



我们可以通过表格线行或者列来定位 grid item。比如：



```html
<div class="grid-container">
  <div class="item item1">1</div>
  <div class="item item2">2</div>
  <div class="item item3">3</div>
  <div class="item item4">4</div>
  <div class="item item5">5</div>
  <div class="item item6">6</div>
</div>


```



```css
.grid-container{
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(2,100px);
  grid-template-rows: repeat(3,100px);
  grid-column-gap: 50px;
  grid-row-gap: 15px;
  background: pink;
}
.item{
  border: 2px solid palegoldenrod;
  color: #fff;
  text-align: center;
  font-size: 20px;
}
.item1{
  grid-row-start: 2;
  grid-row-end: 3;
  grid-column-start: 2;
  grid-column-end: 3;
  background: #fffa90;
  color: #000;
}
```

效果：



![](https://user-gold-cdn.xitu.io/2017/8/20/326b7e1856e61524c26322e510271c95?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)



### 二十四面试问题


#### 1、当一个元素的宽高设置百分比是相对于什么计算的;


当按百分比给一个元素的设置宽时，是相对于父容器的宽度计算；



对于一下表示竖向距离的属性时(padding-top,padding-bottom,margin-top,margin-bottom)等,



按照百分比设置时，也是相对于父元素的宽度，而不是高度;



#### 2、png、jpg、gif图片格式，分别什么时候用


1. png是便携式网络图片（Portable Network Graphics）是一种无损数据压缩位图文件格式.优点是：压缩比高，色彩好。 大多数地方都可以用。
2. jpg是一种针对相片使用的一种失真压缩方法，是一种破坏性的压缩，在色调及颜色平滑变化做的不错。在www上，被用来储存和传输照片的格式。
3. gif是一种位图文件格式，以8位色重现真色彩的图像。可以实现动画效果.



#### 3、消除图片底部间隙的方法：


+ 图片块状化 - 无基线对齐：`img { display: block; }`
+ 图片底线对齐：`img { vertical-align: bottom; }`
+ 行高足够小 - 基线位置上移：`.box { line-height: 0; }`
+ 将字体大小设为0，基线高度与字体大小有关 `.box { font-size: 0; }`



#### 4、基于伪元素的图片内容生成技术


需求：图片还没加载时就把 `alt` 信息呈现出来。



实现：图片没有 `src` ，因此，`::before`和 `::after` 可以生效，我们可以通过 `content` 属性呈现 alt 属性值。

```css
img::after{
  / 生成 alt 信息 /
  content: attr(alt);
  / 尺寸和定位 /
  postion:absolute; bottom: 0;
  width:100%;
  background-color:rgba(0,0,0,.5);
  transform: translateY(100%);
  transition: transform .2s;
}
img:hover::after{
  transform: translateY(0);
}
```



当我们给图片添加src 属性时图片从普通元素变成替换元素，原本还支持的 `::before`和 `::after` 此时全部无效，此时再hover图片，是不会有任何信息出现的。



#### 5、css加载会阻塞DOM树渲染？
css加载不会阻止DOM树解析,会阻止DOM树渲染；CSS加载过程中，会解析DOM守护，等CSS加载完，根据最终的样式渲染DOM树;



#### 6、css加载会阻塞js运行吗？
css加载会阻塞后面的js语句的执行





#### 7、针对上面两点的优化方案：


+ 使用CDN(因为CDN会根据你的网络状况，替你挑选最近的一个具有缓存内容的节点为你提供资源，因此可以减少加载时间)
+ 对css进行压缩(可以用很多打包工具，比如webpack,gulp等，也可以通过开启gzip压缩)
+ 合理的使用缓存(设置cache-control,expires,以及E-tag都是不错的，不过要注意一个问题，就是文件更新后，你要避免缓存而带来的影响。其中一个解决防范是在文件名字后面加一个版本号)
+ 减少http请求数，将多个css文件合并，或者是干脆直接写成内联样式(内联样式的一个缺点就是不能缓存)



#### 8、浏览器渲染过程：


渲染流程:  
![](https://pic2.zhimg.com/80/v2-e4744784c328c5c7a1527ff0822c1a5d_720w.png)



从流程我们可以看出来



1. DOM解析和CSS解析是两个并行的进程，所以这也解释了为什么CSS加载不会阻塞DOM的解析。
2. 然而，由于Render Tree是依赖于DOM Tree和CSSOM Tree的，所以他必须等待到CSSOM Tree构建完成，也就是CSS资源加载完成(或者CSS资源加载失败)后，才能开始渲染。因此，CSS加载是会阻塞Dom的渲染的。
3. 由于js可能会操作之前的Dom节点和css样式，因此浏览器会维持html中css和js的顺序。因此，样式表会在后面的js执行前先加载执行完毕。所以css会阻塞后面js的执行。



**备注:DOMcontentLoaded & onload**



1、onload:就是等待页面的所有资源都加载完成才会触发，这些资源包括css、js、图片视频等。



2、DOMContentLoaded：当初始的 **HTML** 文档被完全加载和解析完成之后，`**DOMContentLoaded**` 事件被触发，而无需等待样式表、图像和子框架的完全加载。



1.  如果页面中同时存在css和js，并且存在js在css后面，则DOMContentLoaded事件会在css加载完后才执行。 
2.  其他情况下，DOMContentLoaded都不会等待css加载，并且DOMContentLoaded事件也不会等待图片、视频等其他资源加载。 
3.  在任何情况下，DOMContentLoaded 的触发不需要等待图片等其他资源加载完成。 
4.  异步脚本情况： 
    -  defer：当 HTML 文档被解析时如果遇见 defer 脚本，则在后台加载脚本，文档解析过程不中断，而等文档解析结束之后，defer 脚本执行。  
**defer 与 DOMContentLoaded**：HTML 文档解析不受defer影响，等 DOM 构建完成之后 defer 脚本执行，但脚本执行之前需要等待 CSSOM 构建完成。所以在 DOM、CSSOM 构建完毕，defer 脚本执行完成之后，DOMContentLoaded 事件触发。 
    -  async：当 HTML 文档被解析时如果遇见 async 脚本，则在后台加载脚本，文档解析过程不中断。脚本加载完成后，文档停止解析，脚本执行，执行结束后文档继续解析。  
**async 与 DOMContentLoaded**：如果 script 标签中包含 async，则 HTML 文档构建不受影响，解析完毕后，DOMContentLoaded 触发，而不需要等待 async 脚本执行、样式表加载等等。 



#### 9、position:sticky


`sticky`跟前面四个属性值都不一样，它会产生动态效果，很像 `relative`和 `fixed`的结合：一些时候是 `relative`定位（定位基点是自身默认位置），另一些时候自动变成 `fixed`定位（定位基点是视口）。



它的具体规则是，当页面滚动，父元素开始脱离视口时（即部分不可见），只要与`sticky`元素的距离达到生效门槛，`relative`定位自动切换为 `fixed`定位；等到父元素完全脱离视口时（即完全不可见），`fixed`定位自动切换回 `relative`定位。





#### 10、长文本处理：


1.  字符超出部分换行：

```css
overflow-wrap:break-word; 
```

2.  字符超出文职使用连字符：

```css
hyphens: auto; 
```

3.  单行文本超出省略：

```css
overflow:hiddle;
text-overflow:ellipsis;
display: -webkit-box;
-webkit-line-clamp:2;
-webkit-box-orient:vertical; 
```

  


### 二十五BEM(块元素编辑器：Block-Element-Modifier)


BEM是一种前端命名方法论。这种巧妙的命名方法让你的CSS类对其他开发者来说更加透明而且有意义。

块（Block）是一个块级元素，可以理解为组件块，比如头部是个block，内容也是block，一个block可能由几个子block组成。

元素（Element）element是block的一部分完成某种功能，element依赖于block，比如在logo中，img是logo的一个element，在菜单中，菜单项是菜单的一个element。

修饰符（Modifier）modifier是用来修饰block或者element的，它表示block或者element在外观或行为上的改变，例如actived。



### 参考资料：


#### 1面试：


+ [50道CSS经典面试题](https://segmentfault.com/a/1190000013325778)【阅读建议：30min】
+ [12个HTML和CSS必须知道的重点难点问题](https://juejin.im/post/6844903567707357197)【阅读建议：30min】



#### 2布局


+ [干货!各种常见布局实现+知名网站实例分析](https://juejin.im/post/6844903574929932301)【阅读建议：1h】
+ [CSS 常见布局方式](https://juejin.im/post/599970f4518825243a78b9d5)【阅读建议：1h】



#### 3Flex


+ [Flex 布局教程：语法篇](http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html)【阅读建议：1h】
+ [Flex 布局教程：实例篇](http://www.ruanyifeng.com/blog/2015/07/flex-examples.html)【阅读建议：1h】
+ [30 分钟学会 Flex 布局](https://zhuanlan.zhihu.com/p/25303493)【阅读建议：30min】
+ [写给自己看的display: flex布局教程](https://www.zhangxinxu.com/wordpress/2018/10/display-flex-css3-css/)【阅读建议：30min】



#### 4移动端


+ [Mars - mobile needs a hero](https://github.com/AlloyTeam/Mars)【阅读建议：无】
+ [腾讯移动Web前端知识库](https://github.com/hoosin/mobile-web-favorites)【阅读建议：无】
+ [关于移动端适配，你必须要知道的](https://juejin.im/post/6844903845617729549)【阅读建议：30min】
+ [如何解决移动端Click事件300ms延迟的问题？](https://zhuanlan.zhihu.com/p/69522350)【阅读建议：20min】
+ [设计方案--移动端延迟300ms的原因以及解决方案](https://www.cnblogs.com/chengxs/p/11064469.html)【阅读建议：20min】
+ [细说移动端 经典的REM布局 与 新秀VW布局](https://cloud.tencent.com/developer/article/1352187)【阅读建议：30min】
+ [移动端1px解决方案](https://juejin.im/post/5d19b729f265da1bb2774865)【阅读建议：30min】
+ [Retina屏的移动设备如何实现真正1px的线？](https://jinlong.github.io/2015/05/24/css-retina-hairlines/)【阅读建议：20min】
+ [rem布局解析](https://juejin.im/post/6844903671143088136)【阅读建议：5min】



#### 5CSS


+ [CSS 常用技巧](https://juejin.im/post/6844903619909648398)【阅读建议：30min】
+ [CSS设置居中的方案总结-超全](https://juejin.im/post/6844903560879013901)【阅读建议：30min】
+ [CSS性能优化的8个技巧](https://juejin.im/post/6844903649605320711?utm_source=gold_browser_extension)【阅读建议：20min】
+ [css加载会造成阻塞吗？](https://juejin.im/post/6844903667733118983?utm_source=gold_browser_extension)【阅读建议：30min】
+ [css加载会造成阻塞吗](https://segmentfault.com/a/1190000018130499)【阅读建议：30min】
+ [不可思议的纯 CSS 滚动进度条效果](https://juejin.im/post/6844903758074216462)【阅读建议：30min]
+ [CSS 定位详解](http://www.ruanyifeng.com/blog/2019/11/css-position.html)【阅读建议：20min】
+ [Css单位px，rem，em，vw，vh的区别](https://www.cnblogs.com/theblogs/p/10516098.html)【阅读建议：10min】
+ [谈谈 rem 与 vw -- rem](https://www.jianshu.com/p/1a9b5d48afa2)【阅读建议：5min】
+ [杀了个回马枪，还是说说position:sticky吧](https://www.zhangxinxu.com/wordpress/2018/12/css-position-sticky/)【阅读建议：20min】
+ [css行高line-height的一些深入理解及应用](https://www.zhangxinxu.com/wordpress/2009/11/css%E8%A1%8C%E9%AB%98line-height%E7%9A%84%E4%B8%80%E4%BA%9B%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3%E5%8F%8A%E5%BA%94%E7%94%A8/)【阅读建议：10min】
+ [浏览器将rem转成px时有精度误差怎么办？](https://www.zhihu.com/question/264372456)【阅读建议：20min】
+ [彻底搞懂word-break、word-wrap、white-space](https://juejin.im/post/6844903667863126030)【阅读建议：20min】



#### 6CSS3


+ [个人总结（css3新特性）](https://juejin.im/post/6844903518520901639)【阅读建议：1h】
+ [高性能 CSS3 动画](https://github.com/AlloyTeam/Mars/blob/master/performance/high-performance-css3-animation.md)【阅读建议：20min】
+ [趣味CSS3效果挑战小汇总](https://juejin.im/post/6844903896473665550)【阅读建议：20min】
+ [从青铜到王者10个css3伪类使用技巧和运用，了解一哈](https://juejin.im/post/6844903654756089864)【阅读建议：20min】



#### 7层叠上下文


+ [彻底搞懂CSS层叠上下文、层叠等级、层叠顺序、z-index](https://juejin.im/post/5b876f86518825431079ddd6)【阅读建议：30min】
+ [深入理解CSS中的层叠上下文和层叠顺序](https://www.zhangxinxu.com/wordpress/2016/01/understand-css-stacking-context-order-z-index/)【阅读建议：40min】



#### 8BFC 块格式化上下文


+ [什么是BFC？什么条件下会触发？应用场景有哪些？](http://47.98.159.95/my_blog/css/008.html)【阅读建议：20min】
+ [学习 BFC (Block Formatting Context)](https://juejin.im/post/6844903495108132877)【阅读建议：20min】
+ [MDN - 块格式化上下文](https://developer.mozilla.org/zh-CN/docs/Web/Guide/CSS/Block_formatting_context)【阅读建议：20min】
+ [BFC(块级格式化上下文)](https://www.jianshu.com/p/498145565e4f)【阅读建议：5min】



#### 9 其他


+ [Web开发者需要知道的CSS Tricks](https://juejin.im/post/6844903576561516558)【阅读建议：无】
+ [CSS世界中那些说起来很冷的知识](https://juejin.im/post/6844903635248218126)【阅读建议：30min】
+ [从网易与淘宝的font-size思考前端设计稿与工作流](https://www.cnblogs.com/lyzg/p/4877277.html)【阅读建议：20min】
+ [2019年，你是否可以抛弃 CSS 预处理器？](https://aotu.io/notes/2019/10/29/css-preprocessor/index.html)【阅读建议：10min】
+ [浅谈 CSS 预处理器（一）：为什么要使用预处理器？](https://github.com/cssmagic/blog/issues/73)【阅读建议：20min】
+ [布局的下一次革新](https://juejin.im/post/6844903666374148103)【阅读建议：20min】

