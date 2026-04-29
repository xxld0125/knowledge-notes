

> 在软件工程中，设计模式（Design Pattern）是对软件设计中普遍存在（反复出现）的各种问题，所提出的解决方案。 ——维基百科
>



#### 一、思维导图
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1666944687733-00e19ccd-e1d4-46cd-8d21-72f98b368468.png)



#### 二、学习目标
1. <font style="color:rgb(51, 51, 51);">充分理解前端设计模式的核心思想和基本理念，在具体的场景中掌握抽象的设计原则</font>
2. <font style="color:rgb(51, 51, 51);">会写代码，会写好代码；</font>
3. <font style="color:rgb(51, 51, 51);">会面试，能言之有物。</font>

<font style="color:rgb(51, 51, 51);"></font>

#### <font style="color:rgb(51, 51, 51);">三、设计模式是什么</font>
> 每一个模式描述了一个在我们周围不断重复发生的问题，以及该问题的解决方案的核心。这样，你就能一次又一次地使用该方案而不必做重复劳动。 —— Christopher Alexander
>



<font style="color:rgb(51, 51, 51);">设计模式是“拿来主义”在软件领域的贯彻实践。和很多人的主观臆断相反，设计模式不是一堆空空如也、晦涩鸡肋的理论，它是一套现成的工具 —— 就好像你想要做饭的时候，会拿起厨具直接烹饪，而不会自己去铸一口锅、磨一把菜刀一样。</font>

<font style="color:rgb(51, 51, 51);">用做数学题来打比方，可能大家会更能体会这种概念 —— 我们解题目的时候，往往会用到很多公式/现成的解题方法。比如已知直角三角形两边长，求另一边，我们会直接用勾股定理（我想应该没有人会每求一次边长都自己推一遍勾股定理才用吧）。</font>

<font style="color:rgb(51, 51, 51);">识别题目特征 —— catch题目想要考查的知识点 —— 快速在脑海中映射出它对应的解决方法，这个过程在我们学生时代几乎是一个本能的、条件反射一样的脑回路机制。在学习设计模式时，如果各位可以回忆起这种“从映射到默写”的思维方式，相信这个学习过程会是轻松的、自然的。</font>

<font style="color:rgb(51, 51, 51);"></font>

#### <font style="color:rgb(51, 51, 51);">四、SOLID设计原则</font>
<font style="color:rgb(51, 51, 51);">设计原则是设计模式的指导理论，它可以帮助我们规避不良的软件设计。SOLID 指代的五个基本原则分别是：</font>

+ <font style="color:rgb(51, 51, 51);">单一功能原则（Single Responsibility Principle）</font>
+ <font style="color:rgb(51, 51, 51);">开放封闭原则（Opened Closed Principle）</font>
+ <font style="color:rgb(51, 51, 51);">里式替换原则（Liskov Substitution Principle）</font>
+ <font style="color:rgb(51, 51, 51);">接口隔离原则（Interface Segregation Principle）</font>
+ <font style="color:rgb(51, 51, 51);">依赖反转原则（Dependency Inversion Principle）</font>

<font style="color:rgb(51, 51, 51);">糟糕，又出现了看似高大上的东西，而且是五个！</font>

<font style="color:rgb(51, 51, 51);">别怕，这五个原则，都不难，而且并不是每一个都要求大家掌握，因为在 JavaScript 设计模式中，主要用到的设计模式基本都围绕“</font>**<font style="color:rgb(51, 51, 51);">单一功能</font>**<font style="color:rgb(51, 51, 51);">”和“</font>**<font style="color:rgb(51, 51, 51);">开放封闭</font>**<font style="color:rgb(51, 51, 51);">”这两个原则来展开。</font>

