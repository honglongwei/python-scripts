#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
   
import urllib   
import urllib2   
import json   


def hostname(IP):   
    url = 'http://www.baidu.com/restful/getAssetByIpAddress'   
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
    values = {'ipAddress': IP}   
    headers = {'User-Agent': user_agent}   
    data = urllib.urlencode(values)   
    req = urllib2.Request(url, data, headers)   
    response = urllib2.urlopen(req)   
    res = response.read()   
    data = json.loads(res)   
    return data
