sadfs#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
__author__ = 'honglongwei'
 
import os
import sys
import time
import zipfile
import datetime
import subprocess
from subprocess import Popen
 
 
#src update package path
src_path = '/tmp/backup'
#des update package path
des_path = {'tomcat': '/tmp/222',
            'apache': '/tmp',
            'websocket': '/tmp'}
#src backup package path
bsrc_path_lt = {'tomcat': ['/tmp/2', '/tmp/1'],
                'apache': ['/tmp'],
                'websocket': ['/tmp']}
#des backup package path
bdes_path = '/tmp/backup'
#service name and server start bin 
srv_up = {'tomcat': '/home/mrdTcomat/app/tomcat/bin/start.sh',
          'apache': '',
          'websocket': ''}
#service name and server stop bin 
srv_down = {'tomcat': '/home/mrdTcomat/app/tomcat/bin/shutdown.sh',
            'apache': '',
            'websocket': ''}
 
 
#change return color
def G(s):
    return "%s[32;2m%s%s[0m"%(chr(27), s, chr(27))
def A(s):
    return "%s[36;2m%s%s[0m"%(chr(27), s, chr(27))
def R(s):
    return "%s[31;2m%s%s[0m"%(chr(27), s, chr(27))
 
 
def start(ServiceName):
    '''
        Desc: Start GameServer
 
        CLI Example:
                opsmod.py ServiceName start
    '''    
    cmd = srv_up[ServiceName]
    proc = Popen(cmd, shell=True)
    return G('Start GameServer is successful !')
 
 
def stop(ServiceName):
    '''
        Desc: Stop GameServer
 
        CLI Example:
                opsmod.py ServiceName stop
    '''    
    cmd = srv_down[ServiceName]
    proc = Popen(cmd, shell=True)
    return G('Stop GameServer is running...,please wait !')
 
 
def status(ServiceName):
    '''
        Desc: Check GameServer Status
 
        CLI Example:
                opsmod.py ServiceName status
    '''    
    cmd = 'ps -ef|grep {0}|grep -v grep'.format(ServiceName)
    proc = Popen(cmd, stdout=subprocess.PIPE, shell=True)
    item = proc.stdout.read()
    cot = len(item.split('\n')) - int(1)
    ret = item + '\n' + '*'*80 + '\n' + 'The total of process is {0} !'.format(cot)
    return G(ret)
 
 
def update(ServiceName, Pkg):
    '''
        Desc: Update GameServer
 
        CLI Example:
                opsmod.py ServiceName update Pkg
    '''    
    if Pkg:
        fl = os.path.join(src_path, Pkg)
        try:
            zfile = zipfile.ZipFile(fl,'r')
            for filename in zfile.namelist():
                zfile.extract(filename, des_path[ServiceName])
            return G('Update is successful !')
        except IOError:
            return R('The package is invalid !!!')
    else:
        return R('The package is invalid !!!')
 
 
def backup(ServiceName):
    '''
        Desc: Backup GameServer
 
        CLI Example:
                opsmod.py ServiceName backup
    '''    
    bakname = ServiceName + '_' +  datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.zip'
    zipname = os.path.join(bdes_path, bakname)
    f = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    for bsrc_path in bsrc_path_lt[ServiceName]:
        bac_path = os.path.dirname(bsrc_path)
        ls_path = bac_path + '/'
        zg_path = bsrc_path.split(ls_path)[1]
        os.chdir(bac_path)
        for dirpath, dirnames, filenames in os.walk(zg_path):
            for filename in filenames:
                f.write(os.path.join(dirpath, filename)) 
    f.close()
    return G('Backup is successful !')
 
 
if __name__== "__main__":
    opts = sys.argv
    try:
        if opts[1]=='-d' or opts[1]=='--help':
            print G('start :') + R('{0}'.format(start.__doc__))
            print G('stop :') + R('{0}'.format(stop.__doc__))
            print G('status :') + R('{0}'.format(status.__doc__))
            print G('update :') + R('{0}'.format(update.__doc__))
            print G('backup :') + R('{0}'.format(backup.__doc__))
        elif opts[2]=='start':
            print start(opts[1])
        elif opts[2]=='stop':
            print stop(opts[1])
        elif opts[2]=='status':
            print status(opts[1])
        elif opts[2]=='backup':
            print backup(opts[1])
        elif opts[2]=='update':
            print update(opts[1], opts[3])
        else:
            print R('Script Parameter Error !!!')
    except IndexError:
        print R('Script Parameter Error !!!')
