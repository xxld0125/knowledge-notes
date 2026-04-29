#### 一、什么是RPC
<font style="color:rgb(77, 77, 77);">RPC是Remote Procedure Call的简称，中文叫远程过程调用。</font>

<font style="color:rgb(77, 77, 77);">简单来说，就是我在本地调用了一个函数，或者对象的方法，实际上是调用了远程机器上的函数，或者远程对象的方法，但是这个通信过程对于程序员来说是透明的，即达到了一种位置上的透明性。</font>**<font style="color:rgb(77, 77, 77);">RPC是一种技术思想而非一种规范</font>**<font style="color:rgb(77, 77, 77);">。协议只规定了 Client 与 Server 之间的点对点调用流程，包括 stub、通信协议、RPC 消息解析等部分，在实际应用中，还需要考虑服务的高可用、负载均衡等问题。</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1668498146931-bf8dd98b-1fd5-452f-8695-73fbb79aa3d0.png)

<font style="color:rgb(77, 77, 77);">说的白话一点，可以这么理解：现在有两台服务器A和B。部署在A服务器上的应用，想调用部署在B服务器上的另一个应用提供的方法，由于不在一个内存空间，不能直接调用，需要通过网络来达到调用的效果。</font>



**RPC优点:**

<font style="color:rgb(77, 77, 77);">RPC主要用于公司内部的服务调用。</font>

<font style="color:rgb(77, 77, 77);">性能消耗低、传输效率高、服务治理方便。</font>



**一句话概括：****<font style="color:rgb(51, 51, 51);">RPC描述了如何使用远程对象或方法就像在本地一样。</font>**

####   
二、什么是gRPC
**<font style="color:rgb(51, 51, 51);">gRPC 是一个高性能、开源和通用的 RPC 框架</font>**<font style="color:rgb(51, 51, 51);">，面向移动和 HTTP/2 设计，提供多语言支持。</font>

<font style="color:rgb(51, 51, 51);">gRPC 基于 HTTP/2 标准设计，带来诸如双向流、流控、头部压缩、单 TCP 连接上的多复用请求等特性。这些特性使得其在移动设备上表现更好，更省电和节省空间占用。</font>

<font style="color:rgb(51, 51, 51);">gRPC使用protocol buffers作为其接口定义语言（IDL）和其基础消息交换格式。</font>

<font style="color:rgb(51, 51, 51);">与许多RPC系统一样，gRPC基于定义服务的思想，指定可以使用其参数和返回类型远程调用的方法。 在服务器端，服务器实现此接口并运行gRPC服务器来处理客户端调用。 在客户端，客户端有一个存根（在某些语言中称为客户端），它提供与服务器相同的方法。 protocol buffers 用于数据序列化。如下定义了person的结构。</font>

<font style="color:rgb(51, 51, 51);"></font>

<font style="color:rgb(51, 51, 51);">gRPC调用过程：</font>

![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1668497899593-ad43e198-3ddf-4ffe-864b-e86507608503.png)

  
<font style="color:rgb(77, 77, 77);">	从上图和文档中可以看出，用gRPC来进行远程调用服务，客户端(client) 仅仅需要gRPC Stub ，通过Proto Request向gRPC Server发起服务调用，然后 gRPC Server通过Proto Response(s)将调用结果返回给调用的client。</font>

  




