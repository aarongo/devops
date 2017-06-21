#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author 行者


import configparser
import paramiko
import threading
import requests
import sys

# 读取配置文件
def readconf():
    cf = configparser.ConfigParser()
    cf.read("setup.conf")
    return cf


# 进程检测
def checkprocess(process, ip, username, cmd, url):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            # 屏幕输出
            for line in out:
                print "IP地址:%s\t程序名称:%s\t进程ID:%s" % (ip, process, str(line))
        ssh.close()
    except:
        print '%s\tError\n' % (ip)
    try:
        r = requests.head(url)
        print "内网访问:%s\t程序名称:%s\t状态:%s" % (ip, process, r.status_code)
    except requests.ConnectionError:
        print "内网访问:%sfailed to connect" % ip

if __name__ == '__main__':
    ip_info = {
        'web1': '10.171.104.1',
        'web2': '10.171.104.2',
        'web3': '10.171.104.3',
        'web4': '10.171.104.4',
        'web5': '10.171.104.5',
        'web6': '10.171.104.6',
        'web7': '10.171.104.7',
        'web8': '10.171.104.8',
        'web9': '10.171.104.9',
        'web10': '10.171.104.10',
        'web11': '10.171.104.11',
        'web12': '10.171.104.12',
        'web13': '10.171.104.13',
        'web14': '10.171.104.14',
        'app1': '10.171.35.1',
        'app2': '10.171.35.18',
        'app3': '10.171.35.19',
        'app4': '10.171.35.20',
        'app5': '10.171.35.21',
        'app6': '10.171.35.22',
        'app7': '10.171.35.23',
        'app9': '10.171.35.24',
        'app10': '10.171.35.17'
    }
    print "----------服务器对应列表-----------"
    for key, value in ip_info.iteritems():
        print "服务器名称:%s\t服务器IP地址:%s" % (key, value)
    print "----------服务器对应列表 END--------"
    web_host = readconf().get('web', 'web').encode('utf-8').split(',')
    app_host = readconf().get('app', 'app').encode('utf-8').split(',')
    front_host = readconf().get('front', 'front').encode('utf-8').split(',')
    process = 'tomcat_%s' % sys.argv[1]
    username = 'cdczhangg'
    cmd = ["ps aux | grep java | grep -v grep |grep %s | awk '{print $2}'" % process]
    threads = []
    if sys.argv[1] == 'web':
        for ip in web_host:
            url = "http://%s/login"% ip
            a = threading.Thread(target=checkprocess, args=(process, ip, username, cmd, url))
            a.start()
            a.join()
    elif sys.argv[1] == 'app':
        for ip in app_host:
            url = "http://%s:%s%s" % (ip,readconf().get('app', 'port'), readconf().get('app', 'url_path'))
            a = threading.Thread(target=checkprocess, args=(process, ip, username, cmd, url))
            a.start()
            a.join()
    elif sys.argv[1] == 'front':
        for ip in front_host:
            url = "http://%s/login"% ip
            a = threading.Thread(target=checkprocess, args=(process, ip, username, cmd, url))
            a.start()
            a.join()
