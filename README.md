script
======

## inoffice.py
出勤记录工具

```
$ inoffice.py --help
usage: inoffice.py [-h] [-m MEMO [MEMO ...]] [-s DATE [DATE ...]] [-o]
                   [-M MONTH] [--fill START END]

出勤记录工具。不带参数运行会进行打卡。

options:
  -h, --help          show this help message and exit
  -m MEMO [MEMO ...]  记录备注
  -s DATE [DATE ...]  记录指定日期的时间
  -o                  导出当月 Excel
  -M MONTH            导出指定月份的 Excel
  --fill START END    填充所有未记录的工作日时间
```

### 使用示例
```
export MYNAME=xxx
inoffice.py
inoffice.py -s 3 3 9:30 18:30
inoffice.py -s 3 10 10:20 19:00
inoffice.py -s 3 13 11:00 19:00
inoffice.py -m 電車乗り間違い -s 3 10
inoffice.py -m 電車乗り間違い -s 3 13
inoffice.py --fill 9:40 18:40
inoffice.py -o
```

### 备注
* 可以看一下脚本文件头部的全局变量定义，尤其是`DATA_FILE`这个路径
* 节假日用的日本的，可以自己改成其他节日库



