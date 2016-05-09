#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import datetime
import paramiko

reload(sys)
sys.setdefaultencoding("utf-8")

username = 'root'
password = '123456'

rsa = [
'ssh-rsa1',
'ssh-rsa2'
]


#change return color
def G(s):
    return "%s[32;2m%s%s[0m"%(chr(27), s, chr(27))
def R(s):
    return "%s[31;2m%s%s[0m"%(chr(27), s, chr(27))
 

def cmd_exc(ip, username, password):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        conn.connect(hostname = ip, username = username, password = password, timeout = 5)
        stdin, stdout, stderr = conn.exec_command(cmd)
        result = stdout.readlines()
        ret = ''.join(result)
    except:
        print R("无法连接")
    conn.close()
    try:
        return G(ret)
    except UnboundLocalError:
        pass


def copy_rsa(ip, username, password):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        conn.connect(hostname = ip, username = username, password = password, timeout = 5)
        stdin, stdout, stderr = conn.exec_command("echo '{0}'>>/root/.ssh/authorized_keys;echo '{1}'>>/root/.ssh/authorized_keys".format(rsa[0], rsa[1]))
        result = stdout.readlines()
        ret = ''.join(result)
    except:
        print R("无法连接")
    conn.close()
    try:
        return G(ret)
    except UnboundLocalError:
        pass


def auto_disk(Disk):
    if os.path.exists('./auto_disk.sh'):
        os.remove('./auto_disk.sh') 
    with open('auto_disk.sh', 'a') as f:
        print >>f, '#!/bin/bash'
        print >>f, 'rpm -aq|grep expect'
        print >>f, 'if [ $? != 0 ];then'
        print >>f, '    yum install -y expect'
        print >>f, 'fi'
        print >>f, '/usr/bin/expect -c"'
        print >>f, 'set timeout -1'
        print >>f, 'spawn  /sbin/fdisk /dev/{0}'.format(Disk)
        print >>f, 'expect \"*m for help*:\"'
        print >>f, 'send -- \"n\r\"' 
        print >>f, 'expect \"*p*\n\"' 
        print >>f, 'send -- \"p\r\"'
        print >>f, 'expect  \"*number (1-4):\"' 
        print >>f, 'send -- \"1\r\"'
        print >>f, 'expect  \"*default 1*:\"'
        print >>f, 'send -- \"\r\"'
        print >>f, 'expect  \"*default*:\"' 
        print >>f, 'send -- \"\r\"'
        print >>f, 'expect  \"*m for help*:\"'
        print >>f, 'send -- \"w\r\"'
        print >>f, 'expect eof'
        print >>f, '"'
        print >>f, 'mkfs.ext4 /dev/{0}1'.format(Disk)
        print >>f, 'echo "/dev/{0}1    /home/    ext4   defaults  0  0" >> /etc/fstab'.format(Disk)
        print >>f, 'mount /dev/{0}1   /home/'.format(Disk)


def sftp_auto(ip, username, password):
    t = paramiko.Transport((ip,22))
    t.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put('./auto_disk.sh','/tmp/auto_disk.sh')
    t.close()
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        conn.connect(hostname = ip, username = username, password = password, timeout = 5)
        stdin, stdout, stderr = conn.exec_command('sh /tmp/auto_disk.sh')
        result = stdout.readlines()
        ret = ''.join(result)
    except:
        print R("无法连接")
    conn.close()
    try:
        return G(ret)
    except UnboundLocalError:
        pass
        


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='ssh_cmd', usage='%(prog)s [options]')
    parser.add_argument('-H','--host', nargs='?', dest='listhost', help='主机/多个主机用","分割')
    parser.add_argument('-f','--file', nargs='?', dest='filehost', help='主机列表文件')
    parser.add_argument('-m','--command', nargs='?', dest='command', help='执行命令')
    parser.add_argument('-I','--init', nargs='?', dest='init', help='自动分区挂盘')
    parser.add_argument('-A','--add', nargs='?', dest='add_rsa', help='添加信任')
    if len(sys.argv)==1:
        parser.print_help()
    else:
        args=parser.parse_args()
        cmd = args.command
        if args.listhost is not None and args.filehost is None: 
            if args.command is not None:
                for ip in args.listhost.split(','):
                    print G(ip) 
                    print G('-'*80)
                    print cmd_exc(ip, username, password)
                    print 
            elif args.init is not None:
                auto_disk(args.init)
                for ip in args.listhost.split(','):
                    print G(ip)
                    print G('-'*80)
                    print sftp_auto(ip, username, password)
                    print
            elif args.add_rsa == 'root':
                for ip in args.listhost.split(','):
                    print G(ip)
                    print G('-'*80)
                    print copy_rsa(ip, username, password)
                    print
            else:
                print R('功能选项为空')
        elif args.listhost is None and args.filehost is not None:
            if args.command is not None:
                try:
                    with open(args.filehost) as f:
                        for ips in f.readlines():
                            ip = ips.replace('\n', '')
                            print G(ip)
                            print G('-'*80)
                            print cmd_exc(ip, username, password)
                            print 
                except IOError:
                    print R('主机列表文件不存在')
            elif args.init is not None:
                auto_disk(args.init)
                for ip in args.listhost.split(','):
                    print G(ip)
                    print G('-'*80)
                    print sftp_auto(ip, username, password)
                    print
            elif args.add_rsa == 'root':
                for ip in args.listhost.split(','):
                    print G(ip)
                    print G('-'*80)
                    print copy_rsa(ip, username, password)
                    print
            else:
                print R('功能选项为空')
        else:
            print R('主机或命令不能为空')

