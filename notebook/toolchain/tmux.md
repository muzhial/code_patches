
## tmux

### 安装

依赖安装:

```bash
yum -y install ncurses-devel
yum -y install libevent-devel
yum -y install tmux
rpm -qa | grep libevent
```

### 使用

快捷键前缀: `Ctrl-b`

tmux 显示说明:

* 左下侧: tmux 会话名
* 中下侧: tmux 当前会话中的窗口
* 右下侧: 当前的日期

### 会话(Session)

一个会话中可以包含多个窗口(Window), 为一个特定项目创建一个 Tmux 会话, 在终端运行: `tmux new -s <name-of-my-session>`

在此基础上, 需要为另一个项目创建新会话, 则需要先按下快捷键前缀(`Ctrl-b`), 然后输入: `new -s <name-of-my-new-session>`

*除非显式地关闭会话, 否则 Tmux 的会话在重启计算机之前都不会消失, 可以在会话之间自由切换*

获取现有会话列表: `Ctrl-b s`, 按下相应会话 id 进入该会话

### 窗口(Window)

窗口是窗格的容器, 若要创建一个窗口, 只需要按下 `Ctrl-b c`; 若要切换窗口, 只需要先按下`Ctrl-b`, 然后再按下想切换的窗口所对应的数字, 该数字会紧挨着窗口的名字显示.

### 窗格(Pane)

创建一个竖直放置的窗格: 开启一个 Tmux 会话之后, 再按下 `Ctrl-b %`, 水平方向分割，按下 `Ctrl-b "`. 在 Tmux 的窗格间移动光标: 先按下 Tmux 的快捷键前缀, 然后再按下对应的方向键进入目标窗格.

### 操作

`tmux new -s name-of-session` 创建一个会话, 查看创建所得的会话: `tmux ls`. 登录一个会话(从终端进入会话): `tmux a(attach) -t name-of-existed-session`. 在某个会话中 `Ctrl-b d` 会退出该会话, 但不会关闭; `Ctrl-d` 将退出并关闭会话.

在终端下销毁会话: `tmux kill-session -t name-of-session`

**重命名会话**

重命名会话: `tmux rename -t old-name-of-session new-name-of-session`

* 快捷键：`<C-b> $`
* `<C-b> :` 进入指令模式，输入：`rename-session [-t current-name] [new-name]`

**重命名窗口**

* 快捷键：`<C-b> ,`
* `<C-b> :` 进入指令模式，输入：`rename-window [-t current-name] [new-name]`

快捷键列表:

|快捷键|功能|
|:------:|:------:|
|d|脱离当前会话, 暂时回到shell界面, attach返回会话|
|s|选择并切换会话|

|快捷键|功能|
|:-----:|:-----:|
|c|创建新窗口|
|&|关闭当前窗口|
|数字|切换到指定窗口|
|p|切换至上一窗口|
|n|切换至下一窗口|
|l|在前后两个窗口间切换|
|,|重命名当前窗口|
|w|通过窗口列表切换窗口|

|快捷键|功能|
|:-----:|:-----:|
|"|将当前面板分为上下|
|%|将当前面板分为左右|
|x|关闭当前面板|
|Ctrl+方向键|以一个单元格大小调整面板大小|
|Alt+方向键|以五个单元格大小调整面板大小|
|方向键|选择切换面板|

复制模式(copy-mode)，`前缀 [` 进入 copy-mode，按 `space` 开始复制，移动光标选择复制区域，按 `Enter` 复制并退出 copy-mode，将光标移到指定位置，按 `前缀 [` 粘贴。

### 配置文件

`~/.tmux.conf` or `/etc/tmux.conf`

然后可以输入如下命令使 conf 生效：进入 tmux 的命令模式，`source-file ~/.tmux.conf`。
```
## set shortcut as vi mode in copy-mode
setw -g mode-keys vi
## setw == set-window-option
## mouse support turn on in Window/Pane
set-window-option -g mode-mouse on
setw -g mouse-resize-pane on
setw -g mouse-select-pane on
setw -g mouse-select-window on
## 禁止 rename window
set-option -g allow-rename off
set -g status-keys vi
set -g history-limit 10000
```
