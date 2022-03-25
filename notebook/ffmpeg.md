## 基础知识

**序列化**

程序运行中，变量皆在内存中，将变量从内存中转为可传输或可存储的过程为序列化。python 中为 pickling，其他语言为 serialization, marshalling，flattening。序列化后的内容写入磁盘，或通过网络传输到别的机器。

**视频编码**

帧内编码(I帧)，帧间编码(B，P帧)

帧间编码：

* 帧间预测(时间冗余) --> 视频序列的相邻图像之间的内容相似性
* 变换(空间冗余) --> 相邻像素的相关性
* 量化(视觉冗余，有损压缩) --> 肉眼对某些视觉细节不敏感
* 熵编码(编码冗余) --> 不同像素值出现的概率不同

**I，P，B帧**

I 帧：关键帧，一帧画面完整保留，解码时只需本帧。压缩率约为 7(~= JPG)。

P 帧：记录本帧与上一帧(I帧或者P帧)的差别，解码时用之前缓存的画面叠加本帧定义的差别，生成最终帧画面。压缩率约为 20。

B 帧：记录本帧与前后帧(I帧或P帧)的区别，B 帧压缩率高，但解码比较耗 CPU 资源。压缩率约为 50。所以可使用 B 帧可节省大量空间以保存 I 帧，这样在相同码率下，画质更好。

如果视频流只有 I 帧或 P 帧，则解码时无需管后面的数据，边读边解，线性行进。B 帧不仅需要读取之前帧数据，还需读取下一帧画面。如果 B 帧丢掉，并用之前帧画面重复，即会造成画面卡顿(丢帧了)。

**音频**

音频采样率：每秒采集多少次，8000，16000，32000，44100，48000。

**压缩方法**

分组：将几帧图像(帧数不宜过多)分为一组(GOP)；每组内定义 I，P，B 三种类型(定义帧)；以 I 帧为基础帧，以 I 帧预测 P，再 I 和 P 预测 B；最后将 I 帧的数据与预测的差值信息进行存储和传输。

(stream --> frame --> package)

**编码与封装**

```
 _______              ______________
|       |            |              |
| input |  demuxer   | encoded data |   decoder
| file  | ---------> | packets      | -----+
|_______|            |______________|      |
                                           v
                                       _________
                                      |         |
                                      | decoded |
                                      | frames  |
                                      |_________|
 ________             ______________       |
|        |           |              |      |
| output | <-------- | encoded data | <----+
| file   |   muxer   | packets      |   encoder
|________|           |______________|
```

编码针对的是未压缩的 YUV 原始数据

封装：媒体的容器，容器即为(1)将编码器生成的多媒体内容(视频，音频，字幕，章节等信息)混合封装在一起的标准。(2)为多媒体内容提供索引，没有容器则只能从前到后，无法进度条拖拽，没有封装可能需要手动载入音频。

常见封装格式：

* AVI，.mov，MPEG 格式(.mpg，.mpeg，.mpe，.dat，.vob，.asf，.3gp，.mp4)
* WMV 格式(.rm，.rmvb)
* flash video 格式(.flv)  .mkv
* MPEG2-TS 格式(.ts)传输流
在流媒体中，尤其直播中常使用 FLV，MPEG2-TS，分别用于 RTMP/HTTP-FLV 和 HLS 协议。

**时间同步**

* DTS(decoding time stamp) 解码时间戳，告诉播放器何时解码这帧数据
* PTS(presentation time stamp) 显示时间戳，告诉播放器何时显示这帧数据

DTS 和 PTS 用于指导播放端行为，但它们是在编码时由编码器生成。音频也有 DTS 和 PTS，但两者通常一致。

示例：

```
DTS:    1   2   3   4
PTS:    1   4   2   3
stream  I   P   B   B
显示顺序 IBBP
```

这时这几帧在视频流中的顺序为 IPBB，这时便体现 PTS 和 DTS 的作用。

当没有 B 帧时，DTS 和 PTS 通常一致。

**ffmpeg时间计算**

`av_rescale_rnd(int64_t a, int64_t b, int64_t c, enum AVRounding rnd)` 计算 `a*b/c`，a 为要换算的值，b 为原来的时间基，c 为要转换的时间基，并分 5 种方式对计算结果取整。

* `static double av_q2d(AVRational a) --> (a.num/a.den)`，根据 pts 计算一帧在整个视频中的时间位置：`timestamp=pts*av_q2d(st->time_base)`。其中 st 为 `AVStream` 对象指针。

**结合实例**

现有 mp4 文件，流信息为：`duration: 90s, 24fps  24tbr  48tbn  48tbc`，其中 `tbr`(time base of rate)帧率，`tbn`(time base of stream)视频流时间基，`tbc`(time base of codec)视频解码时间基。

调试结果其 pts 输出为：0，2，4，6，8，...。都是偶数的原因为帧率为 24，即 `2=48/24`，故某一帧在视频流中的时间位置：`timestamp=6/48`，调试输出 `duration` 为 4320，即真实视频长度为 `4320/48=90s`。如果需要进行时间基转换为 `{1, 1000}` 则为 `2*((1/48)/(1/1000))=41.6667~=42, 4*((1/48)/(1/1000))=83.33~=83, 6*((1/48)/(1/1000))=125`


**command lines**

* rtsp to rtmp: `ffmpeg -rtsp_transport tcp -i <input> -r 15 -s 1920x1080 -f flv -an rtmp://ip/av001`

**附件**

* rtmp rtsp hls 协议优趣点和特点
* 流媒体服务器(七牛，reds，FMS，crtmpserver)

## nginx配置示例

```
rtmp {
    server {
        listen 1935;
        chunk_size 4096;
        application rtmplive {
            live on;
            max_connections 1024;
        }

        application hls {
            #allow play all;
            live on;
            hls on;
            hls_path html/hls;
            hls_fragment 2s;
            hls_playlist_length 10s;
        }
    }
}
http {
    ... other config ...

    server {
        listen 8181;
        server_name 10.2.11.244;
        location /hls {
            type {
                #application/vnd.apple.mpegurl m3u8;
                application/x-mpegURL;
                video/mp2t ts;
            }
            root html;
            add_header Cache-Control no-cache;
            add_header Access-Control-Allow-Credentials true;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods GET,POST;
            add_header Access-Control_Allow-Headers X-Requested-with;
        }
    }

    server {
        listen 8282;
        server_name 10.2.11.244;
        location / {
            root html/dist;
            index index.html;
            try_files $uri $uri/ /index.html;
            add_header Cache-Control no-cache;
            add_header Access-Control-Allow-Credentials true;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods GET,POST;
            add_header Access-Control_Allow-Headers X-Requested-with;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root html;
        }
    }
}
```

该配置场景为前端 vue 编译的静态资源位于 `html/dist`，hls 协议的分片 ts 将位于 `html/hls`，8282 的前端服务中将调用 8181 端口指向的 hls 的 ts 资源。

假如 A(172.18.250.2:6713) 上部署着视频服务，B(10.3.0.179) 上部署 vue hls 前端服务或者 flask hls 服务，B 可以访问 A 服务器，而访问 B 前端服务的机器无法访问 A，即与 A 网络不通，使用反响代理进行解决。

一个反向代理的例子：

```
server {
    listen 8686;
    server_name 10.3.0.179;
    location / {
        proxy_pass http://127.0.0.1:8080;
        add_header Cache-Control no-cache;
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control_Allow-Headers X-Requested-with;
    }
}
```

B 中的前端服务中无法通过 `http://172.18.250.2:6713` 获取 A 的视频资源，故可以作如下配置后，可通过 `http://10.3.0.179:6713` 间接获取 A 的视频资源：

```
server {
    listen 6713;
    server_name 10.3.0.179;
    location / {
        proxy_pass http://172.18.250.2:6713;
    }
}
```

## ffmpeg推流

`ffmpeg -i wtf.ts -map 0 -c copy -ignore_unknown -f segment -segment_list "F:\Program Files\nginx-rtmp-win32-dev\html\hls\out.m3u8" -segment_time 30 "F:\Program Files\nginx-rtmp-win32-dev\html\hls\out%03d.ts"`

从文件进行推流和从流地址推，区别很多：

```
// rtmp --> hls
// success: rtmp://localhost:1935/hls/test    fail: http://localhost:8181/hls/test.m3u8
ffmpeg -re -i rtmp://10.2.5.89/rtoh/K1208618N-SX -c copy -f flv rtmp://localhost:1935/hls/test (成功，但还是rtmp流)
// push stream failed
ffmpeg -re -i rtmp://10.2.5.89/rtoh/K1208618N-SX -c copy -f hls rtmp://localhost:1935/hls/test (失败)

// rtmp --> hls
// success: access by http://localhost:8181/hls/test.m3u8
ffmpeg -re -i rtmp://10.2.5.89/rtoh/K1208618N-SX -c copy \
                                                 -flags -global_header \
                                                 -hls_time 2 \
                                                 -hls_list_size 6 \
                                                 -hls_wrap 10 \
                                                 "F:\Program Files\nginx-rtmp-win32-dev\html\hls\test.m3u8"
```


## ffmpeg sdk C/C++
```
ffmpeg -i test.mp4 -c copy -f flv rtmp://192.168.1.107/rtoh/test
ffplay rtmp://192.168.1.107/rtoh/test -fflags nobuffer

gcc test.c -o test -lavformat -lavcodec -lswscale -lswresample -lavutil -lm –lz

gcc encoder.c -o encoder  -I../my_ffmpeg/include/ -L../my_ffmpeg/lib/ -lavformat -lavcodec -lswscale -lavutil -lavfilter –lavdevice
```

## ref
* [rtsp and rtmp github](https://github.com/xiongziliang/ZLMediaKit)
* [rtsp to rtmp](https://www.stephenwagner.com/2016/11/10/rtsp-to-rtmp-ip-camera-to-youtube-live-streaming/), [rtsp2rtmp](http://www.voidcn.com/article/p-nkndgdhg-bev.html)
* [centos build ffmpeg from src](https://www.jianshu.com/p/a3c52c7c68eb), [another](https://trac.ffmpeg.org/wiki/CompilationGuide/Centos)
* [ffmpeg-encoding-course](http://slhck.info/ffmpeg-encoding-course/#/)
* [Nginx反代m3u8资源加速HLS流媒体](https://www.vpsdp.net/nginxs-reverse-proxy-hls/)
* [Nginx正向代理与反向代理](https://www.jianshu.com/p/ae76c223c6ef)
* https://juejin.im/post/5bacbd395188255c8d0fd4b2
* [Nginx正向代理配置](http://twei.site/2017/07/28/Nginx%E6%AD%A3%E5%90%91%E4%BB%A3%E7%90%86%E9%85%8D%E7%BD%AE/)
* [nginx代理实现内网主机访问公网服务](https://www.cnblogs.com/saneri/p/8390845.html)
* [Nginx Rtmp Module - HLS切片和级联播放](https://blog.csdn.net/liwf616/article/details/77886991)
* http://www.williammalone.com/articles/create-html5-canvas-javascript-drawing-app/
