#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu


import git
from subprocess import STDOUT, call
import shutil
import os
from config_base import Read_Conf as readconfig


class Custom_Git(object):

    def __init__(self, config=readconfig().o_conf()):

        if config != 1:

            self.repo_path = config.get("repo", "repo_path")

            self.repo_export = config.get("repo", "repo_export_path")

            self.git_bin = config.get("system", "git_bin")

    def client(self):

        repo = git.Repo(self.repo_path)

        client = repo.git

        return client

    # 版本信息
    def branch_version(self):

        version = self.client().log("--pretty=format:'%h'", "-1")

        return version

    # 切换分支
    def branch_switch(self, branch_name):

        # 所有分支
        branches = self.client().branch()

        # 默认分支
        default = "master"

        # 处理同一分支部署多次
        if branch_name in branches:

            """1. 首先切换成 Master 2. 更新 Master 分支 获取远端分支或者程序的更改 3. 删除输入的分支"""
            self.client().checkout(default)

            self.client().branch("-D", branch_name)

            self.client().pull()

            self.client().checkout(branch_name)

        else:

            self.client().checkout(branch_name)

            self.client().pull()

    # 检出代码
    def export_branch(self, branch_name):

        if os.path.exists(self.repo_export):
            shutil.rmtree(self.repo_export)

        if not os.path.exists(self.repo_export):
            os.makedirs(self.repo_export)

        # 检出 GIT 工作目录
        export_command = "{0} archive {1} | tar -x -C {2}".format(self.git_bin, branch_name, self.repo_export)

        FNULL = open(os.devnull, 'w')

        # 更换工作目录
        os.chdir(self.repo_path)

        ret_code = call(export_command, shell=True, stdout=FNULL, stderr=STDOUT)

        return ret_code