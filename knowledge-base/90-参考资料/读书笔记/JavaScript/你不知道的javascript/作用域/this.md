### 为什么要使用this
this 提供了一种更优雅的方式来隐式“传递”一个对象引用，因此可以将 API 设计得更加简洁并且易于复用。

随着你的使用模式越来越复杂，显式传递上下文对象会让代码变得越来越混乱，使用 this则不会这样。当我们介绍对象和原型时，你就会明白函数可以自动引用合适的上下文对象有多重要。



### 误解
`this` 指向函数的作用域。这个问题有点复杂，因为在某种情况下它是正确的，但是在其他情况下它却是错误的。

需要明确的是，this 在任何情况下都不指向函数的词法作用域。在 JavaScript 内部，作用域确实和对象类似，可见的标识符都是它的属性。但是作用域“对象”无法通过 JavaScript代码访问，它存在于 JavaScript 引擎内部。

思考一下下面的代码，它试图（但是没有成功）跨越边界，使用 this 来隐式引用函数的词法作用域：

```javascript
function foo() {
  var a = 2;
  this.bar();
}

function bar() {
  console.log( this.a );
}

foo(); // ReferenceError: a is not defined
```

这段代码中的错误不止一个。虽然这段代码看起来好像是我们故意写出来的例子，但是实际上它出自一个公共社区中互助论坛的精华代码。这段代码非常完美（同时也令人伤感）地展示了 this 多么容易误导人。

首先，这段代码试图通过 `this.bar()` 来引用 `bar()` 函数。这是绝对不可能成功的，我们之后会解释原因。调用 `bar()` 最自然的方法是省略前面的 `this`，直接使用词法引用标识符。

此外，编写这段代码的开发者还试图使用 this 联通 foo() 和 bar() 的词法作用域，从而让bar() 可以访问 foo() 作用域里的变量 a。这是不可能实现的，你不能使用 this 来引用一个词法作用域内部的东西。

每当你想要把 this 和词法作用域的查找混合使用时，一定要提醒自己，这是无法实现的。



### this到底是什么
this 是在运行时进行绑定的，并不是在编写时绑定，它的上下文取决于函数调用时的各种条件。this 的绑定和函数声明的位置没有任何关系，只取决于函数的调用方式。

当一个函数被调用时，会创建一个活动记录（有时候也称为执行上下文）。这个记录会包含函数在哪里被调用（调用栈）、函数的调用方法、传入的参数等信息。this 就是记录的其中一个属性，会在函数执行的过程中用到。



### 调用位置
在理解 this 的绑定过程之前，首先要理解调用位置：调用位置就是函数在代码中被调用的位置（而不是声明的位置）。

通常来说，寻找调用位置就是寻找“函数被调用的位置”，但是做起来并没有这么简单，因为某些编程模式可能会隐藏真正的调用位置。

最重要的是要分析调用栈（就是为了到达当前执行位置所调用的所有函数）。我们关心的调用位置就在当前正在执行的函数的前一个调用中。



### 绑定规则
#### 默认绑定
最常用的函数调用类型：独立函数调用。可以把这条规则看作是无法应用其他规则时的默认规则。

```javascript
function foo() {
  console.log(a);
}

var a = 2;

foo(); // 2
```

	接下来我们可以看到当调用 `foo()` 时，`this.a` 被解析成了全局变量 `a`。为什么？因为在本例中，函数调用时应用了 `this` 的默认绑定，因此 `this` 指向全局对象。

那么我们怎么知道这里应用了默认绑定呢？可以通过分析调用位置来看看 `foo()` 是如何调用的。在代码中，`foo()` 是直接使用不带任何修饰的函数引用进行调用的，因此只能使用默认绑定，无法应用其他规则。

如果使用严格模式（strict mode），那么全局对象将无法使用默认绑定，因此 `this` 会绑定到 `undefined`。



#### 隐式绑定
另一条需要考虑的规则是调用位置是否有上下文对象。

```javascript
function foo() {
  console.log( this.a );
}

var obj = {
  a: 2,
  foo: foo
};

obj.foo(); // 2
```

	当函数引用有上下文对象时，隐式绑定规则会把函数调用中的 `this` 绑定到这个上下文对象。因为调用 `foo()` 时 `this` 被绑定到 `obj`，因此 `this.a` 和 `obj.a` 是一样的。



**<font style="color:#DF2A3F;">对象属性引用链中只有最顶层或者说最后一层会影响调用位置</font>**。举例来说：

```javascript
function foo() {
  console.log( this.a );
}

var obj2 = {
  a: 42,
  foo: foo
};

var obj1 = {
  a: 2,
  obj2: obj2
};

obj1.obj2.foo(); // 42
```



##### 隐式丢失
一个最常见的 this 绑定问题就是被隐式绑定的函数会丢失绑定对象，也就是说它会应用默认绑定，从而把 `this` 绑定到全局对象或者 `undefined` 上，取决于是否是严格模式。

```javascript
function foo() {
  console.log( this.a );
}

var obj = {
  a: 2,
  foo: foo
};

var bar = obj.foo; // 函数别名！
var a = "oops, global"; // a 是全局对象的属性
bar(); // "oops, global"
```

	虽然 `bar` 是 `obj.foo` 的一个引用，但是实际上，它引用的是 `foo` 函数本身，因此此时的 `bar()` 其实是一个不带任何修饰的函数调用，因此应用了默认绑定。



如果把函数传入语言内置的函数而不是传入你自己声明的函数，会发生什么呢？结果是一样的，没有区别：

```javascript
function foo() {
  console.log( this.a );
}

var obj = {
  a: 2,
  foo: foo
};

var a = "oops, global"; // a 是全局对象的属性
setTimeout( obj.foo, 100 ); // "oops, global"
```



#### 显示绑定
函数的 `call(..)` 和 `apply(..)` 方法，它们的第一个参数是一个对象，它们会把这个对象绑定到`this`，接着在调用函数时指定这个 `this`。因为你可以直接指定 `this` 的绑定对象，因此我们称之为显式绑定。

```javascript
function foo() {
  console.log( this.a );
}

var obj = {
  a:2
};

foo.call( obj ); // 2
```

	通过 `foo.call(..)`，我们可以在调用 `foo` 时强制把它的 `this` 绑定到 `obj` 上。

:::info
如果你传入了一个原始值（字符串类型、布尔类型或者数字类型）来当作 this 的绑定对象，这个原始值会被转换成它的对象形式（也就是 `new String(..)`、`new Boolean(..)` 或者 `new Number(..)`）。这通常被称为“装箱”。

:::



##### 硬绑定
ES5 中提供了内置的方法 `Function.prototype.bind`，它的用法如下：

```javascript
function foo(something) {
  console.log( this.a, something );
  return this.a + something;
}

var obj = {
  a:2
};

var bar = foo.bind( obj );
var b = bar( 3 ); // 2 3
console.log( b ); // 5
```

	`bind(..)` 会返回一个硬编码的新函数，它会把参数设置为 this 的上下文并调用原始函数。



##### API调用的“上下文”
第三方库的许多函数，以及 JavaScript 语言和宿主环境中许多新的内置函数，都提供了一个可选的参数，通常被称为“上下文”（context），其作用和 `bind(..)` 一样，确保你的回调函数使用指定的 `this`。

```javascript
function foo(el) {
  console.log( el, this.id );
}

var obj = {
  id: "awesome"
};

// 调用 foo(..) 时把 this 绑定到 obj
[1, 2, 3].forEach( foo, obj );
// 1 awesome 2 awesome 3 awesome
```

	这些函数实际上就是通过 `call(..)` 或者 `apply(..)` 实现了显式绑定，这样你可以少些一些代码。



#### new 绑定
使用 `new` 来调用函数，或者说发生构造函数调用时，会自动执行下面的操作。

1. 创建一个全新的对象
2. 这个新对象的原型对象执行构造函数的原型对象。
3. 这个新对象会绑定到函数调用的`this`。
4. 如果构造函数未返回其他对象，那么 `new` 表达式中的函数调用会自动返回这个新对象。



```javascript
function foo(a) {
  this.a = a;
}
var bar = new foo(2);
console.log( bar.a ); // 2
```

使用 `new` 来调用 `foo(..)` 时，我们会构造一个新对象并把它绑定到 `foo(..)` 调用中的 `this`上。`new` 是最后一种可以影响函数调用时 `this` 绑定行为的方法，我们称之为 `new` 绑定。



### 优先级
现在我们可以根据优先级来判断函数在某个调用位置应用的是哪条规则。可以按照下面的顺序来进行判断：



1. 函数是否在 `new` 中调用（`new` 绑定）？如果是的话 this 绑定的是新创建的对象。  
`var bar = new foo()`



注意：`new`绑定和`call`、`apply`是不允许同时使用的。

2. 函数是否通过 `call`、`apply`（显式绑定）或者`bind`？如果是的话，`this` 绑定的是  
指定的对象。  
`var bar = foo.call(obj2)`



注意：`bind`优先级高于`call`、`apply`。

3. 函数是否在某个上下文对象中调用（隐式绑定）？如果是的话，`this` 绑定的是那个上  
下文对象。  
`var bar = obj1.foo()`
4. 如果都不是的话，使用默认绑定。如果在严格模式下，就绑定到 `undefined`，否则绑定到  
全局对象。  
`var bar = foo()`



### 绑定例外
#### 被忽略的this
如果你把 `null` 或者 `undefined` 作为 `this` 的绑定对象传入 `call`、`apply` 或者 `bind`，这些值在调用时会被忽略，实际应用的是默认绑定规则：

```javascript
function foo() {
  console.log( this.a );
}

var a = 2;
foo.call( null ); // 2
```

如果函数并不关心 `this` 的话，你仍然需要传入一个占位值，这时 `null` 可能是一个不错的选择，就像代码所示的那样。



##### 更安全的this
一种“更安全”的做法是传入一个特殊的对象，把 this 绑定到这个对象不会对你的程序产生任何副作用。

这个对象就是一个空的非委托对象。在 JavaScript 中创建一个空对象最简单的方法都是 `Object.create(null)`。`Object.create(null) 和 {}` 很 像， 但 是 并 不 会 创 建 `Object.prototype` 这个委托，所以它比 `{}`“更空”。

```javascript
function foo(a,b) {
  console.log( "a:" + a + ", b:" + b );
}

// 空对象
var ø = Object.create( null );

// 把数组展开成参数
foo.apply( ø, [2, 3] ); // a:2, b:3

// 使用 bind(..) 进行柯里化
var bar = foo.bind( ø, 2 );
bar( 3 ); // a:2, b:3
```



#### 间接引用
注意的是，你有可能（有意或者无意地）创建一个函数的“间接引用”，在这种情况下，调用这个函数会应用默认绑定规则。

间接引用最容易在赋值时发生：

```javascript
function foo() {
  console.log( this.a );
}

var a = 2;
var o = { a: 3, foo: foo };
var p = { a: 4 };
o.foo(); // 3
(p.foo = o.foo)(); // 2
```

	赋值表达式 `p.foo = o.foo` 的返回值是目标函数的引用，因此调用位置是 `foo()` 而不是 `p.foo()` 或者 `o.foo()`。根据我们之前说过的，这里会应用默认绑定。



#### 软绑定
硬绑定这种方式可以把 `this` 强制绑定到指定的对象（除了使用 `new` 时），防止函数调用应用默认绑定规则。问题在于，硬绑定会大大降低函数的灵活性，使用硬绑定之后就无法使用隐式绑定或者显式绑定来修改 `this`。

如果可以给默认绑定指定一个全局对象和 `undefined` 以外的值，那就可以实现和硬绑定相同的效果，同时保留隐式绑定或者显式绑定修改 `this` 的能力。

可以通过一种被称为软绑定的方法来实现我们想要的效果：

```javascript
if (!Function.prototype.softBind) {
  Function.prototype.softBind = function(obj) {
    var fn = this;
    // 捕获所有 curried 参数
    var curried = [].slice.call( arguments, 1 );
    var bound = function() {
      return fn.apply(
        (!this || this === (window || global)) ?
          obj : this
        curried.concat.apply( curried, arguments )
      );
    };
    bound.prototype = Object.create( fn.prototype );
    return bound;
  };
}
```

	除了软绑定之外，`softBind(..)` 的其他原理和 ES5 内置的 `bind(..)` 类似。它会对指定的函数进行封装，首先检查调用时的 `this`，如果 `this` 绑定到全局对象或者 `undefined`，那就把指定的默认对象 `obj` 绑定到 `this`，否则不会修改 `this`。此外，这段代码还支持可选的柯里化。



### this词法
之前介绍的四条规则已经可以包含所有正常的函数。但是 ES6 中介绍了一种无法使用这些规则的特殊函数类型：箭头函数。

箭头函数并不是使用 `function` 关键字定义的，而是使用被称为“胖箭头”的操作符 `=>` 定义的。箭头函数不使用 `this` 的四种标准规则，而是根据外层（函数或者全局）作用域来决定 `this`。



箭头函数最常用于回调函数中，例如事件处理器或者定时器：

```javascript
function foo() {
  setTimeout(() => {
  // 这里的 this 在此法上继承自 foo()
    console.log( this.a );
  },100);
}

var obj = {
  a:2
};

foo.call( obj ); // 2
```



箭头函数可以像 `bind(..)` 一样确保函数的 `this` 被绑定到指定对象。

