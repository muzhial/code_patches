#!/bin/bash

# 在bash shell中, $()与``(反引号)都是用来做命令替换(command substitution)的

######
# 1
######
dir=$(ls -l ~/Downloads/caffe-master/src/caffe/layers | awk '/^-/ {print $NF}')
for i in $dir
do
   echo $i
done

#####
# 2
# 比较两个目录下文件名不重复的
#####
dir1=~/Downloads/caffe-master/src/caffe/layers
dir2=~/SourceCode/Colorize_Greyscale/colorization/caffe_private_pascal/src/caffe/layers
find "$dir1/" "$dir2/" -printf '%P\n' | sort | uniq -u

#####
# 3
# 分卷压缩
#####
tar -zcf - filename | split -b 45M - outfilename.tar.gz

cat outfilename.tar.gz* | tar -zx

#####
# 4
# sslocal 启动
#####
# sed 's/".*\.kingss.me"/"server": "jp.kingss.me"/' fuck_gfw.json > fuck_gfwa.json
# fuck_gfw.sh sf4 start/restart

rm -f fuck_gfw.json
echo "{" >> fuck_gfw.json
echo "    \"server\": \"$1.kingss.me\"," >> fuck_gfw.json
echo '    "server_port": 36296,' >> fuck_gfw.json
echo '    "local_port": 1080,' >> fuck_gfw.json
echo '    "password": "muzhi4_95",' >> fuck_gfw.json
echo '    "timeout": 600,' >> fuck_gfw.json
echo '    "method": "aes-256-cfb"' >> fuck_gfw.json
echo "}" >> fuck_gfw.json

cat fuck_gfw.json | tail -n +2 | head -n 1

if [ "$2" == "start" ]; then
    echo "vi6.174" | sudo -S sslocal -c fuck_gfw.json -d start
    echo "start done!"
elif [ "$2" == "restart" ]; then
    echo "vi6.174" | sudo -S sslocal -c fuck_gfw.json -d restart
    echo "restart done!"
fi

#######
# 5
# xargs and wget
#######
for i in `seq 0 499`
do
    echo https://s3.amazonaws.com/google-landmark/train/images_$(printf "%03d" $i).tar >> url_list_train.txt
done

for i in `seq 0 99`
do
    echo https://s3.amazonaws.com/google-landmark/index/images_$(printf "%03d" $i).tar >> url_list_index19.txt
done

for i in `seq 0 19`
do
    echo https://s3.amazonaws.com/google-landmark/test/images_$(printf "%03d" $i).tar >> url_list_test19.txt
done

for split in "train" "index19" "test19"
do
    xargs -a url_list_${split}.txt -L 1 -P $WORKERS wget -c --tries=0
    ls -1 | grep tar | xargs -IXXX -P $WORKERS tar -xvf XXX -C ../input/${split}
    # ls -1 | grep tar | xargs -L 1 -P $WORKERS rm
done

#######
# 6
# expect
# must install `expect` first
# then run: expect some_shell_file
#######

#!/bin/expect
set timeout 100
set passwd "Gree@bdc123456!"
spawn ssh root@10.0.20.164
expect "root"
send "$passwd\n"
interact


################################################
# 7
# 批量杀死进程
################################################
ps -ef|grep gunicorn|awk '{print $2}'|xargs kill -9
