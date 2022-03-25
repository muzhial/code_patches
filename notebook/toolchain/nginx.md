## nginx

### 常规配置

`conf.d/vhost.conf`

```
#server
#{
#    listen 80;
#    server_name www.kantchen.top;
#    location / {
#        proxy_redirect off;
#        proxy_set_header Host $host;
#        proxy_set_header X-Real-IP $remote_addr;
#        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#        proxy_pass http://www.kantchen.top:3000;
#    }
#    access_log /var/log/nginx/www.kantchen.top_access.log;
#}

server
{
    listen 9002;
    server_name 120.27.104.101;
    location / {
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:2368;
    }
    access_log /var/log/nginx/ghost_selfblog_access.log;
}
```

### 视频推流配置

```
worker_processes  auto;
events {
    worker_connections  1024;
}

# RTMP configuration
rtmp {
    server {
        listen 1935; # Listen on standard RTMP port
        chunk_size 4000;

        application show {
            live on;
            # Turn on HLS
            hls on;
            hls_path /mnt/hls/;
            hls_fragment 3;
            hls_playlist_length 60;
            # disable consuming the stream from nginx as rtmp
            deny play all;
        }
    }
}

http {
    sendfile off;
    tcp_nopush on;
    aio on;
    directio 512;
    default_type application/octet-stream;

    server {
        listen 8080;

        location / {
            # Disable cache
            add_header 'Cache-Control' 'no-cache';

            # CORS setup
            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Expose-Headers' 'Content-Length';

            # allow CORS preflight requests
            if ($request_method = 'OPTIONS') {
                add_header 'Access-Control-Allow-Origin' '*';
                add_header 'Access-Control-Max-Age' 1728000;
                add_header 'Content-Type' 'text/plain charset=UTF-8';
                add_header 'Content-Length' 0;
                return 204;
            }

            types {
                application/dash+xml mpd;
                application/vnd.apple.mpegurl m3u8;
                video/mp2t ts;
            }

            root /mnt/;
        }
    }
}
```

另一种配置

```
worker_processes  auto;

events {
    worker_connections  1024;
}

## HLS server streaming
rtmp {
    server {
        listen 1935; # Listen on standard RTMP port
        chunk_size 4000;
        application live{
            live on;
            deny play all;
            push rtmp://localhost/show;
            on_publish http://localhost:3001/auth;
            on_publish_done http://localhost:3001/done;
        }
        application show {
            live on;
            # Turn on HLS
            hls on;
            hls_nested on;
            hls_fragment_naming system;
            hls_path /Users/toan/Sites/mnt/hls/;
            hls_fragment 3;
            hls_playlist_length 60;

            # disable consuming the stream from nginx as rtmp
            deny play all;
        }
    }
}
#end hls server stream

http {
    sendfile off;
    tcp_nopush on;
    #aio on;
    directio 512;
    default_type application/octet-stream;

    server {
        listen       80;
        server_name  localhost;
        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }
    }

    server {
        listen 8080;

        location /hls {
            # Disable cache
            add_header Cache-Control no-cache;

            # CORS setup
            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Expose-Headers' 'Content-Length';

            # allow CORS preflight requests
            if ($request_method = 'OPTIONS') {
                add_header 'Access-Control-Allow-Origin' '*';
                add_header 'Access-Control-Max-Age' 1728000;
                add_header 'Content-Type' 'text/plain charset=UTF-8';
                add_header 'Content-Length' 0;
                return 204;
            }

            types {
                application/vnd.apple.mpegurl m3u8;
                video/mp2t ts;
            }

            root /Users/toan/Sites/mnt/;
        }
    }
}
```

有效的经过验证的配置

```
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;

events {
    worker_connections  1024;
}

rtmp {
    server {
        listen 1935;
        chunk_size 4096;

        application rtoh {
            live on;
            hls on;
            hls_path /mnt/hls;
 	    hls_fragment 1s;
        }
    }
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;
        #server_name 10.2.5.89;

        #charset koi8-r;
	    root /mnt/;
        #access_log  logs/host.access.log  main;
        location / {
            #root   html;
            index  index.html index.htm;
            add_header Cache-Control no-cache;
            add_header Access-Control-Allow-Credentials true;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods GET,POST;
            add_header Access-Control_Allow-Headers X-Requested-with;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }

    server {
        listen 8888;
        server_name 10.2.5.89;

        location /socket.io/ {
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_pass "http://127.0.0.1:5000/socket.io/";
        }

        location /{
            proxy_pass http://127.0.0.1:5000;
            add_header Cache-Control no-cache;
            add_header Access-Control-Allow-Origin *;
            client_max_body_size 5m;
        }
    }

    server {
        listen 8899;
        server_name localhost;

        location /socket.io/ {
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_pass "http://127.0.0.1:5050/socket.io/";
        }

        location / {
                proxy_pass http://127.0.0.1:5050;
                add_header Cache-Control no-cache;
                add_header Access-Control-Allow-Origin *;
            }
    }

    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}
}
```

### 缩略图配置

官方 nginx docker 通过 `nginx -V` 查看配置，输出可能无 `ngx_http_image_filter_module`，但在 `/etc/nginx/modules` 下可找到。故配置为：

`/etc/nginx/nginx.conf`

```
user nginx;
worker_processes 1;
# load ngx_http_image_filter_module
# at the top level! That is where daemon, user, http are defined.
load_module modules/ngx_http_image_filter_module.so;

http {
    ......
}
```
`/etc/nginx/conf.d/some.conf`
```
server {
    listen 80;
    server_name localhost;

    # if image save path: /usr/share/nginx/html/images/*.jpg
    root /usr/share/nginx/html;
    location /images {
        #expires 7d;
        gzip_static on;
        add_header Cache-Control public;
        add_header X-Pownered "nginx_image_filter";
        # HTTP Response Header 增加 proxy_cache 的命中状态，以便于以后调试，检查问题
        add_header X-Cache-Status $upstream_cache_status;
        proxy_pass http://127.0.0.1/_img/uploads;
        # 将缩略图缓存在服务，避免每次请求都重新生成
        proxy_cache uploads_thumb;
        # 当收到 HTTP Header Pragma: no-cache 的时候，忽略 proxy_cache
        # 此配置能让浏览器强制刷新的时候，忽略 proxy_cache 重新生成缩略图
        proxy_cache_bypass $http_pragma;
        # 由于 Upload 文件一般都没参数的，所以至今用 host + document_uri 作为
        proxy_cache_key "$host$document_uri";
        # 有效的文件，在服务器缓存 7 天
        proxy_cache_valid 200 7d;
        proxy_cache_use_stale error timeout invalid_header updating;
        proxy_cache_revalidate on;
        # 处理 proxy 的 error
        proxy_intercept_errors on;
        error_page   415 = /assets/415.png;
        error_page   404 = /assets/404.png;
    }

    # 原始图片
    location /_img/uploads {
        alias /usr/share/nginx/html/images/$filename;
        expires 7d;
    }

    # 缩略图
    location ~* /_img/uploads/(.+)!(large|lg|md|sm|xs)$ {
        set $filename /uploads/$1;

        if (-f $filename) {
            break;
        }

        # 根据 URL 地址 ! 后面的图片版本来准备好需要的参数（宽度、高度、裁剪或缩放）
        set $img_version $2;
        set $img_type resize;
        set $img_w    -;
        set $img_h    -;
        if ($img_version = 'large') {
            set $img_type resize;
            set $img_w    1920;
        }
        if ($img_version = 'lg') {
            set $img_type crop;
            set $img_w    192;
            set $img_h    192;
        }
        if ($img_version = 'md') {
            set $img_type crop;
            set $img_w    96;
            set $img_h    96;
        }
        if ($img_version = 'sm') {
            set $img_type crop;
            set $img_w    48;
            set $img_h    48;
        }
        if ($img_version = 'xs') {
            set $img_type crop;
            set $img_w    32;
            set $img_h    32;
        }
        rewrite ^ /_$img_type;
    }

    # 缩放图片的处理
    location /_resize {
        alias /usr/share/nginx/html/images$filename;
        image_filter resize $img_w $img_h;
        image_filter_jpeg_quality 95;
        image_filter_buffer         20M;
        image_filter_interlace      on;
    }

    # 裁剪图片的处理
    location /_crop {
        alias /usr/share/nginx/html/images$filename;
        image_filter crop $img_w $img_h;
        image_filter_jpeg_quality 95;
        image_filter_buffer         20M;
        image_filter_interlace      on;
    }
    }
}
```
**参考**

* https://ruby-china.org/topics/31498
* https://www.cnblogs.com/freeweb/p/5764493.html
* https://learnku.com/articles/21870



## nginx视频推流

### nginx编译安装

#### 1. nginx rtmp依赖

`sudo apt-get install build-essential libpcre3 libpcre3-dev libssl-dev`

#### 2. nginx和nginx-rtmp-module

下载源码: `git clone https://github.com/arut/nginx-rtmp-module.git`

下载 [nginx](http://nginx.org/en/download.html) 源码, 进入到解压后的 nginx 主目录

```
./configure --prefix=/usr/local/nginx --add-module=/path/to/nginx-rtmp-module --with-http_ssl_module --with-debug

make

sudo make install
```

### 启动与问题

#### 1. 启动

`/usr/local/nginx/sbin/nginx -t`

`/usr/local/nginx/sbin/nginx`

`/usr/local/nginx/sbin/nginx -t && nginx -s reload`

`/usr/local/nginx/sbin/nginx -s stop`

`nginx -c conf/nginx.conf`

#### 2. Pushing live stream to nginx using rtmp

nginx accepts rtmp stream as input. For a proper HLS stream the video codec should be `x264` and audio codec `aac/mp3/ac3` most commonly being `aac`

1. From existing rtmp stream already in h264

if you have an existing rtmp stream in the correct codec, you can skip ffmpeg and tell nginx to pull the stream directly. In order to do so add a pull directive under application section in nginx.conf like so

```
application show {
    live on;
    pull rtmp://example.com:4567/sports/channel3 live=1;
    # to change the local stream name use this syntax: ... live=1 name=ch3;

    # other directives...
    # hls_...
}
```

### 参考

[1](https://docs.peer5.com/guides/setting-up-hls-live-streaming-server-using-nginx/)
[2](https://hackernoon.com/build-live-video-streaming-server-use-ffmpeg-nginx-rtmp-module-nodejs-82e1bb58949e)
[3](https://cxuef.github.io/linux/%E3%80%90%E7%BD%AE%E9%A1%B6%E3%80%91%E6%90%AD%E5%BB%BAnginx-rtmp%E7%9B%B4%E6%92%AD%E6%9C%8D%E5%8A%A1%E5%99%A8%EF%BC%8Cffmpeg%E6%A8%A1%E6%8B%9F%E6%8E%A8%E6%B5%81/)
