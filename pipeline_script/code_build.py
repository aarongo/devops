#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

"""
前端项目编译打包
"""

from subprocess import PIPE, Popen
import os
from datetime import datetime
import sys
import argparse


class Code_Build_Tools(object):

    def __init__(self, e_git, p_name, e_yarn, b_env, export_path):
        # GIT 环境变量
        self.e_git = e_git
        # 项目民称
        self.p_name = p_name
        # 前端工具 yarn 环境变量
        self.e_yarn = e_yarn
        # 项目导出目录
        self.export_path = export_path
        # 项目编译环境名称
        self.b_env = b_env

    # 前端代码打包
    def Code_Build(self):
        build_cmd = ["%s install " % self.e_yarn, "%s build -t %s -e %s" % (self.e_yarn, self.p_name, self.b_env)]
        try:
            print "\033[32mBuilding....\033[0m"
            for cmd in build_cmd:
                time1 = datetime.now().strftime('%H:%M:%S')
                # 编译命令
                # 更换工作目录
                os.chdir(self.export_path)
                print "\033[32mCheckout Directory {0}\033[0m".format(self.export_path)
                # 运行编译命令
                build_status = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                # 显示编译进度---使用时间作为记录标识
                while True:
                    # 编译显示信息
                    build_info = "\033[32mRunBuilding-->Time:\033[0m" + datetime.now().strftime('%H:%M:%S')
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
        except KeyboardInterrupt:
            print "\033[32m 退出编译\033[0m"

if __name__ == '__main__':
    # 处理执行参数
    def check_arg(args=None):
        parser = argparse.ArgumentParser(description="EG: '%(prog)s' Build Front Code")
        parser.add_argument('-t', '--target', help='build project name')
        parser.add_argument('-e', '--environment', help='build env for online or test')
        parser.add_argument('-l', '--tools', help='project build tools')
        parser.add_argument('-g', '--git', help='project git path')
        parser.add_argument('-s', '--export', help='prject export path')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        return parser.parse_args(args)

    args = check_arg(sys.argv[1:])

    git_bin = args.git

    export_dir = args.export

    target_name = args.target

    env_name = args.environment

    yarn_tools = args.tools

    run_export = Code_Build_Tools(
        e_git=git_bin,
        p_name=target_name,
        e_yarn=yarn_tools,
        export_path=export_dir,
        b_env=env_name
    )

    run_export.Code_Build()