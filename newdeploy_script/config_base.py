#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

"""
项目脚本配置文件读取
"""

import ConfigParser
import os


class Read_Conf(object):

    # 读取配置文件
    def o_conf(self):

        conf_path = os.path.abspath(os.path.dirname(__file__))

        # 判断配置文件是否存在
        if os.path.exists("{0}/project.conf".format(conf_path)):

            conf = ConfigParser.ConfigParser()

            conf.read("{0}/project.conf".format(conf_path))

            return conf

        else:

            messages = {
                # 配置文件未生成,请生成配置文件
                "status": 1
            }

            return messages
