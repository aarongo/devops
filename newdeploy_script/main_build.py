#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

"""
所有工程统一进行编译
"""

from handle_git import Custom_Git as git
from m_project_build import Maven_Build as maven
import argparse
import sys


def code_operation(branch, project):

    # 初始化 GIT 操作
    opera = git(branch, project)

    # 切换分之
    opera.branch_switch()

    # 检出分之
    opera.export_branch()


def code_build(branch):

    # 初始化 maven 操作
    opera = maven(branch)

    # 前端文件拷贝
    opera.Transfer_File()

    # 代码编译
    opera.Maven_Code_Build()

    # 生成文件处理
    opera.Files_Handle()


def check_arg(args=None):
    parser = argparse.ArgumentParser(description="EG: '%(prog)s'  build maven project")
    parser.add_argument('-p', '--project', default='default', help='branch name')
    parser.add_argument('-b', '--branch', help='branch name')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def main():
    # 接收所有参数
    args = check_arg(sys.argv[1:])

    branch_name = args.branch

    project_name = args.project

    code_operation(branch_name, project_name)

    code_build(branch_name)


if __name__ == '__main__':

    main()