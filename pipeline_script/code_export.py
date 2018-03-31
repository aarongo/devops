#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

"""
前端项目检出
"""

import os
import shutil
from subprocess import call, STDOUT
import argparse
import sys


class Code_Export(object):

    def __init__(self, p_code, export_path, b_name, e_git):
        # 源代码目录
        self.p_code = p_code
        # GIT环境变量
        self.e_git = e_git
        # 源代码导出目录
        self.export_path = export_path
        # 分之名
        self.b_name = b_name

    # 检出代码
    def front_codeexport(self):
        print "\033[32m等待检出目录........\033[0m"
        if os.path.exists(self.export_path):
            shutil.rmtree(self.export_path)
            os.makedirs(self.export_path)
        else:
            os.makedirs(self.export_path)
        export_cmd = "%s archive %s | tar -x -C %s" % (self.e_git, self.b_name, self.export_path)
        r_null = open(os.devnull, 'w')
        # 更换工作目录, 导出纯净代码
        os.chdir(self.p_code)
        ret_code = call(export_cmd, shell=True, stdout=r_null, stderr=STDOUT)
        if ret_code == 0:
            print "\033[32m 检出目录成功.....\033[0m"


if __name__ == '__main__':
    # 处理执行参数
    def check_arg(args=None):
        parser = argparse.ArgumentParser(description="EG: '%(prog)s' Build Front Code")
        parser.add_argument('-t', '--export', help='export code')
        parser.add_argument('-e', '--environment', help='git env')
        parser.add_argument('-b', '--branch', help='branch name')
        parser.add_argument('-s', '--directory', help='source code ')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        return parser.parse_args(args)

    args = check_arg(sys.argv[1:])

    git_bin = args.environment

    code_path = args.directory

    branch_name = args.branch

    export_dir = args.export

    run_export = Code_Export(
        p_code=code_path,
        e_git=git_bin,
        export_path=export_dir,
        b_name=branch_name
    )

    run_export.front_codeexport()