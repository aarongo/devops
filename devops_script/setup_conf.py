#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

"""
初始化项目配置文件--生成project.log
"""


import argparse
import ConfigParser
import os
import sys


class Custom_Conf(object):

    def __init__(self, repo_path, repo_export_path, env, repository, project_name, project_version, conf_path, logs_path, wx_repo, wx_repo_export, team_repo, team_repo_export):
        self.repo_path = repo_path
        self.repo_export_path = repo_export_path
        self.env = env
        self.repository = repository
        self.project_name = project_name
        self.project_version = project_version
        self.conf_path = conf_path
        self.logs_path = logs_path
        self.wx_repo = wx_repo
        self.wx_repo_export = wx_repo_export
        self.team_repo = team_repo
        self.team_repo_export = team_repo_export

    # 配置配置文件
    def init_conf(self):

        conf_path = "{0}/{1}".format(os.path.abspath(os.path.dirname(__file__)), "conf")

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
        conf.set("conf", "path", "{0}".format(self.conf_path))

        # 配置脚本存放路径
        conf.set("logs", "path", "{0}".format(self.logs_path))

        # 配置前端仓库地址
        conf.set("repo_front", "repo_path", "{0}".format(self.wx_repo))
        conf.set("repo_front", "repo_path_two", "{0}".format(self.team_repo))
        conf.set("repo_front", "repo_export_path", "{0}".format(self.wx_repo_export))
        conf.set("repo_front", "repo_export_path_two", "{0}".format(self.team_repo_export))

        with open("{0}/project.conf".format(conf_path), "w+") as f:
            conf.write(f)


# 初始化传入参数 repo_path, repo_export_path, env, repository, project_name, project_version
def check_arg(args=None):
    parser = argparse.ArgumentParser(description="EG: '%(prog)s'  生成部署脚本所需配置")
    parser.add_argument('-r', '--repo_path', help='后端项目版本库路径')
    parser.add_argument('-e', '--export_path', help='后端项目版本库导出路径')
    parser.add_argument('-s', '--env', help='后端项目项目编译参数--环境--对应 pom.xml 标签')
    parser.add_argument('-t', '--repository', help='后端项目文件存放位置')
    parser.add_argument('-p', '--project_name', help='后端项目部署文件名-名称')
    parser.add_argument('-v', '--project_version', help='后端项目部署文件名-版本')
    parser.add_argument('-c', '--conf_path', help='项目配置文件')
    parser.add_argument('-d', '--logs_path', help='项目日志存放路径')
    parser.add_argument('-w', '--wx_repo', help='微信版本库路径')
    parser.add_argument('-x', '--wx_repo_export', help='微信版本库导出路径')
    parser.add_argument('-m', '--tm_repo', help='拼团版本库路径')
    parser.add_argument('-g', '--tm_repo_export', help='拼团版本库导出路径')
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
    strong_path = args.logs_path
    wx_repo = args.wx_repo
    wx_export = args.wx_repo_export
    tm_repo = args.tm_repo
    tm_export = args.tm_repo_export
    setup = Custom_Conf(repo_path, export_path, env, repository, project_name, project_version, conf_path, strong_path, wx_repo, wx_export, tm_repo, tm_export)
    setup.init_conf()


if __name__ == '__main__':
    main()
