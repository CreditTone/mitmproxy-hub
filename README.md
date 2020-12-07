# 欢迎使用mitmproxy-hub

mitmproxy非常适合捕捉网络流量，但是对于Java用户没有简单的接口。软件测试社区，特别是爬虫、中间人攻击测试人员，希望能够捕获设备在Java测试期间发出的网络请求。

为此,基于grpc开发了mitmproxy的中央服务，任何语言都可以基于mitm_hub.proto实现的回调定义生成自己的远程客户端代码。以便在你的语言环境上也能像在python本地一样，使用remotemitmproxy。

### 推荐环境
```
Mitmproxy: 5.3.0
Python:    3.6.8
OpenSSL:   OpenSSL 1.1.1h  22 Sep 2020
Platform:  Darwin-20.1.0-x86_64-i386-64bit
```

### 安装mitmproxy
```
pip3 install mitmproxy
```

### 下载项目
```
git clone xxx
```

### 启动mitmproxy-hub
```
python3 server.py
```