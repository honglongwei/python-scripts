#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import os
import time
import datetime
 
 
def GetLog(num):
    fls = []
    for dirpath, dirnames, filenames in os.walk('/opt/logbak'):
        for filename in filenames:
            fn = os.path.join(dirpath, filename)
            now_time = datetime.datetime.now()
            last_time = now_time + datetime.timedelta(days=-num)
            tg_time = last_time.strftime('%Y-%m-%d')
            endf = tg_time + '.tgz'
            if filename.startswith('xxx_') and filename.endswith(endf):
                if os.path.exists(fn):
                    fls.append(fn)
                else:
                    pass
            else:
                pass
     
    xlog = []
    for a in fls:
        xlog.append(a[13:17])
    xlog.sort()
    return xlog
 

blog = GetLog(2)
alog = GetLog(1)
'''
 交集:list(set(a).intersection(set(b))) 
 并集:list(set(a).union(set(b))) 
 差集:list(set(b).difference(set(a))) // b中有而a中没有的
'''
jdata = set(blog).intersection(set(alog)) #交集
mor = list(set(alog).difference(jdata))   #新增
les = list(set(blog).difference(jdata))   #减少
if len(mor) == 0 and len(les) == 0:
    print 0
elif len(mor) == 0 and len(les) != 0:
    print '-: {0}'.format(','.join(les))
elif len(mor) != 0 and len(les) == 0:
    print '+: {0}'.format(','.join(mor))
else:
    print '+: {jia}\n-: {shao}'.format(jia=','.join(mor), shao=','.join(les))
