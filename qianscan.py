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
import random
import chardet
import requests
import threading

EXIT = False
DICT = []
DOMAIN = ''
HEADER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
OUTPUT = []
STATUS = []
THREAD = 55
OUTPUT_FILE = ''
NEVER_STOP = False
TIMEOUT_QUANTITY = 0
HELP_INFO = '''usage: python dirscan.py domain [OPTIONS]

    -h: show this help information
    -d: dictionary file, default: data/default.list
    -t: number of threads, default threads: 55
    -i: request headers file
    -o: save the result to output file
    -s: set other HTTP status code to print, default: 200 status code only
    -q: quiet mode, does not interact when timeout error

    more help information: https://github.com/scorcsoft/qianscan

output: [url]   [http status code]'''

def help():
    print(HELP_INFO)
    exit()

def getEncoding(file):
    fp = open(file,'rb')
    d = fp.read()
    fp.close()
    return chardet.detect(d["encoding"])

def loadDict(file):
    print("\033[1;34m[*]\033[0m Loading the dictionary file into memory, please wait...")
    try:
        n = 0
        encoding = getEncoding(file)
        for i in open(file,encoding=encoding): #thank you for the bug report from "Hu1J", https://github.com/Scorcsoft/qianscan/issues/1
            i = i.strip("\r\n") # for Linux
            i = i.strip("\n") # for bugdows
            if i:
                DICT.append(i)
                n += 1
        print("\033[1;32m[+]\033[0m loading completed. %d dictionary"%(n))
        return n
    except:
        print("\n\033[1;31m[!]\033[0m Cant open the dictionary file: %s"%(file))
        exit()

def setRequestHeader(file):
    try:
        for i in open(file):
            tmp = i.split(":")
            v = ""
            if len(tmp) >= 2:
                v = tmp[1].strip("\n")
            k = tmp.strip("\n")
            HEADER[k.strip("\r\n")] = v.string("\r\n")
            
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
                                continue
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
                                    d = raw_input("\033[1;31m[!]\033[0m It has timeout 50 times here, Maybe your IP is locked, Keep scanning?[y/n]?>_ ")
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

arg = getopt.getopt(sys.argv[2:],'-h-d:-t:-i:-o:-s:-q',[])
dir_file = 'data/default.list'
for opt_n,opt_v in arg[0]:
    if opt_n == "-h":
        help()
        continue
    if opt_n == "-q":
        NEVER_STOP = True
        continue
    if opt_n == "-d":
        dir_file = opt_v
        continue
    if opt_n == "-t":
        THREAD = int(opt_v)
        continue
    if opt_n == "-i":
        setRequestHeader(opt_v)
        continue
    if opt_n == "-o":
        OUTPUT_FILE = opt_v
        continue
    if opt_n == "-s":
        for i in opt_v.split(","):
            STATUS.append(int(i))
        if 200 in STATUS:
            STATUS.remove(200)

if len(sys.argv) < 2 or sys.argv[1] == "-h":
    help()
DOMAIN = sys.argv[1]
try:
    h = requests.get(url=DOMAIN,headers=HEADER,timeout=3)
except:
    print("\033[1;31m[!]\033[0m Cant open the website: %s, check your network"%(DOMAIN))
    exit()

impossibleUrl = ''
for i in range(255):
    impossibleUrl += chr(random.randint(97,123))
h = requests.get(url = "%s/%s"%(DOMAIN,impossibleUrl),headers=HEADER)
if h.status_code == 200:
    if raw_input("\033[1;31m[!]\033[0m Maybe all url will return a 200 status code, Keep the scan?[y/n]: ") != 'y':
        exit()

dict_size = loadDict(dir_file)
if dict_size < (THREAD * 2):
    THREAD = dict_size / 2
if THREAD < 1:
    THREAD = 1
print("\033[1;34m[*]\033[0m This project will rewrite when sometime")
tmp = "\033[1;31m Quiet mode\033[0m" if NEVER_STOP else ""
print("\033[1;34m[*]\033[0m Starting. Threads: %s.%s\n"%(THREAD,tmp))

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
    print("\n\033[1;32m[+]\033[0m Scan completed")
if OUTPUT_FILE:
    saveResult()
