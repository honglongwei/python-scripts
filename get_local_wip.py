#coding:utf-8

import os
import Queue
import codecs
import requests
import threading, subprocess
from time import ctime, sleep, time
from bs4 import BeautifulSoup

def get_out_ip(url):
    req = requests.get(url)

    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding
        global encode_content
        encode_content = req.content.decode(encoding, 'replace')

        return encode_content[encode_content.find("<center>") + 1: encode_content.find("</center>")].replace("center>", "")

def get_real_url(url=r'http://www.ip138.com/'):
    r = requests.get(url)
    txt = r.text
    soup = BeautifulSoup(txt,"html.parser").iframe
    return soup["src"]

class ThreadUrl(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            host = self.queue.get()
            ret = subprocess.Popen('ping -n 600 '+ host, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            with open('iflytek/{0}.log'.format(host), 'a') as f:
                print >>f, ret.stdout.read()
            self.queue.task_done()

def startPing():
    for i in range(100):
        t=ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
    for host in ['140.143.0.175', '39.107.78.159', '120.92.31.91', '117.121.21.146', '117.121.21.146', '42.62.116.34', '42.62.42.10', '121.201.83.170', '59.107.24.5']:
        queue.put(host)
    queue.join()

if __name__ == '__main__':
    print '*'*40
    print '*' + u'   欢迎使用网络质量检测工具   ' + '*'
    print '*' + '                                      ' + '*'
    print '*' + u'  程序运行过程中,请不要关闭程序窗口!  ' + '*'
    print '*'*40
    if not os.path.exists('iflytek'):
        os.makedirs('iflytek')
    ip = get_out_ip(get_real_url())
    f = codecs.open('iflytek/ISP.log', 'w', 'utf-8')
    f.write(ip)
    queue = Queue.Queue()
    ret = startPing()


#pip install pyinstaller
#pyinstaller -F get_local_wip.py  >> dist/get_local_wip.exe
