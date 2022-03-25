## nginx with rtmp module

`brew info nginx-full` 可输出

```
Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

Run port 80:
 $ sudo chown root:wheel /usr/local/opt/nginx-full/bin/nginx
 $ sudo chmod u+s /usr/local/opt/nginx-full/bin/nginx
Reload config:
 $ nginx -s reload
Reopen Logfile:
 $ nginx -s reopen
Stop process:
 $ nginx -s stop
Waiting on exit process
 $ nginx -s quit

To have launchd start denji/nginx/nginx-full now and restart at login:
  brew services start denji/nginx/nginx-full
Or, if you don't want/need a background service you can just run:
  nginx
```

`lsof -i tcp:8080`

## mac 命令行读写 ntfs

```bash
diskutil list
LABEL=muzhi none ntfs rw,auto,nobrowse
cd /Volumes
ls
open .

# 弹出
diskutil unmountdisk /dev/disk2
```

有人反映在 fstab 中添加这一行 “LABEL=TOSHIBA none ntfs rw,auto,nobrowse” 有时候会不管用，硬盘不仅不在桌面上显示，而且依然没有写权限，给出了方法，说直接使用硬盘的 UUID，我试了一下，可用，将方法一并放到这里，一共有两步：

* 查询硬盘的UUID

```bash
# 打开terminal, 输入：
diskutil info /Volumes/TOSHIBA
```

会出现包含 UUID 信息的一大段输出，其中，`Volume UUID: B83735C0-40A9-478B-9689-FD98941041C3`，这一行的B83735C0-40A9-478B-9689-FD98941041C3 就是硬盘 TOSHIBA 的 UUID，下面会用到。

* 在 fstab 中添加配置文字

```bash
# 特别注意，逗号“，”后面没有空格
UUID=B83735C0-40A9-478B-9689-FD98941041C3 none ntfs rw,auto,nobrowse
```

* 推出硬盘，重新插入，发现桌面上没有硬盘图标，进入 terminal:

```bash
cd /Volumes/
ls
# 就可以看到TOSHIBA了
# 可以用ln -s命令在桌面上创建TOSHIBA的软链接：
mkdir -p ~/Desktop/toshiba       # 在桌面上创建目录toshiba
ln -s /Volumes/TOSHIBA ~/Desktop/toshiba
# 然后我们就可以在桌面上直接访问TOSHIBA硬盘了。
```

## MacOS 下 tkinter 配置

* [参考](https://github.com/pyenv/pyenv/issues/1375)

## pyenv

```
export CPPFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix bzip2)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include"

export LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib -L$(xcrun --show-sdk-path)/usr/lib"
```

```
brew install zlib
export LDFLAGS="-L/usr/local/opt/zlib/lib"
export CPPFLAGS="-I/usr/local/opt/zlib/include"
pyenv install 3.7.9
```
