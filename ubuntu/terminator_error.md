<!--
 * @Author: lexcalibur
 * @Date: 2021-12-08 15:30:37
 * @LastEditors: lexcaliburr
 * @LastEditTime: 2021-12-08 15:32:45
-->

见如下错误
```
xxxx@xxxx:~$ /usr/bin/terminator
  File "/usr/bin/terminator", line 123
    except (KeyError,ValueError), ex:
```

原因  
terminator使用的是python2，但是当把ubuntu的默认python改为python3时，会报上述错误

修正，启动程序改为调用python2
```sh
#/usr/bin/python -> #/usr/bin/python2
```