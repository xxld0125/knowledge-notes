# <font style="color:rgb(23, 43, 77);">为什么会有 paas 应用</font>
<font style="color:rgb(23, 43, 77);">集团级的战略性要求，懂的都懂</font>

# <font style="color:rgb(23, 43, 77);">使用痛点（缺点和不足）</font>
<font style="color:rgb(23, 43, 77);">使用痛点就不说了，用过的人自然知道，无非就是那几个方面的痛点问题</font>

<font style="color:rgb(23, 43, 77);">这里主要讲讲目前客服这些 PaaS 化的应用，仍旧存在的一些局限问题或者说缺点不足：</font>

+ <font style="color:rgb(23, 43, 77);">UI 样式问题</font>
    - <font style="color:rgb(23, 43, 77);">平台组件开放的样式调整能力太有限，有些 UI 效果无法实现</font>
+ <font style="color:rgb(23, 43, 77);">交互问题</font>
    - <font style="color:rgb(23, 43, 77);">组件的事件类型和钩子太少，有些交互也无法实现，比如事件前的钩子的处理场景</font>
+ <font style="color:rgb(23, 43, 77);">个性化组件太多</font>
    - <font style="color:rgb(23, 43, 77);">依赖的平台组件过少，过多的依赖了自定义开发的个性化组件，导致维护成本很高</font>
    - <font style="color:rgb(23, 43, 77);">不多这个问题至少只是成本增高，不至于像其他的玩不下去，无法实现</font>
+ <font style="color:rgb(23, 43, 77);">线上问题难以排查定位</font>
    - <font style="color:rgb(23, 43, 77);">因为不是像传统的本地代码开发方式，无法直接打断点，打日志来定位，排查基本靠猜</font>
+ <font style="color:rgb(23, 43, 77);">扩展应用粒度、页面个性化粒度太高</font>
    - <font style="color:rgb(23, 43, 77);">针对一些微小的个性化需求，只能走扩展应用模式，页面粒度的个性化，导致维护、同步的成本也很高</font>
+ <font style="color:rgb(23, 43, 77);">SaaS 环境很难玩个性化需求</font>
    - <font style="color:rgb(23, 43, 77);">SaaS 环境后端就一套代码，如果用租户扩展应用模式来实现个性化需求，一个扩展应用一个新的站点地址，现有的后端逻辑和离线 App 项目无法支持，需要改造针对租户级别配置 PaaS 应用站点地址</font>
+ <font style="color:rgb(23, 43, 77);">客服工单系统在越秀环境目前是离线包走 App 热更新模式</font>
    - <font style="color:rgb(23, 43, 77);">注意：越秀使用客服工单系统，是离线 + 在线两种模式均有使用，因此目前每次发布，除了下载离线包发热更新外，PaaS 平台也需要发布</font>
    - <font style="color:rgb(23, 43, 77);">离线包其实是下载构建后的资源包，这意味着不同分支的合并操作仍旧会有冲突问题</font>
    - <font style="color:rgb(23, 43, 77);">而且切个访问的后端接口环境，都需要重新打包，操作繁琐</font>
+ <font style="color:rgb(23, 43, 77);">平台的分支开发模式功能不够完善</font>
    - <font style="color:rgb(23, 43, 77);">平台只支持建分支，不支持合并时的冲突解决，导致合并分支时，如果出现冲突，解决成本太大，要么学习元数据意义，要么直接废弃某个分支，把在废弃分支上的修改全部手动在新分支上再操作一遍</font>

<font style="color:rgb(23, 43, 77);">  
</font>

# <font style="color:rgb(23, 43, 77);">优点和好处</font>
+ <font style="color:rgb(23, 43, 77);">非研发人员也可以直接实现某些需求（但目前没体验到）</font>
+ <font style="color:rgb(23, 43, 77);">大量个性化功能时可直接复用组件，减少开发成本（其实传统开发模式也能实现）</font>
+ <font style="color:rgb(23, 43, 77);">快速拖拽兑现需求（通常仅适用于业务简单的页面，对于复杂业务，反而增大开发成本）</font>

<font style="color:rgb(23, 43, 77);">  
</font>

# <font style="color:rgb(23, 43, 77);">后面怎么玩</font>
<font style="color:rgb(23, 43, 77);">站在使用方角度，我们要达到既使用了 paas 技术，又不给自己加负的话，两个方面吧：一是尽量只用 paas 实现业务简单的页面，二就是尽量抽空学习下 paas 内部实现，成为 paas 专家来提高效率吧</font>

<font style="color:rgb(23, 43, 77);">否则的话，就是等 paas 团队把一些痛点问题都解决了，等待 paas 平台的完善吧</font>

+ <font style="color:rgb(23, 43, 77);">比如提高本地开发调试的效率，改了函数不用重新页面等待那么久等等</font>
+ <font style="color:rgb(23, 43, 77);">组件库完善点</font>

<font style="color:rgb(23, 43, 77);">还有，针对目前的一些用法，后续可以改善下玩法：</font>

+ <font style="color:rgb(23, 43, 77);">越秀客服工单系统的离线资源包方用法</font>
    - <font style="color:rgb(23, 43, 77);">后面可以直接改成在线用法，不过首屏加载性能得看看怎么样</font>
+ <font style="color:rgb(23, 43, 77);">中间代理站点模式</font>
    - <font style="color:rgb(23, 43, 77);">加这个中间代理站点是为了解决两个问题：锁版本 + 微信 JSSDK 的安全域名校验</font>
    - <font style="color:rgb(23, 43, 77);">所以如果不需要这两个问题，可以看看能否去掉中间代理站点</font>
    - <font style="color:rgb(23, 43, 77);">如果中间代理站点去不掉，那需要考虑下，怎么再 SaaS 环境下使用这个代理站点</font>
        * <font style="color:rgb(23, 43, 77);">因为有可能 SaaS 环境下的不同租户，实际代理到的是不同的 PaaS 站点</font>
        * <font style="color:rgb(23, 43, 77);">所以可能得思考下，代理站点的配置改造，以及后端获取 paas 应用站点的逻辑改造，都需要支持根据租户级配置不同 paas 应用站点</font>
+ <font style="color:rgb(23, 43, 77);">平台组件样式无法实现</font>
    - <font style="color:rgb(23, 43, 77);">hook 里想办法去通过 js 走样式覆盖吧</font>
        * <font style="color:rgb(23, 43, 77);">尽量不影响全局，所以建议可以试试在需要覆盖样式的组件上拉个空组件（可以自定义实现个），然后 hook 里通过添加 css 的兄弟选择器的方式来作用到需要覆盖样式的组件上</font>
+ <font style="color:rgb(23, 43, 77);">服务 API 没有钩子拦截处理数据</font>
    - <font style="color:rgb(23, 43, 77);">要么让后端直接处理成前端需要的数据</font>
    - <font style="color:rgb(23, 43, 77);">要么等平台的数据源优化改造</font>
    - <font style="color:rgb(23, 43, 77);">要么想法子，自己通过函数去调接口，然后获取表单组件，手动通过 setData 来设置表单数据</font>
+ <font style="color:rgb(23, 43, 77);">拉他们的元数据仓库</font>
    - <font style="color:rgb(23, 43, 77);">通过查看 git 提交变化，来确认各个分支，或者不同人都修改过什么东西</font>
    - <font style="color:rgb(23, 43, 77);">元数据仓库里包含了页面、函数库、业务对象、服务，所有在 paas 平台上添加的东西，都能看到</font>

