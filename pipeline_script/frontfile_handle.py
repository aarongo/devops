#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author EdwardLiu

"""
前端编译后生成文件处理--传送的后端项目中
"""


import os
import shutil
import argparse
import sys


class File_Handle(object):
    def __init__(self, project_name, f_export, b_export, f_branch):
        self.f_branch = f_branch
        self.f_export = f_export
        self.b_export = b_export
        self.project_name = project_name

    # 处理前端项目文件
    def Transfer_File(self):

        if self.project_name == "mobilewap":
            # 后端存放前端文件路径
            maven_project_front_path = "{0}/cybershop-{1}/src/main/webapp/{2}".format(self.b_export, "wap", "wap")
        else:
            maven_project_front_path = "{0}/cybershop-{1}/src/main/webapp/{2}".format(self.b_export, self.project_name, self.project_name)

        # 前端生成文件
        frontfile_path = "{0}/{1}".format(self.f_export, self.f_branch)

        if os.path.exists(maven_project_front_path):

            shutil.rmtree(maven_project_front_path)

            shutil.copytree(frontfile_path, maven_project_front_path)

        else:

            shutil.copytree(frontfile_path, maven_project_front_path)


def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="EG: '%(prog)s' Build Front Code")
    parser.add_argument('-f', '--frontexport', help='front export path')
    parser.add_argument('-b', '--branch', help='front project branch name')
    parser.add_argument('-p', '--project', help='maven project export path')
    parser.add_argument('-d', '--mavenexport', help='maven project exprot path')
    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def main():

    args = check_arg(sys.argv[1:])

    front_export = args.frontexport

    branch_name = args.branch

    project_name = args.project

    maven_exprot = args.mavenexport

    run_handle = File_Handle(
        project_name=project_name,
        f_export=front_export,
        b_export=maven_exprot,
        f_branch=branch_name
    )

    run_handle.Transfer_File()


if __name__ == '__main__':
    main()