# 针对 APISIX 耗时不稳定的一个测试用例

## 背景说明
我们公司部门正在将API灰度切换到APISIX，切换了一些业务之后，收到用户方反馈切换后延时变大，导致部分请求异常。感觉不可思议，于是直接针对现网测试了下，发现确实存在抖动现象（业务正常耗时在25ms左右，但是偶尔抖动到200ms~800ms）。
为了排除网络、配置等因素，我们直接基于官方给出的`example`在本地网络环境做了类似的测试，发现也存在10倍左右振幅的抖动现象！

这里整理到github，方便官方大佬帮忙定位，整体测试说明如下：

## 用例说明
用例基于官方`example`改造：[https://github.com/apache/apisix-docker/tree/master/example](https://github.com/apache/apisix-docker/tree/master/example)，改动如下：
- 删除不需要的启动项，只保留`apisix`、`etcd`和`nginx`；
- `apisix`docker版本改为最新的`centos-2.10.2`;
- Docker改为HOST网络模式

## 测试步骤
- 启动容器：`docker-compose up -d`
- 路由配置：`cd test && bash init.sh`
- 启动测试：
    - 测试通过APISIX代理NGINX(2 upstreams)：`python start_test.py`
    - 直接测试后端Nginx(1upstream)：`python start_test_upstream.py`
## 结果预览
- 机器环境：4核8G centos 7.2
- 测试结果：

### 测试通过APISIX代理NGINX(2 upstreams)
```
[root@centos ~/apisix-latency-test/test]# ./start_test.py 
cost: 12ms
cost: 11ms
cost: 13ms
cost: 11ms
cost: 13ms
cost: 22ms
cost: 13ms
cost: 15ms
cost: 14ms
cost: 13ms
cost: 11ms
cost: 13ms
cost: 17ms
cost: 12ms
Latency stats:
0ms: 9750
0~2ms: 181
5~10ms: 25
2~5ms: 22
>10ms: 21
[root@centos ~/apisix-latency-test/test]# ./start_test.py 
cost: 13ms
cost: 11ms
cost: 12ms
cost: 15ms
cost: 11ms
cost: 11ms
cost: 11ms
cost: 11ms
cost: 13ms
cost: 14ms
cost: 14ms
cost: 11ms
cost: 13ms
cost: 13ms
cost: 12ms
Latency stats:
0ms: 9726
0~2ms: 191
2~5ms: 32
5~10ms: 28
>10ms: 22
```

### 直接测试后端Nginx(1upstream)
```
[root@centos ~/apisix-latency-test/test]# ./start_test_upstream.py 
Latency stats:
0ms: 9979
2~5ms: 11
0~2ms: 8
5~10ms: 1
>10ms: 0
[root@centos ~/apisix-latency-test/test]# ./start_test_upstream.py 
Latency stats:
0ms: 9970
0~2ms: 22
2~5ms: 4
5~10ms: 3
>10ms: 0
```

## 抓包分析
抓包命令：`tcpdump -iany -nn port 9080 or port 8000 or port 8001 -vvv -w start_test.cap`
分析截图：
![image](https://user-images.githubusercontent.com/9711651/143400924-e2c560bb-d2b8-4894-a0ea-4c60cedd8385.png)
很明显后端Nginx耗时0.04ms，而APISIX耗时14ms。

## 初步结论
整个测试完全在本地完成，网络损耗可以忽略不计，但是从结果来看`APISIX`的耗时不是特别稳定，存在较大波动的现象，希望官方可以帮忙定位下问题出在哪，非常感谢！
