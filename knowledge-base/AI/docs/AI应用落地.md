# 落地场景
| **用户类型** | **核心需求** | **典型场景案例** | **关键技术** |
| --- | --- | --- | --- |
| **<font style="color:rgb(64, 64, 64);">个人开发者</font>** | <font style="color:rgb(64, 64, 64);">效率工具轻量化</font> | <font style="color:rgb(64, 64, 64);">- 代码补全（GitHub Copilot模式）   </font><font style="color:rgb(64, 64, 64);">- 自媒体文案生成（含多平台风格适配）</font> | <font style="color:rgb(64, 64, 64);">Prompt工程、API调用</font> |
| **<font style="color:rgb(64, 64, 64);">创业团队</font>** | <font style="color:rgb(64, 64, 64);">快速验证MVP</font> | <font style="color:rgb(64, 64, 64);">- 智能客服（FAQ精准匹配+长尾问题兜底）   </font><font style="color:rgb(64, 64, 64);">- 竞品舆情日报自动生成</font> | <font style="color:rgb(64, 64, 64);">RAG、规则引擎混合架构</font> |
| **<font style="color:rgb(64, 64, 64);">大型企业</font>** | <font style="color:rgb(64, 64, 64);">现有系统智能化改造</font> | <font style="color:rgb(64, 64, 64);">- CRM客户画像自动更新   </font><font style="color:rgb(64, 64, 64);">- 供应链风险预测看板</font> | <font style="color:rgb(64, 64, 64);">微调模型、私有化部署</font> |
| **<font style="color:rgb(64, 64, 64);">行业场景</font>** | <font style="color:rgb(64, 64, 64);">垂直领域深度赋能</font> | <font style="color:rgb(64, 64, 64);">医疗：影像报告AI初筛+医生复核   </font><font style="color:rgb(64, 64, 64);">教育：个性化错题本生成+知识点溯源</font> | <font style="color:rgb(64, 64, 64);">多模态模型、领域知识图谱</font> |




# AI应用核心概念
+ 训练：**大量的数据来训练，并且这个数据一定要是领域数据**
+ 模型：**通过大量数据训练除了模型，还需要数据标注**
+ Prompt优化：**<font style="color:#DF2A3F;">前端重点</font>**
+ 输出：**<font style="color:#DF2A3F;">前端重点</font>**

**<font style="color:#DF2A3F;"></font>**

# 核心架构模式对比
| **模式** | **技术指标** | **优势** | **局限** | **适用场景** | **2023行业实践案例** |
| --- | --- | --- | --- | --- | --- |
| **<font style="color:rgb(64, 64, 64);">RAG</font>** | <font style="color:rgb(64, 64, 64);">- 响应延迟: 300-800ms   </font><font style="color:rgb(64, 64, 64);">- 最小数据需求: 1000QA对</font> | <font style="color:rgb(64, 64, 64);">• 支持实时知识更新   </font><font style="color:rgb(64, 64, 64);">• 规避模型幻觉风险   </font><font style="color:rgb(64, 64, 64);">• 可解释性强（可溯源引用）</font> | <font style="color:rgb(64, 64, 64);">• 多跳推理能力弱   </font><font style="color:rgb(64, 64, 64);">• 检索精度影响结果   </font><font style="color:rgb(64, 64, 64);">• 上下文长度受限</font> | <font style="color:rgb(64, 64, 64);">- 法律条款查询系统   </font><font style="color:rgb(64, 64, 64);">- 产品说明书问答   </font><font style="color:rgb(64, 64, 64);">- 企业知识库助手</font> | <font style="color:rgb(64, 64, 64);">平安智能客服系统升级</font> |
| **<font style="color:rgb(64, 64, 64);">微调</font>** | <font style="color:rgb(64, 64, 64);">- 训练成本:</font><font style="color:rgb(64, 64, 64);"> </font><font style="color:rgb(64, 64, 64);">50</font><font style="color:rgb(64, 64, 64);">−</font><font style="color:rgb(64, 64, 64);">50</font><font style="color:rgb(64, 64, 64);">−</font><font style="color:rgb(64, 64, 64);">500/epoch   </font><font style="color:rgb(64, 64, 64);">- 最低数据需求: 10k样本</font> | <font style="color:rgb(64, 64, 64);">• 领域术语精准掌握   </font><font style="color:rgb(64, 64, 64);">• 输出风格可控   </font><font style="color:rgb(64, 64, 64);">• 推理速度最快（无检索开销）</font> | <font style="color:rgb(64, 64, 64);">• 知识固化难更新   </font><font style="color:rgb(64, 64, 64);">• 存在过拟合风险   </font><font style="color:rgb(64, 64, 64);">• 数据标注成本高</font> | <font style="color:rgb(64, 64, 64);">- 医疗报告生成   </font><font style="color:rgb(64, 64, 64);">- 金融财报分析   </font><font style="color:rgb(64, 64, 64);">- 法律文书润色</font> | <font style="color:rgb(64, 64, 64);">阿里医疗大模型CMT-1</font> |
| **<font style="color:rgb(64, 64, 64);">Agent</font>** | <font style="color:rgb(64, 64, 64);">- 任务耗时: 2-5倍单步调用   </font><font style="color:rgb(64, 64, 64);">- 内存消耗: 2-3x基础模型</font> | <font style="color:rgb(64, 64, 64);">• 复杂任务拆解能力   </font><font style="color:rgb(64, 64, 64);">• 支持多工具调用   </font><font style="color:rgb(64, 64, 64);">• 动态决策路径</font> | <font style="color:rgb(64, 64, 64);">• 开发调试复杂度高   </font><font style="color:rgb(64, 64, 64);">• 错误传播风险   </font><font style="color:rgb(64, 64, 64);">• 需设计补偿机制</font> | <font style="color:rgb(64, 64, 64);">- 智能投资顾问   </font><font style="color:rgb(64, 64, 64);">- 旅行规划助手   </font><font style="color:rgb(64, 64, 64);">- 自动化测试脚本生成</font> | <font style="color:rgb(64, 64, 64);">AutoGPT企业定制版</font> |
| **<font style="color:rgb(64, 64, 64);">提示工程</font>** | <font style="color:rgb(64, 64, 64);">- 开发周期: 1-3天   </font><font style="color:rgb(64, 64, 64);">- 维护成本: 低</font> | <font style="color:rgb(64, 64, 64);">• 零训练成本   </font><font style="color:rgb(64, 64, 64);">• 即时生效   </font><font style="color:rgb(64, 64, 64);">• 可组合复用</font> | <font style="color:rgb(64, 64, 64);">• 效果受限于基座模型   </font><font style="color:rgb(64, 64, 64);">• 长流程控制困难   </font><font style="color:rgb(64, 64, 64);">• 难以处理专业领域问题</font> | <font style="color:rgb(64, 64, 64);">- 社交媒体文案生成   </font><font style="color:rgb(64, 64, 64);">- 邮件模板定制   </font><font style="color:rgb(64, 64, 64);">- 简单数据分析</font> | <font style="color:rgb(64, 64, 64);">Notion AI提示库</font> |
| **<font style="color:rgb(64, 64, 64);">混合架构</font>** | <font style="color:rgb(64, 64, 64);">- 典型配置: RAG+微调+规则引擎</font> | <font style="color:rgb(64, 64, 64);">• 精准性与灵活性平衡   </font><font style="color:rgb(64, 64, 64);">• 关键环节可人工干预   </font><font style="color:rgb(64, 64, 64);">• 故障隔离</font> | <font style="color:rgb(64, 64, 64);">• 系统复杂度最高   </font><font style="color:rgb(64, 64, 64);">• 需要多技能团队   </font><font style="color:rgb(64, 64, 64);">• 链路延迟叠加</font> | <font style="color:rgb(64, 64, 64);">- 医疗诊断辅助系统   </font><font style="color:rgb(64, 64, 64);">- 金融风控决策   </font><font style="color:rgb(64, 64, 64);">- 工业设备故障排查</font> | <font style="color:rgb(64, 64, 64);">腾讯混元大模型系统</font> |
| **<font style="color:rgb(64, 64, 64);">模型蒸馏</font>** | <font style="color:rgb(64, 64, 64);">- 压缩率: 30%-70%   </font><font style="color:rgb(64, 64, 64);">- 精度损失: 5%-15%</font> | <font style="color:rgb(64, 64, 64);">• 适合边缘部署   </font><font style="color:rgb(64, 64, 64);">• 推理能耗降低   </font><font style="color:rgb(64, 64, 64);">• 继承大模型能力</font> | <font style="color:rgb(64, 64, 64);">• 依赖教师模型质量   </font><font style="color:rgb(64, 64, 64);">• 领域迁移能力弱   </font><font style="color:rgb(64, 64, 64);">• 需要调参经验</font> | <font style="color:rgb(64, 64, 64);">- 手机端语音助手   </font><font style="color:rgb(64, 64, 64);">- IoT设备智能控制   </font><font style="color:rgb(64, 64, 64);">- 实时翻译笔</font> | <font style="color:rgb(64, 64, 64);">华为端侧小模型PanGu-Σ</font> |


---

#### <font style="color:rgb(64, 64, 64);">关键补充说明：</font>
1. **<font style="color:rgb(64, 64, 64);">混合架构趋势</font>**<font style="color:rgb(64, 64, 64);">：</font>
    - <font style="color:rgb(64, 64, 64);">金融行业典型方案：RAG（实时政策） + 微调模型（风控规则） + 规则引擎（合规校验）</font>
    - <font style="color:rgb(64, 64, 64);">医疗场景最佳实践：检索增强（最新论文） → 微调模型（诊断建议） → 人工审核工作流</font>
2. **<font style="color:rgb(64, 64, 64);">技术演进方向</font>**<font style="color:rgb(64, 64, 64);">：</font>
    - **<font style="color:rgb(64, 64, 64);">RAG 2.0</font>**<font style="color:rgb(64, 64, 64);">：</font>
        * <font style="color:rgb(64, 64, 64);">多模态检索（文本+表格+图像联合检索）</font>
        * <font style="color:rgb(64, 64, 64);">自适应分块策略（动态调整chunk大小）</font>
        * <font style="color:rgb(64, 64, 64);">混合检索器（关键词+向量+图检索）</font>
    - **<font style="color:rgb(64, 64, 64);">微调优化</font>**<font style="color:rgb(64, 64, 64);">：</font>
        * <font style="color:rgb(64, 64, 64);">参数高效微调（LoRA/QLoRA）</font>
        * <font style="color:rgb(64, 64, 64);">增量持续学习（避免灾难性遗忘）</font>
        * <font style="color:rgb(64, 64, 64);">安全微调（毒性过滤+偏见矫正）</font>
3. **<font style="color:rgb(64, 64, 64);">Agent新范式</font>**<font style="color:rgb(64, 64, 64);">：</font>
    - **<font style="color:rgb(64, 64, 64);">Recursive Agent</font>**<font style="color:rgb(64, 64, 64);">：任务→子任务树形分解</font>
    - **<font style="color:rgb(64, 64, 64);">Self-Debug</font>**<font style="color:rgb(64, 64, 64);">：自动验证输出并修正</font>
    - **<font style="color:rgb(64, 64, 64);">Human-in-the-loop</font>**<font style="color:rgb(64, 64, 64);">：关键节点人工确认</font>

---

<font style="color:rgb(64, 64, 64);">该对比表增加了可量化的技术指标和最新行业案例，并补充了架构演进方向。实际选型时建议通过以下维度评估：</font>

1. **<font style="color:rgb(64, 64, 64);">数据维度</font>**<font style="color:rgb(64, 64, 64);">：标注数据量/更新频率/结构化程度</font>
2. **<font style="color:rgb(64, 64, 64);">性能需求</font>**<font style="color:rgb(64, 64, 64);">：响应延迟/并发量/准确率阈值</font>
3. **<font style="color:rgb(64, 64, 64);">资源限制</font>**<font style="color:rgb(64, 64, 64);">：GPU算力/内存容量/运维成本</font>
4. **<font style="color:rgb(64, 64, 64);">合规要求</font>**<font style="color:rgb(64, 64, 64);">：数据隐私/可解释性/审计追踪</font>

****

# AI应用开发切入点
**AI开发平台**

+ **AI 工作流 react-flow / vue-flow**
+ **RAG 管道**
+ **Agent 功能**
+ **模型管理**
+ **丰富节点接入**

****

# 扩展知识
+ **SSE**
+ **EventSource**
+ **低代码平台 DSL**



