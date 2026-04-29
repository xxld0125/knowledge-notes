# Cursor 配置
+ 新旧项目配置 `.cursorignore`
+ 新旧项目 `CodeBase Indexing****`
+ 模型选择 `cluade-3.7-sonnet`
+ 打开 `Large Context`
+ Docs 添加相关文档，比如 `element ui`官方文档等
+ MCP 配置 `sequentialthinking`、`fileSystem`等****



# 梳理老项目功能
如何梳理老项目待重构模块的功能呢，之前自己开发的话，一般是自己看代码再梳理成功能文档。

现在的话，我们可以让 Cursor 直接帮我们梳理功能文档。



## AI 梳理问题部位功能文档
```markdown
# 问题部位页面重构

## 背景
"部位及相关问题"是一个管理问题部位及其关联问题分类的功能模块。用户可以添加、编辑、删除和排序部位，并为每个部位关联相应的问题分类。系统通过左右分栏的形式，左侧展示部位列表，右侧展示选中部位关联的问题分类。

## 目标
1. 保留原有功能完整性
2. 提高代码可维护性
3. 优化用户界面和交互体验
4. 模块化代码结构
5. 提高页面加载和操作响应速度

## 约束
1. 保持与系统其他模块的兼容性
2. 维持数据结构和接口不变
3. 确保向后兼容性
4. 不改变业务逻辑核心流程
5. 确保代码符合项目规范

## 功能需求

### 部位管理
- 展示部位列表，支持拖拽排序
- 添加新部位功能（包含部位名称、排序号、项目归属）
- 编辑现有部位（标题、排序、项目类型）
- 删除部位功能（删除前需确认）
- 选中部位后高亮显示并加载其关联的问题分类

### 问题分类关联
- 展示选中部位关联的问题分类（树形结构）
- 关联新的问题分类（支持搜索、多选）
- 当部位无关联问题时显示提示信息并提供快捷关联入口

### 数据交互
- 异步加载部位列表数据
- 异步获取问题分类数据
- 保存部位排序顺序
- 获取系统配置项（如isLfProjectTypeProblemRule）

## 模块功能描述

### 主模块
核心功能模块，负责初始化页面、事件绑定、数据加载和协调其他模块。
- 获取系统配置（灰度发布特性控制）
- 加载部位列表数据
- 管理部位选中状态
- 协调部位操作（添加、编辑、删除、排序）
- 处理问题分类关联

### 编辑模块
负责部位的添加和编辑功能。
- 弹出编辑表单
- 表单验证（部位名称、排序号）
- 项目归属处理（支持二进制处理多选）
- 提交表单数据

### 关联问题分类模块
负责部位与问题分类的关联管理。
- 获取已关联问题分类
- 获取可选问题分类
- 支持问题分类搜索过滤
- 管理问题分类选择状态
- 保存关联关系

## API接口
1. 获取部位列表：`parameter/position-list/list`
2. 添加/编辑部位：`parameter/position-list/save`
3. 删除部位：`parameter/position-list/delete`
4. 保存排序：`parameter/position-list/sort`
5. 获取已关联问题分类：`parameter/position-list/problem-class-tree`
6. 获取可选问题分类：`parameter/problem-lib/problem-class-tree?v=2`
7. 保存关联关系：`parameter/position-list/save-problem-position-class`
8. 获取系统配置：`dailyservice/engineer/get-process-flow-settings`

## 注意事项
1. 重构时保留原有功能逻辑不变
2. 注意变量命名与现有约定保持一致
3. 对接口参数格式不做改变
4. 确保UI交互逻辑清晰易懂
5. 做好错误处理和提示展示
6. 针对isLfProjectTypeProblemRule特性，保持灰度发布特性兼容性
```



## 功能业务逻辑流程图
流程图可以更清晰的让 AI 了解具体的业务流程。

![](https://cdn.nlark.com/yuque/__mermaid_v3/07739cd7541797414b2b27aa61a17dcf.svg)



## 接口梳理
一般来说重构接口后端需要提供接口文档，可以让将文档喂给 AI。但是如果后端未提供，且重构后接口只是做迁移，接口返回无变化时，可以让 AI 梳理老项目的接口详细信息。



### 1. 获取部位列表
**接口路径** **：**`parameter/position-list/list`

**请求方式** **：GET**

**入参** **：**

```json
{
  "page": 1, // 页码
  "pageSize": 9999 // 每页数量，通常设为9999获取全部数据
}
```

**返回数据** **：**

```json
{
  "errcode": 0, // 错误码，0表示成功
  "errmsg": "", // 错误信息
  "data": {
    "items": [
      {
        "id": "1", // 部位ID
        "title": "厨房", // 部位名称
        "sort": 1, // 排序号
        "project_type": "3" // 项目归属类型
      },
      {
        "id": "2",
        "title": "卫生间",
        "sort": 2,
        "project_type": "1"
      }
      // 更多部位...
    ],
    "total": 10 // 总数量
  }
}
```

### 2. 添加/编辑部位
**接口路径** **：**`parameter/position-list/save`

**请求方式** **：POST**

**入参** **：**

```json
{
  "id": "1", // 部位ID，添加时不传
  "title": "厨房", // 部位名称
  "sort": 1, // 排序号
  "project_type": 3 // 项目归属类型（二进制表示，如3表示11，房产和公建都勾选）
}
```

**返回数据** **：**

```json
{
  "errcode": 0, // 错误码，0表示成功
  "errmsg": "", // 错误信息
  "data": {
    "id": "1" // 成功时返回部位ID
  }
}
```

### 3. 删除部位
**接口路径** **：**`parameter/position-list/delete`

**请求方式** **：GET**

**入参** **：**

```json
{
  "id": "1" // 要删除的部位ID
}
```

**返回数据** **：**

```json
{
  "errcode": 0, // 错误码，0表示成功
  "errmsg": "", // 错误信息
  "data": {
    "success": true // 是否删除成功
  }
}
```

### 4. 保存排序
**接口路径** **：**`parameter/position-list/sort`

**请求方式** **：POST**

**入参** **：**

```json
{
  "ids": ["1", "3", "2", "4"] // 排序后的部位ID数组，按顺序排列
}
```

**返回数据** **：**

```json
{
  "errcode": 0, // 错误码，0表示成功
  "errmsg": "", // 错误信息
  "data": {
    "success": true // 是否保存成功
  }
}
```

### 5. 获取已关联问题分类
**接口路径** **：**`parameter/position-list/problem-class-tree`

**请求方式** **：GET**

**入参** **：**

```json
{
  "position_id": "1", // 部位ID
  "project_type": "3" // 项目归属类型（灰度功能启用时需要）
}
```

**返回数据** **：**

```json
{
  "errcode": 0, // 错误码，0表示成功
  "errmsg": "", // 错误信息
  "data": [
    {
      "code": "A", // 分类编码
      "treeText": "热水器", // 分类名称
      "value": "1", // 分类ID
      "childNode": [
        // 子节点数组
        {
          "code": "A-1",
          "treeText": "无法加热",
          "value": "11",
          "childNode": []
        }
      ]
    }
    // 更多问题分类...
  ]
}
```

### 6. 获取可选问题分类
**接口路径** **：**`parameter/problem-lib/problem-class-tree`

**请求方式** **：GET**

**入参** **：**

```json
{
  "type": 1, // 类型，固定值1
  "is_disable": 0, // 是否禁用，0表示未禁用
  "project_type": "3" // 项目归属类型（灰度功能启用时需要）
}
```

**返回数据** **：**

```json
{
  "errcode": 0, // 错误码，0表示成功
  "errmsg": "", // 错误信息
  "data": [
    {
      "code": "A", // 分类编码
      "treeText": "热水器", // 分类名称
      "value": "1", // 分类ID
      "childNode": [
        // 子节点数组
        {
          "code": "A-1",
          "treeText": "无法加热",
          "value": "11",
          "childNode": []
        }
      ]
    }
    // 更多问题分类...
  ]
}
```

### 7. 保存关联关系
**接口路径** **：**`parameter/position-list/save-problem-position-class`

**请求方式** **：POST**

**入参** **：**

```json
{
  "class_ids": "[\"11\",\"12\",\"13\"]", // JSON字符串形式的分类ID数组
  "position_id": "1" // 部位ID
}
```

**返回数据** **：**

```json
{
  "errcode": 0, // 错误码，0表示成功
  "errmsg": "", // 错误信息
  "data": {
    "success": true // 是否保存成功
  }
}
```



# 新项目初始化
问题部位参数页重构后的代码在 kffrontend 仓库中。所以需要梳理  kffrontend 开发的规范。

## 项目开发 rules
如果之前已初始化该项目的 rules，就不需要处理了。但是该 rules 需要长期维护。

rules 初版可以让 Cursor 读取仓库代码后直接生成。



```markdown
# Vue2项目开发规范及Cursor提示词

## 角色和背景

你是一位精通前端开发的AI助手，专注于Vue.js、Element-UI以及当前KF项目的技术栈，同时熟练掌握Cursor IDE环境下的AI辅助开发技术。你能帮助开发者优化代码结构、提高开发效率，并提供最佳实践方案。你对项目结构、组件设计模式和命名规范有深入理解，能够确保新增代码与现有项目保持一致。

## 技术栈精通

### Vue2相关
- Vue 2.6.x (项目使用Vue 2.6.11)
- Vuex 3.x (状态管理)
- Vue Router 3.x (路由管理)
- 熟练应用Vue的组件化开发、生命周期管理、计算属性、监听器、自定义指令等

### UI框架
- Element-UI 2.14.x (主要UI组件库)
- @yl/ui (基于Element-UI的定制组件库)
- 项目自定义的Kf前缀组件 (如KfSelect、KfTree等)

### 构建工具
- Vite 4.x (现代化构建工具)
- 熟悉项目环境变量、代理配置和构建优化
- 了解webpack相关配置，能够解决构建过程中的常见问题

### 项目依赖库
- axios (HTTP请求)
- lodash-es (实用工具库)
- moment (日期处理)
- echarts (图表)
- sortablejs (拖拽排序)
- qs (查询字符串解析)
- vue-codemirror (代码编辑器)
- xss (防XSS攻击)

## 项目目录结构

- src/api: API接口定义
- src/assets: 静态资源(CSS、图片、图标等)
- src/components: 公共组件，包含多个Kf前缀的公共组件
- src/directives: 自定义Vue指令
- src/router: 路由配置
- src/services: 公共服务层
- src/store: Vuex状态管理
- src/utils: 工具方法
- src/views: 页面组件
- src/plugins: 插件配置
- src/config: 项目配置
- src/docs: 项目文档

## 开发规范

### 命名规范

- **组件命名规则**
  - 公共组件使用Kf前缀，采用PascalCase（大驼峰）方式命名，如`KfTree`、`KfSelect`等
  - 组件文件夹命名采用kebab-case（短横线）命名，如`kf-tree`、`kf-select`
  - 组件文件可以使用index.vue作为入口文件，或使用与组件同名的文件如`kfSelect.vue`
  - 页面组件通常按功能模块放置在views目录下对应子目录

- **变量命名规则**
  - 组件prop属性采用camelCase（小驼峰）方式命名
  - 组件事件命名采用kebab-case（短横线）方式，如`@item-selected`
  - 方法名采用camelCase（小驼峰）方式，事件处理方法建议以`handle`开头

### 组件设计规范

- **组件设计原则**
  - 单一职责原则：每个组件只负责一项特定功能
  - 组件应具有明确的API接口：通过props接收输入，通过events发送输出
  - 组件内部实现应尽量独立，不依赖外部状态
  - 复杂组件应拆分为多个小型组件，而非一个庞大组件

- **组件API设计**
  - 优先使用v-model进行数据双向绑定
  - 使用`model`选项自定义组件的`v-model`行为
  - 关注组件的可扩展性，通过插槽提供内容自定义能力
  - 组件props定义应明确类型和默认值，必要时添加验证规则

- **组件通信**
  - 父子组件通信：props向下传递，events向上发送
  - 非父子组件通信：使用Vuex状态管理或祖先/后代注入（provide/inject）
  - 避免使用EventBus等难以追踪的全局事件机制
  - 避免滥用$parent、$children、$refs直接操作组件实例
  - **严格遵循单向数据流**：不直接修改props属性，而是通过事件通知父组件更新数据
  - 使用深拷贝处理传入的复杂数据结构，避免意外的引用修改
  - 对于需要传递给多个组件的共享状态，优先使用Vuex防止状态不一致
  - 避免组件间的直接依赖，减少组件间的耦合度

### 代码规范

#### HTML模板规范

- 使用双引号（"）包裹属性值
- 复杂的计算逻辑应使用计算属性代替内联表达式
- 条件渲染优先使用`v-if`，只有在频繁切换时使用`v-show`
- 循环渲染必须设置唯一的`:key`属性
- 保持模板结构简洁清晰，避免过多的嵌套和复杂的条件判断

```vue
<template>
  <div class="kf-component">
    <div v-if="showHeader" class="kf-component-header">
      <slot name="header"></slot>
    </div>
    <div class="kf-component-body">
      <slot></slot>
    </div>
    <div v-if="showFooter" class="kf-component-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>
```

#### JavaScript代码规范

- **组件选项顺序**
  1. name（组件名称）
  2. components（组件注册）
  3. model（v-model 配置）
  4. props（属性）
  5. data（数据）
  6. computed（计算属性）
  7. watch（监听器）
  8. 生命周期钩子（按照它们被调用的顺序）
  9. methods（方法）

- props定义示例:
```js
props: {
  value: {
    type: [String, Number, Array],
    default: ''
  },
  options: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: '请选择'
  },
  disabled: {
    type: Boolean,
    default: false
  }
}
```

- model选项示例:
```js
model: {
  prop: 'value',
  event: 'change'
}
```

- 组件内部方法命名使用小驼峰风格
- 事件处理方法建议以`handle`开头
- 避免在组件中使用过多的计算属性和方法，保持组件的简洁性
- 遵循项目现有的ESLint和Prettier规范

#### CSS样式规范

- 组件样式应使用scoped属性限制作用域，避免样式污染
- 可复用的样式应抽取为公共样式类
- 类名命名遵循项目既有的命名规范和风格
- 避免使用!important，通过提高选择器优先级解决样式冲突
- 样式应关注组件的可响应式布局，适配不同尺寸屏幕

```vue
<style scoped>
.kf-component {
  /* 组件基础样式 */
}
.kf-component-header {
  /* 头部样式 */
}
.kf-component-body {
  /* 主体样式 */
}
.kf-component-footer {
  /* 底部样式 */
}
</style>
```

### 最佳实践

- **性能优化**
  - 适当使用v-show和v-if优化条件渲染性能
  - 为v-for循环提供唯一stable的key
  - 避免在模板中使用复杂表达式，应使用计算属性或方法
  - 重量级的计算使用缓存和记忆化

- **代码复用**
  - 抽取通用逻辑为mixins或utility函数
  - 对于可复用的UI组件，应提供足够的配置选项
  - 使用插槽（slots）增强组件的灵活性
  - 对于二次封装的Element-UI组件，保持API的一致性与可预测性

- **项目实践**
  - 遵循项目已有的开发风格和模式
  - 保持代码的一致性和可维护性
  - 合理利用项目中已有的工具函数和通用组件
  - 遵循ESLint规则，保持代码风格统一

## AI开发助手指导

在使用AI开发助手时，应注意以下几点：

1. **了解项目上下文**：先向AI提供足够的项目背景信息，包括组件的使用场景、数据结构和交互需求

2. **分步骤请求**：对于复杂需求，将其拆分为多个小步骤，逐步向AI求助

3. **代码审查**：对AI生成的代码进行审查，确保符合项目规范和业务需求

4. **提供具体指导**：向AI提供具体的输入示例和期望输出，使其能更准确地理解需求

5. **迭代优化**：基于初步生成的代码，通过多次迭代与AI沟通，逐步优化至满意的结果

## 使用AI助手的工作流程

1. **分析需求**：首先清晰描述你的需求或问题，提供必要的上下文
2. **指定方向**：明确告知AI你期望的解决方案类型（组件开发、问题诊断等）
3. **迭代改进**：根据AI的初步输出给予反馈，进行多轮优化
4. **集成到项目**：确认解决方案符合项目规范后，集成到项目中
5. **验证结果**：测试实现效果，确保满足业务需求

作为一名AI助手，我将帮助你遵循这些规范和最佳实践，共同打造高质量的Vue2前端应用。
```



## 新模块开发 rules
```markdown
# 新页面功能开发规范

## 角色与目标

作为Vue2项目前端开发专家和AI辅助开发顾问，我将帮助你创建一个符合项目规范的页面模块，确保其在功能、样式、交互、性能等方面与现有页面保持一致性，并通过AI辅助开发提高效率。

## 开发规范与最佳实践

### 目录结构与命名
- 新页面应放在`src/views/{功能模块}`对应功能的子目录中
- 复杂功能需要拆分组件放在`components`子目录中
- 文件命名遵循：页面用`PascalCase.vue`，组件用`PascalCase.vue`

### 组件选择与使用
1. **布局组件**：
   - 使用`<layout-content>`作为页面主体容器
   - 设置面包屑导航需使用`breadcrumbs-back-list`属性（注意属性名称）
   - 页面标题统一使用`title`和`sub-title`属性
   - 面包屑数据需要使用`commonService.getParameterBreadcrumb()`方法获取
   ```vue
   <layout-content :breadcrumbs-back-list="breadcrumbsBackList" title="功能名称" sub-title="子功能名称">
     <!-- 内容区 -->
   </layout-content>
   ```

   ```js
   // 导入commonService
   import commonService from '@/services/common/commonService';

   export default {
     data() {
       return {
         breadcrumbsBackList: [] // 注意变量名为breadcrumbsBackList
       }
     },
     async created() {
       // 获取面包屑配置
       const breadcrumb = await commonService.getParameterBreadcrumb();
       this.breadcrumbsBackList = [breadcrumb];
     }
   }
   ```

2. **表单组件优先级**：
   - 优先使用指定的组件
   - 其次使用`yl-`前缀组件(input,button等)
   - 最后考虑基础`el-`前缀组件(form,switch,select等)
   ```vue
   <!-- 如果指定kf-select, 则使用kf-select -->
   <kf-select v-model="value" :options="options" />

   <!-- 其次选择 -->
   <yl-select v-model="value" :options="options" />

   <!-- 基础组件 -->
   <el-select v-model="value">
     <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
   </el-select>
   ```

3. **高级交互组件**：
   - 树形组件默认使用`el-tree`
   - 弹窗组件默认使用`yl-dialog`
   - 弹窗确认使用`yl-popconfirm`组件，支持复杂内容时使用`el-popover`
   - 使用`v-loading`指令显示加载状态，可选择全局Loading或区域Loading
   - 大数据展示场景使用虚拟滚动`virtual-scroll`组件(无要求默认不适用)

### API调用与数据管理
1. **API导入规范**：
   ```js
   // 正确方式
   import { fetchListData, submitForm } from '@/api/module-name';

   // 避免以下方式
   import * as api from '@/api/module-name';
   ```

2. **数据加载模式**：
   ```js
   // 推荐模式
   async fetchData() {
     this.loading = true;
     try {
       const { data } = await fetchListData(this.params);
       this.tableData = data.list || [];
     } catch (error) {
       this.$message.error('数据加载失败');
       console.error(error);
     } finally {
       this.loading = false;
     }
   }
   ```

3. **Vuex状态管理**：
   - 页面间共享数据应存放在Vuex中
   - 使用`mapState`、`mapGetters`、`mapActions`辅助函数
   - 异步操作统一在actions中处理，mutations保持同步

## AI辅助开发功能

### Cursor AI提示词模板

1. **创建新页面提示词**：
   ```
   请帮我创建一个符合KF项目规范的Vue2新页面：
   1. 页面名称：[页面名称]
   2. 功能描述：[简要描述页面功能]
   3. 主要组件：[需要使用的主要组件，如表格、表单等]
   4. 数据结构：[主要数据结构]
   5. API接口：[需要调用的API接口]

   请确保：
   - 使用layout-content作为主布局
   - 使用yl前缀组件
   - 遵循项目代码组织规范
   - 包含基础的数据加载和错误处理
   ```

2. **页面组件拆分提示词**：
   ```
   我正在开发[页面名称]，需要将以下复杂功能拆分为组件：

   [功能描述]

   请帮我设计一个名为[组件名]的可复用组件，要求：
   1. 组件命名
   2. 清晰定义props接口
   3. 提供必要的事件通知
   4. 内部状态管理
   5. 组件文档示例
   ```

3. **性能优化提示词**：
   ```
   以下是我的[组件/页面]代码，存在性能问题（[描述问题]）：

   [代码片段]

   请帮我分析并优化，重点关注：
   1. 不必要的渲染
   2. 大数据处理
   3. 组件拆分
   4. 计算属性与缓存
   ```

### AI辅助开发技巧

1. **代码生成策略**：
   - 先使用AI生成页面基础结构
   - 针对复杂逻辑部分单独提问
   - 要求AI提供代码解释和最佳实践说明

2. **增量开发模式**：
   - 先生成框架代码→测试→填充具体功能
   - 复杂功能拆分为多个小步骤
   - 每完成一步进行代码审查和测试

3. **问题诊断模式**：
   - 提供完整上下文和错误信息
   - 描述预期行为和实际行为
   - 允许AI提供多种可能的解决方案

## 常见问题与解决方案

1. **数据加载后UI未更新**
   - 问题：使用复杂数据结构时可能导致Vue无法检测变化
   - 解决：使用`Vue.set`或`this.$set`、数组操作使用`splice`方法

2. **组件通信问题**
   - 问题：父子组件或兄弟组件间数据传递混乱
   - 解决：
     - 使用Props+Events模式，复杂场景考虑Vuex进行集中管理
     - 严格遵循单向数据流，避免直接修改props变量
     - 处理复杂数据结构时，使用深拷贝防止引用污染
     - 复杂组件可考虑provide/inject机制，但要注意维护成本

3. **表单验证触发时机**
   - 问题：表单验证时机不正确
   - 解决：正确设置`trigger`属性，如`blur`、`change`等

4. **性能优化**
   - 问题：大数据渲染卡顿
   - 解决：使用虚拟滚动、懒加载、分页加载等技术

## AI辅助开发工作流

1. **需求分析阶段**：
   - 使用AI帮助拆解复杂需求
   - 生成功能点清单和技术选型建议

2. **架构设计阶段**：
   - 使用AI生成页面结构草图
   - 设计组件拆分和数据流结构

3. **编码实现阶段**：
   - 使用AI生成基础页面框架
   - 针对复杂功能单独提问
   - 每个功能模块完成后进行代码审查

4. **测试与优化阶段**：
   - 使用AI诊断问题并提供修复方案
   - 进行性能优化建议

5. **总结与文档阶段**：
   - 生成组件使用文档
   - 总结开发经验和最佳实践

## 最佳实践自查清单

☐ 页面结构是否遵循项目规范？
☐ 是否合理使用了kf/yl前缀组件？
☐ 错误处理是否完善？
☐ 加载状态是否提供良好的用户体验？
☐ 表单验证是否合理？
☐ API调用是否规范？
☐ 代码组织是否清晰？
☐ 样式是否符合项目风格？
☐ 性能是否经过优化？
☐ 是否考虑了不同分辨率下的显示？

通过以上规范和指南，结合AI辅助开发技术，可以高效地开发出符合项目标准的新页面，并保持代码质量和一致性。
```



# 高保真处理
重构/开发的页面模块都需要按照高保真来进行开发，如何让 AI 开发的代码尽可能的还原高保真？



目前想到两种方法，效果一般。

## 高保真截图
第一个方法就是直接对高保真进行截图，然后喂给 AI。



## 蓝湖根据高保真生成参考的代码
蓝湖提供了高保真对应的参考代码，也可以喂给 AI。



# 需求开发文档
最后还需要补充在新项目开发的相关信息：比如重构后有改动的需求内容、如何在新的技术栈实现功能等信息。

+ 明确新页面开发的目录位置

```markdown
请帮我完成以下文件的开发：
1. API接口文件：src/api/baseMaterial/positionList.js
2. 页面组件：src/views/baseMaterial/paramSetting/positionList/index.vue
3. 路由配置更新：src/router/modules/baseMaterial.js
```



+ 接口是否都要新增，是否有接口不需要处理



+ 指定工具

```markdown
实现左侧部位列表组件，具体功能：
1. 展示部位列表数据，初始化自动选中第一个部位
2. 实现列表拖拽排序（使用sortablejs）
3. 部位hover时展示删除、编辑、排序按钮
4. 点击部位项切换选中状态，高亮显示
5. 添加新部位按钮，点击打开添加弹窗
6. 列表为空时显示适当提示
```



+ 指定组件

```markdown
删除部位确认弹窗：
   - 使用Vue.prototype.$confirm实现删除确认弹窗

实现右侧问题分类展示区域：
1. 使用Element UI的Tree组件展示问题分类树形结构
2. 当选中部位变化时，加载并展示对应的关联问题分类
3. 无关联问题分类时显示提示信息和快速关联入口
4. 提供"关联问题分类"按钮，点击打开关联弹窗

```



+ 指定实现逻辑

```markdown
实现问题分类关联弹窗：
1. 创建弹窗组件，分为左右两栏：
   - 左侧：可选问题分类树形选择区（支持搜索、多选）
   - 右侧：已选问题分类实时展示区（以树形结构展示，与左侧保持一致）
2. 右侧必须使用树形结构展示已选择的问题分类，不可使用列表形式
3. 左侧勾选时，右侧实时更新显示已勾选数据
4. 打开弹窗时自动回填已关联的问题分类（在左侧树中选中相应节点）
5. 无论问题部位是否有关联问题分类，勾选左侧分类时右侧始终能实时展示选中的分类
6. 提供确认、取消按钮，确认后保存关联关系
7. 关联成功后刷新右侧问题分类展示区
8. 左侧树搜索实现高亮匹配文本效果：
   - 搜索匹配文本以蓝色高亮显示
   - 父节点包含匹配文本时，其所有子节点也应显示
   - 使用v-html方式实现搜索文本高亮效果
   - 参考components/filterTree/index.vue中实现的搜索效果
9. 数据处理逻辑：
   - 获取已关联分类：从后端获取问题部位已关联的问题分类树结构数据
   - 数据转换：将树结构数据转换为ID列表时，**只提取叶子节点ID**，避免重复选择
   - 弹窗回填：使用提取的叶子节点ID列表设置树组件的选中状态
   - 数据保存：保存时只提交叶子节点ID，父节点状态由子节点决定
```



+ 指定开发流程

```markdown
推荐按以下步骤开发：
1. 先创建API文件和Mock数据
2. 实现基础页面结构和路由配置(基于高保真生成的参考代码进行开发)
3. 开发部位列表基础功能(基于高保真生成的参考代码进行开发)
4. 实现部位的添加/编辑/删除功能
5. 开发拖拽排序功能
6. 实现问题分类展示功能(基于高保真生成的参考代码进行开发)
7. 开发问题分类关联弹窗(基于高保真生成的参考代码进行开发)
8. 处理灰度功能适配
9. 完善UI细节和交互体验(基于高保真生成的参考代码进行开发)
10. 全面测试各功能点
```



+ 参考文档

```markdown
开发过程中参考：
1. 高保真图片中的UI设计
2. Element UI官方文档：https://element.eleme.cn/
3. Vue.Draggable文档：https://github.com/SortableJS/Vue.Draggable
4. 项目现有代码：/Users/xulingfeng/Desktop/GIT/KF/kffrontend/src/api/baseMaterial/
5. 原始实现：/Users/xulingfeng/Desktop/GIT/KF/customerservice-integration/customerservice/web/modules/js/parameter/position-list/
```



+ 高保真生成的参考代码



# AI 开发
将相关开发信息整理到一个 markdown 中，提供给 Cursor 。让其进行 agent 开发。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1744361373306-08013d15-47d7-422e-9f1f-82db49d0f4ef.png)



## 注意点
+ 上下文指定上面提到的 rules，要求在 rules 规则下进行开发
+ 可以将高保真截图添加到上下文中
+ 使用 agent 模式 ，claude-3.7 模型(效果更好，但是消耗更多次数)
+ 可以使用 MCP `sequentialthinking`结构化拆解问题
+ 长期维护 rules



# 效果
功能通过调试提示词大致可以实现(目前是通过多轮调试提示词才实现，比较耗费时间和请求次数)，但是 UI 和高保真比还是有一定距离。后续开发时间需要投入到 code review、UI 调整、cursor rules 维护、需求文档更新等。



## AI 开发页面效果
![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1744361876419-080925d6-193b-4410-94d3-e8f9c04f9420.png)

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1744361898167-2e02f704-4291-41f0-858e-eb36b351b27c.png)

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1744361916180-00a228a2-0181-4cda-a3f6-c77c42665593.png)



# 思考
+ 如何提升高保真提示词的准确性，蓝湖有无提供相关工具或者是否有相关的 MCP 工具？
+ AI 开发后自测 - 开发集成 AI 自动化测试？







