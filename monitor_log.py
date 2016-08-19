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
if len(blog) > len(alog):
    print '-' + ' ' + ','.join(list(set(blog).difference(set(alog)))) #交集:list(set(a).intersection(set(b))) 并集:list(set(a).union(set(b))) 差集:list(set(b).difference(set(a))) # b中有而a中没有的
elif len(blog) < len(alog):
    print '+' + ' ' + ','.join(list(set(alog).difference(set(blog))))
else:
    print 0


