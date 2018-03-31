#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author EdwardLiu

"""
后端项目检出
"""

import os
from subprocess import call, STDOUT
import shutil
import sys
import argparse


class Maven_Export(object):
    def __init__(self, e_git, export_path, b_name, s_code):
        # maven 项目源码目录
        self.s_code = s_code
        self.e_git = e_git
        # 源代码检出目录
        self.export_path = export_path
        self.b_name = b_name

    # git export
    def Code_Export(self):
        print "\033[32m等待检出Maven Project目录........\033[0m"
        if os.path.exists(self.export_path):
            shutil.rmtree(self.export_path)
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
        # 检出 SVN 工作目录
        export_command = "{0} archive {1} | tar -x -C {2}".format(self.e_git, self.b_name, self.export_path)
        FNULL = open(os.devnull, 'w')
        # 更换工作目录
        os.chdir(self.s_code)
        ret_code = call(export_command, shell=True, stdout=FNULL, stderr=STDOUT)
        if ret_code == 0:
            print "Maven Project code export success"


def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="EG: '%(prog)s' Build Front Code")
    parser.add_argument('-s', '--source', help='prject export path')
    parser.add_argument('-b', '--branch', help='maven project branch name')
    parser.add_argument('-p', '--export', help='maven project export path')
    parser.add_argument('-e', '--git', help='branch name')
    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def main():

    args = check_arg(sys.argv[1:])

    s_codepath = args.source

    git_bin = args.git

    p_export = args.export

    branch_name = args.branch

    run_mavenproject = Maven_Export(
        e_git=git_bin,
        export_path=p_export,
        s_code=s_codepath,
        b_name=branch_name
    )
    run_mavenproject.Code_Export()


if __name__ == '__main__':
    main()