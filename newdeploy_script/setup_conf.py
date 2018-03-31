#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu


import ConfigParser
import os


# 配置配置文件
def set_conf():

    conf_path = os.path.abspath(os.path.dirname(__file__))

    conf = ConfigParser.ConfigParser()

    conf.read("{0}/base.conf".format(conf_path))

    # 设置版本库路径
    conf.set("repo", "repo_path", "/Users/lonny/Documents/jenkinsfile")

    # 设置版本库导出路径
    conf.set("repo", "repo_export_path", "/Users/lonny/Downloads/test")

    # 设置项目编译参数--环境--对应 pom.xml 标签
    conf.set("build-options", "env", "zmsy_test")

    # 设置项目文件存放位置
    conf.set("repository", "path", "/software")

    # 设置项目部署文件名
    conf.set("project", "name", "sy-cybershop")
    conf.set("project", "version", "0.0.1")

    with open("{0}/project.conf".format(conf_path), "w+") as f:
        conf.write(f)


set_conf()