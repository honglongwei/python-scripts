#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import xlwt
import time
import json
import urllib
import urllib2
import datetime
import paramiko
import commands


reload(sys)
sys.setdefaultencoding("utf-8")

username = 'root'
password = '123456'

url_idc = 'http://www.baidu.com/assetInfo' 
url_clound = 'http://www.tengxun.com/cloudAsset' 

def GetAllSeal(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
    if url == url_clound:
        values = {'test': 'demo'} 
    elif url == url_idc:
        values = {'product': u'运维'}
    else:
        return 'URL is Error !!!'
    headers = {'User-Agent': user_agent} 
    data = urllib.urlencode(values) 
    req = urllib2.Request(url, data, headers) 
    response = urllib2.urlopen(req) 
    res = response.read() 
    a = json.loads(res) 
    return a


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  

    font = xlwt.Font() 
    font.name = name 
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font
    return style

def WriteDateExcel():
    Tm = datetime.datetime.now().strftime('%Y-%m-%d')
    urls = [url_clound, url_idc]
    wbk = xlwt.Workbook(encoding='utf-8')
    for url in urls:
        result = GetAllSeal(url)
        if url == url_clound:
            sheet1 = wbk.add_sheet(u'云资产扫描结果', cell_overwrite_ok=True)
            row0 = [u'业务', u'负责人', u'外网IP', u'内网IP', u'操作系统', u'扫描结果'] 
            for x in xrange(len(row0)):
                sheet1.write(0, x, row0[x], set_style('Times New Roman',220,True))
            for i in xrange(len(result)):
                conn = paramiko.SSHClient()
                conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    conn.connect(hostname = result[i]['WIp'], username = 'root', timeout = 1)
                    stdin, stdout, stderr = conn.exec_command("iptables -nvL|grep -E '10.0.0.0/8|10.12.0.0/16'")
                    cdt = stdout.readlines()
                    ret = ''.join(cdt)
                except:
                    ret = u'无法连接'
                contl = [result[i]['Name'], result[i]['Responser'], result[i]['WIp'], result[i]['LIp'], result[i]['os'], ret]
                for j in xrange(len(contl)):
                    sheet1.write(i+1, j, contl[j])
        elif url == url_idc:
            sheet2 = wbk.add_sheet(u'物理机扫描结果', cell_overwrite_ok=True)
            row0 = [u'项目', u'负责人', u'外网IP', u'内网IP', u'操作系统', u'扫描结果'] 
            for x in xrange(len(row0)):
                sheet2.write(0, x, row0[x], set_style('Times New Roman',220,True))
            for i in xrange(len(result)):
                conn = paramiko.SSHClient()
                conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    conn.connect(hostname = result[i]['wIp'], username = 'root', timeout = 1)
                    stdin, stdout, stderr = conn.exec_command("iptables -nvL|grep -E '10.0.0.0/8|10.12.0.0/16'")
                    cdt = stdout.readlines()
                    ret = ''.join(cdt)
                except:
                    ret = u'无法连接'
                contl = [result[i]['Name'], result[i]['Owner'], result[i]['wIp'], result[i]['lIp'], result[i]['os'], ret]
                for j in xrange(len(contl)):
                    sheet2.write(i+1, j, contl[j])
        else:
            return 'URL is Error !!!'
    wbk.save('checkseal_{0}.xls'.format(Tm))


if __name__ == "__main__":
    WriteDateExcel()
