#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

"""
处理前端代码编译完成后生成的文件进行处理
"""


import os
import shutil
import argparse
import sys


class Build_File(object):

    def __init__(self, b_name, export_path):

        # 前端分支名称
        self.b_name = b_name

        # 前端项目检出目录
        self.export_path = export_path

    # 编译后文件处理
    def Build_File_Handle(self):

        print "\033[32m整理编译后文件....\033[0m"
        """
            # 处理前端代码编译后对生成文件的处理
            1. 将编译好的文件根据分之名与时间进行区分
            2. 将区分后的目录拷贝到maven 项目对应目录下
        """
        after_path_src = "%s/%s" % (self.export_path, "dist")

        after_path = "%s/%s" % (self.export_path, self.b_name)

        if os.path.exists(after_path):

            shutil.rmtree(after_path)

            shutil.copytree(after_path_src, after_path)

        else:

            shutil.copytree(after_path_src, after_path)


if __name__ == '__main__':
    # 处理执行参数
    def check_arg(args=None):
        parser = argparse.ArgumentParser(description="EG: '%(prog)s' Build Front Code")
        parser.add_argument('-s', '--export', help='prject export path')
        parser.add_argument('-b', '--branch', help='branch name')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        return parser.parse_args(args)

    args = check_arg(sys.argv[1:])

    export_dir = args.export

    branch_name = args.branch

    run_handle_file = Build_File(
        b_name=branch_name,
        export_path=export_dir
    )

    run_handle_file.Build_File_Handle()