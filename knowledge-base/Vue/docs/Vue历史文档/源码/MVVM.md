### 一、Vue设计流程 - new Vue过程
主要通过监听器(`Observer`)、订阅器(`Dep`)、订阅者(`Watcher`)、解析器(`Compiler`)实现；



### 二、初始化流程
1. 创建`Vue`实力对象，初始化实力对象的`options`参数，在`Vue`初始阶段，`init()`方法执行时，会执行`initState(vm)`。

`initState()`方法主要是对`props`、`methods`、`data`、`computed`、`watch`等属性进行初始化，其中对`data`的初始化由`initData(vm)`实现；

` initData()`的作用：

    - 实现数据代理；
    - 将data进行数据劫持；



2. 通过遍历调用`_proxyData()`方法将`Vue`实例对象的`data`数据代理到`Vue`实例对象上，即`vm.data.xxx => vm.data`;



3. 调用`observe()`方法，只对对象操作
    1. 创建一个`Observer`实例(对于非`Vnode`的对象类型添加一个`Observer`实例)；
        1. `Observer`实例创建过程：
            1. 实例化`Dep`实例，作用:给`$set/set`手动`notify()`使用;
            2. 对于数组数据，指定修改后的数据原型(七种修改数据本身的方法),调用`Observer`原型上的`observeArray()`方法； 
            3. `observerArray()`作用：对数组数据遍历调用`observe()`方法；
            4. 对纯对象数据，调用`Observer`原型上的`walk`方法，
    2. 调用`walk()`、`convert()`及`defineReactive()`方法实现数据劫持；
    3. `defineReactive()`方法会为每个劫持的属性创建一个`Dep`类(订阅器)；
        1. 如果属性值为对象，则会继续调用`observe()`方法递归劫持；
        2. 当访问该属性时，`getter`通过`Dep.target`判断是否调用`dep.depend()`方法进行依赖收集；
        3. `dep.depend()`触发`watch`的`addDep()`方法，收集`watcher`；
        4. 当修改该属性时，`setter`通过`dep.notify()`方法通知订阅者更新视图，如果更新后的值为对象，则调`observe()`方法进行数据劫持；

 

4. 创建一个`Compile`实例：
    1. 判断闯入的`option.el`参数是否为`ElementNode`，不是的话，获取挂载点的`DOM`元素
    2. 调用`Compile`原型上的`node2Fragment()`方法，作用：将获取的原生节点拷贝到文档碎片`Fragment`上;
    3. 调用`Compile`原型上的`init()`方法 => 调用`Compile`原型上的`compileElement()`方法；
        1. 作用：对所有节点及其子节点进行扫描解析编译，调用对应的指令渲染函数进行数据渲染，并调用对应的指令更新函数进行方法绑定；
        2. 实现过程：
            1. 遍历所有节点及其子节点，判断节点类型，根据节点类型调用对应的编译方法(元素节点：`compile()`,文本节点：`compileText()`;
            2. `compileText()`作用:将文本节点上的{{}}内的变量替换为对应的数据；
            3. `compile()`作用：对元素节点上的指令进行解析，普通指令进行数据绑定及渲染，事件指令绑定对应的方法；
            4. 完成绑定后，去除节点碎片上绑定的事件`removeAttribute`；



5. 解析元素节点时，会创建`watcher`实例；
    1. 调用`Watcher`原型上的`get`方法，触发实例的`getter()`方法，触发`dep.depend()`方法，再触发`Dep.target.addDep()`方法，触发`dep.addSub(this)`,实现将依赖加入对应的`dep`实例的`sub`数组中；
    2. 在`vm._render()`过程中，会出触发所有数据的getter，完成所有依赖的收集；



### 三、响应式流程
1. 监听用户输入事件，对用户输入的事件进行监听，通过初始化调用的`observe()`方法，对数据进行监听；
2. 调用`Vue`实例对象的数据设置方法更新数据，被监听的数据被修改时，会触发`setter`方法；
    1. `setter`方法的作用：
        1. 更新修改值；
        2. 如果新的值是`Object`的话，继续进行监听；
        3. 调用`dep.notify()`方法；
    2. `dep.notify()`方法会对`dep`实例中的`subs`数组进行遍历，调用数组元素`sub`(`watcher`实例)的`update()`方法，`update()`方法触发`run()`方法：
        1. `run()`方法的作用：调用Watcher原型上的`get()`方法，获取更新后的值，与更新之前的值比较，若不同，则调用`compile`过程中传入的方法更新对应视图节点，同时更新`dep.subs`的`watcher`
        2. `get()`方法的作用：会触发相应属性的`getter`方法，再触发`dep.depend()`方法，再触发`watch.addDep()`方法；`addDep()`方法的作用：通过判断`watcher.depIds`是否有对应的`dep.id`,决定是否调用`dep.addSub()`方法将当前`watcher`加入到对应的`dep.subs`数组(如果没有对应的`dep.id`，则调用`dep.addSub()`;



