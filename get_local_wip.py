#encoding: utf-8
import requests
from bs4 import BeautifulSoup


# 获取公网出口IP
def get_out_ip(url):
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    print('ip:' + ip)
    return ip


def get_real_url(url=r'http://www.ip138.com/'):
    r = requests.get(url)
    txt = r.text
    soup = BeautifulSoup(txt,"html.parser").iframe
    return soup["src"]


if __name__ == '__main__':
    ip = get_out_ip(get_real_url())
    with open("result.log", "a") as f:
        print >>f, ip

#pip install pyinstaller
#pyinstaller -F get_local_wip.py  >> dist/get_local_wip.exe
