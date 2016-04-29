#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
  
import re  
import sys  
import json  
import urllib  
import urllib2  
   
class zabbixtools:  
   
    def __init__(self, hostip, hostname):  
        self.url = "http://8.8.8.8/zabbix/api_jsonrpc.php"  
        self.header = {"Content-Type": "application/json"}  
        self.authID = self.user_login()  
        self.hostip = hostip.strip("\n")  
        self.hostname = hostname.strip("\n")  
      
    def user_login(self):  
        data = json.dumps(  
            {  
                "jsonrpc": "2.0",  
                "method": "user.login",  
                "params": {  
                    "user": "zabbix",  
                    "password": "zabbix"  
                    },  
                "id": 0  
                })  
   
        request = urllib2.Request(self.url,data)  
        for key in self.header:  
            request.add_header(key,self.header[key])  
        try:  
            result = urllib2.urlopen(request)  
        except URLError as e:  
            print "Auth Failed, Please Check Your Name And Password:"  
        else:  
            response = json.loads(result.read())  
            result.close()  
            authID = response['result']  
            return authID  
   
    def get_data(self,data,hostip=""):  
        request = urllib2.Request(self.url,data)  
        for key in self.header:  
            request.add_header(key,self.header[key])  
        try:  
            result = urllib2.urlopen(request)  
        except Exception,e:  
            if hasattr(e,'reason'):  
                print "we Failed to reach a server"  
                print 'reason:',e.reason  
            elif hasattr(e,'code'):  
                print "the server could not fulfaild the request"  
                print "error code:",e.code  
            return 0  
        else:  
            response = json.loads(result.read())  
            result.close()  
            return response  
   
   
    def host_get(self):  
        # 生成json格式数据  
        data = json.dumps(  
            {  
                "jsonrpc": "2.0",  
                    "method": "host.get",  
                    "params": {  
                        "output":["hostid","name","status","host"],  
                        "filter": {"host": [self.hostip]}  
                        },  
                    "auth": self.authID,  
                    "id": 1  
            })  
        res = self.get_data(data)['result']  
        if (res != 0) and (len(res) != 0):  
            host = res[0]  
            return   host['hostid']  
        else:  
            print "host_get error please check define host_get()"  
            return 0  
   
    def host_update(self):  
        host = self.host_get()  
        data = json.dumps(  
            {  
                 "jsonrpc": "2.0",  
                 "method": "host.update",  
                 "params": {  
                         "hostid": host,  
                         "name": self.hostname.encode('utf8')  
                        },  
                 "auth": self.authID,  
                 "id": 1  
                 })  
        res = self.get_data(data)   
        
              
def hostname(IP):  
    url = 'http://www.baidu.com/restful/getAssetByIpAddress'   
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
    values = {'ipAddress': IP}   
    headers = {'User-Agent': user_agent}   
    data = urllib.urlencode(values)   
    req = urllib2.Request(url, data, headers)   
    response = urllib2.urlopen(req)   
    res = response.read()   
    a = json.loads(res)   
    #lable = a['returnedInfo']  
    if a:  
        lable = a[0]  
        if len(lable):  
            #leader = a['returnedInfo'][0]['productLeader']  
            leader = a[0]['productLeader']  
            jif = a[0]['cloudSource']  
            #product = a['returnedInfo'][0]['productName']  
            product = a[0]['productName']  
            #os = a['returnedInfo'][0]['osInfo'][0:7]  
       #     os = a[0]['osInfo'][0:7]  
            #owner = a['returnedInfo'][0]['productOwner']  
            owner = a[0]['productOwner']  
            HOSTNAME = "%s_%s_%s_%s_%s" % (IP, u"", product, u"", u"")  
            return  HOSTNAME  
        else:  
            return 0  
    else:  
        print IP  
   
   
if __name__ == "__main__":   
    for line in open("hosts.log"):  
        host = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)  
        IP = host[0]  
        print IP  
        b = hostname(IP)  
        if  b:  
            update = zabbixtools(line,b)  
            update.host_update()  
        else:  
            print b  
