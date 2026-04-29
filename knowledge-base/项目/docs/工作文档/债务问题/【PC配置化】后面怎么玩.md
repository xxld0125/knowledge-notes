PC 端的配置化是我搞出来的东西。当初想的是，在一些比较类似的页面开发时，能够快速搭建复用。以及在一些个性化需要里，可以派上用场。

不过，经过这么多迭代下来，目前这个配置化也跟 PaaS 类似，有点变成债务问题了，因为对于其他人来说，这是个加负的东西

既然是加负，那么就有必要来看看，后面改怎么玩下去，会比较良性

# <font style="color:rgb(23, 43, 77);">使用痛点（缺点和不足）</font>
+ 上手成本大
    - 需要学习并掌握元数据的几种规则配置（initRules，eventListener，dataSource，conditions）
    - 需要掌握 type=slot2 自定义组件，type=dataService 自定义函数两种用法
+ 排查问题麻烦
    - 组件联动、初始化等都封装在配置化内部实现。比较难以跟踪
+ 逻辑复杂，维护难
    - 任务登记页的各种表单的显隐联动逻辑、表单值的清空等都配置在元数据的各种组件的各种事件上，导致要加个逻辑进去时，很难找到需要在哪些地方加
+ 数据流混乱，完全不知道表单值在哪里被修改了
    - 现在表单值可以在：元数据配置的规则里修改、slot2 自定义插槽组件里修改、业务或预置组件里修改、dataService 函数里修改，导致在调试时，有时根本不知道究竟是哪里修改了表单值
+ 发布 SQL 操作繁琐、维护难
    - 每次发布时，都需要先本地合并分支，再生成元数据 SQL，最后整理到 sql-list 发布清单上，操作繁琐
    - 如果线上发生回退，还需要找到 sql-list 之前的发布记录，重发元数据 SQL 来回退

# <font style="color:rgb(23, 43, 77);">后面怎么玩</font>
如果觉得不会用，不怎么好用，那么可以不用，基于这个角度，分两种场景来处理：

+ 对于新页面，不用配置化实现
+ 对于**已经用配置化实现的页面，需要逐步去改造，淡化元数据里的逻辑（这个下面会再具体展开讲）**

不过，我个人是觉得，表单页由于会越来越复杂，确实会导致越来越难以用配置化兑现后续需求，表单页能不用就不用吧

至于列表页、详情页，其实还是可以考虑下看看，毕竟已经有了这些页面场景所需的一些基本布局容器组件、基础组件，这些通过元数据复用起来也挺方便的，而且又很少有业务逻辑，所以应该还好

但不管怎么样，总还会接触到配置化相关，因为已用配置化实现的，除非完全重构掉，否则还得维护下去，那么，针对上面一些使用痛点，下面给一些我的建议：

+ 上手成本大
    - 这个没办法，必须要掌握。但其实不用死记硬背，如果你能够了解配置化的思想的话，你会发现，元数据里各种配置，其实就分为两个维度：
        * UI组件渲染所需的配置，比如 width，label，hidden，style 等等
            + 那么很明显，这类的配置规则根本不需要记，因为就分为通用的和各自的，有些配置比如 width 是所有组件通用，有些配置，比如 options 可能只有下拉框之类的组件有
            + 但不管哪一类，你总能在对应的组件代码里找到，所以需要用的时候知道去哪找就行
        * 组件联动交互所需的配置，比如点击事件，初始化规则，事件响应行为，条件表达式
            + 这一类规则的记忆和用法，其实有个办法，就是你抛弃掉 vue 这种双向绑定框架的思想，回归 jQuery 时代的思想，你就能记得很清楚，也能知道该怎么用这些规则了
            + 比如某个组件点击后，影响了其他组件显隐，那么你就按照正常写 jQuery 代码思想，在点击的组件上去配置点击事件，事件的响应行为里需要去更改指定组件的显隐（怎么找到指定组件，组件 id 咯）
            + 不过，用到后面，我确实也觉得，在一些交互多变的场景里，这些组件联动最好还是不要直接配置在元数据上面了，不然很难扩展后续需求。针对这种场景用法，就是 dataService 写函数来实现了
    - 用多了，其实也还好，其实就是掌握怎么快速去找到需要的配置规则就行
+ 排查问题麻烦
    - 配置化引擎的代码就在代码里，排查虽然麻烦，但至少还有途径，直接引擎内部去打日志跟踪排查
+ 数据流混乱，完全不清楚哪里修改了表单值
    - 尽量把元数据里如果有配置业务逻辑的规则，全部都用 dataService 方式用代码去替换掉吧
    - 尽量只在 dataService 的函数里，或者自定义组件这两种场景去修改表单值吧
    - 调试的话，记得善用 dataService 的 serviceName=log 的内置函数，来跟踪配置的元数据规则究竟有没有被执行到
+ 发布 SQL 操作繁琐
    - 直接把元数据放在代码里维护就好（方案：config-form 组件的 code 不要配置字段，这样就会直接使用本地的。或者让后端把表里的元数据 is_delete = 1，接口没返回元数据也会用本地的）
    - 放后端是为了以后可以有直接发 SQL 而不需要发版的场景
        * 但这意味着，元数据里就需要配置一系列业务逻辑进去，虽然可以实现，但后期维护太麻烦了
        * 元数据尽量确保只负责配置组件的布局、顺序、宽高等等就好了，业务逻辑还是用  dataService 的方案用代码来维护把
+ 逻辑复杂、维护难
    - 这个解决方案就是淡化元数据里的逻辑，如果元数据里配置的仅仅只是各个基础组件、容器组件搭配形成的页面，这样元数据里的逻辑复杂度是不是就降低很多了
    - 举个实际的例子：

```plain
// 配置组件的初始化规则  
initRules: [
  {
// 当满足条件：表单对象的 type 字段值不等于表扬时（formModel.type !== '表扬'），执行 handles
    conditionType: "every",
    conditions: [
      {
        type: "expression",
        expression: "!==",
        leftDataSource: {
          type: "formModel",
          dataKey: "type",
          fieldConfig: {
            key: "label",
            value: "value"
          },
          targetFormId: "nextOperator"
        },
        rightDataSource: {
          type: "constant",
          value: "表扬"
        }
      }
    ],
    handles: [
// 更新组件的显隐，hidden = formModel.type === 咨询 && formModel.is_reponsed !== 0
      {
        type: "hidden",
        value: 0,
        valueFrom: {
          type: "condition",
          conditions: [
            {
              type: "expression",
              expression: "===",
              leftDataSource: {
                type: "formModel",
                dataKey: "type",
                fieldConfig: {
                  key: "label",
                  value: "value"
                },
                targetFormId: "nextOperator"
              },
              rightDataSource: {
                type: "constant",
                value: "咨询"
              }
            },
            {
              type: "expression",
              expression: "!==",
              leftDataSource: {
                type: "formModel",
                dataKey: "is_reponsed",
                fieldConfig: {
                  key: "label",
                  value: "value"
                },
                targetFormId: "nextOperator"
              },
              rightDataSource: {
                type: "constant",
                value: "0"
              }
            }
          ],
          conditionType: "every"
        }
      }
    ]
  },
  {
// 当满足条件：表单对象的 type 字段值不等于表扬时（formModel.type === '表扬'），执行 handles
    conditionType: "every",
    conditions: [
      {
        type: "expression",
        expression: "===",
        leftDataSource: {
          type: "formModel",
          dataKey: "type",
          fieldConfig: {
            key: "label",
            value: "value"
          },
          targetFormId: "nextOperator"
        },
        rightDataSource: {
          type: "constant",
          value: "表扬"
        }
      }
    ],
    handles: [
      {
// 更新组件的显隐，hidden = formModel.type === '表扬'
        type: "hidden",
        value: 0,
        valueFrom: {
          type: "condition",
          conditions: [
            {
              type: "expression",
              expression: "===",
              leftDataSource: {
                type: "formModel",
                dataKey: "type",
                fieldConfig: {
                  key: "label",
                  value: "value"
                },
                targetFormId: "nextOperator"
              },
              rightDataSource: {
                type: "constant",
                value: "表扬"
              }
            }
          ],
          conditionType: "every"
        }
      }
    ]
  }
]
```

  


上面这串元数据规则，是之前配置在登记页的后续处理人组件的初始化逻辑里的。简单来说，在元数据上配置了该组件的初始化显隐逻辑：当 type = 维修，投诉时，直接显示组件；当 type = 咨询时，且 is_responsed = 0 即未答复时，才显示，否则隐藏；当type = 表扬时，隐藏。

显隐逻辑不复杂，但用元数据配置起来，就特别复杂，而且不好理解，而且后续很难扩展

那么，怎么把这串元数据用 dataService 的写代码思路来替换掉呢？

首先，你要先理清这串元数据含义

然后修改元数据：

```plain
initRules: [{
  conditionType: 'every',
  conditions: [],
  handles: [
    {
      type: 'hidden',
      value: 0,
      valueFrom: {
        type: 'condition',
        conditions: [
          {
            type: 'dataService',
            serviceName: 'yxdcOnInitHiddenNextOperator'
          }
        ],
        conditionType: 'every'
      }
    }
  ]
}]



// 后续处理人初始化时判断显隐
function yxdcOnInitHiddenNextOperator({ context, $event }) {
  const activeTask = context.getStore()?.state().activeTask;
  if (activeTask) {
    if (activeTask.type === '维修') {
      if (activeTask.front_status === '待指派') {
        return activeTask.guarantee_type !== '保修范围内' && activeTask.repair_type === '公区维修';
      } else {
        return activeTask.repair_type === '公区维修';
      }
    } else if (activeTask.type === '投诉') {
      return false;
    } else if (activeTask.type === '咨询') {
      return activeTask.is_reponsed !== '0';
    }
  }
  return true;
}
```

  


就用这种思路，慢慢把元数据里的业务逻辑全部都用 dataService 的写代码方式替换掉。

如果有时间，直接干掉这个页面，重构，废弃这个配置化吧

  


