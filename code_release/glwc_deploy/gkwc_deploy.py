#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu


import argparse
from subprocess import Popen, PIPE
import logging
import logging.config
import sys, os

# 编译后代码存放路径及推送目录
PROJECT_REPOSITORY = "/software/project_repository"
# code 存放位置
CODE_WORKSPACE = "/software/git_code_registroy/code"


# 部署记录日志
def recordlog():
    loger_path = "/software/script/logger.conf"
    logging.config.fileConfig(loger_path)
    logger = logging.getLogger("gkwc")
    return logger


def rollbacklog():
    loger_path = "/software/script/logger.conf"
    logging.config.fileConfig(loger_path)
    logger = logging.getLogger("success")
    return logger


# 获取代码最新版本号
def get_version():
    command = """git log --pretty=format:"%h" -1"""
    os.chdir(CODE_WORKSPACE)
    ret_code = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    if ret_code == 0:
        messages = "get git version success"
        recordlog().info(messages)
    stdout, stderr = ret_code.communicate()
    return stdout


# 推送项目文件
def pushproject(project_name):
    print "\033[32m等待项目文件推送......\033[0m"
    # 使用ansible rsync模块直接推送到远端
    push_project_directory = "%s/%s" % (PROJECT_REPOSITORY, project_name)
    push_command = """ansible-playbook /etc/ansible/roles/push.yml --extra-vars "hosts=%s src_dir=%s dest_dir=%s" """ % (
        project_name, push_project_directory, PROJECT_REPOSITORY)
    code_push = Popen(push_command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = code_push.communicate()
    messages = "project push to remote Server success "
    recordlog().info(messages)
    print stdout


# 部署项目
def deployproject(project_name, code_time, git_number, tags_name):
    print "\033[32m项目正在部署重启.....\033[0m"
    # ansible 处理软连接、重启项目、检测（脚本输出）项目状态
    ansible_path = "ansible-playbook"
    repository_path = "%s/%s" % (PROJECT_REPOSITORY, project_name)
    other_vars = "hosts=%s project_name=%s repository=%s time=%s git_number=%s" % (
        project_name, project_name, repository_path, code_time, git_number)
    playbook_path = "/etc/ansible/roles/gkwc_deploy.yml"
    deploy_command = """%s %s --tags %s --extra-vars "%s" """ % (
        ansible_path, playbook_path, tags_name, other_vars)
    print deploy_command
    code_deploy = Popen(deploy_command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = code_deploy.communicate()
    print stdout
    if code_deploy.returncode == 0:
        messages = "project deploy successful "
        recordlog().info(messages)
        messages_success = "%s#%s#%s" % (code_time, git_number, project_name)
        rollbacklog().info(messages_success)


# 检测以部署的项目
def checkdeploy():
    path = "/software/script/success.log"
    file_object = open(path, 'rU')
    list_tmp = {}
    try:
        for line in file_object:
            number = (line.split(':')[-1]).split('#')[1]
            d_time = (line.split(':')[-1]).split('#')[0]
            p_name = (line.split(':')[-1]).split('#')[2].strip('\n')
            list_tmp[number] = {"d_time": d_time, "p_name": p_name}
    finally:
        file_object.close()
    return list_tmp


# 回退部署
'''
根据项目已部署记录进行回退
'''


def rollbackdeploy(git_number, project_name, tags_name):
    for number in checkdeploy():
        pro_name = checkdeploy()[number]['p_name']
        if number == git_number and project_name == pro_name:
            code_time = checkdeploy()[number]['d_time']
            ansible_path = "ansible-playbook"
            repository_path = "%s/%s" % (PROJECT_REPOSITORY, project_name)
            other_vars = "hosts=%s project_name=%s repository=%s time=%s git_number=%s" % (
                project_name, project_name, repository_path, code_time, git_number)
            playbook_path = "/etc/ansible/roles/glwc.yml"
            rollback_command = """%s %s --tags %s --extra-vars "%s" """ % (
                ansible_path, playbook_path, tags_name, other_vars)
            rollback_code = Popen(
                rollback_command, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = rollback_code.communicate()
            print stdout
            if rollback_code.returncode == 0:
                messages = "project rollback successful git_number is %s" % git_number
                recordlog().info(messages)


def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="EG: '%(prog)s'  deploy or rollback glwc ht online")
    parser.add_argument(
        '-n', '--number', help='input git number allow is none')
    parser.add_argument('-p', '--project', choices=[
        'web', 'front', 'web-merchant'], help='input project name')
    parser.add_argument('-o', '--operate', choices=['rollback', 'deploy'])
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def main():
    args = check_arg(sys.argv[1:])
    if args.number is None:
        number = get_version()
    else:
        number = args.number
    # 时间  年-月-日
    # CODE_TIME = datetime.now().strftime("%Y-%m-%d")
    if args.operate == 'rollback':
        rollbackdeploy(git_number=number,
                       project_name=args.project, tags_name=args.operate)
    if args.operate == 'deploy':
        messages = "deploy git number:%s-deploy project:%s" % (number, args.project)
        recordlog().info(messages)
        pushproject(project_name=args.project)

        # 对比生成目录的时间(解决刚好在00:00执行的任务)
        get_dir_time_path = PROJECT_REPOSITORY + "/" + args.project

        def compare(x, y):
            stat_x = os.stat(get_dir_time_path + "/" + x)
            stat_y = os.stat(get_dir_time_path + "/" + y)
            if stat_x.st_ctime < stat_y.st_ctime:
                return -1
            elif stat_x.st_ctime > stat_y.st_ctime:
                return 1
            else:
                return 0

        # 获取最后生成的目录时间(相当于目录名称)
        last_time = os.listdir(get_dir_time_path)
        last_time.sort(compare)
        deployproject(project_name=args.project, code_time=last_time[-1], git_number=number, tags_name=args.operate)

if __name__ == '__main__':
    main()