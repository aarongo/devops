#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
@author: EdwardLiu 
@contact: lonnyliu@126.com

@file: write_logs.py
@time: 2018/4/11 16:58

"""

import yaml
import logging.config
from config_base import Read_Conf as readconfig


class Write_Logs(object):

    def __init__(self, conf=readconfig().o_conf()):

        self.conf_path = conf.get("log_path", "conf_path")

    def write_log(self, write_way):
        log_conf = "{0}/logging.yml".format(self.conf_path)
        with open(log_conf, 'r') as f_conf:
            dict_conf = yaml.load(f_conf)
        logging.config.dictConfig(dict_conf)

        logger = logging.getLogger(write_way)
        return logger

