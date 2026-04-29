# 原理
`computed`是定义在`vm`上的一个特殊的`getter`方法。之所以说特殊，是因为在`vm`上定义`getter`方法时，`get`并不是用户提供的函数，而是Vue.js内部的一个代理函数。在代理函数中可以结合`Watcher`实现缓存与收集依赖等功能。

我们知道计算属性的结果会被缓存，且只有在计算属性所依赖的响应式属性或者说计算属性的返回值发生变化时才会重新计算。那么，如何知道计算属性的返回值是否发生了变化？这其实是结合`Watcher`的`dirty`属性来分辨的：当`dirty`属性为`true`时，说明需要重新计算“计算属性”的返回值；当`dirty`属性为`false`时，说明计算属性的值并没有变，不需要重新计算。

当计算属性中的内容发生变化后，计算属性的`Watcher`与组件的`Watcher`都会得到通知。计算属性的Watcher会将自己的dirty属性设置为true，当下一次读取计算属性时，就会重新计算一次值。然后组件的Watcher也会得到通知，从而执行render函数进行重新渲染的操作。由于要重新执行render函数，所以会重新读取计算属性的值，这时候计算属性的`Watcher`已经把自己的`dirty`属性设置为`true`，所以会重新计算一次计算属性的值，用于本次渲染。



简单来说，计算属性会通过`Watcher`来观察它所用到的所有属性的变化，当这些属性发生变化时，计算属性会将自身的`Watcher`的`dirty`属性设置为`true`，说明自身的返回值变了。



![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1749452511332-02acb38d-d2dc-4781-bf91-e9c592cc7653.png)



这个`getter`方法被触发时会做两件事。

+ 计算当前计算属性的值，此时会使用`Watcher`去观察计算属性中用到的所有其他数据的变化。同时将计算属性的`Watcher`的`dirty`属性设置为`false`，这样再次读取计算属性时将不再重新计算，除非计算属性所依赖的数据发生了变化。
+ 当计算属性中用到的数据发生变化时，将得到通知从而进行重新渲染操作。



**注意**

如果是在模板中读取计算属性，那么使用组件的`Watcher`观察计算属性中用到的所有数据的变化。如果是用户自定义的`watch`，那么其实是使用用户定义的`Watcher`观察计算属性中用到的所有数据的变化。**<font style="color:#DF2A3F;">其区别在于当计算属性函数中用到的数据发生变化时，向谁发送通知</font>**。



**<font style="color:#DF2A3F;">说明</font>**

计算属性的一个特点是有缓存。计算属性函数所依赖的数据在没有发生变化的情况下，会反复读取计算属性，而计算属性函数并不会反复执行。



# 实现细节
```javascript
// 通过参数告诉Watcher类应该生成一个供计算属性使用的watcher实例。
const computedWatcherOptions = { lazy: true }

// 初始化计算属性
function initComputed (vm, computed) {
  // _computedWatchers保存所有计算属性的watcher实例
  const watchers = vm._computedWatchers = Object.create(null)
  // 计算属性在SSR环境中，只是一个普通的getter方法
  const isSSR = isServerRendering()

  // 循环computed对象
  for (const key in computed) {
    const userDef = computed[key]
    // 获取getter函数
    const getter = typeof userDef === 'function' ? userDef : userDef.get
    if (process.env.NODE_ENV !== 'production' && getter == null) {
      warn(
        `Getter is missing for computed property "${key}".`,
        vm
      )
    }

    // 在非SSR环境中，为计算属性创建内部观察器
    if (!isSSR) {
      watchers[key] = new Watcher(
        vm,
        // 第二个参数的getter是用户设置的计算属性的get函数。
        getter || noop,
        noop,
        computedWatcherOptions
      )
    }

    // 判断当前循环到的计算属性的名字是否已经存在于vm中
    if (!(key in vm)) {
      // 如果不存在，则使用defineComputed函数在vm上设置一个计算属性
      defineComputed(vm, key, userDef)
    } else if (process.env.NODE_ENV !== 'production') {
      // 当计算属性的名字已经存在于vm中时，说明已经有了一个重名的data或者props，
      // 也有可能是与methods重名，这时候不会在vm上定义计算属性。
      if (key in vm.$data) {
        warn(`The computed property "${key}" is already defined in data.`, vm)
      } else if (vm.$options.props && key in vm.$options.props) {
        warn(`The computed property "${key}" is already defined as a prop.`, vm)
      }
    }
  }
}
```



```javascript
const sharedPropertyDefinition = {
  enumerable: true,
  configurable: true,
  get: noop,
  set: noop
}

export function defineComputed (target, key, userDef) {
  // 判断computed是否应该有缓存, 非服务端渲染需要缓存
  const shouldCache = !isServerRendering()

  // 判断userDef的类型是函数还是对象
  if (typeof userDef === 'function') {
    // 如果是函数，则将函数理解为getter函数

    // userDef是一个普通的getter方法，没有缓存。
    // createComputedGetter(key)是计算属性的getter
    sharedPropertyDefinition.get = shouldCache
      ? createComputedGetter(key)
      : userDef
    sharedPropertyDefinition.set = noop
  } else {
    // 如果是对象，则将对象的get方法作为getter方法，set方法作为setter方法。
    sharedPropertyDefinition.get = userDef.get
      ? shouldCache && userDef.cache !== false
        ? createComputedGetter(key)
        : userDef.get
      : noop
    sharedPropertyDefinition.set = userDef.set
      ? userDef.set
      : noop
  }
  if (process.env.NODE_ENV !== 'production' &&
      sharedPropertyDefinition.set === noop) {
    sharedPropertyDefinition.set = function () {
      warn(
        `Computed property "${key}" was assigned to but it has no setter.`,
        this
      )
    }
  }
  // 调用Object.defineProperty方法在target对象上设置key属性
  Object.defineProperty(target, key, sharedPropertyDefinition)
}
```

	

计算属性的缓存与响应式功能主要在于是否将`getter`方法设置为`createComputedGetter`函数执行后的返回结果。



这个函数是一个高阶函数，它接收一个参数`key`并返回另一个函数`computedGetter`。最终被设置到`getter`方法中的函数其实是被返回的`computedGetter`函数。在非服务端渲染环境下，每当计算属性被读取时，`computedGetter`函数都会被执行。



```javascript
function createComputedGetter (key) {
  return function computedGetter () {
    // this._computedWatchers属性保存了所有计算属性的watcher实例
    const watcher = this._computedWatchers && this._computedWatchers[key]

    if (watcher) {
      // 判断watcher.dirty是否为true
      // watcher.dirty属性用于标识计算属性的返回值是否有变化，
      // 如果它为true，说明计算属性所依赖的状态发生了变化，
      // 它的返回值有可能也会有变化，所以需要重新计算得出最新的结果。
      if (watcher.dirty) {
        // 执行this.get方法重新计算一下值，然后将this.dirty设置为false。
        watcher.evaluate()
      }
      if (Dep.target) {
        // 将读取计算属性的那个Watcher添加到计算属性所依赖的所有状态的依赖列表中
        watcher.depend()
      }
      return watcher.value
    }
  }
}
```



使用计算属性的同学大多会有一个疑问：为什么我在模板里只使用了一个计算属性，但是把计算属性中用到的另一个状态给改了，模板会重新渲染，它是怎么知道自己需要重新渲染的呢？

这是因为组件的`Watcher`观察了计算属性中所依赖的所有状态的变化。当计算属性中所依赖的状态发生变化时，组件的`Watcher`会得到通知，然后就会执行重新渲染操作。

```javascript
export default class Watcher {
  constructor (vm, expOrFn, cb, options) {
    // 隐藏无关代码

    if (options) {
      this.lazy = !!options.lazy
    } else {
      this.lazy = false
    }

    this.dirty = this.lazy

    this.value = this.lazy
      ? undefined
      : this.get()
  }

  // 执行this.get方法重新计算一下值，然后将this.dirty设置为false。
  evaluate () {
    this.value = this.get()
    this.dirty = false
  }

  // 遍历this.deps属性, 并依次执行dep实例的depend方法。
  // 该属性中保存了计算属性用到的所有状态的dep实例
  // 而每个属性的dep实例中保存了它的所有依赖

  // 执行dep实例的depend方法可以将组件的watcher实例添加到dep实例的依赖列表中

  // this.deps是计算属性中用到的所有状态的dep实例，
  // 而依次执行了dep实例的depend方法就是将组件的Watcher依次加入到这些dep实例的依赖列表中，
  // 这就实现了让组件的Watcher观察计算属性中用到的所有状态的变化。
  // 当这些状态发生变化时，组件的Watcher会收到通知，从而进行重新渲染操作。
  depend () {
    let i = this.deps.length
    while (i--) {
      this.deps[i].depend()
    }
  }
}
```



# 新版的实现调整
前面我们介绍组件的`Watcher`会观察计算属性中用到的所有数据的变化。这就导致一个问题：如果计算属性中用到的状态发生了变化，但最终计算属性的返回值并没有变，这时计算属性依然会认为自己的返回值变了，组件也会重新走一遍渲染流程。只不过最终由于虚拟DOM的`Diff`中发现没有变化，所以在视觉上并不会发现UI有变化，其实渲染函数会被执行。

也就是说，计算属性只是观察它所用到的所有数据是否发生了变化，但并没有真正去校验它自身的返回值是否有变化，所以当它所使用的数据发生变化后，它就认为自己的返回值也会有变化，但事实并不总是这样。

为了解决这个问题，作者把计算属性的实现做了一些改动，**改动后的逻辑是：组件的**`**Watcher**`**不再观察计算属性用到的数据的变化，而是让计算属性的**`**Watcher**`**得到通知后，计算一次计算属性的值，如果发现这一次计算出来的值与上一次计算出来的值不一样，再去主动通知组件的**`**Watcher**`**进行重新渲染操作。这样就可以解决前面提到的问题，只有计算属性的返回值真的变了，才会重新执行渲染函数。**

****

新版计算属性的内部原理。与之前最大的区别就是组件的`Watcher`不再观察数据的变化了，而是只观察计算属性的`Watcher`（把组件的`watcher`实例添加到计算属性的`watcher`实例的依赖列表中），然后计算属性主动通知组件是否需要进行渲染操作。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1749454113526-302d1521-cc29-459d-84ca-f25c3db61aa3.png)



+ 使用组件的`Watcher`观察计算属性的`Watcher`，也就是把组件的`Watcher`添加到计算属性的`Watcher`的依赖列表中，让计算属性的`Watcher`向组件的`Watcher`发送通知。
+ 使用计算属性的`Watcher`观察计算属性函数中用到的所有数据，当这些数据发生变化时，向计算属性的`Watcher`发送通知。



如果是在模板中读取计算属性，那么使用组件的`Watcher`观察计算属性的`Watcher`；如果是用户使用`vm.$watch`定义的`Watcher`，那么其实是使用用户定义的`Watcher`观察计算属性的`Watcher`。**其区别是当计算属性通过计算发现自己的返回值发生变化后，计算属性的**`**Watcher**`**向谁发送通知。**

****

`createComputedGetter`函数中的内容发生了变化，改动后的代码如下：

```javascript
function createComputedGetter (key) {
  return function computedGetter () {
    const watcher = this._computedWatchers && this._computedWatchers[key]
    if (watcher) {
      // depend方法被执行后，会将读取计算属性的那个Watcher添加到计算属性的Watcher的依赖列表中，
      // 这可以让计算属性的Watcher向使用计算属性的Watcher发送通知。
      watcher.depend()

      // 将watcher.evaluate()的返回值当作计算属性函数的计算结果返回出去。
      return watcher.evaluate()
    }
  }
}
```

```javascript
export default class Watcher {
  constructor (vm, expOrFn, cb, options) {
    // 隐藏无关代码

    if (options) {
      this.computed = !!options.computed
    } else {
      this.computed = false
    }

    this.dirty = this.computed

    if (this.computed) {
      this.value = undefined
      this.dep = new Dep()
    } else {
      this.value = this.get()
    }
  }

  // 当计算属性中用到的数据发生变化时，计算属性的Watcher的update方法会被执行
  // 此时会判断当前Watcher是不是计算属性的Watcher，
  // 如果是，那么有两种模式，一种是主动发送通知，另一种是将dirty设置为true
  update () {
    if (this.computed) {
      if (this.dep.subs.length === 0) {
        this.dirty = true
      } else {
        // activated模式要求至少有一个依赖
        this.getAndInvoke(() => {
          this.dep.notify()
        })
      }
    }
    // 隐藏无关代码
  }

  // 这个函数的作用是对比计算属性的返回值。只有计算属性的返回值真的发生了变化，
  // 才会执行回调，从而主动发送通知让组件的Watcher去执行重新渲染逻辑。
  getAndInvoke (cb) {
    const value = this.get()
    if (
      value !== this.value ||
      isObject(value) ||
      this.deep
    ) {
      const oldValue = this.value
      this.value = value
      this.dirty = false
      if (this.user) {
        try {
          cb.call(this.vm, value, oldValue)
        } catch (e) {
          handleError(e, this.vm, `callback for watcher "${this.expression}"`)
        }
      } else {
        cb.call(this.vm, value, oldValue)
      }
    }
  }

  // evaluate方法稍微有点改动
  evaluate () {
    // 先通过dirty属性判断返回值是否发生了变化，
    if (this.dirty) {
      // 如果发生了变化，就执行get方法重新计算一次，然后将dirty属性设置为false，
      // 表示数据已经是最新的，不需要重新计算，最后返回本次计算出来的结果。
      this.value = this.get()
      this.dirty = false
    }
    return this.value
  }

  // depend方法的改动有点大
  // 不再是将Dep.target添加到计算属性所用到的所有数据的依赖列表中
  // 而是改成了将Dep.target添加到计算属性的依赖列表中
  depend () {
    // this.dep用于在实例化Watcher时进行判断，如果为计算属性用的Watcher，
    // 则实例化一个dep实例并将其放在this.dep属性上。
    if (this.dep && Dep.target) {
      this.dep.depend()
    }
  }
}
```

