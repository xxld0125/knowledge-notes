### 一、概述:Virtual DOM 主要实现步骤
+ 用`JS`对象模拟`DOM`树 - `element.js`
+ 对比两颗虚拟`DOM`树的差异 - `diff.js`
+ 将两个虚拟`DOM`对象的差异应用到真正的`DOM`树 - `patch.js`

### 二、Vue源码 Virtual - DOM 简析
1. 在`Vue.js`中，`Virtual DOM`是用`Vnode`这个`Class`描述的，主要借鉴了`snabbdom`实现
    1. `Vnode`的核心属性
        1. `tag`：标签属性
        2. `data`：包含了`class`、`attribute`、`style`及绑定的事件
        3. `children`：`vnode`的子节点
        4. `text`：文本属性
        5. `elem`：对应的真实`DOM`节点
        6. `key`：`vnode`标记；



2. 虚拟`DOM`的创建：
    1. 从`new Vue()`到虚拟`DOM`的创建过程实例化`Vue`实例，调用`vm._init()`,调用`vm.$mount`,调用`mountedComponent()`,`mountedComponent()`的核心是实例化一个`watcher`，在他的回调中调用`updateComponent()`,在此方法中调用`vm._render()`方法形成虚拟`DOM`，最终调用`vm._update()`更新`DOM`;
    2. 核心方法：
        1. `Vue._render()`方法，用来将实例渲染成虚拟`Node`
        2. 其中通过`vm.$createElement()`,创建`Vnode`



3. `diff`过程；
    1. `diff`过程：实例化一个`Watcher`,会被添加到所绑定变量的依赖中，一旦`model`的响应式的数据发生变化，响应式数据所维护的`dep`数组会调用`dep.notify()`方法完成所有依赖遍历执行工作，包括视图更新，及`updateComponent()`方法的调用，`updateComponent()`方法调用`vm._update()`方法实现视图更新，其中最关键的方法是`vm._patch_()`方法;
    2. 核心方法： `vm.__patch__()`方法，主要是完成`oldVnode`和`vnode`的`diff`过程，并根据需要操作的`vdom`打`patch`，最后生成新的真实`DOM`节点，并完成视图的更新工作；
    3. `__patch__()`实现过程：

在`patch()`方法中，一般分为两种情况：

        1. `oldVnode`不存在，会创建新节点；
        2. `oldVnode`存在，会对`oldVnode`和`Vnode`进行`diff`及`patch`的过程；其中`patch`过程会调用`sameVnode()`对两个`Vnode`进行基本属性的`diff`：
            1. 只有当两个元素的基本属性相同(标签名，key值，表单类型等)的情况下才会认为两个`vnode`只是局部发生了更新，然后会对这两个`vnode`进行`diff`；
            2. 如果这两个`Vnode`的基本属性存在不一致，那么会跳过`diff`过程，根据`vnode`新建一个真实`DOM`，删除老的`DOM`节点；
            3. `diff`过程主要通过`patchVnode()`进行；`diff`过程分为几种：
                1. 对文本节点判断，如果`oldVnode.text !== Vnode.text`,则直接进入文本节点的替换
                2. 如`oldVnode`有文本节点，而`Vnode`没有，那么就清空这个文本节点
                3. 在`oldVnode`、`Vnode`没有文本节点的情况下，进入子节点的`diff`
                4. 在`oldCh`和`ch`都存在且不同的情况，调用`updateChildren()`对子节点进行`diff`
                5. 若`oldCh`不存在，`ch`存在，首先清空`oldVnode`的文本节点，同时调用`addVnodes()`将`ch`添加到真实`DOM`上
                6. 若`oldCh`存在，`ch`不存在，则删除真实`DOM`下的`oldCh`子节点；
            4. 子节点`diff`流程分析：通过`updateChildren()`方法，是`diff`过程中最关键的部分；在遍历`diff`之前，给`oldCh`和`newCh`都添加了一个`startIndex`和`endIndex`作为遍历的索引，当`oldCh`或`newCh`遍历完成后(完成条件：`oldCh`和`newCh`的`startIndex >= endIndex`，`diff`就停止；
                1. 无`key`的`diff`过程：
                    1. 头头对比：对比两个数组的头部,如果找到,就把新节点`patch`到旧节点,`oldStartIndex`后移
                    2. 尾尾对比: 对比两个数组的尾部,如果找到,就把新节点`patch`到旧节点,`oldEndIndex`前移
                    3. 旧尾新头对比: 交叉对比,旧尾新头,,就把新节点`patch`到旧节点,`oldEndIndex`前移,`newStartIndex`后移
                    4. 旧头新尾对比: 交叉对比,旧头新尾,,就把新节点`patch`到旧节点,`oldStartIndex`后移,`newEndIndex`后移
                    5. 遍历的过程结束后,`newStartIndex > newEndIndex`,说明`oldCh`存在多余的节点,最后就需要将这些多余的节点删除,或`oldStartIndex > oldEndIndex`,就将`newCh`中多余的`Vnode`放到根据在`newCh`的位置插入插入到`DOM`中

总结: 在`vnode`不带`key`的情况下,每一轮的`diff`过程都是起始和结束进行比较,知道`oldCh`和`newCh`被遍历完;

                2. 在有`key`的`diff`过程:

利用`key`对比：用新指针对应节点的`key`去旧数组中寻找对应的节点，这里分三种情况，如果没有对应的`key`，那么创建新的节点，如果有`key`并且是相同节点，把新节点`patch`到旧节点，如果有`key`，但不是相同节点，则创建新节点；

总结：当`vnode`带`key`的情况，在每一轮的`diff`过程中，当起始和结束都没有找到`sameVnode`时，然后再判断在`newStartVnode`的属性是否有`key`，且在`oldKeyToIndx`中找到相应的节点，如果找到相应的节点，则删除`oldCh`中对应的`Vnode`；



4. `patch`过程：

    将两个虚拟`DOM`的差异应用到真实`DOM`上；

