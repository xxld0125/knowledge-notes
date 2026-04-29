#### 一、背景
移动客服实现PBC化，能够独立交付集成到第三方系统中；智慧客服事业部产品目前都是大单体模式，移动客服产品经过多次的不完整的演进现状分析：



1、经过多次的不完整的演进导致多套逻辑并存。

2、多仓库职责不明确多端业务互相共存，业务间耦合严重，需求兑现难度高周期长。

3、产品声明周期管理不全，开放性支撑不足，技术、接口文档维护不全。

4、质量低客户满意度低，由于历史债务导致的小事故频发，数据存储架构未隔离，验房与客服产品数据间多处存在偶尔。

5、治理和运行效率存在显著问题，慢SQL、复杂SQL(业务逻辑盲区)；域名多且乱。



#### 二、目标
消除以上常年累月存在的问题；核心的工单模块，以微服务形态对外提供统一的服务。



#### 三、BFF定位
![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671518158422-e2d76736-6eae-4b37-9321-c98e756510e7.png)



上图是移动客服逻辑架构图，可以清晰的看出BFF层需要对接:

+ **前端UI层**
+ **调用go服务**
+ **调用php服务**
+ **open api(第三方对接场景)**
+ **php服务调用**
+ **。。。**



#### 四、业务场景
**结合以上BFF对接场景，归类下，主要是三种业务流程。**

1. **UI层接口调用**



![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671524838871-f3eb8540-f5c7-4992-960e-5c36d82d74f9.png)



2. **第三方调用客服接口（bff-go层处理）**

MIP平台,鉴权方法:<font style="color:#333333;">整体采用</font><font style="color:#ff0000;">md5/sha256</font><font style="color:#333333;">来进行通信秘钥的</font><font style="color:#ff0000;">对称加密</font><font style="color:#333333;">比对计算。暂不处理.</font>



![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671529416381-274c7c17-0462-4416-aeb4-c7e8f255e2f8.png)

****

****

3. **php调用go接口**

服务化的切换策略是`绞杀`，未完全切换完成时，存在<font style="color:#333333;">php服务调用go服务的场景。调用方式采用</font><font style="color:#ff0000;">http</font><font style="color:#333333;">通讯方式，在通讯安全上，整体采用</font><font style="color:#ff0000;">md5/sha256</font><font style="color:#333333;">来进行通信秘钥的</font><font style="color:#ff0000;">对称加密</font><font style="color:#333333;">比对计算。</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1671525447035-73dc5da2-d2f5-48dc-ae9c-829240e3067e.png)







#### 五、demo落地
具体见文档[BFF项目初始化](https://www.yuque.com/u25370234/kb/xm445rbobi0onlsg)。



#### 六、相关地址
##### 1、贾维斯
[https://jarvis.myscrm.cn/m/application/service-governance/service/baseInfo?node_id=25&namespace_code=default](https://jarvis.myscrm.cn/m/application/service-governance/service/baseInfo?node_id=25&namespace_code=default)



##### 2、Mars
[https://mars.myscrm.cn/branches-new?filter_token=9e96ec3327ea48de900c06ab66b4c27b&oid=1](https://mars.myscrm.cn/branches-new?filter_token=9e96ec3327ea48de900c06ab66b4c27b&oid=1)



##### 3、Apollo
[https://apollo-test-kefu.myscrm.cn/config.html?#/appid=bff-kefu-demo](https://apollo-test-kefu.myscrm.cn/config.html?#/appid=bff-kefu-demo)

****

##### 4、MiddleMan
[https://api.myscrm.cn/project/17734/interface/api/master](https://api.myscrm.cn/project/17734/interface/api/master)



##### 5、公共组接口文档
[https://console.apipost.cn/project/0d45f491-3369-481e-9a8e-ed264fb46f3a/lately](https://console.apipost.cn/project/0d45f491-3369-481e-9a8e-ed264fb46f3a/lately)









****

