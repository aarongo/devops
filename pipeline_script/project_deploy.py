#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author EdwardLiu

import os
from subprocess import Popen, PIPE
import sys
from datetime import datetime
import zipfile
import argparse


class Project_Deploy(object):
    def __init__(self, project_name, b_name, codeexport, deploy_way,
                 deploy_time, project_repo, git_number):
        # 项目版本
        self.git_number = git_number
        # 项目部署方式
        self.deploy_way = deploy_way
        # 项目处理时间
        self.deploy_time = deploy_time
        # 项目名称
        self.project_name = project_name
        # 代码检出目录
        self.code_export = codeexport
        # 分支名称
        self.branch_name = b_name
        # 编译后代码存放路径及推送目录
        self.project_repo = project_repo

    # 代码编译
    def codebuild(self):
        try:
            time1 = datetime.now().strftime('%H:%M:%S')
            # 编译命令
            CODE_BUILD_COMMAND = "mvn clean install -Pzmsy_test -Dmaven.test.skip=true"
            # 更换工作目录
            os.chdir(self.code_export)
            # 运行编译命令
            build_status = Popen(CODE_BUILD_COMMAND, shell=True, stdout=PIPE, stderr=PIPE)
            # 显示编译进度---使用时间作为记录标识
            while True:
                # 编译显示信息
                build_info = "\033[32mRunBuilding-->Time:\033[0m" + \
                    datetime.now().strftime('%H:%M:%S')
                # 获取编译输出
                nextline = build_status.stdout.readline()
                # 如果没有输出就退出
                if nextline == '' and build_status.poll() is not None:
                    break
                # 显示部署进度
                # sys.stdout.write('%s\r' % build_info)
                # 打印编译信息
                sys.stdout.write(nextline)
                # 刷新打印缓存
                sys.stdout.flush()
            stdout, stderr = build_status.communicate()

            time2 = datetime.now().strftime('%H:%M:%S')
            # 计算时间差
            FMT = '%H:%M:%S'
            time_diff = datetime.strptime(time2, FMT) - datetime.strptime(
                time1, FMT)
            if build_status.returncode == 0:
                print "\033[33m编译用时:\033[0m" + "%s" % time_diff
                print "\033[32mBuild syzm_online Is successful\033[0m"
            else:
                print "\033[32mBuild syzm_test Is Failed\033[0m"
                print stderr
            return build_status.returncode
        except KeyboardInterrupt:
            print "\033[32m 退出编译\033[0m"

    # 文件处理
    def codewar(self):
        print "\033[32m项目包(%s)处理.请等待...........\033[0m" % self.project_name
        # 项目名称
        CODE_WAR_NAME = "sy-cybershop-%s-3.1.1-SNAPSHOT" % self.project_name
        PROJECT_PATH = "%s/%s/%s/%s/%s" % (self.project_repo, self.project_name, self.deploy_time, self.git_number, CODE_WAR_NAME)
        if not os.path.exists(PROJECT_PATH):
            os.makedirs(PROJECT_PATH)
        # 项目包生成路径
        PROJECT_WAR_PATH = "%s/cybershop-%s/target/%s" % (self.code_export, self.project_name, CODE_WAR_NAME) + ".war"
        # 直接将项目包解压到项目目录
        try:
            zip_ref = zipfile.ZipFile(PROJECT_WAR_PATH, 'r')
            zip_ref.extractall(PROJECT_PATH)
            zip_ref.close()
            print "\033[32m项目包(%s)处理完成!!!\033[0m" % self.project_name
        except IOError:
            print "\033[31m%s Is Not Exists Please Run bulid\033[0m" % PROJECT_WAR_PATH

    # 推送项目文件
    def pushproject(self):
        print "\033[32m等待项目文件推送......\033[0m"
        # 使用ansible rsync模块直接推送到远端
        push_project_directory = "%s/%s" % (self.project_repo, self.project_name)
        push_command = """ansible-playbook /etc/ansible/roles/push_v1.yml --extra-vars "hosts=%s src_dir=%s dest_dir=%s" """ % (self.project_name, push_project_directory, self.project_repo)
        code_push = Popen(push_command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = code_push.communicate()
        print stdout

    # 部署项目
    def deployproject(self):
        print "\033[32m项目正在部署重启.....\033[0m"
        # ansible 处理软连接、重启项目、检测（脚本输出）项目状态
        ansible_path = "ansible-playbook"
        repository_path = "%s/%s" % (self.project_repo, self.project_name)
        other_vars = "hosts=%s project_name=%s repository=%s time=%s git_number=%s" % (self.project_name, self.project_name, repository_path, self.deploy_time, self.git_number)
        playbook_path = "/etc/ansible/roles/syzm.yml"
        deploy_command = """%s %s --tags %s --extra-vars "%s" """ % (ansible_path, playbook_path, self.deploy_way, other_vars)
        code_deploy = Popen(deploy_command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = code_deploy.communicate()
        print stdout


def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="EG: '%(prog)s'  deploy or rollback syzm ht online")
    parser.add_argument('-b', '--branch', help='input git branch')
    parser.add_argument('-p', '--project', choices=['mobilewap', 'wxshop'], help='input project name')
    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


# get git last number
def get_version(project_repo):
    command = """git log --pretty=format:"%h" -1"""
    os.chdir(project_repo)
    ret_code = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = ret_code.communicate()
    return stdout


def main():

    args = check_arg(sys.argv[1:])

    # 项目根目录
    project_base_repo = "/software/git_code_registroy/ld"

    way_deploy = "deploy"

    time_deploy = datetime.now().strftime("%Y-%m-%d")

    if args.project == "mobilewap":
        p_name = "wap"
    else:
        p_name = args.project

    codeexport_path = "/software/git_code_export/syzm_test"

    p_repo = "/software/project_repository"

    branch_name = args.branch

    number_git = get_version(project_base_repo)

    Run_build = Project_Deploy(
        git_number=number_git,
        project_name=p_name,
        deploy_way=way_deploy,
        b_name=branch_name,
        codeexport=codeexport_path,
        deploy_time=time_deploy,
        project_repo=p_repo)

    Run_build.codebuild()

    Run_build.codewar()

    Run_build.pushproject()

    Run_build.deployproject()


if __name__ == '__main__':
    main()