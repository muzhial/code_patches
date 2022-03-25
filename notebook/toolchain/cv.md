## opencv编译

### ubuntu下

* GCC 4.4.x or later
* CMake 2.8.7 or higher
* Git
* GTK+2.x or higher, including headers (libgtk2.0-dev)
* pkg-config
* Python 2.6 or later and Numpy 1.5 or later with developer packages (python-dev, python-numpy)
* ffmpeg or libav development packages: libavcodec-dev, libavformat-dev, libswscale-dev
* [optional] libtbb2 libtbb-dev
* [optional] libdc1394 2.x
* [optional] libjpeg-dev, libpng-dev, libtiff-dev, libjasper-dev, libdc1394-22-dev
* [optional] CUDA Toolkit 6.5 or higher

```
[编译器] sudo apt-get install build-essential
[必备] sudo apt-get install cmake git
[必备] sudo apt-get install libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
[可选] sudo apt-get install python3-dev python3-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
```

#### 安装

```
cd opencv
mkdir build
cd build
```

用 `cmake` 生成 `makefile`:
```
#编译成release版本，安装路径/usr/local/
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
```

由于 ubuntu18.04 预装 python3, 所以系统里有两个版本的 python, cmake 的时候默认是给 python2 编译, 所以需要把 python3 设为默认, 并关闭为 python2 的编译, 启动为 python3 的库编译:
```
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 -D BUILD_opencv_python3=ON -D BUILD_opencv_python2=OFF ..
```
cmake 完成后输出信息, 无误则可进行 make, 如果 python 不是默认安装的可通过可选选项配置正确路径. 也可以通过 cmake-gui 来进行配置, 各种选项比较清楚.

```
make -j4
sudo make install
```

`export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig`

查看 opencv 版本: `pkg-config --modversion opencv`

### Mac OS

```
$ brew install cmake pkg-config
$ brew install jpeg libpng libtiff openexr
$ brew install eigen tbb
```

*zipimport.ZipImportError: can't decompress data; zlib not available*  --> 问题

```
CFLAGS="-I$(xcrun --show-sdk-path)/usr/include" pyenv install -v 3.6.7

export LDFLAGS=-L/usr/local/opt/zlib/lib
export CPPFLAGS=-I/usr/local/opt/zlib/include
```

*tcl-tk*

```
brew install tcl-tk

For compilers to find tcl-tk you may need to set:
  export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
  export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"

For pkg-config to find tcl-tk you may need to set:
  export PKG_CONFIG_PATH="/usr/local/opt/tcl-tk/lib/pkgconfig"

$ tclsh
$ info patch

```

`export LDFLAGS="-L/usr/local/opt/tcl-tk/lib -L/usr/local/opt/zlib/lib -L/usr/local/opt/sqlite/lib"`

`export CPPFLAGS="-I/usr/local/opt/tcl-tk/include -I/usr/local/opt/zlib/include -I/usr/local/opt/sqlite/include"`

`export LDFLAGS="-L/usr/local/opt/zlib/lib"`

`export CPPFLAGS="-I/usr/local/opt/zlib/include"`
```
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local -DPYTHON_DEFAULT_EXECUTABLE=/Users/muzhi/.pyenv/shims/python -DBUILD_opencv_python2=ON -DBUILD_opencv_python3=OFF -DPYTHON3_EXECUTABLE=/Users/muzhi/.pyenv/shims/python -DPYTHON_LIBRARY= ..
```

```
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D PYTHON3_LIBRARY=`python -c 'import subprocess ; import sys ; s = subprocess.check_output("python-config --configdir", shell=True).decode("utf-8").strip() ; (M, m) = sys.version_info[:2] ; print("{}/libpython{}.{}.dylib".format(s, M, m))'` \
    -D PYTHON3_INCLUDE_DIR=`python -c 'import distutils.sysconfig as s; print(s.get_python_inc())'` \
    -D PYTHON3_EXECUTABLE=$VIRTUAL_ENV/bin/python \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D BUILD_EXAMPLES=ON ..
```
标准版
```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D PYTHON3_LIBRARY=`python3 -c 'import subprocess ; import sys ; s = subprocess.check_output("python3-config --configdir", shell=True).decode("utf-8").strip() ; (M, m) = sys.version_info[:2] ; print("{}/libpython{}.{}.dylib".format(s, M, m))'` \
    -D PYTHON3_INCLUDE_DIR=`python3 -c 'import distutils.sysconfig as s; print(s.get_python_inc())'` \
    -D PYTHON3_EXECUTABLE=/usr/local/bin/python3 \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON ..
```

For compilers to find sqlite you may need to set:
  export LDFLAGS="-L/usr/local/opt/sqlite/lib"
  export CPPFLAGS="-I/usr/local/opt/sqlite/include"

For pkg-config to find sqlite you may need to set:
  export PKG_CONFIG_PATH="/usr/local/opt/sqlite/lib/pkgconfig"
