# 简介
是一款**<font style="color:#DF2A3F;">渐进式</font>**的JavaScript框架。

**所谓渐进式框架，就是把框架分层。最核心的部分是视图层渲染，然后往外是组件机制，在这个基础上再加入路由机制，再加入状态管理，最外层是构建工具，**

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748334540424-49738cc3-b89e-43ce-9154-320fce13b255.png)



# 变化侦测
Vue.js最独特的特性之一是看起来并不显眼的响应式系统。

从状态生成DOM，再输出到用户界面显示的一整套流程叫作渲染，应用在运行时会不断地进行重新渲染。而响应式系统赋予框架重新渲染的能力，其重要组成部分是变化侦测。变化侦测是响应式系统的核心，没有它，就没有重新渲染。框架在运行时，视图也就无法随着状态的变化而变化。

变化侦测是响应式系统的核心，没有它，就没有重新渲染。框架在运行时，视图也就无法随着状态的变化而变化。

简单来说，变化侦测的作用是侦测数据的变化。当数据变化时，会通知视图进行相应的更新。

## Object 的变化侦测
### 如何追踪变化
有两种方法可以侦测到变化：使用`Object.defineProperty`和ES6的`Proxy`。

每当从`data`的`key`中读取数据时，`get`函数被触发；每当往`data`的`key`中设置数据时，`set`函数被触发。

```javascript
function defineReactive (data, key, val) {
  Object.defineProperty(data, key, {
    enumerable: true,
    configurable: true,
    get: function () {
      return val
    },
    set: function (newVal) {
      if(val === newVal){
        return
      }
      val = newVal
    }
  })
}
```



### 如何收集依赖
如果只是把`Object.defineProperty`进行封装，那其实并没什么实际用处，**<font style="color:#DF2A3F;">真正有用的是收集依赖</font>**。



如何收集依赖？

思考一下，我们之所以要观察数据，**其目的是当数据的属性发生变化时，可以通知那些曾经使用了该数据的地方。**

****

**总结起来，其实就一句话，在getter中收集依赖，在setter中触发依赖。**



### 依赖收集在哪里
将依赖收集的代码封装成一个 `Dep` 类，专门管理依赖。

```javascript
export default class Dep {
  constructor () {
    this.subs = []
  }

  addSub (sub) {
    this.subs.push(sub)
  }

  removeSub (sub) {
    remove(this.subs, sub)
  }

  depend () {
    if (window.target) {
      this.addSub(window.target)
    }
  }

  notify () {
    const subs = this.subs.slice()
    for (let i = 0, l = subs.length; i < l; i++) {
      subs[i].update()
    }
  }
}

function remove (arr, item) {
  if (arr.length) {
    const index = arr.indexOf(item)
    if (index > -1) {
      return arr.splice(index, 1)
    }
  }
}
```



```javascript
function defineReactive (data, key, val) {
  let dep = new Dep()
  Object.defineProperty(data, key, {
    enumerable: true,
    configurable: true,
    get: function () {
      dep.depend()
      return val
    },
    set: function (newVal) {
      if(val === newVal){
        return
      }
      val = newVal
      dep.notify()
    }
  })
}
```

****

### 依赖是谁
我们收集的依赖是`window.target`，那么它到底是什么？我们究竟要收集谁呢？

我们要通知用到数据的地方，而使用这个数据的地方有很多，而且类型还不一样，既有可能是模板，也有可能是用户写的一个`watch`，这时需要抽象出一个能集中处理这些情况的类 `Watcher`。



### 什么是 Watcher
`Watcher`是一个中介的角色，数据发生变化时通知它，然后它再通知其他地方。

关于`Watcher`，先看一个经典的使用方式：

```javascript
 // keypath
vm.$watch('a.b.c', function (newVal, oldVal) {
   // 做点什么
})
```



好像只要把这个`watcher`实例添加到`data.a.b.c`属性的`Dep`中就行了。然后，当`data.a.b.c`的值发生变化时，通知`Watcher`。

```javascript
export default class Watcher {
  constructor (vm, expOrFn, cb) {
    this.vm = vm
    // 执行this.getter()，就可以读取data.a.b.c的内容
    this.getter = parsePath(expOrFn)
    this.cb = cb
    this.value = this.get()
  }

  get() {
    window.target = this
    let value = this.getter.call(this.vm, this.vm)
    window.target = undefined
    return value
  }

  update () {
    const oldValue = this.value
    this.value = this.get()
    this.cb.call(this.vm, this.value, oldValue)
  }
}
```



在`get`方法中先把`window.target`设置成了`this`，也就是当前`watcher`实例，然后再读一下`data.a.b.c`的值，这肯定会触发`getter`。

触发了`getter`，就会触发收集依赖的逻辑。而关于收集依赖，上面已经介绍了，会从`window.target`中读取一个依赖并添加到`Dep`中。

依赖注入到`Dep`中后，每当`data.a.b.c`的值发生变化时，就会让依赖列表中所有的依赖循环触发`update`方法，也就是`Watcher`中的`update`方法。而`update`方法会执行参数中的回调函数，将`value`和`oldValue`传到参数中。



### 递归侦测所有 key
我们希望把数据中的所有属性（包括子属性）都侦测到，所以要封装一个`Observer`类。这个类的作用是将一个数据内的所有属性（包括子属性）都转换成`getter`/`setter`的形式，然后去追踪它们的变化。

我们定义了`Observer`类，它用来将一个正常的`object`转换成被侦测的`object`。然后判断数据的类型，只有`Object`类型的数据才会调用`walk`将每一个属性转换成`getter`/`setter`的形式来侦测变化。

最后，在`defineReactive`中新增`new Observer(val)`来递归子属性，这样我们就可以把`data`中的所有属性（包括子属性）都转换成`getter`/`setter`的形式来侦测变化。当data中的属性发生变化时，与这个属性对应的依赖就会接收到通知。也就是说，只要我们将一个`object`传到`Observer`中，那么这个`object`就会变成响应式的`object`。

```javascript
/**
 * Observer类会附加到每一个被侦测的object上。
 * 一旦被附加上，Observer会将object的所有属性转换为getter/setter的形式
 * 来收集属性的依赖，并且当属性发生变化时会通知这些依赖
 */
export class Observer {
  constructor (value) {
    this.value = value

    if (!Array.isArray(value)) {
      this.walk(value)
    }
  }

  /**
   * walk会将每一个属性都转换成getter/setter的形式来侦测变化
   * 这个方法只有在数据类型为Object时被调用
   */
  walk (obj) {
    const keys = Object.keys(obj)
    for (let i = 0; i < keys.length; i++) {
      defineReactive(obj, keys[i], obj[keys[i]])
    }
  }
}

function defineReactive (data, key, val) {
  // 新增，递归子属性
  if (typeof val === 'object') {
    new Observer(val)
  }
  let dep = new Dep()
  Object.defineProperty(data, key, {
    enumerable: true,
    configurable: true,
    get: function () {
      dep.depend()
      return val
    },
    set: function (newVal) {
      if(val === newVal){
        return
      }

      val = newVal
      dep.notify()
    }
  })
}
```



### Object 的问题
数据的变化是通过`getter`/`setter`来追踪的。也正是由于这种追踪方式，有些语法中即便是数据发生了变化，Vue.js也追踪不到。

+ 添加属性
+ 删除属性

为了解决这个问题，Vue.js提供了两个API——`vm.$set`与`vm.$delete`



### Data、Observer、Dep 和 Watcher 之间的关系
![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748338195569-cb4a2c88-cd76-46e2-be6a-53b238dbcf1a.png)

## Array 的变化侦测
数组可以通过原型上的方法修改，比如 `push` 等方法。此时 `Object`那种通过`getter`/`setter`的实现方式就行不通了。

### 如何追踪变化
我们可以用自定义的方法去覆盖原生的原型方法。用一个拦截器覆盖`Array.prototype`。之后，每当使用`Array`原型上的方法操作数组时，其实执行的都是拦截器中提供的方法，比如`push`方法。然后，在拦截器中使用原生`Array`的原型方法去操作数组。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748338530215-184dcded-88e1-410d-b339-5de4c49bec5a.png)

### 拦截器
拦截器其实就是一个和`Array.prototype`一样的`Object`，里面包含的属性一模一样，只不过这个`Object`中某些可以改变数组自身内容的方法是我们处理过的。

`Array`原型中可以改变数组自身内容的方法有7个，分别是`push`、`pop`、`shift`、`unshift`、`splice`、`sort`和`reverse`。

```javascript
const arrayProto = Array.prototype
export const arrayMethods = Object.create(arrayProto);
[
  'push',
  'pop',
  'shift',
  'unshift',
  'splice',
  'sort',
  'reverse'
]
.forEach(function (method) {
  // 缓存原始方法
  const original = arrayProto[method]
  Object.defineProperty(arrayMethods, method, {
    value: function mutator (...args) {
      return original.apply(this, args)
    },
    enumerable: false,
    writable: true,
    configurable: true
  })
})
```



### 使用拦截器覆盖 Array 原型
将一个数据转换成响应式的，需要通过`Observer`，所以我们只需要在`Observer`中使用拦截器覆盖那些即将被转换成响应式`Array`类型数据的原型。

将拦截器（加工后具备拦截功能的`arrayMethods`）赋值给`value.__proto__`，通过`__proto__` 可以很巧妙地实现覆盖`value`原型的功能。

```javascript
export class Observer {
  constructor (value) {
    this.value = value

    if (Array.isArray(value)) {
      value.__proto__ = arrayMethods
    } else {
      this.walk(value)
    }
  }
}
```



![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748340097098-8059b183-315a-4f36-8cfc-da84a33b28d5.png)

### 将拦截器方法挂在到数组的属性上
虽然绝大多数浏览器都支持这种非标准的属性（在ES6之前并不是标准）来访问原型，但并不是所有浏览器都支持！因此，我们需要处理不能使用 `__proto__` 的情况。

Vue的做法非常粗暴，如果不能使用 `__proto__`，就直接将`arrayMethods`身上的这些方法设置到被侦测的数组上：

```javascript
import { arrayMethods } from './array'

// __proto__ 是否可用
const hasProto = '__proto__' in {}
const arrayKeys = Object.getOwnPropertyNames(arrayMethods)

export class Observer {
  constructor (value) {
    this.value = value

    if (Array.isArray(value)) {
      // 修改
      const augment = hasProto
        ? protoAugment
        : copyAugment
      augment(value, arrayMethods, arrayKeys)
    } else {
      this.walk(value)
    }
  }

  ……
}

function protoAugment (target, src, keys) {
  target.__proto__ = src
}

function copyAugment (target, src, keys) {
  for (let i = 0, l = keys.length; i < l; i++) {
    const key = keys[i]
    def(target, key, src[key])
  }
}
```

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748340249417-79e78e53-b1f7-4baf-954d-232e04ee4790.png)

### 如何收集依赖
我们之所以创建拦截器，本质上是为了得到一种能力，一种当数组的内容发生变化时得到通知的能力。

`Object`的依赖前面介绍过，是在`defineReactive`中的`getter`里使用`Dep`收集的，每个`key`都会有一个对应的`Dep`列表来存储依赖。

`Array`的依赖和`Object`一样，也在`defineReactive`中收集。



### 依赖列表存在哪儿
Vue.js把`Array`的依赖存放在`Observer`中。

我们之所以将依赖保存在`Observer`实例上，是因为在`getter`中可以访问到`Observer`实例，同时在`Array`拦截器中也可以访问到`Observer`实例。

```javascript
export class Observer {
  constructor (value) {
    this.value = value
    this.dep = new Dep() // 新增dep

    if (Array.isArray(value)) {
      const augment = hasProto
        ? protoAugment
        : copyAugment
      augment(value, arrayMethods, arrayKeys)
    } else {
      this.walk(value)
    }
  }
  // ……
}
```



### 依赖收集
新增了函数`observe`，它尝试创建一个`Observer`实例。如果`value`已经是响应式数据，不需要再次创建`Observer`实例，直接返回已经创建的`Observer`实例即可，避免了重复侦测`value`变化的问题。

通过`observe`我们得到了数组的`Observer`实例（`childOb`），最后通过`childOb`的`dep`执行`depend`方法来收集依赖。

```javascript
function defineReactive (data, key, val) {
  let childOb = observe(val) // 修改
  let dep = new Dep()
  Object.defineProperty(data, key, {
    enumerable: true,
    configurable: true,
    get: function () {
      dep.depend()

      // 新增
      if (childOb) {
        childOb.dep.depend()
      }
      return val
    },
    set: function (newVal) {
      if(val === newVal){
        return
      }

      dep.notify()
      val = newVal
    }
  })
}

/**
 * 尝试为value创建一个Observer实例，
 * 如果创建成功，直接返回新创建的Observer实例。
 * 如果value已经存在一个Observer实例，则直接返回它
 */
export function observe (value, asRootData) {
  if (!isObject(value)) {
    return
  }
  let ob
  if (hasOwn(value, '__ob__') && value.__ob__ instanceof Observer) {
    ob = value.__ob__
  } else {
    ob = new Observer(value)
  }
  return ob
}
```



### 在拦截器中获取 Observer 实例
`Array`拦截器是对原型的一种封装，所以可以在拦截器中访问到`this`（当前正在被操作的数组）。

而`dep`保存在`Observer`中，所以需要在`this`上读到`Observer`的实例：

```javascript
// 工具函数
function def (obj, key, val, enumerable) {
  Object.defineProperty(obj, key, {
    value: val,
    enumerable: !!enumerable,
    writable: true,
    configurable: true
  })
}

export class Observer {
  constructor (value) {
    this.value = value
    this.dep = new Dep()
    def(value, '__ob__', this) // 新增

    if (Array.isArray(value)) {
      const augment = hasProto
        ? protoAugment
        : copyAugment
      augment(value, arrayMethods, arrayKeys)
    } else {
      this.walk(value)
    }
  }
  // ……
}
```

在上面的代码中，我们在`Observer`中新增了一段代码，它可以在`value`上新增一个不可枚举的属性 `__ob__`，这个属性的值就是当前`Observer`的实例。

`__ob__` 的作用不仅仅是为了在拦截器中访问`Observer`实例这么简单，还可以用来标记当前`value`是否已经被`Observer`转换成了响应式数据。

也就是说，所有被侦测了变化的数据身上都会有一个 `__ob__` 属性来表示它们是响应式的。上一节中的`observe`函数就是通过 `__ob__` 属性来判断：如果`value`是响应式的，则直接返回 `__ob__`；如果不是响应式的，则使用`new Observer`来将数据转换成响应式数据。



当`value`身上被标记了 `__ob__` 之后，就可以通过`value.__ob__` 来访问`Observer`实例。如果是`Array`拦截器，因为拦截器是原型方法，所以可以直接通过`this.__ob__`来访问`Observer`实例。

```javascript
;[
  'push',
  'pop',
  'shift',
  'unshift',
  'splice',
  'sort',
  'reverse'
]
.forEach(function (method) {
  // 缓存原始方法
  const original = arrayProto[method]
  Object.defineProperty(arrayMethods, method, {
    value: function mutator (...args) {
      const ob = this.__ob__ // 新增
      return original.apply(this, args)
    },
    enumerable: false,
    writable: true,
    configurable: true
  })
})
```



我们在`mutator`函数里通过`this.__ob__` 来获取`Observer`实例。



### 向数组的依赖发送通知
我们调用了`ob.dep.notify()`去通知依赖（`Watcher`）数据发生了改变。

```javascript
;[
  'push',
  'pop',
  'shift',
  'unshift',
  'splice',
  'sort',
  'reverse'
]
.forEach(function (method) {
  // 缓存原始方法
  const original = arrayProto[method]
  def(arrayMethods, method, function mutator (...args) {
    const result = original.apply(this, args)
    const ob = this.__ob__
    ob.dep.notify()  // 向依赖发送消息
    return result
  })
})
```



### 侦测数组中元素的变化
前面说过如何侦测数组的变化，指的是数组自身的变化，比如是否新增一个元素，是否删除一个元素等。

其实数组中保存了一些元素，它们的变化也是需要侦测的。比如，当数组中object身上某个属性的值发生了变化时，也需要发送通知。

此外，如果用户使用了push往数组中新增了元素，这个新增元素的变化也需要侦测。

**<font style="color:#DF2A3F;">也就是说，所有响应式数据的子数据都要侦测，不论是</font>**`**<font style="color:#DF2A3F;">Object</font>**`**<font style="color:#DF2A3F;">中的数据还是</font>**`**<font style="color:#DF2A3F;">Array</font>**`**<font style="color:#DF2A3F;">中的数据。</font>**



我们要在`Observer`中新增一些处理，让它可以将`Array`中的每一项也转换成响应式的。

```javascript
export class Observer {
  constructor (value) {
    this.value = value
    def(value, '__ob__', this)

    // 新增
    if (Array.isArray(value)) {
      this.observeArray(value)
    } else {
      this.walk(value)
    }
  }

  /**
   * 侦测Array中的每一项
   */
  observeArray (items) {
    for (let i = 0, l = items.length; i < l; i++) {
      observe(items[i])
    }
  }

  // ……
}
```

### 侦测新增元素的变化
**数组中有一些方法是可以新增数组内容的，比如**`**push**`**，而新增的内容也需要转换成响应式来侦测变化，否则会出现修改数据时无法触发消息等问题。因此，我们必须侦测数组中新增元素的变化。**

****

想要获取新增元素，我们需要在拦截器中对数组方法的类型进行判断。如果操作数组的方法是`push`、`unshift`和`splice`（可以新增数组元素的方法），则把参数中新增的元素拿过来，用`Observer`来侦测。

```javascript
;[
  'push',
  'pop',
  'shift',
  'unshift',
  'splice',
  'sort',
  'reverse'
]
.forEach(function (method) {
  // 缓存原始方法
  const original = arrayProto[method]
  def(arrayMethods, method, function mutator (...args) {
    const result = original.apply(this, args)
    const ob = this.__ob__
    let inserted // 获取新增的元素
    switch (method) {
      case 'push':
      case 'unshift':
        inserted = args
        break
      case 'splice':
        inserted = args.slice(2)
        break
    }
    if (inserted) ob.observeArray(inserted) // 对新增数据进行响应式处理
    ob.dep.notify()
    return result
  })
})
```



### Array 的问题
对Array的变化侦测是通过拦截原型的方式实现的。正是因为这种实现方式，其实有些数组操作Vue.js是拦截不到的。

+ 通过数组下标修改元素值
+ 修改数组 length

## 变化侦测相关的 API 实现原理
### vm.$watch
#### 用法
`vm.$watch( expOrFn, callback, [options] )`，用于观察一个表达式或computed函数在Vue.js实例上的变化。



`vm.$watch`返回一个取消观察函数，用来停止触发回调：

```javascript
var unwatch = vm.$watch('a', (newVal, oldVal) => {})
// 之后取消观察
unwatch()
```



为了发现对象内部值的变化，可以在选项参数中指定`deep: true`：

```javascript
vm.$watch('someObject', callback, {
  deep: true
})
vm.someObject.nestedValue = 123
// 回调函数将被触发
```



`immediate`。在选项参数中指定`immediate: true`，将立即以表达式的当前值触发回调：

```javascript
vm.$watch('a', callback, {
  immediate: true
})
// 立即以 'a' 的当前值触发回调
```



#### watch 的内部原理
`vm.$watch`其实是对`Watcher`的一种封装。

```javascript
Vue.prototype.$watch = function (expOrFn, cb, options) {
  const vm = this
  options = options || {}
  const watcher = new Watcher(vm, expOrFn, cb, options)
  if (options.immediate) {
    cb.call(vm, watcher.value)
  }
  return function unwatchFn () {
    watcher.teardown()
  }
}
```

	

如果`expOrFn`是函数，则直接将它赋值给`getter`；如果不是函数，再使用`parsePath`函数来读取`keypath`中的数据。这里`keypath`指的是属性路径，例如`a.b.c.d`就是一个`keypath`，说明从`vm.a.b.c.d`中读取数据。

当`expOrFn`是函数时，会发生很神奇的事情。它不只可以动态返回数据，其中读取的所有数据也都会被`Watcher`观察。**<font style="color:#DF2A3F;">当</font>**`**<font style="color:#DF2A3F;">expOrFn</font>**`**<font style="color:#DF2A3F;">是字符串类型的</font>**`**<font style="color:#DF2A3F;">keypath</font>**`**<font style="color:#DF2A3F;">时，</font>**`**<font style="color:#DF2A3F;">Watcher</font>**`**<font style="color:#DF2A3F;">会读取这个</font>**`**<font style="color:#DF2A3F;">keypath</font>**`**<font style="color:#DF2A3F;">所指向的数据并观察这个数据的变化。而当</font>**`**<font style="color:#DF2A3F;">expOrFn</font>**`**<font style="color:#DF2A3F;">是函数时，</font>**`**<font style="color:#DF2A3F;">Watcher</font>**`**<font style="color:#DF2A3F;">会同时观察</font>**`**<font style="color:#DF2A3F;">expOrFn</font>**`**<font style="color:#DF2A3F;">函数中读取的所有</font>**`**<font style="color:#DF2A3F;">Vue.js</font>**`**<font style="color:#DF2A3F;">实例上的响应式数据</font>**。也就是说，如果函数从Vue.js实例上读取了两个数据，那么Watcher会同时观察这两个数据的变化，当其中任意一个发生变化时，Watcher都会得到通知。说明事实上，Vue.js中计算属性（`Computed`）的实现原理与`expOrFn`支持函数有很大的关系。

```javascript
export default class Watcher {
  constructor (vm, expOrFn, cb) {
    this.vm = vm
    // expOrFn参数支持函数
    if (typeof expOrFn === 'function') {
      this.getter = expOrFn
    } else {
      this.getter = parsePath(expOrFn)
    }
    this.cb = cb
    this.value = this.get()
  }

  // ……
}
```



#### deep 参数的实现原理
要想实现`deep`的功能，其实就是除了要触发当前这个被监听数据的收集依赖的逻辑之外，还要把当前监听的这个值在内的所有子值都触发一遍收集依赖逻辑。

```javascript
export default class Watcher {
  constructor (vm, expOrFn, cb, options) {
    this.vm = vm

    // 新增
    if (options) {
      this.deep = !!options.deep
    } else {
      this.deep = false
    }

    this.deps = []
    this.depIds = new Set()
    this.getter = parsePath(expOrFn)
    this.cb = cb
    this.value = this.get()
  }

  get () {
    window.target = this
    let value = this.getter.call(vm, vm)
    // 新增
    if (this.deep) {
      traverse(value)
    }
    window.target = undefined
    return value
  }

  // ……
}
```

在上面的代码中，如果用户使用了`deep`参数，则在`window.target = undefined`之前调用`traverse`来处理`deep`的逻辑。

一定要在`window.target = undefined`之前去触发子值的收集依赖逻辑，这样才能保证子集收集的依赖是当前这个`Watcher`。

要递归`value`的所有子值来触发它们收集依赖的功能。

```javascript
const seenObjects = new Set()

export function traverse (val) {
  _traverse(val, seenObjects)
  seenObjects.clear()
}

function _traverse (val, seen) {
  let i, keys
  const isA = Array.isArray(val)
  
  // 它不是Array和Object，或者已经被冻结，那么直接返回，什么都不干。
  if ((!isA && !isObject(val)) || Object.isFrozen(val)) {
    return
  }
  
  // 然后拿到val的dep.id，用这个id来保证不会重复收集依赖。
  if (val.__ob__) {
    const depId = val.__ob__.dep.id
    if (seen.has(depId)) {
      return
    }
    seen.add(depId)
  }

  // 如果是数组，则循环数组，将数组中的每一项递归调用 _traverse
  if (isA) {
    i = val.length
    while (i--) _traverse(val[i], seen)
  } else {
    // 如果是Object类型的数据，则循环Object中的所有key，然后执行一次读取操作，再递归子值：
    // 其中val[keys[i]] 会触发getter，也就是说会触发收集依赖的操作，
    // 这时window.target还没有被清空，会将当前的Watcher收集进去
    keys = Object.keys(val)
    i = keys.length
    while (i--) _traverse(val[keys[i]], seen)
  }
}
```



### vm.$set
#### 用法
`vm.$set( target, key, value )`

使用它，可以为`object`新增属性，然后Vue.js就可以将这个新增属性转换成响应式的。

#### 源码
```javascript
export function set (target: Array<any> | Object, key: any, val: any): any {

  // 数组时: 通过splice给新增的val转换为响应式
  if (Array.isArray(target) && isValidArrayIndex(key)) {
    target.length = Math.max(target.length, key)
    target.splice(key, 1, val)
    return val
  }

  // 已存在时: 直接修改数据
  if (key in target && !(key in Object.prototype)) {
    target[key] = val
    return val
  }
  
  const ob = (target: any).__ob__
  // 判断target是否为Vue实例或根数据对象
  // 满足上述任一条件（即目标是Vue实例或根数据对象），则：
  // 直接返回, 不做响应式处理
  if (target._isVue || (ob && ob.vmCount)) {
    return val
  }

  // 如果target不是响应式数据, 也直接返回
  if (!ob) {
    target[key] = val
    return val
  }

  // 在响应式数据上新增一个属性, 然后向target的依赖触发变化通知
  defineReactive(ob.value, key, val)
  ob.dep.notify()
  return val
}

```

### vm.$delete
`vm.$delete`的作用是删除数据中的某个属性。由于Vue.js的变化侦测是使用`Object.defineProperty`实现的，所以如果数据是使用`delete`关键字删除的，那么无法发现数据发生了变化。

#### 用法
`vm.$delete( target, key )`

#### 源码
```javascript
export function del (target: Array<any> | Object, key: any) {
  // 数组时: 通过splice自动向依赖发送通知
  if (Array.isArray(target) && isValidArrayIndex(key)) {
    target.splice(key, 1)
    return
  }
  
  const ob = (target: any).__ob__
  // 判断target是否为Vue实例或根数据对象
  // 满足上述任一条件（即目标是Vue实例或根数据对象），则：
  // 直接返回, 不做响应式处理
  if (target._isVue || (ob && ob.vmCount)) {
    return
  }

  // 不是target上的属性, 终止
  if (!hasOwn(target, key)) {
    return
  }

  delete target[key]

  // 不是响应式数据, 不处理
  if (!ob) {
    return
  }

  // 通知依赖
  ob.dep.notify()
}
```

# 虚拟 DOM
`vnode`是`JavaScript`中一个很普通的对象，这个对象的属性上保存了生成`DOM`节点所需要的一些数据。

对两个虚拟节点进行比对是虚拟`DOM`中最核心的算法（即`patch`），它可以判断出哪些节点发生了变化，从而只对发生了变化的节点进行更新操作。

虚拟`DOM`在Vue.js中所做的事是提供虚拟节点`vnode`和对新旧两个`vnode`进行比对，并根据比对结果进行DOM操作来更新视图。



## VNode
vnode可以理解成节点描述对象，它描述了应该怎样去创建真实的DOM节点。

渲染视图的过程是先创建vnode，然后再使用vnode去生成真实的DOM元素，最后插入到页面渲染视图。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748418794874-9d0f752d-b07f-4e17-905e-1d7b0b3e6251.png)



**Vue.js目前对状态的侦测策略采用了中等粒度。当状态发生变化时，只通知到组件级别，然后组件内使用虚拟DOM来渲染视图。**



**节点类型**

+ **注释节点**
+ **文本节点**
+ **元素节点**
+ **组件节点**
+ **函数式组件**
+ **克隆节点**

## patch
虚拟DOM最核心的部分是`patch`，它可以将`vnode`渲染成真实的DOM。

`patch`也可以叫作`patching`算法，通过它渲染真实DOM时，并不是暴力覆盖原有DOM，而是比对新旧两个`vnode`之间有哪些不同，然后根据对比结果找出需要更新的节点进行更新。

之所以要这么做，主要是因为DOM操作的执行速度远不如`JavaScript`的运算速度快。因此，把大量的DOM操作搬运到JavaScript中，使用`patching`算法来计算出真正需要更新的节点，最大限度地减少DOM操作，从而显著提升性能。这本质上其实是使用JavaScript的运算成本来替换DOM操作的执行成本，而JavaScript的运算速度要比DOM快很多，这样做很划算，所以才会有虚拟DOM。



对比两个vnode之间的差异只是patch的一部分，这是手段，而不是目的。**patch的目的其实是修改DOM节点，也可以理解为渲染视图。**



### patch 介绍
patch的过程其实就是创建节点、删除节点和修改节点的过程。

+ 新增节点
    - 当`oldVnode`不存在而`vnode`存在时，就需要使用vnode生成真实的DOM元素并将其插入到视图中
    - 当`vnode`和`oldVnode`完全不是同一个节点时，需要使用vnode生成真实的DOM元素并将其插入到视图当中。
+ 删除节点
    - 当一个节点只在`oldVnode`中存在时，我们需要把它从DOM中删除
    - 当`oldVnode`和`vnode`完全不是同一个节点时，替换过程是将新创建的DOM节点插入到旧节点的旁边，然后再将旧节点删除，从而完成替换过程
+ 更新节点：当新旧两个节点是相同的节点时，我们需要对这两个节点进行比较细致的比对，然后对`oldVnode`在视图中所对应的真实节点进行更新。



![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748424338386-47972b7b-4559-46ce-b153-2ad5bf5a5ac6.png)





### 更新子节点策略
当新节点的子节点和旧节点的子节点都存在并且不相同时，会进行子节点的更新操作。

更新子节点大概可以分为4种操作：更新节点、新增节点、删除节点、移动节点位置。



对比两个子节点列表（`children`），首先需要做的事情是循环。循环`newChildren`（新子节点列表），每循环到一个新子节点，就去`oldChildren`（旧子节点列表）中找到和当前节点相同的那个旧子节点。

如果在`oldChildren`中找不到，说明当前子节点是由于状态变化而新增的节点，我们要进行创建节点并插入视图的操作；如果找到了，就做更新操作；如果找到的旧子节点的位置和新子节点不同，则需要移动节点等。



![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748484794085-943bb0ea-5afa-4c6b-8c4d-b98316092e37.png)





# 模版编译原理
## 模版编译
**模板编译的主要目标就是生成渲染函数。**

模板编译在整个渲染过程中的位置。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748486274057-16d5f6fe-1427-49fb-9822-edd3f56fadcc.png)



### 将模板编译成渲染函数
将模板编译成渲染函数可以分两个步骤，先将模板解析成AST（`Abstract SyntaxTree`，抽象语法树），然后再使用AST生成渲染函数。

但是由于静态节点不需要总是重新渲染，所以在生成AST之后、生成渲染函数之前这个阶段，需要做一个操作，那就是遍历一遍AST，给所有静态节点做一个标记，这样在虚拟DOM中更新节点时，如果发现节点有这个标记，就不会重新渲染它。



所以，在大体逻辑上，模板编译分三部分内容：

+ 将模板解析为AST
+ 遍历AST标记静态节点
+ 使用AST生成渲染函数



这三部分内容在模板编译中分别抽象出三个模块来实现各自的功能，分别是：

+ 解析器
+ 优化器
+ 代码生成器

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748499979767-953bba85-7497-4ac9-b9a3-64f69bbb3a45.png)



#### 解析器
作用就是将模板解析成AST。

在解析器内部，分成了很多小解析器，其中包括过滤器解析器、文本解析器和HTML解析器。



#### 优化器
作用是遍历AST，检测出所有静态子树（永远都不会发生变化的DOM节点）并给其打标记。

总体来说，优化器的主要作用是避免一些无用功来提升性能。因为静态节点除了首次渲染，后续不需要任何重新渲染操作。



#### 代码生成器
作用是将AST转换成渲染函数中的内容，这个内容可以称为“代码字符串”。



例如，一个简单的模板：

```html
<p title="Berwin" @click="c">1</p>
```

生成后的代码字符串是：

```javascript
with(this){
  return _c(
    'p',
    {
      attrs:{"title":"Berwin"},
      on:{"click":c}
    },
    [_v("1")]
  )
}
```

这样一个代码字符串最终导出到外界使用时，会将代码字符串放到函数里，这个函数叫作渲染函数。

## 解析器
解析器要实现的功能是将模板解析成AST。

```html
<div>
  <p>{{name}}</p>
</div>
```

转换成AST后的样子如下：

```javascript
{
  tag: "div"
  type: 1,
  staticRoot: false,
  static: false,
  plain: true,
  parent: undefined,
  attrsList: [],
  attrsMap: {},
  children: [
    {
      tag: "p"
      type: 1,
      staticRoot: false,
      static: false,
      plain: true,
      parent: {tag: "div", ...},
      attrsList: [],
      attrsMap: {},
      children: [{
        type: 2,
        text: "{{name}}",
        static: false,
        expression: "_s(name)"
      }]
    }
  ]
}
```



**其实AST并不是什么很神奇的东西，不要被它的名字吓倒。它只是用JavaScript中的对象来描述一个节点，一个对象表示一个节点，对象中的属性用来保存节点。**

****

构建AST层级关系其实非常简单，我们只需要维护一个栈（stack）即可，用栈来记录层级关系，这个层级关系也可以理解为DOM的深度。



## 优化器
作用是在AST中找出静态子树并打上标记。



标记静态子树有两点好处：

+ 每次重新渲染时，不需要为静态子树创建新节点；
+ 在虚拟DOM中打补丁（patching）的过程可以跳过。



优化器的内部实现主要分为两个步骤：

1. 在AST中找出所有静态节点并打上标记；
2. 在AST中找出所有静态根节点并打上标记。



什么是静态根节点？如果一个节点下面的所有子节点都是静态节点，并且它的父级是动态节点，那么它就是静态根节点。



### 判断一个节点是否为静态节点
```javascript
function isStatic (node) {
  if (node.type === 2) { // 带变量的动态文本节点
    return false
  }
  if (node.type === 3) { // 不带变量的纯文本节点
    return true
  }
  return !!(node.pre || (
    !node.hasBindings && // 没有动态绑定
    !node.if && !node.for && // 没有v-if或v-for或v-else
    !isBuiltInTag(node.tag) && // 不是内置标签
    isPlatformReservedTag(node.tag) && // 不是组件
    !isDirectChildOfTemplateFor(node) &&
    Object.keys(node).every(isStaticKey)
  ))
}
```

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748502297322-ac994d18-7604-4c27-bc5b-a97fff4da54f.png)



静态子树的所有子节点应该都是静态节点。因此，我们需要在子节点被打上标记之后重新校对当前节点的标记是否准确，具体的做法是：

```javascript
function markStatic (node) {
  node.static = isStatic(node)
  if (node.type === 1) {
    for (let i = 0, l = node.children.length; i < l; i++) {
      const child = node.children[i]
      markStatic(child)

      if (!child.static) { // 如果有子节点不是静态节点, 则该节点也不是静态节点
        node.static = false
      }
    }
  }
}
```



### 标记所有的静态根节点
找出静态根节点的过程与找出静态节点的过程类似，都是从根节点开始向下一层一层地用递归方式去找。不一样的是，如果一个节点被判定为静态根节点，那么将不会继续向它的子级继续寻找。因为静态子树肯定只有一个根，就是最上面的那个静态节点。



有一种情况，即便它真的是静态根节点，也不会被标记为静态根节点，因为其优化成本大于收益。这种情况是一个元素节点只有一个文本节点或者没有子节点。



静态根节点的标记在静态节点标记之后。



## 代码生成器
是将AST转换成渲染函数中的内容，这个内容可以称为代码字符串。

代码字符串可以被包装在函数中执行，这个函数就是我们通常所说的渲染函数。

渲染函数被执行之后，可以生成一份VNode，而虚拟DOM可以通过这个VNode来渲染视图。



+ 元素节点：`createElement`(`_c`)
+ 文本节点：`createTextVNode`(`_v`)
+ 注释节点：`createEmptyVNode`(`_e`)



如果节点是元素节点，那么代码字符串是这样的：

`_c(<tagname>, <data>, <children>)`



举例：

模版代码：

```html
<div id="app">
  <p>{{name}}</p>
</div>

```



生成的代码字符串：

```javascript
with(this) {
  return _c('div', {
    attrs: {
      "id": "app"
    }
  }, [_c('p', [_v(_s(name))])])
}
```



# 整体流程
## 架构设计与项目结构
### 目录结构
```bash
├── scripts                  # 与构建相关的脚本和配置文件
├── dist                     # 构建后的文件
├── flow                     # Flow的类型声明
├── packages                 # vue-server-renderer和vue-template-compiler，它们作为单独的
│                              NPM包发布
├── test                     # 所有的测试代码
├── src                      # 源代码
│   ├── compiler             # 与模板编译相关的代码
│   ├── core                 # 通用的、与平台无关的运行时代码
│   │   ├── observer         # 实现变化侦测的代码
│   │   ├── vdom             # 实现虚拟DOM的代码
│   │   ├── instance         # Vue.js实例的构造函数和原型方法
│   │   ├── global-api       # 全局API的代码
│   │   └── components       # 通用的抽象组件
│   ├── server               # 与服务端渲染相关的代码
│   ├── platforms            # 特定平台代码
│   ├── sfc                  # 单文件组件（* .vue文件）解析逻辑
│   └── shared               # 整个项目的公用工具代码
└── types                    # TypeScript类型定义
    └── test                 # 类型定义测试
```



#### 构建版本
+ 完整版：构建后的文件同时包含**编译器**和**运行时**。
+ 编译器：负责将模板字符串编译成JavaScript渲染函数
+ 运行时：负责创建Vue.js实例，渲染视图和使用虚拟DOM实现重新渲染，基本上包含除编译器外的所有部分。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748505011462-b68b3896-2e69-4ba7-81a1-153829a3541b.png)



#### 打包格式
+ `UMD`：UMD版本的文件可以通过 <script> 标签直接在浏览器中使用。jsDelivr CDN提供的可以在线引入Vue.js的地址（[https://cdn.jsdelivr.net/npm/vue](https://cdn.jsdelivr.net/npm/vue)），就是运行时+编译器的UMD版本。
+ `CommonJS`：CommonJS版本用来配合较旧的打包工具，比如Browserify或webpack 1，这些打包工具的默认文件（pkg.main）只包含运行时的CommonJS版本（vue.runtime.common.js）。
+ `ES Module`：ES Module版本用来配合现代打包工具，比如webpack 2或Rollup，这些打包工具的默认文件（pkg.module）只包含运行时的ES Module版本（vue.runtime.esm.js）。



### 架构设计
**整体分为三个部分：核心代码、跨平台相关和公用工具函数。**

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748505407231-1b88b1ca-d6d6-4148-9de7-235c9944add0.png)





1. 架构是分层的，最底层是一个普通的构造函数，最上层是一个入口，也就是将一个完整的构造函数导出给用户使用
2. 构造函数上一层的一些方法会最终添加到构造函数的prototype属性中
3. 再上一层的方法最终会添加到构造函数上，这些方法叫作全局API（Global API），例如Vue.use
4. 再往上一层是与跨平台相关的内容
5. 在构建时，首先会选择一个平台，然后将特定于这个平台的代码加载到构建文件中
6. 再上一层是渲染层，其中包含两部分内容：服务端渲染相关的内容和编译器相关的内容。同时，这一层的内容是可选的，构建时会根据构建的目标文件来选择是否需要将编译器加载进来。事实上，这一层并不权威，因为服务端渲染相关的代码只存在于Web平台下，而且这两个平台有各自的编译器配置。这里之所以把它们放到渲染层，是因为它们都是与渲染相关的内容。

如果构建只包含运行时代码的版本，就不会将渲染层中编译器部分的代码加载进来。

7. 最顶层是入口，也可以叫作出口。对于构建工具和Vue.js的使用者来说，这是入口；对于Vue.js自身来说，这是出口。在构建文件时，不同平台的构建文件会选择不同的入口进行构建操作。



从整体结构上看，下面三层的代码是与平台无关的核心代码，上面三层是与平台相关的代码。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748505743675-4e8aaba4-7c2c-48ba-a8ed-c6ddeb383a70.png)



## 实例方法与全局 API 的实现原理
```javascript
import { initMixin } from './init'
import { stateMixin } from './state'
import { renderMixin } from './render'
import { eventsMixin } from './events'
import { lifecycleMixin } from './lifecycle'
import { warn } from '../util/index'

function Vue (options) {
  if (process.env.NODE_ENV !== 'production' &&
      !(this instanceof Vue)
     ) {
    warn('Vue is a constructor and should be called with the `new` keyword')
  }
  this._init(options)
}

initMixin(Vue)
stateMixin(Vue)
eventsMixin(Vue)
lifecycleMixin(Vue)
renderMixin(Vue)

export default Vue
```

定义了Vue构造函数，然后分别调用了`initMixin`、`stateMixin`、`eventsMixin`、`lifecycleMixin`和`renderMixin`这5个函数，并将Vue构造函数当作参数传给了这5个函数。这5个函数的作用就是向`Vue`的原型中挂载方法。以函数`initMixin`为例，它的实现方式是这样的：

```javascript
export function initMixin (Vue) {
  Vue.prototype._init = function (options) {
    // 做些什么
  }
}
```

当函数`initMixin`被调用时，会向`Vue`构造函数的`prototype`属性添加`_init`方法。执行`new Vue()`时，会调用 `_init`方法，该方法实现了一系列初始化操作，包括整个生命周期的流程以及响应式系统流程的启动等。



### 数据相关的实例方法
与数据相关的实例方法有3个，分别是`vm.$watch`、`vm.$set`和`vm.$delete`。它们是在`stateMixin`中挂载到`Vue`的原型上的。



### 事件相关的实例方法
与事件相关的实例方法有4个，分别是：`vm.$on`、`vm.$once`、`vm.$off`和`vm.$emit`。这4个方法是在`eventsMixin`中挂载到`Vue`构造函数的`prototype`属性中的。

#### vm.$on
用法：`vm.$on(event, callback)`，监听当前实例上的自定义事件，事件可以由`vm.$emit`触发。回调函数会接收所有传入事件所触发的函数的额外参数。

事件的实现方式并不难，只需要在注册事件时将回调函数收集起来，在触发事件时将收集起来的回调函数依次调用即可。

`vm._events`是一个对象，用来存储事件，在执行`new Vue()`时，`Vue`会执行`this._init`方法进行一系列初始化操作，其中就会在Vue.js的实例上创建一个 `_events`属性，用来存储事件。

```javascript
Vue.prototype.$on = function (event, fn) {
  const vm = this
  if (Array.isArray(event)) {
    for (let i = 0, l = event.length; i < l; i++) {
      this.$on(event[i], fn)
    }
  } else {
    (vm._events[event] || (vm._events[event] = [])).push(fn)
  }
  return vm
}
```

#### vm.$off
用法：`vm.$off([event, callback])`，移除自定义事件监听器。

+ 如果没有提供参数，则移除所有的事件监听器。
+ 如果只提供了事件，则移除该事件所有的监听器。
+ 如果同时提供了事件与回调，则只移除这个回调的监听器。



```javascript
Vue.prototype.$off = function (event, fn) {
  const vm = this
  // 没有提供参数，则移除所有的事件监听器
  if (!arguments.length) {
    vm._events = Object.create(null)
    return vm
  }

  // event支持数组
  if (Array.isArray(event)) {
    for (let i = 0, l = event.length; i < l; i++) {
      this.$off(event[i], fn)
    }
    return vm
  }

  const cbs = vm._events[event]
  if (!cbs) {
    return vm
  }
  
  // 只提供了事件，则移除该事件所有的监听器。
  if (arguments.length === 1) {
    vm._events[event] = null
    return vm
  }

  // 只移除与fn相同的监听器
  if (fn) {
    const cbs = vm._events[event]
    let cb
    let i = cbs.length
    while (i--) {
      cb = cbs[i]
      if (cb === fn || cb.fn === fn) {
        cbs.splice(i, 1)
        break
      }
    }
  }
  return vm
}
```



#### vm.$once
用法： `vm.$once(event, callback)`，监听一个自定义事件，但是只触发一次，在第一次触发之后移除监听器。

实现这个功能的一个思路是：在`vm.$once`中调用`vm.$on`来实现监听自定义事件的功能，当自定义事件触发后会执行拦截器，将监听器从事件列表中移除。

```javascript
Vue.prototype.$once = function (event, fn) {
  const vm = this
  function on () {
    vm.$off(event, on)
    fn.apply(vm, arguments)
  }
  on.fn = fn
  vm.$on(event, on)
  return vm
}
```



#### vm.$emit
用法：`vm.$emit( event, [...args] )`，触发当前实例上的事件。附加参数都会传给监听器回调。

所有的事件监听器回调函数都会存储在`vm._events`中，所以触发事件的实现思路是使用事件名从`vm._events`中取出对应的事件监听器回调函数列表，然后依次执行列表中的监听器回调并将参数传递给监听器回调。

```javascript
Vue.prototype.$emit = function (event) {
  const vm = this
  let cbs = vm._events[event]
  if (cbs) {
    const args = toArray(arguments, 1)
    for (let i = 0, l = cbs.length; i < l; i++) {
      try {
        cbs[i].apply(vm, args)
      } catch (e) {
        handleError(e, vm, `event handler for "${event}"`)
      }
    }
  }
  return vm
}
```



### 生命周期相关的方法
与生命周期相关的实例方法有4个，分别是`vm.$mount`、`vm.$forceUpdate`、`vm.$nextTick`和`vm.$destroy`。

其中有两个方法是从`lifecycleMixin`中挂载到`Vue`构造函数的`prototype`属性上的，分别是`vm.$forceUpdate`和`vm.$destroy`。

`vm.$nextTick`方法是从`renderMixin`中挂载到`Vue`构造函数的`prototype`属性上的。

`vm.$mount`方法则是在跨平台的代码中挂载到`Vue`构造函数的`prototype`属性上的。

#### vm.$forceUpdate
作用：`vm.$forceUpdate()`的作用是迫使Vue.js实例重新渲染。注意它仅仅影响实例本身以及插入插槽内容的子组件，**<font style="color:#DF2A3F;">而不是所有子组件</font>**。

我们只需要执行实例`watcher`的`update`方法，就可以让实例重新渲染。Vue.js的每一个实例都有一个`watcher`。手动执行实例`watcher`的`update`方法，就可以使Vue.js实例重新渲染。



#### vm.$destroy
作用：完全销毁一个实例，它会清理该实例与其他实例的连接，并解绑其全部指令及监听器，同时会触发`beforeDestroy`和`destroyed`的钩子函数。

这个方法并不是很常用，大部分场景下并不需要销毁组件，只需要使用v-if或者v-for等指令以数据驱动的方式控制子组件的生命周期即可。



**销毁实例的逻辑：**

1. 向Vue.js实例添加 `_isBeingDestroyed`属性来表示Vue.js实例 准备开始销毁
2. 触发`beforeDestroy`钩子函数
3. 需要清理当前组件与父组件之间的连接。组件就是Vue.js的实例，所以要清理当前组件与父组件之间的连接，只需要将当前组件实例从父组件实例的`$children`属性中删除即可(Vue.js实例的 `$children`属性存储了所有子组件)。
4. 销毁实例上的所有`watcher`，也就是说需要将实例上所有的依赖追踪断掉。
    1. `vm._watcher`：组件所有用到的状态相关的依赖
    2. `vm._watchers`：`vm.$watch`收集的依赖
5. 向Vue.js实例添加 `_isDestroyed`属性来表示Vue.js实例已经被销毁
6. 将当前实例对应 `vnode` 上的指令清空
7. 触发`destroyed`钩子函数
8. 移除实例上的所有事件监听器



完整代码

```javascript
Vue.prototype.$destroy = function () {
  const vm = this
  if (vm._isBeingDestroyed) {
    return
  }
  callHook(vm, 'beforeDestroy')
  vm._isBeingDestroyed = true

  // 删除自己与父级之间的连接
  const parent = vm.$parent
  if (parent && !parent._isBeingDestroyed && !vm.$options.abstract) {
    remove(parent.$children, vm)
  }
  // 从watcher监听的所有状态的依赖列表中移除watcher
  if (vm._watcher) {
    vm._watcher.teardown()
  }
  let i = vm._watchers.length
  while (i--) {
    vm._watchers[i].teardown()
  }
  vm._isDestroyed = true
  // 在vnode树上触发destroy钩子函数解绑指令
  vm.__patch__(vm._vnode, null)
  // 触发destroyed钩子函数
  callHook(vm, 'destroyed')
  // 移除所有的事件监听器
  vm.$off()
}
```



#### vm.$nextTick
[nextTick](https://www.yuque.com/u25370234/rnh6ph/xn5363uuuyc68tio)



#### vm.$mount
[nextTick](https://www.yuque.com/u25370234/rnh6ph/xn5363uuuyc68tio)





### 全局 API 的实现原理


#### Vue.extend
用法：`Vue.extend( options )`，使用基础Vue构造器创建一个“子类”，其参数是一个包含“组件选项”的对象。其中`data`选项是特例，在`Vue.extend()`中，它必须是函数。



其中子类是如何继承Vue的能力的。

```javascript
const Sub = function VueComponent(options) {
  this._init(options)
}
// 继承原型
Sub.prototype = Object.create(Super.prototype)
Sub.prototype.constructor = Sub
Sub.cid = cid++
```

#### Vue.nextTick
用法：`Vue.nextTick( [callback, context] )`，在下次DOM更新循环结束之后执行延迟回调，修改数据之后立即使用这个方法获取更新后的DOM。

与`vm.$nextTick`实现原理一样。

#### Vue.set
用法：`Vue.set( target, key, value)`，设置对象的属性。如果对象是响应式的，确保属性被创建后也是响应式的，同时触发视图更新。这个方法主要用于避开Vue不能检测属性被添加的限制。

与`vm.$set`实现原理一样。

#### Vue.delete
用法：`Vue.delete( target, key )`，删除对象的属性。如果对象是响应式的，确保删除能触发更新视图。这个方法主要用于避开Vue.js不能检测到属性被删除的限制。

与`vm.$delete`实现原理一样。

#### Vue.directive
用法：`Vue.directive( id, [definition] )`，注册或获取全局指令。

```javascript
// 注册
Vue.directive('my-directive', {
  bind: function () {},
  inserted: function () {},
  update: function () {},
  componentUpdated: function () {},
  unbind: function () {}
})

// 注册（指令函数）
Vue.directive('my-directive', function () {
  // 这里将会被bind和update调用
})

// getter方法，返回已注册的指令
var myDirective = Vue.directive('my-directive')
```



实现原理：

`Vue.directive`方法接收两个参数`id和``definition`，它可以注册或获取指令，这取决于`definition`参数是否存在。如果`definition`参数不存在，则使用`id`从`this.options['directives']`中读出指令并将它返回；如果`definition`参数存在，则说明是注册操作，那么进而判断`definition`参数的类型是否是函数。

如果是函数，则默认监听`bind`和`update`两个事件，所以代码中将`definition`函数分别赋值给对象中的`bind`和`update`这两个方法，并使用这个对象覆盖`definition`；如果`definition`不是函数，则说明它是用户自定义的指令对象，此时不需要做任何操作，直接将用户提供的指令对象保存在`this.options['directives']`上即可。

```javascript
// 用于保存指令的位置
Vue.options = Object.create(null)
Vue.options['directives'] = Object.create(null)

Vue.directive = function (id, definition) {
  if (!definition) {
    return this.options['directives'][id]
  } else {
    if (typeof definition === 'function') {
      definition = { bind: definition, update: definition }
    }
    this.options['directives'][id] = definition
    return definition
  }
}
```

#### Vue.filter
用法：`Vue.filter( id, [definition] )`，注册或获取全局过滤器。

```javascript
// 注册
Vue.filter('my-filter', function (value) {
  // 返回处理后的值
})

// getter方法，返回已注册的过滤器
var myFilter = Vue.filter('my-filter')
```



Vue.js允许自定义过滤器，可被用于一些常见的文本格式化。过滤器可以用在两个地方：双花括号插值和`v-bind`表达式。过滤器应该被添加在JavaScript表达式的尾部，由“管道”符号指示：

```javascript
<!-- 在双花括号中 -->
{{ message | capitalize }}

<!-- 在v-bind中 -->
<div v-bind:id="rawId | formatId"></div>
```



与`Vue.directive`类似，`Vue.filter`的作用仅仅是注册或获取全局过滤器。它们俩的注册过程也很类似，将过滤器保存在`Vue.options['filters'] `中即可。

#### Vue.component
用法：`Vue.component( id, [definition] )`，注册或获取全局组件。注册组件时，还会自动使用给定的id设置组件的名称。

```javascript
// 注册组件，传入一个扩展过的构造器
Vue.component('my-component', Vue.extend({ /* ... */ }))

// 注册组件，传入一个选项对象（自动调用Vue.extend）
Vue.component('my-component', { /* ... */ })

// 获取注册的组件（始终返回构造器）
var MyComponent = Vue.component('my-component')
```



与`Vue.directive`相同，`Vue.component`只是注册或获取组件。注册组件的实现原理很简单，只需要将组件保存在某个地方即可。

如果发现`definition`参数是`Object`类型，则调用`Vue.extend`方法将它变成Vue的子类，使用`Vue.component`方法注册组件。

```javascript
Vue.options['components'] = Object.create(null)

Vue.component = function (id, definition) {
  if (!definition) {
    return this.options['components'][id]
  } else {
    if (isPlainObject(definition)) {
      definition.name = definition.name || id
      definition = Vue.extend(definition)
    }
    this.options['components'][id] = definition
    return definition
  }
}
```

#### Vue.use
用法：`Vue.use( plugin )`，安装Vue.js插件。如果插件是一个对象，必须提供`install`方法。如果插件是一个函数，它会被作为`install`方法。调用`install`方法时，会将`Vue`作为参数传入。`install`方法被同一个插件多次调用时，插件也只会被安装一次。

```javascript
Vue.use = function (plugin) {
  const installedPlugins = (this._installedPlugins || (this._installedPlugins = []))
  // 判断插件是不是已经被注册过，如果被注册过，则直接终止方法执行
  if (installedPlugins.indexOf(plugin) > -1) {
    return this
  }

  // 获取其他参数, 第一个参数保证是Vue
  const args = toArray(arguments, 1)
  args.unshift(this)
  if (typeof plugin.install === 'function') {
    plugin.install.apply(plugin, args)
  } else if (typeof plugin === 'function') {
    plugin.apply(null, args)
  }
  installedPlugins.push(plugin)
  return this
}
```

#### Vue.mixin
用法：`Vue.mixin( mixin )`，全局注册一个混入（`mixin`），影响注册之后创建的每个Vue.js实例。插件作者可以使用混入向组件注入自定义行为（例如：监听生命周期钩子）。**<font style="color:#DF2A3F;">不推荐在应用代码中使用</font>****。**`Vue.mixin`方法注册后，会影响之后创建的每个Vue.js实例。



其实现原理并不复杂，只是将用户传入的对象与Vue.js自身的`options`属性合并在一起。这里的`this.options`其实就是`Vue.options`。

```javascript
import { mergeOptions } from '../util/index'

export function initMixin (Vue) {
  Vue.mixin = function (mixin) {
    this.options = mergeOptions(this.options, mixin)
    return this
  }
}
```

因为`mixin`方法修改了`Vue.options`属性，而之后创建的每个实例都会用到该属性，所以会影响创建的每个实例。但也正是因为有影响，所以`mixin`在某些场景下才堪称神器。

#### Vue.compile
用法：`Vue.compile( template )`，编译模板字符串并返回包含渲染函数的对象。只在完整版中才有效。

`Vue.compile = compileToFunctions`，其中 `compileToFunctions` 实现原理可查看[vm.$mount](https://www.yuque.com/u25370234/rnh6ph/hgob9l5ov1bra3f9)。

#### Vue.version
提供字符串形式的Vue.js安装版本号。

`Vue.version`是一个属性。在构建文件的过程中，我们会读取`package.json`文件中的`version`，并将读取出的版本号设置到`Vue.version`上。

具体实现步骤是：Vue.js在构建文件的配置中定义了 `__VERSION__` 常量，使用`rollup-plugin-replace`插件在构建的过程中将代码中的常量 `__VERSION__` 替换成`package.json`文件中的版本号。



## 生命周期
[生命周期](https://www.yuque.com/u25370234/rnh6ph/bgiw4habk99lc77h)



## 指令的奥秘


## 过滤器的奥秘


## 最佳实践
