## 基本概念
```
|---------------|         |---------------|
| docker client1|         | docker client1|
|---------------|         |---------------|
      \                          /
       \                        /
    |------------------------------|
    |        docker守护进程         |
    |           /     \            |  ==》 docker主机
    |         容器    容器          |
    |------------------------------|
```
* 镜像：用户基于镜像运行自己的容器，是基于联合文件系统的层式结构
* registry：保存用户构建的镜像
* 容器：将应用程序或服务打包进容器

docker 基于 C/S 架构设计，docker 命令是在客户端通过 REST API 与 docker 引擎交互，而 Dockerfile 中的 `RUN` 等命令其实是在服务端，而非本地构建，所以引入上下文

当构建的时候，用户会指定构建镜像上下文的路径，docker build 命令得知这个路径后，会将路径下的所有内容打包，然后上传给 Docker 引擎。这样 Docker 引擎收到这个上下文包后，展开就会获得构建镜像所需的一切文件。

如果在 Dockerfile 中这么写：`COPY ./package.json /app/`。这并不是要复制执行 docker build 命令所在的目录下的 package.json，也不是复制 Dockerfile 所在目录下的 package.json，而是复制 上下文(context)目录下的 package.json。

因此，COPY 这类指令中的源文件的路径都是相对路径。这也是初学者经常会问的为什么 COPY ../package.json /app 或者 COPY /opt/xxxx /app 无法工作的原因，因为这些路径已经超出了上下文的范围，Docker 引擎无法获得这些位置的文件。如果真的需要那些文件，应该将它们复制到上下文目录中去。

```
$ docker build -t nginx:v3 .
Sending build context to Docker daemon 2.048 kB
```
现在就可以理解刚才的命令 `docker build -t nginx:v3 .` 中的这个 `.`，实际上是在指定上下文的目录，docker build 命令会将该目录下的内容打包交给 Docker 引擎以帮助构建镜像。

有些初学者在发现 COPY /opt/xxxx /app 不工作后，于是干脆将 Dockerfile 放到了硬盘根目录去构建，结果发现 docker build执行后，在发送一个几十 GB 的东西，极为缓慢而且很容易构建失败。那是因为这种做法是在让 docker build 打包整个硬盘，这显然是使用错误。一般来说，应该会将 Dockerfile 置于一个空目录下，或者项目根目录下。如果该目录下没有所需文件，那么应该把所需文件复制一份过来。如果目录下有些东西确实不希望构建时传给 Docker 引擎，那么可以用 `.gitignore` 一样的语法写一个 `.dockerignore`，该文件是用于剔除不需要作为上下文传递给 Docker 引擎的。

在默认情况下，如果不额外指定 Dockerfile 的话，会将上下文目录下的名为 Dockerfile 的文件作为 Dockerfile。这只是默认行为，实际上 Dockerfile 的文件名并不要求必须为 Dockerfile，而且并不要求必须位于上下文目录中，比如可以用 `-f ../Dockerfile.php` 参数指定某个文件作为 Dockerfile。一般习惯性的会使用默认的文件名 Dockerfile，以及会将其置于镜像构建上下文目录中。

**[tips]** 镜像是 docker 生命周期中的构建和打包阶段，容器是启动或执行阶段

## 使用

* `docker info` or `docker inspect [container]`

显示 docker 系统信息，包括镜像和容器数

* `docker version`

显示版本信息

* `docker images [options] [repository[:tag]]`

列出本地镜像
```
docker images -a     列出本地所有镜像
docker images ubuntu 列出本地所有镜像中 repository 为 ubuntu 的镜像
```

* `docker ps [options]`

```
-a    列出所有容器，包括运行和停止的
-l    最后一次运行的容器，正在运行和停止的
```

* `docker search [OPTIONS] TERM`

```
docker search -s 10 mysql    从 docker hub 中查找所有镜像名包含 mysql 并且收藏数大于 10 的镜像
```

* `docker start/stop/restart [OPTIONS] CONTAINER [CONTAINER...]`

启动/停止/重启一个或多个容器，后跟容器名或者容器id

* `docker attach [OPTIONS] CONTAINER`

要 attach 上去的容器必须正在运行，可以同时连接上同一个container来共享屏幕(与screen命令的attach类似)

* `docker exec [OPTIONS] CONTAINER COMMAND [ARG...]`

在运行的容器中执行命令，在容器内额外启动新进程，在容器内有后台任务和交互式任务两种，后台任务运行无交互需求，交互式任务则保持在前台运行。

`-t -i` --> 为执行的进程创建 TTY 并捕捉 STDIN。

```
-d  分离模式: 在后台运行
-i  即使没有附加也保持 STDIN 打开
-t  分配一个伪终端
```

* `docker port CONTAINER`

* `docker rm [OPTIONS] CONTAINER [CONTAINER...]`

如：docker rm -f db01 db02

```
-f  通过SIGKILL信号强制删除一个运行中的容器
-v  删除与容器关联的卷
-l  移除容器间的网络连接，而非容器本身
```

* `docker rmi [OPTIONS] IMAGE [IMAGE...]`

```
-f  强制删除
--no-prune  不移除该镜像的过程镜像，默认移除
```

删除本地所有镜像：`docker rmi $(docker images -a -q)`

删除所有容器，先得停止所有容器：`docker stop $(docker ps -aq)`

删除所有停止容器：`docker container prune`

删除 untagged images：`docker rmi $(docker images | grep "^<none>" | awk "{print $3}")`

* `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

创建一个新的容器并运行一个命令，Docker会在隔离的容器中运行进程，当运行 docker run 命令时，Docker会启动一个进程，并为这个进程分配其独占的文件系统、网络资源和以此进程为根进程的进程组。在容器启动时，镜像可能已经定义了要运行的二进制文件、暴露的网络端口等，但是用户可以通过docker run命令重新定义(docker run可以控制一个容器运行时的行为，它可以覆盖docker build在构建镜像时的一些默认配置)

```
-a stdin   指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项
-d         后台运行容器，并返回容器ID
-i         以交互模式运行容器，通常与 -t 同时使用，允许你对容器内的标准输入 (STDIN) 进行交互
-t         为容器重新分配一个伪输入终端，通常与 -i 同时，使用在新容器内指定一个伪终端或终端
-P         随机端口映射，容器内部端口随机映射到主机的高端口
-p         指定端口映射，格式为：主机(宿主)端口:容器端口
--name="niubi" or --name niubi   为容器指定名字否则随机分配，命名必须唯一
--dns 8.8.8.8  指定容器的 DNS 服务器，默认同于宿主机
-h "mars"      指定容器的hostname
-e username="ritchie"   设置环境变量
--env-file=[]           从指定文件读入环境变量
--cpuset="0-2" or --cpuset="0,1,2"   绑定容器到指定CPU运行
-m       设置容器使用内存最大值
--net="bridge"      指定容器的网络连接类型，支持 bridge/host/none/container 四种类型
--link=[]           添加链接到另一个容器
--expose=[]         开放一个端口或一组端口
```

`docker run -i -t --name test centos:latest /bin/bash` --> docker 首先检测本地是否存在 centos:latest 镜像，没有则从官方维护的 Docker Hub 中下载。`exit` or `CTRL + D` 退出容器，容器将停止运行。该命令会进入到容器中。退出后，使用 `docker start test` 返回容器名，再使用 `docker attach test` 进入容器(终端)

启动容器设置工作目录，或者启动容器多条 command：

`docker run -it -w /root/flask -p 5000:5000 -v /root/docker_src/flask:/root/flask -d --name app centos:v1 /bin/bash`

`docker run -it -p 5000:5000 -v /root/docker_src/flask:/root/flask -d --name app centos:v1 /bin/sh -c "cd /root/flask; python3.6 run.py"`

* 删除中间镜像

在执行 `docker build` 时，会产生 `<none>` 中间镜像，`docker images -a` 可以看到。

删除命令：
```
sudo docker rmi $(sudo docker images --filter dangling=true -q)
```
或者：
```
sudo docker ps -a | grep "Exited" | awk '{print $1 }'|xargs sudo docker stop
sudo docker ps -a | grep "Exited" | awk '{print $1 }'|xargs sudo docker rm
sudo docker images|grep none|awk '{print $3 }'|xargs sudo docker rmi
```

* 删除虚浮镜像

除了 docker pull 可能导致这种情况，docker build 也同样可以导致这种现象。由于新旧镜像同名，旧镜像名称被取消，从而出现仓库名、标签均为 <none> 的镜像。这类无标签镜像也被称为 虚悬镜像(dangling image) ，可以用下面的命令专门显示这类镜像，删除虚浮镜像的命令：`docker image prune`

## 镜像操作

* 镜像导入导出

```
docker save IMAGE_ID > IMAGE.tar

docker load < IMAGE.tar
```

* 镜像合并

参考此文 [链接](http://dockone.io/article/527)

## 容器管理

### 自动重启容器

"sh -c" 命令，它可以让 bash 将一个字串作为完整的命令来执行。

`docker run --restart=always --name daemon_dave_restart -d centos:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"`

```
--restart    该标志设置为 always，则无论容器退出码为何，皆会自动重启该容器
--restart=on-failure:5     当容器退出码为非 0 时，自动重启，另外其还接受一个可选的重启次数参数
```

## docker commit 方式创建镜像

先创建容器，再在容器中做修改，修改完成退出容器，`docker commit -m "desc" CONTAINER IMAGE`

## Dockerfile 方式


## nginx 部署/图片服务器

`mkdir -p ~/nginx/www ~/nginx/logs ~/nginx/conf` 在宿主机上执行

`docker cp nginx-test:/etc/nginx/nginx.conf ~/nginx/conf` 拷贝容器内 Nginx 默认配置文件到本地当前目录下的 conf 目录

`docker run -d -p 9091:80 --name nginx-test -v ~/Docker/nginx/www:/usr/share/nginx/html -v ~/Docker/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v ~/Docker/nginx/logs:/var/log/nginx nginx`

默认挂载的路径权限为读写。如果指定为只读可以用：ro `-v ~/Docker/nginx/www:/usr/share/nginx/html:ro`

`cd ~/nginx/www`  创建 index.html

`docker kill -s HUP container-name`

`docker restart container-name`

## 使用示例

### mmdetection

```bash
sudo docker run -it -p 8022:22 -p 8090:8888 --shm-size='32767m' --env PATH=/opt/conda/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --gpus all --name mmdet-mz-test2 -v /home/ubuntu/mz/data:/data gdgdgd/mz:v1.0 bash
```

### vscode 远程连接 docker container

以下操作在容器中：

```bash
apt install -y openssh-server

mkdir /var/run/sshd
# echo 'root:passwd' | chpasswd
echo 'root:muzhi' | chpasswd
# 注意取消注释
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
echo "export VISIBLE=now" >> /etc/profile
```

## QnA

> ERROR: Unexpected bus error encountered in worker. This might be caused by insufficient shared memory (shm)

出现这个错误的情况是，在服务器上的docker中运行训练代码时，batch size设置得过大，shared memory不够（因为docker限制了shm）。解决方法是，将Dataloader的num_workers设置为0。

## some example

### muzhiv1.0

**muzhi:v1.0**

`curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey > gpgkey`

```
ARG PYTORCH="1.6.0"
ARG CUDA="10.1"
ARG CUDNN="7"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0+PTX"
ENV TORCH_NVCC_FLAGS="-Xfatbin -compress-all"
ENV CMAKE_PREFIX_PATH="$(dirname $(which conda))/../"

COPY gpgkey .
RUN cat gpgkey | apt-key add -
RUN apt-get update --allow-insecure-repositories \
  && apt-get install -y git ninja-build libglib2.0-0 \
  libsm6 libxrender-dev libxext6 zip unzip cmake \
  openssh-server libgl1-mesa-glx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN conda clean --all

RUN pip install mmcv-full==latest+torch1.6.0+cu101 -f https://download.openmmlab.com/mmcv/dist/index.html
WORKDIR /
```

### mmseg deploy dockerfile

```
# deploy
FROM mm-muzhi:v1.0

COPY ssh-10 /root/.ssh
WORKDIR /

# RUN pip install onnx onnx-simplifier
RUN GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" git clone git@gitlab.gddi.com:muzhi/mmseg.git

WORKDIR /mmseg
RUN pip install -e .
docker build --no-cache -f mmseg-dockerfile -t hub.gddi.com/nw_mirrors/mmseg:v0.0.10-mmseg .
```

### ssh 密码设置

vs code 远程设置

```
apt install -y openssh-server

mkdir /var/run/sshd
# echo 'root:muzhi' | chpasswd
echo 'root:muzhi' | chpasswd
# 注意取消注释
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

echo "export VISIBLE=now" >> /etc/profile
```

### docker 示例

```bash
docker run -it -p 9122:22 --shm-size='32767m' --ipc=host --name mz-seg-mobile -v /mnt:/mnt:ro mm-muzhi:v1.0 bash

docker run -it -p 8122:22 --shm-size='32767m' --name mz-face-recg -v /mnt:/mnt:ro 075708 bash

docker run -it -p 10022:22 --gpus all --name mz-tensorrt -v /home/ubuntu/muzhi/Code/TensorRT/:/workspace/TensorRT -v /home/ubuntu/muzhi/Code/TensorRT-7.1.3.4:/tensorrt -v /mnt:/mnt:ro tensorrt-ubuntu:latest
```
