## 管道与重定向

```bash
# 文件被打开两次, 且stderr会覆盖之前的stdout
command > a 2> a
# 文件只被打开一次
command > a 2>&1

# 将stdout输出到/dev/null, 再将stderr重定向到stdout, stderr和stdout都会写入/dev/null
# &1中的&可以理解为引用
command > /dev/null 2>&1
# 将stderr重定向到stdout, 即输出到显示屏, 再将stdout输出到/dev/null
command 2>&1 > /dev/null

# 比如
nohup python /path/to/python/main.py 2&1 > /dev/null &
```

## 下载

- wget

```
wget --no-check-certificate --content-disposition https://github.com/ctripcorp/apollo/releases/download/v1.5.1/apollo-adminservice-1.5.1-github.zip
```

- curl

```
curl -LJO https://github.com/ctripcorp/apollo/releases/download/v1.5.1/apollo-adminservice-1.5.1-github.zip
```

## visudo

修改用户权限

```bash
visudo /etc/sudoers
```

```
# 允许root用户执行任意路径下的任意命令
root ALL=(ALL) ALL
# 允许wheel用户组中用户执行任意命令
%wheel ALL=(ALL) ALL
%wheel ALL=(ALL) NOPASSWD : ALL
```

## update-alternatives

`update-alternatives` 维护系统命令链接符的工具, 可以对某个工具的多个软件版本进行管理, 通过它可以很方便的设置系统默认使用哪个命令的哪个软件版本.

`sudo update-alternatives --config vim`

## systemctl

`systemctl --> service + chkconfig`

|功能|old|new|
|:-----:|:-----:|:-----:|
|某服务自启动(关闭)|chkconfig --level 3 httpd on(off)|systemctl enable(disable) httpd.service|
|检查服务状态|service httpd status|systemctl status httpd.service|
|显示所有已启动服务|chkconfig --list|systemctl list-units --type=service|
|启动服务|service httpd start|systemctl start httpd.service|

## netstat

`::ffff:69.72.177.140:80`: `::ffff:` is the IPv6 prefix for an IPv4 address mapped into IPv6 space. It means that it is an IPv6 socket that is used for IPv4.

## 链接动态库

`ldd` 命令

* 法一

临时有效: `export LD_LIBRARY_PATH=路径`

* 法二

链接动态链接库是由动态链接器决定的. 动态链接器首先在 LD_LIBRARY_PATH 中查找, 然后在 /etc/ld.so.cache 中查找, 在 root 权限下, 用 ldconfig 读取 /etc/ld.so.conf 文件并生成缓存文件, 如果还找不到就在系统默认路径中查找, 先在 /usr/lib 再在 /lib 中查找. 则可以将库路经写在 /etc/ld.so.conf 文件中, 然后 ldconfig.

* 法三

将库文件复制进 /usr/lib 或 /lib中.

## about device info

＊ cpuinfo and meminfo

物理 cpu 个数
```bash
cat /proc/cpuinfo | grep 'physical id' | sort | uniq | wc -l
```

每个物理 cpu 核数
```bash
cat /proc/cpuinfo|grep 'cpu cores'|uniq
```

逻辑 cpu 个数
```bash
cat /proc/cpuinfo|grep 'processor'|wc -l
```

内存信息
```bash
cat /proc/meminfo

free -mh
```

## 通信相关

查看端口占用
```bash
lsof -i:<port>
```
## 查看发行版

```bash
lsb_release -a

cat /etc/centos-release(redhat-release)
cat /etc/issue
cat /proc/verion
```

## 抓包

```bash
tcpdump -i ens160 port 8800 and host 172.73.160.100 >> tcpdump_result.pcap
tcpdump -s 0 -v -i any -w test_server.pcap port 8800 or 5060 or 5061 or 5062 or 5063
```

## kill
```bash
ps -ef | grep rtprecv | grep -v grep | awk '{print $2}' | xargs kill -9
# OR
killall -9 rtprecv
```

## tar 分卷解压缩

```bash
tar -zcf - filename | split -b xxx - outfilename.tar.gz
# xxx是你想要的每个包的大小，只输入数字默认单位是byte
# 输入数字+K，单位是KB
# 输入数字+M，单位是MB
# 输入数字+G，单位是GB

cat outfilename.tar.gz.* | tar -zx
```

## 自动挂载

```bash
fdisk -l                         # 查看可挂载磁盘
df -h                            # 查看已经挂载磁盘
mount /dev/sdb1 /run/media/u01
sudo blkid                       # 查看磁盘属性和UUID
vim /etc/fstab
UUID=*************  /u01  ext4  defaults  1  1
```

## QnA

> 目录软链接时注意带 '/' 和不带 '/' 的区别？

带 / 删除的是目标目录下的文件，目标目录和软连接依然存在；不带 / 删除的是软连接本身。

> ssh 连接问题？

ssh-keygen -f "/home/gdd/.ssh/known_hosts" -R "[192.168.1.11]:9022"

## awk head tail

![awk_head_tail](./pics/awk_head_tail.png)

`cat img_list.txt | tail -n +10001 | head -n 10000 | awk -F '[/.]' '{print $NF}'`

## 挂载

- 挂载远程

```
sudo apt install nfs-common

sudo mount -t nfs4 -o soft 192.168.1.66:/volume1/gddi-nas /mnt/gddi-nas
sudo umount /mnt/gddi-nas
```

## system and kernel

```shell
# 系统架构 x86_64, arm64, aarch
arch
# 内核版本
cat /proc/version
uname -a
# 系统版本
cat /etc/issue
# 指令集
cat /proc/cpuinfo
```
