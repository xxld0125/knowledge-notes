# 环境要求
`>= node 18`

# 安装
`npm install -g @anthropic-ai/claude-code`

# 配置
## 项目配置
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "xxxx",
    "ANTHROPIC_AUTH_TOKEN": "xxxx"
  }
}

```



## 全局配置
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "xxxx",
    "ANTHROPIC_AUTH_TOKEN": "xxxx"
  }
}

```



# 使用
## 常用命令
+ claude：启动交互模式
+ claude -c：继续最近的对话
+ claude -r：恢复之前的对话
+ claude "任务"：运行一次性任务
+ claude -p "查询"：<font style="color:rgb(62, 62, 62);">运行一次性查询，然后退出</font>
+ claude commit：创建 Git 提交
+ ...

## 常用指令
+ init
+ compact
+ mcp
+ review
+ cost
+ exit 或 Ctrl+C：<font style="color:rgb(62, 62, 62);">退出 Claude Code</font>
+ clear：<font style="color:rgb(62, 62, 62);">清除对话历史</font>
+ <font style="color:rgb(62, 62, 62);">...</font>



## 开发模式
会话期间使用 `<font style="color:#DF2A3F;">Shift+Tab</font>` 循环切换权限模式来切换到计划模式。



+ default：默认模式(手动接受)
+ accept edit on：<font style="color:rgb(62, 62, 62);">自动接受模式</font>
+ plan mode on：规划任务



Yolo：全权限模式(命令行：`<font style="color:#DF2A3F;">claude --dangerously-skip-permissions</font>`)



设置默认开发模式

```javascript
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```



## 思考命令
+ think：简单思考
+ think ultra：深度思考

## 上下文
### 图片
1. 将图像拖放到 Claude Code 窗口中
2. 复制图像并使用 ctrl+v 粘贴到 CLI 中（不要使用 cmd+v）
3. 向 Claude 提供图像路径。例如，“Analyze this image: /path/to/your/image.png”



### 引用文件/目录
使用 @ 快速包含文件或目录

## 自定义指令
在`.claude/commands`目录下的增加的自定义指令。



### 自定义变量
使用 `$ARGUMENTS` 占位符创建命令文件



## 用量查询
### 监控 token 用量
+ 查看当天用量：`npx ccusage@latest`
+ 实时监控消耗速度：`npx ccusage@latest blocks --live`



# 进阶
## CLAUDE.md
当前项目始终生效的配置文件

### 初始化
+ 通过`/init`初始化 `CLAUDE.md`文件
+ 输入 `#`进入规则编辑模式创建`CLAUDE.md`文件
+ 手动创建`CLAUDE.md`文件



## 管理允许工具列表
+ `/permission`：向允许列表添加或移除工具
+ 编辑 `.claude/settings.json`或 `~/.claude.json`
+ 使用`--allowedTools`cli 标志进行会话特定的权限设置



## MCP




# 生态工具
## Super-design(生成设计图)
1. 页面布局(要求提供 5 种)
2. 主题设计(要求提供 5 种)
3. 主题色(coolors) 
4. 动画设计(animatopy)

## Shadcn UI(组件库)
1.自定义主题(tweakcn)

## coolors(主题色)
## Claude Code(VSCODE 插件)




