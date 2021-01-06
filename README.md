# 一个能让任何语言使用mitmproxy的方法 mitmproxy-hub

我们都知道mitmproxy非常适合捕捉网络流量，但是对于其他语言上用户没有配套的接口。软件测试社区，特别是爬虫、中间人攻击测试人员，希望能够捕获设备在Java/golang/c++测试期间发出的网络请求。

为此,我想出一套通用的解决方案。基于grpc开发了mitmproxy的中央服务，任何语言都可以基于mitm_hub.proto实现的回调定义生成自己的远程客户端代码。以便在你的语言环境上也能像在python本地一样，使用remotemitmproxy。

### 原理介绍
[mitmproxy-hub](https://github.com/CreditTone/mitmproxy-hub "mitmproxy-hub")定义了其他任何语言可以生成的proto3序列化代码，借助于grpc高效的跨进程通信。使得其他语言可以对mitmproxy内部的流量进行无死角的监控。

![mitmproxy-hub架构图](https://opensourcefile.oss-cn-beijing.aliyuncs.com/mitmproxy-hub.png "mitmproxy-hub架构图")

### 推荐环境
```
Mitmproxy: 5.3.0
Python:    3.6.8
OpenSSL:   OpenSSL 1.1.1h  22 Sep 2020
Platform:  Darwin-20.1.0-x86_64-i386-64bit
```

### 安装mitmproxy
```
pip3 install mitmproxy==5.3.0
```

### 启动mitmproxy-hub
```
python3 server.py
```

### 基于mitmproxy-hub proto生成的java版mitmproxy-java
```
https://github.com/CreditTone/mitmproxy-java
```