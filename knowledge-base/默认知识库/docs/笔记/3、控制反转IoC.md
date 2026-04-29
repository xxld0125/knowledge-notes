一、IoC

控制反转（Inversion of Control，缩写为 IoC）是[面向对象编程](https://link.juejin.cn/?target=https%3A%2F%2Fbaike.baidu.com%2Fitem%2F%25E9%259D%25A2%25E5%2590%2591%25E5%25AF%25B9%25E8%25B1%25A1%25E7%25BC%2596%25E7%25A8%258B%2F254878)中的一种设计原则，可以用来降低计算机[代码](https://link.juejin.cn/?target=https%3A%2F%2Fbaike.baidu.com%2Fitem%2F%25E4%25BB%25A3%25E7%25A0%2581%2F86048)之间的[耦合度](https://link.juejin.cn/?target=https%3A%2F%2Fbaike.baidu.com%2Fitem%2F%25E8%2580%25A6%25E5%2590%2588%25E5%25BA%25A6%2F2603938)。其中最常见的方式叫做[依赖注入](https://link.juejin.cn/?target=https%3A%2F%2Fbaike.baidu.com%2Fitem%2F%25E4%25BE%259D%25E8%25B5%2596%25E6%25B3%25A8%25E5%2585%25A5%2F5177233)（Dependency Injection，简称DI），还有一种方式叫“依赖查找”（Dependency Lookup）。通过控制反转，对象在被创建的时候，由一个调控系统内所有对象的外界实体将其所依赖的对象的引用传递给它。也可以说，依赖被注入到对象中。



二、简单实现

```javascript
class A {
  constructor(params) {
    this.params = params
  }
}

class B extends A {
  constructor(params) {
    super(params)
  }
  run() {
    console.log(this.params);
  }
}

new B('hello').run();
```

我们可以看到，B 中代码的实现是需要依赖 A 的，两者的代码耦合度非常高。在两者之间的业务逻辑复杂程度增加的情况下，维护成本与代码可读性都会随着增加，并且很难再多引入额外的模块进行功能拓展。

为了解决这个情况，我们可以引入一个 IoC 容器：



```javascript
class A {
  constructor(params) {
    this.params = params
  }
}

class C {
  constructor(params) {
    this.params = params
  }
}

class Container {
  constructor() { this.modules = {} }

  provide(key, object) { this.modules[key] = object }

  get(key) { return this.modules[key] }
}

const mo = new Container();

mo.provide('a', new A('hello'))
mo.provide('c', new C('world'))

class B {
  constructor(container) {
    this.a = container.get('a');
    this.c = container.get('c');
  }
  run() {
    console.log(this.a.params + ' ' + this.c.params)
  }
}

new B(mo).run();
```

	如上述代码所示，在引入 IoC 容器 container 之后，B 与 A 的代码逻辑已经解耦，可以单独拓展其他功能，也可以方便地加入其他模块 C。所以在面对复杂的后端业务逻辑中，引入 IoC 可以降低组件之间的耦合度，实现系统各层之间的解耦，减少维护与理解成本。

