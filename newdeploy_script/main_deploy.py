#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

from deploy_project import Deploy_Project
import argparse
import sys


def push_deploy(name, tags):

    # 初始化部署函数
    deploy = Deploy_Project(name)

    # 推送部署文件
    deploy.push_project()

    # 项目部署
    deploy.deploy_project(tags)


def check_arg(args=None):
    parser = argparse.ArgumentParser(description="EG: '%(prog)s'  build maven project")
    parser.add_argument('-p', '--project_name', help='deploy project name')
    parser.add_argument('-t', '--tags', help='deploy way')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def main():

    # 获取所有参数
    args = check_arg(sys.argv[1:])

    project_name = args.project_name

    tags_name = args.tags

    push_deploy(project_name, tags_name)


if __name__ == '__main__':

    main()


