#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import os
import sys
import time
import re
import zipfile
import datetime
from subprocess import Popen
 
#groupid
gid = ''
#src update package path
src_path = 'D:\\update'
#des update package path
des_path = 'D:\\'
#process list
pro_lt = ''
#src backup package path
bsrc_path_lt = ['D:\\bin', 'D:\\conf', 'D:\\tdata'] 
#des backup package path
bdes_path = 'D:\\backup'
 
 
def check_start():
    filelist =  os.listdir('D:{0}\\Log'.format(gid)) 
    fls = []
    for filename in filelist:
        log_list = ['', '', '', '', '']
        for file_log in log_list:
            log_s = file_log + '_' + datetime.datetime.now().strftime('%Y%m%d%H') 
            if  filename.startswith(log_s) and filename.endswith('.txt'):
                fl_nm = os.path.join('D:{0}\\Log'.format(gid), filename)
                with open(fl_nm) as f:
                    if 'Server initialize end server started!' in f.read():
                        ret = '{0} - Ok!'.format(filename)
                        fls.append(ret)
                    else:
                        ret = '{0} - Failed!'.format(filename)
                        fls.append(ret)
            else:
                pass
    rtfl = []            
    for srnm in ['', '', '', '', '']:           
        retls = []
        for dnm in fls:
            if re.match(srnm, dnm):
                retls.append(dnm)
            else:
                pass
        rtfl.append(retls[-1])
    if 'Failed!' in ''.join(rtfl):
        print ''.join(rtfl).replace('!', '\n')
        sys.exit(1)
    else:
        return ''.join(rtfl).replace('!', '\n')
 
print check_start()
