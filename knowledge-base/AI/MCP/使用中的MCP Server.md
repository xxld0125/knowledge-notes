# Sequential Thinking
## 功能
结构化思考工具，将复杂问题分解为可管理步骤，通过一个可以随着理解深入而适应和发展的顺序思考过程。



## 配置
`npx -y @modelcontextprotocol/server-sequential-thinking`



# Software Planning Tools
## 功能
软件规划工具，通过交互式，结构化的方法促进软件开发规划，**<font style="color:#DF2A3F;">帮助将复杂的软件项目分解为可管理的任务，跟踪实施进度，并维护详细的开发计划</font>**。



# browsertools
## 功能
让 AI 能够监控浏览器行为，抓取日志、网络请求、截图、辅助调试和交互。



## å 配置
`npx @agentdeskai/browser-tools-mcp`





# 现有配置
```json
{
  "mcpServers": {
    "Sequential Thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    },
    "browsertools": {
      "command": "npx",
      "args": [
        "@agentdeskai/browser-tools-mcp"
      ]
    },
    "puppeteer": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-puppeteer"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/xulingfeng/Desktop/GIT/"
      ]
    }
  }
}
```

