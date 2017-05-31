#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import MySQLdb


with open('/var/logs/install.log') as f:
    a = f.read().strip().split('\n')
    hostl = []
    for i in a:
        b = i.split('\t')
        if b[3] == 'stop':
            hostl.append(b[1])
        else:
            pass
    for host in list(set(hostl)):
        conn= MySQLdb.connect(
                              host='localhost',
                              port = 3306,
                              user='root',
                              passwd='111111',
                              db ='pj_install',
           )
        try:
            #select
            sql = "select * from automsg where HostName='{0}'".format(host)
            cur = conn.cursor()
            cur.execute(sql)
            ret = cur.fetchone()

            #update
            update_sql = "update installretmsg set status=2, msg=u'安装成功!' where id={0}".format(int(ret[0]))
            cur.execute(update_sql)

            cur.close()
            conn.commit()
            conn.close()
        except:
            pass
