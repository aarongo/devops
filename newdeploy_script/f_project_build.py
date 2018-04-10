#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/4/6 下午2:23
# @Author : EdwardLiu
# @Site :
# @File : f_project_build.py

import os
import sys
from datetime import datetime
from subprocess import PIPE, Popen

from config_base import Read_Conf as readconfig
from handle_git import Custom_Git as git


class Front_Project(object):

    def __init__(self, branch, project, conf=readconfig().o_conf()):

        self.branch_name = branch

        self.project = project

        self.repo_path = conf.get("repo_front", "repo_path")

        self.repo_export = conf.get("repo_front", "repo_export_path")

        self.npm_bin = conf.get("system", "npm_bin")

        self.yarn_bin = conf.get("system", "yarn_bin")

        self.build_env = conf.get("front-build-options", "build_env")

        self.build_way = conf.get("front-build-options", "build_way")

    # 编译前端代码
    def Build(self):

        build_cmd = ["{0} install ".format(self.npm_bin), "{0} {1} -t {2}} -e {3}}".format(
            self.yarn_bin, self.build_way, self.project, self.build_env)]

        build_return_code = 0

        try:
            for cmd in build_cmd:
                time1 = datetime.now().strftime('%H:%M:%S')
                # 编译命令
                # 更换工作目录
                os.chdir(self.repo_export)
                # 运行编译命令
                build_status = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                # 显示编译进度---使用时间作为记录标识
                while True:
                    # 编译显示信息
                    build_info = "\033[32mRunBuilding-->Time:\033[0m" + \
                        datetime.now().strftime('%H:%M:%S')
                    # 获取编译输出
                    nextline = build_status.stdout.readline()
                    # 如果没有输出就退出
                    if nextline == '' and build_status.poll() is not None:
                        break
                    # 显示部署进度
                    # sys.stdout.write('%s\r' % build_info)
                    # 打印编译信息
                    sys.stdout.write(nextline)
                    # 刷新打印缓存
                    sys.stdout.flush()
                stdout, stderr = build_status.communicate()

                time2 = datetime.now().strftime('%H:%M:%S')
                # 计算时间差
                FMT = '%H:%M:%S'
                time_diff = datetime.strptime(
                    time2, FMT) - datetime.strptime(time1, FMT)
                if build_status.returncode == 0:
                    print "\033[33m编译用时:\033[0m" + "%s" % time_diff
                    print "\033[32mBuild Code Is successful cmd is %s\033[0m" % cmd
                else:
                    print "\033[32mBuild code Is Failed cmd is %s\033[0m" % cmd
                    print stderr
                build_return_code += build_status.returncode
            return build_return_code
        except KeyboardInterrupt:
            exit(1)
