#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
@author: EdwardLiu 
@contact: lonnyliu@126.com

@file: main_f_build.py
@time: 2018/4/10 15:35

"""
import argparse
import sys

from utils.f_project_build import Front_Project as wx
from utils.f_teamshop_build import Front_Project as team
from utils.handle_git import Custom_Git as git


def code_operation(branch, project):

    # 初始化 GIT 操作
    opera = git(branch, project)

    # 切换分之
    opera.branch_switch()

    # 检出分之
    opera.export_branch()


def code_build_wx(branch, project):

    # 初始化 maven 操作
    opera = wx(branch, project)

    # 代码编译
    opera.Build()

    # 生成文件处理
    opera.file_handle()


def code_build_team(branch):

    # 初始化 maven 操作
    opera = team(branch)

    # 代码编译
    opera.Build()

    # 生成文件处理
    opera.file_handle()


#
def name_process(branch_name, project):

    if project == 'wxshop':

        code_operation(branch_name, "wxshop")

        code_build_wx(branch_name, "wxshop")

    elif project == 'teamshop':

        code_operation(branch_name, 'teamshop')

        code_build_team(branch_name)


def check_arg(args=None):
    parser = argparse.ArgumentParser(description="EG: '%(prog)s'  build maven project")
    parser.add_argument('-p', '--project', default=['wxshop', 'teamshop'], help="需要编译的环境")
    parser.add_argument('-b', '--branch', default='master', help='分之名称')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    return parser.parse_args(args)


def main():
    # 接收所有参数
    args = check_arg(sys.argv[1:])

    branch_name = args.branch

    project = args.project

    # 增加个例化项目配置
    if isinstance(project, list):
        for name in project:

            name_process(project=name, branch_name=branch_name)

    else:

        name_process(project=project, branch_name=branch_name)


if __name__ == '__main__':

    main()

