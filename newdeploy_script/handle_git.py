#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

"""
项目 版本库 公用操作类
"""

import git
from subprocess import STDOUT, call
import shutil
import os
from config_base import Read_Conf as readconfig
import yaml
import logging.config


class Custom_Git(object):

    def __init__(self, branch_name, config=readconfig().o_conf()):

        self.branch_name = branch_name

        if config != 1:
            self.repo_path = config.get("repo", "repo_path")

            self.repo_export = config.get("repo", "repo_export_path")

            self.git_bin = config.get("system", "git_bin")

            self.conf_path = config.get("log_path", "conf_path")

    # 记录日志,后续部署调用该日志进行项目部署
    def write_log(self):
        log_conf = "{0}/logging.yml".format(self.conf_path)
        with open(log_conf, 'r') as f_conf:
            dict_conf = yaml.load(f_conf)
        logging.config.dictConfig(dict_conf)

        logger = logging.getLogger('git_info')
        return logger

    def client(self):

        repo = git.Repo(self.repo_path)

        client = repo.git

        return client

    # 版本信息
    def branch_version(self):

        version = self.client().log("--pretty=format:'%h'", "-1")

        # eval 将字符串str当成有效的表达式来求值并返回计算结果--去除返回结果中的引号
        return eval(version.encode("utf-8"))

    # 切换分支
    def branch_switch(self):

        print ("Checkout Branch {0}".format(self.branch_name))

        # 所有分支
        branches = self.client().branch()

        # 默认分支
        default = "master"

        # 处理同一分支部署多次
        if self.branch_name in branches:

            # 此处是不是如果存在该分支只需要更新即可？？
            print ("删除分支并且重新检出分支")

            """1. 首先切换成 Master 2. 更新 Master 分支 获取远端分支或者程序的更改 3. 删除输入的分支"""
            self.client().checkout(default)

            self.client().branch("-D", self.branch_name)

            self.client().pull()

            self.client().checkout(self.branch_name)

        else:

            self.client().checkout(self.branch_name)

            self.client().pull()

        messages = "switch branch {0} successful".format(self.branch_name)

        self.write_log().info(messages)

    # 检出代码
    def export_branch(self):

        print ("Export Branch {0}".format(self.branch_name))

        if os.path.exists(self.repo_export):
            shutil.rmtree(self.repo_export)

        if not os.path.exists(self.repo_export):
            os.makedirs(self.repo_export)

        # 检出 GIT 工作目录
        export_command = "{0} archive {1} | tar -x -C {2}".format(self.git_bin, self.branch_name, self.repo_export)

        FNULL = open(os.devnull, 'w')

        # 更换工作目录
        os.chdir(self.repo_path)

        ret_code = call(export_command, shell=True, stdout=FNULL, stderr=STDOUT)

        messages = "export branch {0} to {1} successful".format(self.branch_name, self.repo_export)

        self.write_log().info(messages)

        return ret_code