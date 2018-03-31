#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author EdwardLiu

"""
后端项目检出
"""

import argparse
import sys
from subprocess import PIPE, Popen, call
import os
from datetime import datetime


class Maven_CodeUpdate(object):
    def __init__(self, code_path, e_git, branch_name):

        self.code_path = code_path
        self.e_git = e_git
        self.branch_name = branch_name

    # 删除分之
    def Delete_branch(self):
        # 删除除 master 外的所有的本地分之---明天做细化
        os.chdir(self.code_path)
        check_branch = "%s branch | wc -l" % self.e_git
        if check_branch != "1":
            delete_branch = """%s checkout master && %s branch | grep -v "master" | xargs %s branch -D""" % (
                self.e_git, self.e_git, self.e_git)
            delete_code = call(delete_branch, shell=True)
            if delete_code == 0:
                print "delete branch success"

    # 切换 GIT分之
    def Swith_branch(self):
        # 经验证后不更新不能获取新分支
        os.chdir(self.code_path)
        # git 直接切换分之
        if self.branch_name != 'master':
            swith_cmd = "%s pull;%s checkout --track origin/%s;%s pull" % (self.e_git, self.e_git, self.branch_name, self.e_git)
            branch_swith = Popen(
                swith_cmd, shell=True, stdout=PIPE, stderr=PIPE)
            while True:
                # 显示信息
                update_info = "\033[32mRuncheckout-->Time:\033[0m" + datetime.now().strftime('%H:%M:%S')
                # 获取输出
                newline = branch_swith.stdout.readline()
                # 如果没有输出就退出
                if newline == '' and branch_swith.poll() is not None:
                    break
                # 打印信息
                sys.stdout.write('%s\r' % update_info)
                # 刷新打印缓存
                sys.stdout.flush()
            stdout, stderr = branch_swith.communicate()
            if branch_swith.returncode == 0:
                print "\033[32mCheckout Branch: %s Is successful\033[0m" % self.branch_name
            else:
                print "\033[32mCheckout Branch: %s Is Failed\033[0m"
                print stderr
                sys.exit(1)
        else:
            print "\033[32m当前分支以是Master 不需要切换.....\033[0m"

    # git Update
    def Code_Update(self):
        print "\33[32m等待更新Maven项目\033[0m"
        try:
            os.chdir(self.code_path)
            cmd = "{0} pull".format(self.e_git)
            code_update = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            while True:
                # 编译显示信息
                update_info = "\033[32mRunupdate-->Time:\033[0m" + datetime.now().strftime('%H:%M:%S')
                # 获取编译输出
                newline = code_update.stdout.readline()
                # 如果没有输出就退出
                if newline == '' and code_update.poll() is not None:
                    break
                # 打印编译信息
                sys.stdout.write('%s\r' % update_info)
                # 刷新打印缓存
                sys.stdout.flush()
            stdout, stderr = code_update.communicate()
            if code_update.returncode == 0:
                print "\033[32mUpdate Maven Project carrefour_online Is successful\033[0m"
            else:
                print "\033[32mUpdate Maven Project carrefour_online Is Failed\033[0m"
                print stderr
                sys.exit(1)
        except KeyboardInterrupt:
            print "\033[31m退出更新\033[0m"


if __name__ == '__main__':

    def check_arg(args=None):
        parser = argparse.ArgumentParser(
            description="EG: '%(prog)s' Build Front Code")
        parser.add_argument('-s', '--codepath', help='prject export path')
        parser.add_argument('-b', '--branch', help='maven project branch name')
        parser.add_argument('-e', '--git', help='branch name')
        parser.add_argument(
            '-v', '--version', action='version', version='%(prog)s 1.0')
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        return parser.parse_args(args)

    args = check_arg(sys.argv[1:])

    source_codepath = args.codepath

    git_bin = args.git

    b_name = args.branch

    run_maven = Maven_CodeUpdate(
        code_path=source_codepath, e_git=git_bin, branch_name=b_name)

    run_maven.Delete_branch()

    run_maven.Swith_branch()

    run_maven.Code_Update()
