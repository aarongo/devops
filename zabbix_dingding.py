#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu


import requests
import json
import sys
from datetime import datetime


def send_dingding(messages):
    headers = {'Content-Type': 'application/json'}
    url = 'https://oapi.dingtalk.com/robot/send?access_token=2fdce2e0b0ce886b30dd21d76c6078b1e1314f3c7ce5d8572bc1fa4701765aec'
    r = requests.post(url=url, data=json.dumps(messages), headers=headers)
    if r.status_code == 200:
        return True


if __name__ == '__main__':
    # 获取到的是 用户里的动作标题
    send_to = sys.argv[1]
    # 发送的标题
    subject = sys.argv[2]
    # 发送内容
    messages = sys.argv[3]
    Time_Now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "%s" % send_to,
            "text": "#### %s\n" % subject +
                    "> %s\n\n" % messages +
                    "**%s**\n" % Time_Now
        }
    }
    sms = send_dingding(messages=payload)
    if sms:
        print "发送钉钉成功"