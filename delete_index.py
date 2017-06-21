#!/usr/bin/env python
# _*_coding:utf-8_*_

from subprocess import PIPE, Popen
import sys

def deleteindex(index_name, month):
    proxy = "unset http_proxy"
    q_proxy = Popen(proxy, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = q_proxy.communicate()
    print stdout
    delete_monuth="logstash-%s-access-%s.*" %(index_name, month)
    d_index = """/usr/bin/curl -XDELETE 'http://10.171.35.11:9200/%s' """% delete_monuth
    d_index_delete = Popen(d_index, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = d_index_delete.communicate()
    print stdout
def usage():
    help = "%s 日志名称 日志年月 EG:%s nginx 2016.12" % (sys.argv[0],sys.argv[0])
    print help
def main():
    usage()
    name = sys.argv[1]
    month_i = sys.argv[2]
    deleteindex(index_name=name, month=month_i)

if __name__ == '__main__':
    main()
