### 一、HTML5新增内容


#### 一、语义化标签：


+  <section> - 章节
+  <nav> - 导航
+  <article> - 完整独立内容块
+ <aside> - 和页面内容关联度较低的内容：例如广告（剩余的）
+ <header> - 页面或者文章头部
+ <footer> - 页面或者文字尾部
+  <main> - 文档主要内容
+  <figure> - 一个和文档有关的图例
+  <figcaption> - 图例说明
+ <mark> - 需要被高亮的引用文字
+ <source> - 为 video 和 audio 指定 媒体源
+ <track> - 为 video 和 audio 指定 文本轨道（字幕）
+ <progress> - 进度条
+ <meter> - 滑动条



#### 二、增强性表单：


1. 新增的表单类型： 
    - color
    - url
    - date
    - output
2. 新增的表单属性： 
    - placehoder
    - required
    - pattern(描述一个正则表单式)
    - min、max：设置元素最大值和最小值
    - step：输入域规定的合法的数字间隔
    - height、width：用于image类型的input标签的图像高度和宽度设置
    - autofocus：页面加载时是否自动获得焦点
    - multiple：规定input元素可选择多个值



#### 三、新增audio和video多媒体标签


#### 四、Canvas绘图


#### 五、SVG绘图


#### 六、地理定位


#### 七、拖放API


#### 八、Web Worker


#### 九、Web Storage


#### 十、WebSocket


### 二、结构语义化


+ 易修改、易维护
+ 无障碍阅读支持
+ 搜索引擎良好，利于 SEO



### 三、层级关系


window > document > html > body



+ `window` 是 `BOM` 的核心对象，它一方面用来获取和设置浏览器的属性和行为，另一方面作为一个全局对象。
+ `document` 对象是一个跟文档相关的对象，拥有一些操作文档内容的功能，但是地位没有 `window` 高。
+ `html` 元素对象跟 `document` 元素对象是属于 `html` 文档的 `DOM` 对象，可以认为就是 `html` 源代码中那些标签化成的对象，它们跟 `div`、`select` 这些对象没有什么根本区别。



### 四、替换元素与不可替换元素


`<input>` 和 `<img>` 虽然是行内元素，但是它们是可以设置宽和高的，因为它们涉及到可替换元素和不可替换元素。



#### 4.1 替换元素


例如：



+ `<img>` 根据 `src` 属性来读取图片信息并显示出来
+ `<input>` 根据标签的 `type` 属性来决定是显示输入框，还是单选按钮。



替换元素有：`<img>`、`<input>`、`<textarea>`、`<select>`、`<object>`。



#### 4.2 不可替换元素


HTML 大多数元素都是不可替换的，即其内容直接展现给浏览器。



例如：



+ `<p>` 直接全部展示



### 五、行内元素与块级元素


#### 5.1、对比
| 块级元素 | 行内元素 |
| --- | --- |
| 独占一行。默认情况下宽度自动填充父元素宽度 | 宽度随元素内容变化。相邻的行内元素会排列在同一行内，直到一行排不下，才会换行。 |
| 可以设置 `width`、`height` | 设置 `width`、`height`无效 |
| 可以设置 `margin` 和 `padding` | 可以设置 `margin-left`、`margin-right`、`padding-left`、`padding-right` |
| 对应：`display: block` | 对应 `display: inline` |




#### 5.2、常见的块级元素与行内元素


##### 5.2.1、块级元素


+ `<div>` - 标签块
+ `<h1>`、`<h2>`、`<h3>`、`<h4>`、`<h5>`、`<h6>` - 标题 1 - 标题 6
+ `<form>` - 表单
+ `<hr>` - 水平线
+ `<ul>` - 无序列表
+ `<ol>` - 有序列表
+ `<li>` - 定义列表项目，用于 `ul` 和 `li` 中
+ `<p>` - 段落
+ `<table>`、`<thead>`、`<tbody>`、`<th>`、`<tr>`、`<td>` - 表格元素



##### 5.2.2、行内元素


+ `<a>` - 超链接或者锚点
+ `<br>` - 换行
+ `<img>` - 图片
+ `<input>` - 输入框
+ `<label>` - 为 `input` 进行标记/标注
+ `<button>` - 按钮
+ `<textarea>` - 多行文本框



#### 5.3、行内元素与块级元素的转化


`display` 属性可以使行内元素和块级元素之间转换。



+ `display: inline` - 转换为行内元素
+ `display: block` - 转换为块级元素
+ `display: inline-block` - 转换为行内块元素



### 六、HTML5新增内容


+ 本地存储
+ 语义化标签
+ canvas
+ audio、vedio标签
+ 拖拽释放api
+ 地理api
+ 。。。等等



### 七、HTML实现SEO


+ html标签合理使用，strong标签语义较强，合理使用;
+ title、meta合理设置;
+ a标签要写title属性、img标签要写alt属性;
+ div要有合理类名、便于搜索引擎爬虫检索;
+ HTML层次清晰，ID不要重复、便于搜索引擎爬虫检索;



### 八、XHTML与HTML的区别


+ 必须被正确嵌套；
+ 必须被关闭；
+ 标签名必须小写；
+ 必须有根元素；



### 九、doctype


1、Doctype的作用：



```plain
DOCTYPE是一种通用标记语言的文档类型申明，作用是：告诉标准通用标记语言解析器，需要使用什么样的文档类型定义来解析文档。
```



2、严格模式和混杂模式的区别及意义：



+ 严格模式的排版和 JS 运作模式是 以该浏览器支持的最高标准运行。
+ 在混杂模式中，页面以宽松的向后兼容的方式显示。模拟老式浏览器的行为以防止站点无法工作。
+ DOCTYPE不存在或格式不正确会导致文档以混杂模式呈现。



3、Doctype文档类型：



该标签可声明三种 DTD 类型，分别表示严格版本、过渡版本以及基于框架的 HTML 文档。



HTML 4.01 规定了三种文档类型：Strict、Transitional 以及 Frameset。  
XHTML 1.0 规定了三种 XML 文档类型：Strict、Transitional 以及 Frameset。  
Standards （标准）模式（也就是严格呈现模式）用于呈现遵循最新标准的网页，而 Quirks  
（包容）模式（也就是松散呈现模式或者兼容模式）用于呈现为传统浏览器而设计的网页。

