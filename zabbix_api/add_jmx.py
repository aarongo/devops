#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json

url = "http://10.6.11.33/api_jsonrpc.php"
header = {"Content-Type": "application/json"}

# 1 登录
def user_login():
    data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": "liubiqian",
                    "password": "liu=LIUM"
                    },
                "id": 0
                })
    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key,header[key])
    try:
        result = urllib2.urlopen(request)
    except urllib2.URLError as e:
        print "Auth Failed, Please Check Your Name And Password:",e.code
    else:
        response = json.loads(result.read())
        result.close()
        authID = response['result']
    return authID


# 公用获取数据
def get_data(data):
    request = urllib2.Request(url, data)
    for key in header:
        request.add_header(key, header[key])
    try:
        result = urllib2.urlopen(request)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
        return 0
    else:
        response = json.loads(result.read())
        result.close()
        return response


# 通过传入的组获取组 id
def host_get_grop(group):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": ["groupid","name"],
                "filter": {
                    "name": [
                        "%s"% group
                    ]
                }
            },
            "auth": user_login(),
            "id": 1
        }
    )
    res = get_data(data=data)['result']
    # 获取 groupid
    groupid = res[0]['groupid']
    return groupid


# 通过组 id 获取 主机(名)和主机 id
def host_get_in_grup(groupid):
    list = {}
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["host","hostid"],
                "groupids": "%s" %groupid,
            },
            "auth": user_login(),
            "id": 1
        }
    )
    res = get_data(data=data)['result']
    for i in range(len(res)):
        list[res[i]['host']] = res[i]['hostid']
    return list


# 根据主机 ID 获取主机 IP地址
def host_ip(hostid):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "hostinterface.get",
            "params": {
                "output": ["ip"],
                "hostids": "%s"% hostid
            },
            "auth": user_login(),
            "id": 1
        }
    )
    res = get_data(data)['result']
    hostip = res[0]['ip']
    # 返回 IP 地址
    return hostip


# 通过主机和主机 id 添加 jmx interfaces
def add_interface(hostip,hostid):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "hostinterface.create",
            "params": {
                "hostid": "%s"% hostid,
                "dns": "",
                "ip": "%s"% hostip,
                "main": 1,
                "port": "28915",
                "type": 4,
                "useip": 1
            },
            "auth": user_login(),
            "id": 1
        }
    )
    res = get_data(data)['result']
    print res


if __name__ == '__main__':
    group = raw_input("请输入主机组名称:")
    groupid = host_get_grop(group="拼实惠WEB集群")
    # 接收IP 地址和 id 对应关系
    list = {}
    # 循环将 IP 与主机 id 进行对应
    out = host_get_in_grup(groupid=groupid)
    for key in out:
        list[host_ip(hostid=out[key])] = out[key]

    # 循环list 进行批量添加 jmx 接口
    for k in list:
        add_interface(k,list[k])