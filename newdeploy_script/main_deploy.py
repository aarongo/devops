#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

from deploy_project import Deploy_Project
import argparse
import sys


def push_deploy(hosts, name, tags):

    # 初始化部署函数
    deploy = Deploy_Project(hosts, name)

    # 推送部署文件
    deploy.push_project()

    # 项目部署
    deploy.deploy_project(tags)


def check_arg(args=None):
    parser = argparse.ArgumentParser(description="EG: '%(prog)s'  build maven project")
    parser.add_argument('-p', '--project_name', choices=['wx', 'teamshop', 'restapi', 'erpdocke', 'web'], help='deploy project name')
    parser.add_argument('-t', '--tags', help='deploy way')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


# 针对项目名称与部署文件不对应
def project_name_handle(project_name):

    if project_name == "restapi":

        project = "mobile"

    elif project_name == "wxshop":

        project = "mobile"

    elif project_name == "wx":

        project = "mobile"

    elif project_name == "teamshop":

        project = "mobile"

    elif project_name == "erpdocke":

        project = "api"

    else:

        project = project_name

    return project


def main():

    # 获取所有参数
    args = check_arg(sys.argv[1:])

    hosts = args.project_name

    project_name = project_name_handle(args.project_name)

    tags_name = args.tags

    push_deploy(hosts, project_name, tags_name)


if __name__ == '__main__':

    main()


