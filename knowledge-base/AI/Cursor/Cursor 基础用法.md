# 官网
[https://www.cursor.com/](https://www.cursor.com/)

# 注册
# 会员
# 功能
## 内置大模型
选择需要的大模型，也支持添加。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737447555978-4acb6db2-22bc-4b11-8038-e72758b34dc1.png)

在聊天框选择大模型

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737447640275-231f9884-f985-40b6-b9ae-d3ea83daac9f.png)



**<font style="color:#DF2A3F;">大模型推荐</font>**`**<font style="color:#DF2A3F;">GPT-4O</font>**`**<font style="color:#DF2A3F;">和</font>**`**<font style="color:#DF2A3F;">CLAUDE-3.5-SONNET</font>**`

`**<font style="color:#DF2A3F;">GPT-4O</font>**`**<font style="color:#DF2A3F;">适合综合问答，建议在CHAT模式使用</font>**

`**<font style="color:#DF2A3F;">CLAUDE-3.5-SONNET</font>**`**<font style="color:#DF2A3F;">适合代码生成，建议在COMPOSER模式使用</font>**



## 聊天框
### Normal / Agent
`Composer` 聊天框支持选择 `Normal` 或 `Agent` 两种模式。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737447946208-4d456dc4-af7b-494b-b264-3a6947c91655.png)



+ `Normal`：可以检索代码库和文档，可以正常创建和写入文件。
+ `Agent`：除了可以创建/写入文件，还可以自动提取上下文、运行终端命令、按照语义搜索代码、执行一些文件操作，属于一种更高级的操作(目前`Agent`只支持`CLAUDE`模型，速度慢于`Normal`)。



根据复杂度选择上面两种模式。如果是一个复杂功能，将其拆解，再一步一步的喂给`Cursor`，这个时候应该使用 `Agent`，因为它可以自动提取上下文，帮你执行一些命令。而针对一些简单功能，使用 `Normal` 就可以了，速度会快很多。



### @操作符
在聊天框输入 `@` 时，会唤起下拉选择框。



+ `**@Files**`**：引用文件(也可以从资源管理器拖动文件到聊天框)**
+ `**@Folders**`**：引用文件夹(也可以从资源管理器拖动文件夹到聊天框)**
+ `**@Code**`**：引用一段代码(也可以选择一段代码，再**`**COMMAND + L**`**)**
+ `**@Docs**`**：引用文档**

支持通过添加文档链接来自定义文档。添加后`Cursor`会自动抓取链接内容，并将其编入索引。

在聊天框选择这个文档中后，`Cursor`会将文档内容纳入上下文。

可以将接口文档链接、需求文档链接或任意文档链接录入进`Docs`。使用时选择对应的文档即可。相当于一个基于项目的私有AI知识库。

在设置中添加文档：

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737449693233-03784010-b05b-4850-83db-4d44137d4ae9.png)



也可以不使用Docs，直接`@在线链接`。这时也会先解析该链接再进行回复。可以用该方法处理一些临时链接。`Docs`适合基于项目添加一些固有的文档。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737450409117-3bf93e2c-883e-4b90-8423-975301f1d03c.png)



**注意点：**

添加文档链接时，建议在URL后面加上`/`。比如：[https://ant.design/components/overview-cn/](https://ant.design/components/overview-cn/)。

这是因为不加`/`时，只会索引该页面内容。加上的话，除了索引该页面内容，也会索引所有子页面和子目录下的内容。



+ `**@Git**`**：支持选择历史Git提交作为上下文，可以用来对比多次提交的差异。**
+ `**@Notepad**`**：**

可以作为临时笔记记录、充当项目的上下文记录、保存AI对话的历史记录。

在 `Cursor` 中`Chat`模式和`Composer`模式的上下文是独立不互通的。

通过`Notepad`记录开发思路、保存重要的代码片段、维护待办事项、存储AI对话记录等。在`Chat`或`Composer`引用`Notepad`进行上下文的互通传递。

+ `**@Suggested**`**：**
+ `**@Codebase**`**：**

采集重要的文件和代码块，并对采集的上下文进行排序、推理、最后给出最匹配的答复。

1.扫描整个项目，查到与指令相关的文件或代码块

2.根据相关性对上下文进行重新排序(越相关越靠前)

3.利用上下文进行推理

4.生成答复



建议每次打开一个新项目时手动进行数据采集。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737452321055-627f219b-b614-4d1d-9ff7-47a5a85f5708.png)



建议配置`.cursorignore`，声明索引需要忽略的文件范围，减少索引的文件数量。



+ `@Lint errors`：用于显示和处理代码检查错误
+ `**@Web**`**：搜索网络内容，AI搜索引擎**



## 规则配置
### 全局配置 Cursor Settings
![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737452494785-63e9b387-dbc0-4113-bd57-a01745620a98.png)



### 项目配置 .cursorrules
```plain

# 前置
- 你是一个前端开发专家, 专注于现代化网站开发

# 项目简介
- 项目是一个基于React的现代Web应用程序, 使用TypeScript和Tailwind CSS构建
- 项目的目标是创建一个功能丰富、响应迅速的Web应用程序, 提供用户友好的界面和流畅的用户体验

# 技术架构
- 使用React作为前端框架
- 使用TypeScript作为编程语言
- 使用Tailwind CSS作为样式框架
- 使用Ant Design作为UI库
- 使用react-router-dom作为路由管理
- 使用react-redux作为状态管理
- 使用react-router-config作为路由配置
- 使用lodash-es作为工具库

# 目录结构
- src/
  - components/ 公共组件
  - pages/ 页面
  - utils/ 工具
  - types/ 类型
  - store/ 状态管理
  - assets/ 资源
    - images/ 图片
    - styles/ 样式
  - app.tsx 应用入口

# 代码规范
- 组件使用大驼峰命名
- 工具函数使用小驼峰命名
- 文件夹使用小写字母, 单词之间使用-连接
- 文件名使用大驼峰命名
- 变量使用小驼峰命名
- 常量使用大写字母, 单词之间使用_连接

# 组件规范
- 使用函数式组件
- 组件文件使用 .tsx 扩展名
- 组件需要添加 displayName
- 使用 forwardRef 转发引用
- 组件需要添加 propTypes

# 样式规范
- 业务css使用tailwindcss

# git提交规范
- commit规范
```



# 技巧和思路
## Cursor乱修改代码问题如何解决
拆解该问题，可以分为三个点。

1. 预防：如何能让AI尽可能的按照我们的心意生成并修改代码(如何向AI提问)
    - 让AI复述需求指令，确认后一致后再要求进行答复，避免因误解而产生的错误答复
    - 明确需求辐射范围，在发出一次指令前，让这个指令范围足够小、指令足够单一化、要有足够的针对性。尽可能的携带上相关代码、文件，并且告诉AI在什么范围内进行修改。
    - 需求拆解，当你有一个足够大的需求，又不方便拆成一步一步喂给AI时。建议在一次问答中将需求内容一条一条的写清晰，做个排序。然后用无序/有序列表的方式提供给AI，让AI能够更清晰的理解你的需求。
    - 把AI当成小孩子，在和AI沟通时尽可能的逻辑清晰，描述问题时加以引导。除了描述问题，也可以将自己的解决思路也发给AI，必要时也可以发一些示例参考。引导AI向自己想要的结果靠拢。



2. 检测：`Composer`一次会修改很多代码，我们如何确定这些修改是我们想要的

可以使用 `SAVE ALL` 暂时保存所有修改，查看效果。确定符合效果，点击 `ACCEPT ALL`采用代码，或者点击 `REJECT ALL`不采用代码。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737453584654-7e019c71-1f24-4087-a046-0472ed6083dc.png)



3. 回滚：经过几次问答后，发现某次问答中AI有乱修改，如何回滚到之前的版本

`Cursor` 针对每次问答会记录一个 `Checkpoint`标记，需要回滚时，找到对应的提问，点击 `RESTORE` 恢复到这次问答之前的代码版本。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737453648755-3f763919-d05a-49fa-86fc-92c98324b849.png)



## Cursor整体使用思路
### 使用Cursor对需求不是很明确时
这时不应该直接让`Composer`帮你写代码，可以现在`Chat`中与AI交流你的想法。先向AI描述你的需求，你想做什么事情。让AI对你的需求有基础的了解，然后去问AI想要完成自己的需求，可以选择哪些方案，并且可以让AI阐述以下各个方案的优缺点。选择对应的方案之后就可以在`Composer`重新编辑你的需求，让AI在你的需求和方案框架内生成代码。

总之有不懂的就在`Chat`中问AI，问明白之后再去`Composer`根据你的理解给AI提示词让它帮你做事情，而不是`Composer`模式下反复尝试，那样会做很多无用功。



### 如果是一个相对复杂的项目
在和`Chat`沟通完需求后，可以将需求做拆解，比如拆成一个个的功能Feature，把这些Feature通过Notepad单独记录下来。然后按照需求步骤，在Composer输入框中选择对应的Notepad去完成需求。在这个过程中Composer的生成有问题，可以新建一个Notepad记录问题，在Chat聊天框中选中这个Notepad询问，得到方案后再更新Nodepad。最后回到Composer选中对应的Nodepad去做生成。这样做的话虽然稍微麻烦些，但是对项目的把控程度是非常高的。



### 已有项目使用CURSOR辅助开发后续需求orBug修复
使用Cursor打开项目之后

1. 检索整个项目生成一个`.cursorignore`，然后更新你想要索引忽略掉的文件
2. 点击设置中 `Codebase indexing`的 `Resync index` 进行重新索引
3. 将项目相关的在线文档，比如需求文档，接口文档、开发相关的技术文档全部录入到docs中以作备用
4. 新建`.cursorrules`，相当于一个前置Prompt提示词，<font style="color:rgb(24, 25, 28);">基于项目约束Ai范围使其尽量精准</font>



## 封存项目文档
Notepad并没有储存在你的项目中，而是在Cursor的缓存中，换个设备就没了。



## 支持给暂存区的代码一键生成commit信息
Cursor会分析当前的更改及以前提交的信息，生成符合上下文的提交信息。会从你的历史提交中学习。

![](https://cdn.nlark.com/yuque/0/2025/png/25743026/1737516856241-8accf2b3-f337-40f5-9334-177f7dce7f2d.png)





## 当一个问题多次处理还是异常时
当遇到复杂问题或问题描述不清晰时，可能会出现一个问题，Cursor多次处理还是未能达到要求的效果。这时候不要继续提问/要求，可以采用以下几个方法。

+ 让Cursor换个思路
+ 让Cursor只聚焦该问题，先不考虑其他限制。解决该问题后，再补充其他的开发项



## Cursor上下文有长度限制, 如何增强上下文
+ Summarized Composers: 可以总结Composer历史对话，当对话变的太长时，可以开启新对话，并引用之前的Composer对话。

那什么时候使用该功能？

当前Composer对话已经超出上下文限制时使用。

如何知道当前对话已经超过上下文限制？

可以在`.cursorrules`中加入一句话，任意固定句式 每次回复都以，“收到xxx”开头。什么时候Cursor的回复没有这句话时，说明这个对话已经超出上下文限制，此时可以开启新对话。



+ <font style="color:rgb(24, 25, 28);">Optional Long Context：允许Cursor在Composer模式下使用更长的代码上下文，默认关闭状态，需要手动开启，但是启动后会消耗更多的fast requests。建议根据需求灵活开启。</font>
+ <font style="color:rgb(24, 25, 28);">README.md记录项目信息</font>

每次开发完功能时，更新README文件，后续可以引用README提供项目最新信息。

+ <font style="color:rgb(24, 25, 28);">Notepads保存常用逻辑</font>

<font style="color:rgb(24, 25, 28);"></font>

## <font style="color:rgb(24, 25, 28);">结合Mermaid流程图</font>


## 合理利用测试用例
输入需求，要求先根据需求编写测试用例，然后再写代码，写完后运行用例，有报错时，修改代码直至完全用例完全通过。



## 借助 typescript, eslint, prettier 保障代码质量


## 问题调试
AI 生成调试的日志，运行后将对应日志给到 AI 进行问题排查及修复。







