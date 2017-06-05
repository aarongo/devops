#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author EdwardLiu


import json
import urllib2


class zabbixtools(object):

    def __init__(self):
        self.url = "http://10.90.3.110:8090/zabbix/api_jsonrpc.php"
        self.header = {"Content-Type": "application/json"}
        self.authID = self.get_auth_id()

    def get_auth_id(self):
        # auth user and password
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": "admin",
                    "password": "aaron@126.com"
                },
                "id": 0
            })
        # create request object
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        # auth and get authid
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            print "Auth Failed, Please Check Your Name AndPassword:", e.code
        else:
            response = json.loads(result.read())
            result.close()
        return response['result']
