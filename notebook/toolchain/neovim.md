
## neovim

补全插件 `ncm2` 等可能需要：
```
pip install pynvim
pip install neovim
```

可能需要配置 `clang` 路径，配置 `python` 路径

以下查看系统剪贴板的支持情况：
```
:echo has('clipboard')
```
不支持试着安装 `yum install xsel`

## vim 使用

> word --> 以非空白字符分割的单词

> WORD --> 以空白字符分割的单词

```
文本对象
   相比于对单个字符的操作，可以对单词、句子、段落等更大范围文本对象执行操作。
   [number]<command>[text object or motion]

   iw --> inner word
   aw --> around word
   e.g.
      viw / ciw / daw
```

### Insert 模式

|快捷键      |备注                        |
|:----------|:--------------------------|
|Ctrl-h     |  删除上一字符(Terminal适用)  |
|Ctrl-w     |  删除上一单词(Terminal适用)  |
|Ctrl-u     |  删除当前行(Terminal适用)    |
|Ctrl-[     |  insert -> normal         |

### Normal 模式

|快捷键              |备注|
|:------------------|:----------------|
|w/W                |  移动到下一个 word/WORD 开头|
|e/E                |  移动到下一个 word/WORD 尾部|
|b/B                |  移动到上一个 word/WORD 开头|
|\*/#               |  当前单词的前向/后向匹配|
|%                  |  跳转到括号匹配|
|Ctrl-d[own] (u[p])  |  下(上)翻半页|
|Ctrl-f[orward]     |  上翻整页|
|Ctrl-b[ackward]    |  下翻整页|
|Ctrl-r             |  恢复撤销|
|u                  |  撤销|
|"ayy               |  yy 到 a 寄存器|
|"ap                |  a 寄存器 p 到当前位置|
|"+                 |  系统剪贴板|
|""                 |  无名剪贴板|
|\<C-p>/\<C-n>      |  单词补全|
|\<C-x> \<C-f>      |  补全文件名|
|\<C-x> \<C-o>      |  代码补全，可能需要安装相关插件|

### 移动

**1. 行内搜索移动(Normal)**

* `f{char}` 快速移动到字符 `{char}` 上；如果匹配到多个，用 `;` (下一个)，`,` (上一个)。
* 屏幕移动(Normal)
    * `H/M/L` 跳转到屏幕开头/中间/结尾
    * `zz` 将当前行置于中间
    * `zt`，`zb` 将当前行置于屏幕上、下

### 修改

#### 1. 删除

* Normal 模式下 `dt"`, `dt)` 删除至某个字符前

#### 2. 替换

* Normal 模式下 `r{char}`，将当前字符替换为 `{char}`，依然为 Normal 模式。`R` 连续替换。
* Normal 模式下 `s`，删除当前字符并自动进入 insert 模式。
* Normal 模式下 `c`，配合文本对象使用，删除并进入 insert 模式，`C` 删除整行进入 insert 模式。
```
   ci"    将引号内的文本删除并进入插入模式
   ci{    将 { 内的文本删并进入插入模式
   di(    将 ( 内的文本删除依旧是 normal 模式
```
#### 3. 命令行查找替换

语法：`:[range] s[ubstitute]/{pattern}/{string}/[flags]`

[range] 表示范围，如：`10,20` 表示 10-20 行，`%` 表示全部。

[flags] 常用标志有：`g` 表示全剧替换，`n` 表示报告匹配到的次数而不替换，可以用来查询匹配次数。

### Buffer Window and Tab

> Buffer: 打开文件的内存缓冲区。

> Window: 是 Buffer 的可视化分割区。

> Tab: 组织窗口为一个工作区。

#### 1. Buffer

使用 `:e file` 编辑文档，默认会将当前 buffer 替换为 file 显示，不重开窗口。

`:ls` 列举当前缓冲区

`:b n` 跳转到第 n 个缓冲区；`:bpre|:bnext|:bfirst|:blast`

#### 2. Window

* `<C-w> s` or `:sp` 水平分割
* `<C-w> v` or `:vs` 垂直分割
* 窗口间移动 `<c-w> w` or `<C-w> [h/j/k/l]`

#### 3. Tab

* `:tabe[dit] {filename}` 在新标签页打开文件
* `<C-w> T` 将当前窗口移到一个新标签页
* `:tabc[lose]` 关闭当前标签页及其中所有窗口
* `:tabn[ext] {N}` or `{N}gt` 切换到编号为 {N} 的标签页
* `:tabn` or `gt` 切到下一标签页
* `:tabp[revious]` or `gT` 切换到上一标签页

### 使用宏

```
   q{register} 进行操作 q  -->  录制并退出宏
   @{register}  -->  回放宏到当前行

   全选 :normal @a  --> 回放宏到所选内容
```

### 插件操作

**nerdcommenter注释插件**
```
<leader>cc   加上注释
<leader>cu   取消注释
```

## 终端快捷键

|快捷键      |备注|
|:----------|:--------|
|Ctrl-a     | 回到行首|
|Ctrl-e     | 回到行尾|
|Ctrl-b     | 前移一|
|Ctrl-f     | 后移一|

## ERR

**1. vim E492: Not an editor command: ^M**

原因: linux 的文件换行符为 `\n`, 但 windows 却非要把 `\r\n` 作为换行符, 所以, vim 在解析从 windows 拷贝到 linux 的的 `vimrc` 时, 因为遇到无法解析的 `\r`, 所以报错.

解决: 设置 vim 配置文件的文件格式为 `unix`.

使用 `vi` 打开 `.vimrc` 文件, 输入命令 `:set fileformat=unix`
