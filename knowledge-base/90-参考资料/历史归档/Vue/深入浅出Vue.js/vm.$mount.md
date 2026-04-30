## 用法
我们并不常用这个方法，**其原因是如果在实例化Vue.js时设置了el选项，会自动把Vue.js实例挂载到DOM元素上**。但理解这个方法却非常重要，因为无论我们在实例化Vue.js时是否设置了el选项，想让Vue.js实例具有关联的DOM元素，只有使用vm.$mount方法这一种途径。

用法：`vm.$mount( [elementOrSelector] )`， 如果Vue.js实例在实例化时没有收到el选项，则它处于“未挂载”状态，没有关联的DOM元素。我们可以使用`vm.$mount`手动挂载一个未挂载的实例。如果没有提供`elementOrSelector`参数，模板将被渲染为文档之外的元素，并且必须使用原生DOM的API把它插入文档中。这个方法返回实例自身，因而可以链式调用其他实例方法。

```javascript
var MyComponent = Vue.extend({
  template: '<div>Hello!</div>'
})

// 创建并挂载到#app（会替换#app）
new MyComponent().$mount('#app')

// 创建并挂载到#app（会替换#app）
new MyComponent({ el: '#app' })

// 或者，在文档之外渲染并且随后挂载
var component = new MyComponent().$mount()
document.getElementById('app').appendChild(component.$el)
```



## 不同版本下的实现
完整版和只包含运行时版本之间的差异在于是否有编译器，而是否有编译器的差异主要在于`vm.$mount`方法的表现形式。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1748572909655-5c3a2fbb-ed88-49d2-b1ff-f70d9778a0e5.png)



### 运行时
在只包含运行时的构建版本中，`vm.$mount`的作用如上面介绍的那样。

只包含运行时版本的`vm.$mount`没有编译步骤，它会默认实例上已经存在渲染函数，如果不存在，则会设置一个。并且，这个渲染函数在执行时会返回一个空节点的`VNode`，以保证执行时不会因为函数不存在而报错。

### 完整版(包括编译器)
它首先会检查`template`或`el`选项所提供的模板是否已经转换成渲染函数（`render`函数）。如果没有，则立即进入编译过程，将模板编译成渲染函数，完成之后再进入挂载与渲染的流程中。



## 实现原理
我们将Vue原型上的 `$mount`方法保存在`mount`中，以便后续使用。然后Vue原型上的 `$mount`方法被一个新的方法覆盖了。新方法中会调用原始的方法，这种做法通常被称为函数劫持。

通过函数劫持，可以在原始功能之上新增一些其他功能。在 下面的代码中，`vm.$mount`的原始方法就是`mount`的核心功能，而在完整版中需要将编译功能新增到核心功能上去。

```javascript
const mount = Vue.prototype.$mount
Vue.prototype.$mount = function (el) {
  // 做些什么
  return mount.call(this, el)
}
```



### 运行时版
对`el`进行类型判断，如果是字符串，则使用`document.querySelector`获取DOM元素，如果获取不到，则创建一个空的`div`元素。如果`el`的类型不是字符串，那么认为它是元素类型，直接返回`el`（如果执行`vm.$mount`方法时没有传递el参数，则返回`undefined`）。

```javascript
const mount = Vue.prototype.$mount
Vue.prototype.$mount = function (el) {
  el = el && inBrowser ? query(el) : undefined
  return mount.call(this, el)
}

function query (el) {
  if (typeof el === 'string') {
    const selected = document.querySelector(el)
    if (!selected) {
      return document.createElement('div')
    }
    return selected
  } else {
    return el
  }
}
```



### 完整版
```javascript
function idToTemplate (id) {
  const el = query(id)
  return el && el.innerHTML
}

function getOuterHTML (el) {
  if (el.outerHTML) {
    return el.outerHTML
  } else {
    const container = document.createElement('div')
    container.appendChild(el.cloneNode(true))
    return container.innerHTML
  }
}

const mount = Vue.prototype.$mount
Vue.prototype.$mount = function (el) {
  el = el && query(el)

  const options = this.$options

  // 是否存在渲染函数，只有不存在时，才会将模板编译成渲染函数
  if (!options.render) {
    let template = options.template
    if (template) {
      if (typeof template === 'string') {
        // template是字符串并且以#开头，则它将被用作选择符。
        // 通过选择符获取DOM元素后，会使用innerHTML作为模板。
        if (template.charAt(0) === '#') {
          template = idToTemplate(template)
        }
      } else if (template.nodeType) {
      // template是字符串，但不是以#开头，就说明template是用户设置的模板
      // 不需要进行任何处理，直接使用即可
        template = template.innerHTML
      } else {
        return this
      }
    } else if (el) {
      // 没有template选项，那么使用getOuterHTML方法从用户提供的el选项中获取模板
      template = getOuterHTML(el)
    }

    // 将模板编译成渲染函数（render函数）赋值给render选项。
    if (template) {
      const { render } = compileToFunctions(
        template,
        {...},
        this
      )
      options.render = render
    }
  }

  return mount.call(this, el)
}
```



## 模版编译成渲染函数
将模板编译成代码字符串并将代码字符串转换成渲染函数的过程是在`compileToFunctions`函数中完成的。

```javascript
function compileToFunctions (template, options, vm) {
  options = extend({}, options)

  // 检查缓存中是否已经存在编译后的模板。如果模板已经被编译，
  // 就会直接返回缓存中的结果，不会重复编译，保证不做无用功来提升性能。
  const key = options.delimiters
    ? String(options.delimiters) + template
    : template
  if (cache[key]) {
    return cache[key]
  }

  // 编译
  const compiled = compile(template, options)

  // 代码字符串转换为函数
  const res = {}
  res.render = createFunction(compiled.render)

  return (cache[key] = res)
}

function createFunction (code) {
  return new Function(code)
}
```



## mountComponent
### 作用
+ 渲染 DOM
+ 收集模版中的响应式数据进行观察



使用`mountComponent`函数将Vue.js实例挂载到DOM元素上。事实上，**将实例挂载到DOM元素上指的是将模板渲染到指定的DOM元素中，而且是持续性的，以后当数据（状态）发生变化时，依然可以渲染到指定的DOM元素中**。

其中 `_update` 的作用是调用虚拟DOM中的`patch`方法来执行节点的比对与渲染操作，而 `_render` 的作用是执行渲染函数，得到一份最新的VNode节点树。

所以在这段代码中，`vm._update(vm._render())`的作用是先调用渲染函数得到一份最新的VNode节点树，然后通过 `_update`方法对最新的VNode和上一次渲染用到的旧VNode进行对比并更新DOM节点。简单来说，就是执行了渲染操作。

Watcher的第二个参数支持函数，当`watcher`执行函数时，函数中所读取的数据都将会触发`getter`去全局找到`watcher`并将其收集到函数的依赖列表中。也就是说，函数中读取的所有数据都将被`watcher`观察。这些数据中的任何一个发生变化时，`watcher`都将得到通知。



```javascript
export function mountComponent(
  vm: Component,
  el: ?Element,
  hydrating?: boolean
): Component {
  // 将传入的DOM元素赋值给vm.$el
  vm.$el = el;
  // 如果没有render函数
  if (!vm.$options.render) {
    // 使用空的VNode作为render函数
    vm.$options.render = createEmptyVNode;

    // 开发环境发出警告
  }
  // 调用beforeMount生命周期钩子
  callHook(vm, "beforeMount");

  // 定义组件更新函数
  let updateComponent;
  updateComponent = () => {
    // 调用_render生成VNode，然后传递给_update方法更新DOM
    vm._update(vm._render(), hydrating);
  };

  // 创建一个渲染Watcher
  // 当数据变化时，这个Watcher会重新执行updateComponent函数
  // 首次创建时会立即执行一次updateComponent
  new Watcher(
    vm,
    updateComponent,
    noop,
    {
      before() {
        // 在Watcher重新执行updateComponent前调用beforeUpdate钩子
        if (vm._isMounted && !vm._isDestroyed) {
          callHook(vm, "beforeUpdate");
        }
      },
    },
    true /* isRenderWatcher */
  );
  
  // 重置hydrating标志
  hydrating = false;

  // 对于手动挂载的实例，在此处调用mounted钩子
  // 对于渲染创建的子组件，在inserted钩子中调用mounted
  if (vm.$vnode == null) {
    // 设置_isMounted为true表示已挂载
    vm._isMounted = true;
    // 调用mounted生命周期钩子
    callHook(vm, "mounted");
  }
  return vm;
}
```

