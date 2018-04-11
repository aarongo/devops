#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
@author: EdwardLiu 
@contact: lonnyliu@126.com

@file: write_logs.py
@time: 2018/4/11 16:58

"""

import logging.config

import yaml

from config_base import Read_Conf as readconfig


class Write_Logs(object):

    def __init__(self, conf=readconfig().o_conf()):
        if conf['status'] != 1:
            self.conf_path = conf.get("log_path", "conf_path")

    """
        记录日志方法
        write_way 根据logging.yml loggers: 名称进行匹配
    """

    def write_log(self, write_way):
        log_conf = "{0}/logging.yml".format(self.conf_path)
        with open(log_conf, 'r') as f_conf:
            dict_conf = yaml.load(f_conf)
        logging.config.dictConfig(dict_conf)

        logger = logging.getLogger(write_way)
        return logger
