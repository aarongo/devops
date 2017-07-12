#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author EdwardLiu

# For syzm pro

import sys
import re
from subprocess import Popen, PIPE


def adduser(user, password):
    config_path = "/etc/ppp/chap-secrets"
    f = open(config_path)
    source = f.read()
    f.close()
    if re.findall(user, source):
        print "\033[31muser is exist!!!\033[0m"
        return 1
    else:
        input_string = "%s\t*\t%s\t*\n" % (user, password)
        print "\033[32mAdd user: %s\tpassword: %s\033[0m" % (user, password)
        vpn_user_config = open(config_path, "a")
        vpn_user_config.write(input_string)
        vpn_user_config.close()


def servicehandle():
    service_command = ["/usr/bin/systemctl restart ipsec", "/usr/bin/systemctl restart xl2tpd"]
    for command in service_command:
        code_update = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = code_update.communicate()
        print stdout, stderr

if __name__ == '__main__':
    try:
        if adduser(user=sys.argv[1], password=sys.argv[2]) == 1:
            pass
        else:
            servicehandle()
    except IndexError, e:
        print "\033[31mPlease input realy user and password!!!!\033[0m"