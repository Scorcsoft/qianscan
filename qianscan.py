#coding=utf-8

##################################################################################################################
#    ____                                                                                                        #
#   /    \    ___     ___      ___   ___     ____    ___     ___     |                                           #
#   |____    /   \   /   \   |/     /   \   /       /   \   |     ---|---                                        #
#        |  |       |     |  |     |        -----  |     |  |---     |                                           #
#    ____/   \___/   \___/   |      \___/   ____/   \___/   |        |__/                                        #
#                                                                           Scorcsoft.com | 天蝎软件 2018-10-04  #
##################################################################################################################

import sys
import getopt
import requests
import threading

EXIT = False
DICT = []
DOMAIN = ''
HEADER = []
OUTPUT = []
STATUS = []
THREAD = 1
OUTPUT_FILE = ''
NEVER_STOP = False
TIMEOUT_QUANTITY = 0
HELP_INFO = '''usage: python dirscan.py domain [OPTIONS]

    -h: show this help information
    -d: dictionary file
    -t: number of threads
    -i: set request headers
    -o: save the result to output file
    -s: http status code

    more help information: https://github.com/scorcsoft/qianscan

output: [url]   [http status code]'''

def help():
    print(HELP_INFO)
    exit()

def loadDict(file):
    print("\033[1;34m[*]\033[0m Loading the dictionary file into memory, please wait...")
    try:
        n = 0
        for i in open(file):
            i = i.strip("\r\n") # for Linux
            i = i.strip("\n") # for bugdows
            if i:
                DICT.append(i)
                n += 1
        print("\033[1;32m[+]\033[0m loading completed. %d dictionary"%(n))
    except:
        print("\n\033[1;31m[!]\033[0m Cant open the dictionary file: %s"%(file))
        exit()

def setRequestHeader(file):
    try:
        for i in open(file):
            tmp = i.split(":")
            HEADER[tmp[0].string("\n")] = tmp[1].strip("\n")
            #此处比较草率，当自定义header只有key，没有value时此处会出现数组下标越界，所以按理说应判断tmp长度。但是现在是2018年10月4日凌晨04:55， 我真的好困。。。就这样写吧，都一样。
    except:
        print("\n\033[1;31m[!]\033[0m Cant open the request header file: %s"%(file))
        exit()

def saveResult():
    file = open(OUTPUT_FILE,"w")
    for i in OUTPUT:
        file.write("%s\n"%(i))
    file.close()
    print("\033[1;32m[+]\033[0m Result has been saved to file: %s"%(OUTPUT_FILE))

class aThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global EXIT
        global NEVER_STOP
        global TIMEOUT_QUANTITY
        while DICT:
            if lock.acquire():
                if DICT:
                    string = DICT.pop()
                    lock.release()
                    url = "%s%s"%(DOMAIN,string)
                    try:
                        h = requests.get(url=url,headers=HEADER,timeout=2)
                        if h.status_code == 200:
                            if lock.acquire():
                                print("%s   \033[1;32m200\033[0m"%(url))
                                if OUTPUT_FILE:
                                    OUTPUT.append(url)
                                lock.release()
                        if STATUS:
                            if lock.acquire():
                                print("%s   \033[1;32m200\033[0m"%(url))
                                if OUTPUT_FILE:
                                    OUTPUT.append(url)
                                lock.release()
                    except:
                        TIMEOUT_QUANTITY += 1
                        if lock.acquire():
                            if TIMEOUT_QUANTITY > 50 and NEVER_STOP == False:
                                if DICT:
                                    d = raw_input("\033[1;31m[!]\033[0m It has timeout 50 times here, Keep scanning?[y/n] > ")
                                    if d == 'y':
                                        NEVER_STOP = True
                                        lock.release()
                                        continue
                                    else:
                                        EXIT = True
                                        print("\033[1;31m[!]\033[0m Scan stop, Too many timeout error.")
                                        del DICT[:]
                            lock.release()
                else:
                    lock.release()                 

arg = getopt.getopt(sys.argv[2:],'-h-d:-t:-i:-o:-s:',[])
dirFile = 'data/default.list'
for opt_n,opt_v in arg[0]:
    if opt_n == "-h":
        help()
    if opt_n == "-d":
        dirFile = opt_v
    if opt_n == "-t":
        THREAD = int(opt_v)
    if opt_n == "-i":
        setRequestHeader(opt_v)
    if opt_n == "-o":
        OUTPUT_FILE = opt_v
    if opt_n == "-s":
        for i in opt_v.split(","):
            STATUS.append(int(i))
        if 200 in STATUS:
            STATUS.remove(200)

if len(sys.argv) < 2 or sys.argv[1] == "-h":
    help()
DOMAIN = sys.argv[1]
'''
try:
    h = requests.get(url=DOMAIN,headers=HEADER,timeout=3)
except:
    print("\033[1;31m[!]\033[0m Cant open the website: %s, check your network"%(DOMAIN))
    exit()
'''
loadDict(dirFile)

print("\033[1;34m[*]\033[0m Starting. Threads: %s"%(THREAD))
threadList = []
lock = threading.Lock()
for i in range(THREAD):
    t = aThread()
    threadList.append(t)
for t in threadList:
    t.start()
for t in threadList:
    t.join()

if EXIT == False:
    print("\033[1;32m[+]\033[0m Scan completed")
if OUTPUT_FILE:
    saveResult()
