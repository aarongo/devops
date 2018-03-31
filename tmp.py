#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu
import time


command_dict = {
        "rpm_get": "rpm -qa | grep -i mysql",
        "path_get": "/usr/bin/whereis mysql"
    }

for cmd in command_dict:
    print cmd,command_dict[cmd]

