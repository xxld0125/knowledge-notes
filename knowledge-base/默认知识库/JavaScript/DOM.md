# 一、常用DOMAPI
1. 获取元素
+ `getElementById`
+ `getElementByName`
+ `getElementByTagName`
+ `querySelector(".class|#id|name")`
+ `querySelectorAll(".class|#id|name")`



2. 创建元素
+  `document.createElement(name)`: 创建一个具体的元素
+ `createDocumentFragment()`:创建一个DOM片段
+  `createTextNode()`:创建一个文本节点



3. 添加元素
+ `document.body.appendChild(node)`



4. 删除元素
+ ` document.body.removeChild(node)`



5. 元素位置
+ `clientHeight`：表示可视区域的高度(不包含`border`和滚动条)；
+ `offsetHeight`：表示可视区域的高度(包含`border`和滚动条)；
+ `scrollHeight`：表示了所有区域的高度，包含了因为滚动被隐藏的部分;
+ `clientTop`：表示边框 `border` 的厚度，在未指定的情况下一般为0;
+ `scrollTop`：滚动后被隐藏的高度，获取对象相对于由 `offsetParent `属性指定的父坐标（`CSS `定位的元素或 `body `元素）距离顶端的高度。





