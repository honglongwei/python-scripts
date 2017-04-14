#/usr/bin/env python
#-*-coding=utf-8-*-

# __author__  = 'Zline'

import requests
import re
from threading import Thread,Lock
import time
import sys
import chardet
import netaddr
import struct
import socket

lock = Lock()

def ip2int(addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]
def int2ip(addr):
        return socket.inet_ntoa(struct.pack("!I", addr))
def int_dec(pagehtml):

        charset = None
        if pagehtml != '':
                # print 'use charset dect'
                enc = chardet.detect(pagehtml)
                # print 'enc= ', enc
                if enc['encoding'] and enc['confidence'] > 0.9:
                        charset = enc['encoding']

                if charset == None:
                        charset_re = re.compile("((^|;)\s*charset\s*=)([^\"']*)", re.M)
                        charset=charset_re.search(pagehtml[:1000]) 
                        charset=charset and charset.group(3) or None

                # test charset
                try:
                        if charset:
                                unicode('test',charset,errors='replace')
                except Exception,e:
                        print 'Exception',e
                        charset = None
        # print 'charset=', charset
        return charset


def http_banner(url):
        ip=url
        try:
                url=requests.get(url,timeout=2)        

                body = url.content
                
                charset = None
                if body != '':
                        charset = int_dec(body)

                if charset == None or charset == 'ascii':
                        charset = 'ISO-8859-1'

                if charset and charset != 'ascii' and charset != 'unicode':
                        try:
                                body = unicode(body,charset,errors='replace')
                        except Exception, e:
                                body = ''
                Struts=url.status_code
                Server=url.headers['server'][0:13]
                if Struts==200 or Struts==403 or Struts==401:
                        title=re.findall(r"<title>(.*)<\/title>",body)
                        if len(title):
                                title = title[0].strip()
                        else:
                                title = ''
                        lock.acquire()
                        print ('%s\t%d\t%-10s\t%s'%(ip.lstrip('http://'),Struts,Server,title))
                        lock.release()
        except (requests.HTTPError,requests.RequestException,AttributeError,KeyError),e:
                pass



if __name__ == '__main__':
        if len(sys.argv) >= 2:
                ips = sys.argv[1]
        else:
                print 'usage: python http_banner.py 192.168.1./24 '
                print 'usage: python http_banner.py 192.168.1.1-192.168.1.254 '
                print 'usage: python http_banner.py 192.168.1./24 8080'
                print 'usage: python http_banner.py 192.168.1.1-192.168.1.254 8080'
                sys.exit()
        port = '80'
        if len(sys.argv) == 3:
                port = sys.argv[2]
                
        if '-' in ips:
                start, end = ips.split('-')
                startlong = ip2int(start)
                endlong = ip2int(end)
                ips = netaddr.IPRange(start,end)
                for ip in list(ips):
                        url='http://%s:%s'%(ip,port)
                        t = Thread(target=http_banner,args=(url,))
                        t.daemon=False
                        t.start()
        elif '/'        in ips:
                ips = netaddr.IPNetwork(ips)
                for ip in list(ips):
                        url='http://%s:%s'%(ip,port) 
                        t = Thread(target=http_banner,args=(url,))
                        t.daemon=False
                        t.start()
