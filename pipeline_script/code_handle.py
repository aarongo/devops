#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author EdwardLiu

"""
前端项目更新与切换分支
"""

from subprocess import Popen, PIPE, call
import sys
from datetime import datetime
import os
import argparse


class Handle_Code(object):
    def __init__(self, e_git, p_code, b_name):
        # 分之名称
        self.branch_name = b_name
        # 源代码目录
        self.code_path = p_code
        # GIT环境变量
        self.git_bin = e_git

    # 删除分之
    def Delete_branch(self):
        # 删除除 master 外的所有的本地分之---明天做细化
        os.chdir(self.code_path)
        check_branch = "%s branch | wc -l" % self.git_bin
        if check_branch != "1":
            delete_branch = """%s checkout master && %s branch | grep -v "master" | xargs %s branch -D""" % (self.git_bin, self.git_bin, self.git_bin)
            delete_code = call(delete_branch, shell=True)
            if delete_code == 0:
                print "delete branch success"

    # 切换 GIT分之
    def Swith_branch(self):
        # 经验证后不更新不能获取新分支
        os.chdir(self.code_path)
        # git 直接切换分之
        if self.branch_name != 'master':
            swith_cmd = "%s pull;%s checkout --track origin/%s;%s pull" % (self.git_bin, self.git_bin, self.branch_name, self.git_bin)
            branch_swith = Popen(swith_cmd, shell=True, stdout=PIPE, stderr=PIPE)
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

    # 更新代码
    def code_update(self):
        print "\33[32m更新项目.......\033[0m"
        try:
            os.chdir(self.code_path)
            update_cmd = "%s pull" % self.git_bin
            code_update = Popen(update_cmd, shell=True, stdout=PIPE, stderr=PIPE)
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
                print "\033[32mUpdate Code Is successful\033[0m"
            else:
                print "\033[32mUpdate Code Is Failed\033[0m"
                print stderr
                sys.exit(1)
        except KeyboardInterrupt:
            print "\033[31m退出更新\033[0m"


if __name__ == '__main__':
    # 处理执行参数
    def check_arg(args=None):
        parser = argparse.ArgumentParser(description="EG: '%(prog)s' Build Front Code")
        parser.add_argument('-e', '--environment', help='input git environment')
        parser.add_argument('-b', '--branch', help='input git branch')
        parser.add_argument('-d', '--directory', help='input code dir')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        return parser.parse_args(args)

    args = check_arg(sys.argv[1:])

    # 获取外部传参
    git_bin = args.environment

    code_path = args.directory

    branch_name = args.branch

    # 重写类变量
    Run_Build = Handle_Code(e_git=git_bin, p_code=code_path, b_name=branch_name)

    # 执行方法
    Run_Build.Delete_branch()

    Run_Build.Swith_branch()

    Run_Build.code_update()
