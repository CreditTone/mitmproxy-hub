import re
import sys
import grpc
import base64
import mitm_hub_pb2
import mitm_hub_pb2_grpc
import threading
from mitmproxy import proxy, options
from mitmproxy.script import concurrent
from mitmproxy import flowfilter
from mitmproxy import ctx, http

class MitmproxyFlower:
    
    def __init__(self,callbackServerAddr,callbackServerPort,mitmproxyId):
        self.callbackServerAddr = callbackServerAddr
        self.callbackServerPort = callbackServerPort
        self.mitmproxyId = mitmproxyId;
        if callbackServerAddr and callbackServerPort:
            notifyServerAddr = callbackServerAddr + ":"+ str(callbackServerPort)
            channel = grpc.insecure_channel(notifyServerAddr)
            self.grpcClient = mitm_hub_pb2_grpc.MitmProxyHubClientServerStub(channel=channel)
            print("callback grpc client >>> ", notifyServerAddr, "\nmitmproxyId >>> ", mitmproxyId)
        else:
            print("no callback info.")
             
    def createMitmRequest(self, req:http.HTTPRequest):
        mitmHeaders = []
        headersMap = dict(req.headers)
        for (k,v) in  headersMap.items():
            mitmHeader = mitm_hub_pb2.MitmHeader(name=k, value=v)
            mitmHeaders.append(mitmHeader)
            mitmRequest = mitm_hub_pb2.MitmRequest(url=req.url, method=req.method, headers=mitmHeaders, content=req.content, mitmproxyId=self.mitmproxyId)
        return mitmRequest

    def request(self, flow: http.HTTPFlow) -> None:
        if not self.grpcClient:
            return
        req:http.HTTPRequest = flow.request
        mitmRequest = self.createMitmRequest(req)
        fixedMitmRequest = self.grpcClient.onMitmRequest(mitmRequest)
        req.url = fixedMitmRequest.url
        req.method = fixedMitmRequest.method
        
        fixedHeadersKeys = set()
        for fixedHeader in fixedMitmRequest.headers:
            fixedHeadersKeys.add(fixedHeader.name)
            req.headers[fixedHeader.name] = fixedHeader.value
        
        #get removedHeadersKeys
        originalHeadersKeys = set(req.headers.keys())
        removedHeadersKeys = originalHeadersKeys - fixedHeadersKeys
        #delete request header key
        for removedHeadersKey in removedHeadersKeys:
            del req.headers[removedHeadersKey]
            
        if fixedMitmRequest.content != mitmRequest.content:
            req.content = fixedMitmRequest.content
            #修改请求体
    
    def response(self, flow: http.HTTPFlow) -> None:
        if not self.grpcClient:
            return
        req:http.HTTPRequest = flow.request
        res:http.HTTPResponse = flow.response
        mitmRequest = self.createMitmRequest(req)
        mitmHeaders = []
        headersMap = dict(res.headers)
        for (k,v) in  headersMap.items():
            mitmHeader = mitm_hub_pb2.MitmHeader(name=k, value=v)
            mitmHeaders.append(mitmHeader)
            mitmResponse = mitm_hub_pb2.MitmResponse(request=mitmRequest, headers=mitmHeaders, content=res.content, statusCode=res.status_code, mitmproxyId=self.mitmproxyId)
        
        fixedMitmResponse = self.grpcClient.onMitmResponse(mitmResponse)
        
        fixedResponseHeadersKeys = set()
        for fixedHeader in fixedMitmResponse.headers:
            res.headers[fixedHeader.name] = fixedHeader.value
            fixedResponseHeadersKeys.add(fixedHeader.name)
        
            
        originalResponseHeadersKeys = set(res.headers.keys())
        removedResponseHeadersKeys = originalResponseHeadersKeys - fixedResponseHeadersKeys
        #delete response header key
        for removedHeadersKey in removedResponseHeadersKeys:
            del res.headers[removedHeadersKey]
        
        res.content = fixedMitmResponse.content
        res.status_code = fixedMitmResponse.statusCode
    
