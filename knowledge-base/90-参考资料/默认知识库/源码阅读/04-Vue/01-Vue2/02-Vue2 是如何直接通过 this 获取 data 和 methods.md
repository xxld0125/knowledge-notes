#### 
#### 一、调试代码-准备
新建一个`html`文件, `vscode`安装`live server`插件,再右键选择`open with live server`, 这样就可以启用本地的服务器,打开页面进行浏览器调试.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script src="https://unpkg.com/vue@2.6.14/dist/vue.js"></script>
    <script>
        const vm = new Vue({
            data: {
                name: 'test_vue',
            },
            methods: {
                sayName(){
                    console.log(this.name);
                }
            },
        });
        console.log(vm.name);
        console.log(vm.sayName());
    </script>
</body>
</html>
```

#### 
#### 二、调试代码-开始
在浏览器的`sourcemap`中的对应位置进行断点开始调试。

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1650800865974-5a7a6e7d-594f-4469-ab26-3ef712a78e12.png)



##### 1、`Vue`构造函数
```javascript
function Vue (options) {
  if (!(this instanceof Vue)
  ) {
    warn('Vue is a constructor and should be called with the `new` keyword');
  }
  this._init(options);
}
```

判断是否通过new 创建vue实例, 不是则报错。

然后进入`_init`方法。



##### 2、`_init`
```javascript
var uid$3 = 0;
function initMixin (Vue) {
  Vue.prototype._init = function (options) {
    var vm = this;
    // a uid
    vm._uid = uid$3++;
    
    var startTag, endTag;
    /* istanbul ignore if */
    if (config.performance && mark) {
      startTag = "vue-perf-start:" + (vm._uid);
      endTag = "vue-perf-end:" + (vm._uid);
      mark(startTag);
    }
    
    // a flag to avoid this being observed
    vm._isVue = true;
    // merge options
    if (options && options._isComponent) {
      // optimize internal component instantiation
      // since dynamic options merging is pretty slow, and none of the
      // internal component options needs special treatment.
      initInternalComponent(vm, options);
    } else {
      vm.$options = mergeOptions(
        resolveConstructorOptions(vm.constructor),
        options || {},
        vm
      );
    }
    /* istanbul ignore else */
    {
      initProxy(vm);
    }
    // expose real self
    vm._self = vm;
    initLifecycle(vm);
    initEvents(vm);
    initRender(vm);
    callHook(vm, 'beforeCreate');
    initInjections(vm); // resolve injections before data/props
    initState(vm);
    initProvide(vm); // resolve provide after data/props
    callHook(vm, 'created');
    
    /* istanbul ignore if */
    if (config.performance && mark) {
      vm._name = formatComponentName(vm, false);
      mark(endTag);
      measure(("vue " + (vm._name) + " init"), startTag, endTag);
    }
    
    if (vm.$options.el) {
      vm.$mount(vm.$options.el);
    }
  };
  }
```

在`_init`函数中,  会初始化生命周期、事件等, `data`和`methods`初始化在`initState`.



##### 3、`initState`
```javascript
function initState (vm) {
    vm._watchers = [];
    var opts = vm.$options;
    if (opts.props) { initProps(vm, opts.props); }
    if (opts.methods) { initMethods(vm, opts.methods); }
    if (opts.data) {
      initData(vm);
    } else {
      observe(vm._data = {}, true /* asRootData */);
    }
    if (opts.computed) { initComputed(vm, opts.computed); }
    if (opts.watch && opts.watch !== nativeWatch) {
      initWatch(vm, opts.watch);
    }
  }
```

在`initState`方法中, 会初始化`props`、`methods`、`data`、`computed`和`watch`等。



##### 4、`initMethods`
```javascript
// 检查字符串是否以 $ 或 _ 开头
function isReserved (str) {
  var c = (str + '').charCodeAt(0);
  return c === 0x24 || c === 0x5F
}

function initMethods (vm, methods) {
  var props = vm.$options.props;
  for (var key in methods) {
    {
      if (typeof methods[key] !== 'function') {
        warn(
          "Method \"" + key + "\" has type \"" + (typeof methods[key]) + "\" in the component definition. " +
          "Did you reference the function correctly?",
          vm
        );
      }
      if (props && hasOwn(props, key)) {
        warn(
          ("Method \"" + key + "\" has already been defined as a prop."),
          vm
        );
      }
      if ((key in vm) && isReserved(key)) {
        warn(
          "Method \"" + key + "\" conflicts with an existing Vue instance method. " +
          "Avoid defining component methods that start with _ or $."
        );
      }
    }
    vm[key] = typeof methods[key] !== 'function' ? noop : bind(methods[key], vm);
  }
  }
```

进入`initMethods`方法， 遍历`methods`中`key`

+ 判断`key`对应的属性值数据类型是否为`function`，不是则弹出`warn`;
+ 判断`key`不与`props`的`key`重复， 不是则弹出`warn`;
+ 判断`key`是否不与`vm`上的属性`key`重复，且`key`不是以`$`或`_`开头不是则弹出`warn`；
+ 将`methods`中的方法，挂到`vm`上;

判断`key`对应的属性值数据类型是否为`function`。

    - 是则通过`bind`方法， 将方法内的`this`指向`vm`。

这样我们在vue组件内，就可以通过this, 获取methods中的方法了。

    - 不是则将一个空函数`noop`挂载到`vm`上；



##### 5、`initData`
```javascript
function initData (vm) {
    var data = vm.$options.data;
    data = vm._data = typeof data === 'function'
      ? getData(data, vm)
      : data || {};
    if (!isPlainObject(data)) {
      data = {};
      warn(
        'data functions should return an object:\n' +
        'https://vuejs.org/v2/guide/components.html#data-Must-Be-a-Function',
        vm
      );
    }
    // proxy data on instance
    var keys = Object.keys(data);
    var props = vm.$options.props;
    var methods = vm.$options.methods;
    var i = keys.length;
    while (i--) {
      var key = keys[i];
      {
        if (methods && hasOwn(methods, key)) {
          warn(
            ("Method \"" + key + "\" has already been defined as a data property."),
            vm
          );
        }
      }
      if (props && hasOwn(props, key)) {
        warn(
          "The data property \"" + key + "\" is already declared as a prop. " +
          "Use prop default value instead.",
          vm
        );	
      } else if (!isReserved(key)) {
        proxy(vm, "_data", key);
      }
    }
    // observe data
    observe(data, true /* asRootData */);
  }
```

+ 判断`data`数据类型是否为`function`，是的话则通过`getData`方法获取`data`，该方法的作用就是，调用`data`方法返回其返回值。

```javascript
function getData (data, vm) {
  // #7573 disable dep collection when invoking data getters
  pushTarget();
  try {
    return data.call(vm, vm)
  } catch (e) {
    handleError(e, vm, "data()");
    return {}
  } finally {
    popTarget();
  }
}
```



+ 判断`data`是否为纯对象，不是则将data赋值为空对象，然后弹出`warn`；
+ 遍历`data`的`key`：
    - 判断`key`是否与`methods`中的`key`相同，是则报错；
    - 判断是否与`props`中的`key`相同，是则报错， 不是则通过`proxy`方法将`data`值代理到`vm`上；
    - `observe`方法处理`data`;





到这里， 对于`methods`和`data`绑定`vm`的处理已经完成了，接下来我们看下具体实现的方法。



#### 三、核心方法解析
##### 1、`bind`方法
初始化`bind`方法时，判断当前环境是否支持原生的`bind`方法， 如果不支持则使用兼容的`bind`方法。

我们手写`bind`时，可以参考这个。

```javascript
function polyfillBind (fn, ctx) {
  function boundFn (a) {
    var l = arguments.length;
    return l
      ? l > 1
        ? fn.apply(ctx, arguments)
        : fn.call(ctx, a)
      : fn.call(ctx)
  }

  boundFn._length = fn.length;
  return boundFn
}

function nativeBind (fn, ctx) {
  return fn.bind(ctx)
}

var bind = Function.prototype.bind
  ? nativeBind
  : polyfillBind;
```

##### 2、`proxy`方法
`proxy`方法通过`Object.defineProperty()`方法， 作用时， 访问`this.xxx`,其实访问的时`this._data.xxx`。

```javascript
var sharedPropertyDefinition = {
  enumerable: true,
  configurable: true,
  get: noop,
  set: noop
};

function proxy (target, sourceKey, key) {
  sharedPropertyDefinition.get = function proxyGetter () {
    return this[sourceKey][key]
  };
  sharedPropertyDefinition.set = function proxySetter (val) {
    this[sourceKey][key] = val;
  };
  Object.defineProperty(target, key, sharedPropertyDefinition);
}
```



#### 四、简化版
```javascript
function nativeBind() {
    return Function.prototype.bind;
}

function polyfillBind() {
    function boundFn (a) {
        var l = arguments.length;
        return l
            ? l > 1
            ? fn.apply(ctx, arguments)
            : fn.call(ctx, a)
            : fn.call(ctx)
    }

    boundFn._length = fn.length;
    return boundFn
}

function bind () {
    return Function.prototype.bind ? nativeBind : polyfillBind;
}

function noop(a, b, c) {};

function initMethods(vm, methods) {
    for (var key in methods) {
      vm[key] = typeof methods[key] !== 'function' ? noop : bind(methods[key], vm);
    }
}

var sharedPropertyDefinition = {
    enumerable: true,
    configurable: true,
    get: noop,
    set: noop
};

function proxy() {
    sharedPropertyDefinition.get = function proxyGetter () {
        return this[sourceKey][key]
    };
    sharedPropertyDefinition.set = function proxySetter (val) {
        this[sourceKey][key] = val;
    };
    Object.defineProperty(target, key, sharedPropertyDefinition);
}

function initData(vm) {
    var data = vm.$options.data;
    var keys = Object.keys(data);
    var methods = vm.$options.methods;
    var i = keys.length;
    while (i--) {
        var key = keys[i];
        {
            if (methods?.hasOwnProperty(key)) {
                throw new Error(`Method ${key} + "\" has already been defined as a data property.`)
            }
        }
        proxy(vm, "_data", key);
    }
}

function Mini (options) {
    var vm = this;
    var opts = options;
    if (opts.methods) {
        initMethods(vm, opts.methods);
    }
    if (opts.data) {
        initData(vm);
    }
}
```



#### 五、小结
`vue`实现将`data`和`methods`中属性或方法代理到`vm`上，主要是通过`bind`和`proxy`方法，大家可以手写下上面的方法，加深印象便于理解。

