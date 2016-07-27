#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'honglongwei'

import os
import sys
import time
import zipfile
import datetime
import subprocess
import salt.client
from salt.output.nested import NestDisplay
from salt.utils import get_colors

#script path
sct_lt = {'start': '/home/game/startup.sh',
          'stop': '/home/game/shutdown.sh'
         }
#pid path
ser_pid = '/home/game/game.pid'
#src update package path
src_path = '/home/update'
#des update package path
des_path = '/home'
#src backup package path
bsrc_path_lt = ['/home/game/config', 
                '/home/game/data', 
                '/home/game/hibernate'] 
#des backup package path
bdes_path = '/home/backup'


# call salt output class
class NestPut(NestDisplay):
    def __init__(self):
        self.colors = get_colors(True)
        self.__dict__.update(get_colors(True))
        self.strip_colors = True

def Prest(data):
    '''
    Display ret data
    '''
    nest = NestPut()
    print '\n'.join(nest.display(data, 0, '', []))


def start():
    '''
    Define func start server
    '''
    if os.path.exists(ser_pid):
        return Prest('GameServer is already running !!!')
    else:
        cmd = sct_lt['start']
        proc = subprocess.Popen(cmd, shell=True)
        return Prest('Start GameServer is successful !!!')


def stop():
    '''
    Define func stop server
    '''
    if os.path.exists(ser_pid):
        cmd = sct_lt['stop']
        proc = subprocess.Popen(cmd, shell=True)
        return Prest('Stop GameServer is successful !!!')
    else:
        return Prest('GameServer is already stopped !!!')
      

def status():
    '''
    Define func status server
    '''
    if os.path.exists(ser_pid):
        return Prest('GameServer is not running !!!')
    else:
        cmd = 'ps -ef|grep \'{0}\'|grep -v grep'.format('server')
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        ret = proc.stdout.read() 
        return Prest(ret)


def backup():
    '''
    Define func backup server
    '''
    bakname = 'gs_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.zip'
    zipname = os.path.join(bdes_path, bakname)
    f = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    for bsrc_path in bsrc_path_lt:
        bac_path = os.path.dirname(bsrc_path)
        ls_path = bac_path + '/'
        zg_path = bsrc_path.split(ls_path)[1]
        os.chdir(bac_path)
        for dirpath, dirnames, filenames in os.walk(zg_path):
            for filename in filenames:
                f.write(os.path.join(dirpath, filename)) 
    f.close()
    return 'Backup is successful !'


def update(pkg):
    '''
    Define func update server
    '''
    if pkg:
        fl = os.path.join(src_path, pkg)
        try:
            zfile = zipfile.ZipFile(fl,'r')
            for filename in zfile.namelist():
                zfile.extract(filename, des_path)
            return 'Update is successful !'
        except IOError:
            return 'The package is invalid !!!' 
    else:
        return 'The package is invalid !!!'



if __name__== "__main__":
    # check arguments
    opts = sys.argv
    if len(opts) < 2:
        print 'start|stop|status|backup|update'
        sys.exit(0)
    elif len(opts) == 2:
        if opts[1]=='start':
            start()
        elif opts[1]=='stop':
            stop()
        elif opts[1]=='status':
            status()
        elif opts[1]=='backup':
            backup()
        else:
            print 'Script Parameter Error !!!'
    elif len(opts) == 3:
        if opts[1]=='update':
            update(opts[2])
        else:
            print 'Script Parameter Error !!!'
    else:
        print 'Script Parameter Error !!!'
