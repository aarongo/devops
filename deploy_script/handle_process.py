#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.compile

"""
    process hanlde files incloud
        1.process status
            use request get Url returncode
        2.process Stop
            use psutil kill process
        3.process start
            use subprocess run shell start process
        4.process log
            use process logs
        5.process restart
"""

# Improt Libary
import psutil
from subprocess import PIPE, Popen, STDOUT
import os
import sys
import requests
import datetime

# Set vars
process_name = "/software/apache-tomcat-jenkins"
url = "http://172.31.1.230:8080"


def process_id():
    # use process name get process pid
    process_base_str = "-Dcatalina.base=%s" % process_name
    pid = {}
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
        except psutil.NoSuchProcess:
            pass
        else:
            if process_base_str in pinfo.get('cmdline'):
                pid[process_name] = pinfo.get('pid')
    return pid


def process_judgment():
    # 判断 URL 的状态码
    messages = ""
    try:
        jenkins_r = requests.get(url, timeout=None)
        return jenkins_r.status_code
    except requests.ConnectTimeout:
        messges = "Timeout"
        return messges
    except requests.ConnectionError:
        messages = "connection"
        return messages
    except requests.HTTPError:
        messages = "httperror"
        return messages
    else:
        return messages


def process_status():
    # judgment process status
    if not process_id().get(process_name) is None:
        if process_judgment() == 200:
            print "\033[32mProcess %s normal\033[0m" \
                % process_name.split('/')[2]
        else:
            print "\033[31mProcess Dont Access By:%s\033[0m" % url + "\n"\
                "\033[31mMesages:%s" % process_judgment()
    else:
        print "\033[31mProcess %s does not exist" % process_name.split('/')[2]


def process_log_info():
    process_log = "tail -f %s/logs/catalina.out " % process_name
    process_logs = Popen(process_log, shell=True,
                         stdout=PIPE, stderr=STDOUT)
    returncode = process_logs.poll()
    try:
        while returncode is None:
            line = process_logs.stdout.readline()
            returncode = process_logs.poll()
            line = line.strip()
            print line
        print returncode
    except KeyboardInterrupt:
        print 'ctrl+d or z'


def process_kill():
    # judgment process exist
    if process_id().get(process_name) is None:
        print "\033[31mProcess %s is Not Started" % process_name.split('/')[2]
        sys.exit(0)
    elif not process_id().get(process_name) is None \
            and process_judgment() != 200:
        print "\033[31mProcess %s is Started But Process access Failed \
            Messages:" % (process_name, process_judgment())
        sys.exit(0)
    # stop process
    PROCESSID = process_id().get(process_name)
    p = psutil.Process(pid=PROCESSID)
    p.kill()
    if process_id().get(process_name) is None:
        print "\033[32mprocess %s stop OK!!!\033[0m" \
            % process_name.split('/')[2]
    else:
        print "\033[31mProcess %s Stop Failed\!!![033[0m" \
            % process_name.split('/')[2]


def process_init():
    # start process
    os.environ["JAVA_HOME"] = "/software/java_1.7"
    if process_id().get(process_name) is None:
        start_time = datetime.datetime.now()
        process_init_command = "%s/bin/startup.sh" % process_name
        start = Popen(process_init_command, stdout=PIPE,
                      stderr=PIPE, shell=True)
        stdout, stderr = start.communicate()
        print stderr
        print "\033[32mWaitting Process %s Start OK !!!\033[0m" \
            % process_name.split('/')[2]
        while process_judgment() != 200:
            pass
        end_time = datetime.datetime.now()
        print "\033[32mprocess start time(s):%s\033[0m" \
            % (end_time - start_time).seconds
    else:
        print "\033[32mProcess %s is Started\033[0m" \
            % process_name.split('/')[2]
