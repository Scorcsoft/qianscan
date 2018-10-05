## qianscan
  这是用Python写的网站目录扫描器，以解决Linux上没有御剑扫描器的尴尬，效率基本能与Windows上的御剑持平，这个扫描器本来打算留到春节假期写，但是由于我白天睡太久，晚上睡不着于是就打开电脑写了。。qianscan，是以某人的名字命名的呢 233333<br>
  data目录里附带了从网络上搜集的字典文件，总计21个字典，200多万行，有PHP、JSP、asp、aspx、目录、后台、备份文件这几种字典。可根据情况自己选择合适的字典，默认字典default.list是Windows上的御剑中的字典。

## usage
  python qianscan.py domain [OPTIONS]
  
## -h
  显示帮助信息
  
## -d
  指定字典文件，例如使用1.txt作为字典：
  ```Bash
  python qianscan.py http://127.0.0.1 -d 1.txt
  ```
  如果没有-d参数，默认使用data目录中的default.list文件。
  如果你觉得我的字典太弱，你也可以用自己的目录字典替换data中的default.list，这样就不用每次都-d指定了。你也可以把字典共享到github。
  
## -t
  指定线程数，例如使用80条线程：
  ```Bash
  python qianscan.py http://127.0.0.1 -t 80
  ```
  一般情况下线程数建议85左右比较合适，默认线程数是55。
  
## -i
  指定http请求头文件：
  ```Bash
  python qianscan.py http://127.0.0.1 -i head.txt
  ```
  如果需要自定义请求头例如User Agent，你可以把请求头保存到文本文件，然后-i参数指定请求头文本文件。
  
## -o
  指定输出文件，例如将结果保存到1.txt：
  ```Bash
  python qianscan.py http://127.0.0.1 -o 1.txt
  ```
  可以把扫描结果保存到指定文件中
  
## -s
  指定其他http状态码，默认只显示200状态码的URL，如果你要显示除200之外的其他状态码的URL，可以用-s来指定。
  例如显示除了200，还显示403状态码的URL：
  ```Bash
  python qianscan.py http://127.0.0.1 -s 403
  ```
  如果有多个状态码用英文逗号分割，例如：
  ```Bash
  python qianscan.py http://127.0.0.1 -s 403,301,302
  ```

## -q
  安静模式，在扫描时，如果出现大量超时错误则会询问是否继续扫描。输入y则继续扫描直到扫完这个字典，直接按回车或输入其他任何字符则终止扫描。如果你不想被询问，可以使用-q参数，例如：
  ```Bash
  python qianscan.py http://127.0.0.1 -q
  ```

## output
  扫描到的目录会显示在终端，url后面的数字是http状态码。200状态码显示为原谅色，其他状态码显示为蓝色。

    
 bb完了。。。
