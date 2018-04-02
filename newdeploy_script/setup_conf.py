#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

"""
初始化项目配置文件--生成project.log
"""


import ConfigParser
import os
import argparse
import sys


class Custom_Conf(object):

    def __init__(self, repo_path, repo_export_path, env, repository, project_name, project_version, conf_path, strong_path):
        self.repo_path = repo_path
        self.repo_export_path = repo_export_path
        self.env = env
        self.repository = repository
        self.project_name = project_name
        self.project_version = project_version
        self.conf_path = conf_path
        self.strong_path = strong_path

    # 配置配置文件
    def init_conf(self):

        conf_path = os.path.abspath(os.path.dirname(__file__))

        conf = ConfigParser.ConfigParser()

        conf.read("{0}/base.conf".format(conf_path))

        # 设置版本库路径
        conf.set("repo", "repo_path", "{0}".format(self.repo_path))

        # 设置版本库导出路径
        conf.set("repo", "repo_export_path", "{0}".format(self.repo_export_path))

        # 设置项目编译参数--环境--对应 pom.xml 标签
        conf.set("build-options", "env", "{0}".format(self.env))

        # 设置项目文件存放位置
        conf.set("repository", "path", "{0}".format(self.repository))

        # 设置项目部署文件名
        conf.set("project", "name", "{0}".format(self.project_name))
        conf.set("project", "version", "{0}".format(self.project_version))

        # 日志配置文件位置
        conf.set("log_path", "conf_path", "{0}".format(self.conf_path))

        # 配置脚本存放路径
        conf.set("strong", "strong_path", "{0}".format(self.strong_path))

        with open("{0}/project.conf".format(conf_path), "w+") as f:
            conf.write(f)


# 初始化传入参数 repo_path, repo_export_path, env, repository, project_name, project_version
def check_arg(args=None):
    parser = argparse.ArgumentParser(description="EG: '%(prog)s'  生成部署脚本所需配置")
    parser.add_argument('-r', '--repo_path', help='版本库路径')
    parser.add_argument('-e', '--export_path', help='版本库导出路径')
    parser.add_argument('-s', '--env', help='项目编译参数--环境--对应 pom.xml 标签')
    parser.add_argument('-t', '--repository', help='项目文件存放位置')
    parser.add_argument('-p', '--project_name', help='项目部署文件名-名称')
    parser.add_argument('-v', '--project_version', help='项目部署文件名-版本')
    parser.add_argument('-c', '--conf_path', help='项目记录日志配置文件')
    parser.add_argument('-d', '--strong_path', help='项目脚本存放路径')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def main():
    args = check_arg(sys.argv[1:])
    repo_path = args.repo_path
    export_path = args.export_path
    env = args.env
    repository = args.repository
    project_name = args.project_name
    project_version = args.project_version
    conf_path = args.conf_path
    strong_path = args.strong_path
    setup = Custom_Conf(repo_path, export_path, env, repository, project_name, project_version, conf_path, strong_path)
    setup.init_conf()


if __name__ == '__main__':
    main()