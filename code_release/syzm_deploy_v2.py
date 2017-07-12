#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: liuyulong@co-mall.com


"""
解决部署时处理软连接
原因：在部署项目的时候有可能存在要挂载静态资源 所以一次性都推过去会冲掉原有的软连接 影响线上使用
改进：
1. 部署推送的时候改为按项目推送 避免一次部署推送所有冲掉软连接
2. 增加部署速度提高准确率
更改后：
在目录结构层增加项目名称一层目录 更改推送配置文件为根据输入的部署项目进行推送相应的目录
"""



import argparse
import logging
import logging.config
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from subprocess import Popen, PIPE
import static_deploy

# jenkins 工作目录
# JENKINS_WORKBASW = "/software/Jenkins_Home/jobs/syzm_test/workspace"
# code 存放位置
CODE_WORKSPACE = "/software/code_registroy/syzm_test"
# 代码 export 目录
CODE_EXPORT = "/software/code_export"
# 代码 export 名称
CODE_EXPORT_NAME = "syzm_test"
# export 路径
export_path = "%s/%s" % (CODE_EXPORT, CODE_EXPORT_NAME)
# 编译后代码存放路径及推送目录
PROJECT_REPOSITORY = "/software/project_repository"


# 部署记录日志
def recordlog():
    loger_path = "/software/script/logger.conf"
    logging.config.fileConfig(loger_path)
    logger = logging.getLogger("syzm")
    return logger

'''
记录部署成功日志
回退部署时调用此日志进行回退
'''


def rollbacklog():
    loger_path = "/software/script/logger.conf"
    logging.config.fileConfig(loger_path)
    logger = logging.getLogger("success")
    return logger


# svn Update
def codeupdate(number):
    print "\33[32m等待更新项目\033[0m"
    try:
        os.chdir(CODE_WORKSPACE)
        SVN_UPDATE_COMMAND = "svn update -r %s" % number
        code_update = Popen(SVN_UPDATE_COMMAND, shell=True,
                            stdout=PIPE, stderr=PIPE)
        while True:
            # 编译显示信息
            update_info = "\033[32mRunupdate-->Time:\033[0m" + \
                datetime.now().strftime('%H:%M:%S')
            # 获取编译输出
            newline = code_update.stdout.readline()
            # 如果没有输出就退出
            if newline == '' and code_update.poll() is not None:
                break
            # 打印编译信息
            sys.stdout.write('%s\r' % update_info)
            # 刷新打印缓存
            sys.stdout.flush()
        stdout, stderr = code_update.communicate()
        if (code_update.returncode == 0):
            print "\033[32mUpdate syzm_test Is successful\033[0m"
            messages = "update code success"
            recordlog().info(messages)
        else:
            print "\033[32mUpdate syzm_test Is Failed\033[0m"
            print stderr
    except KeyboardInterrupt:
        print "\033[31m退出更新\033[0m"


# svn export
def codeexport():
    print "\033[32m等待检出目录........\033[0m"
    if os.path.exists(export_path):
        shutil.rmtree(export_path)
    if not os.path.exists(CODE_EXPORT):
        os.makedirs(CODE_EXPORT)
    # 检出 SVN 工作目录
    export_command = "svn export %s %s/%s" % (CODE_WORKSPACE, CODE_EXPORT, CODE_EXPORT_NAME)
    FNULL = open(os.devnull, 'w')
    ret_code = subprocess.call(export_command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    if ret_code == 0:
        messages = "code export success"
        recordlog().info(messages)
    return ret_code


# 代码编译
def codebuild():
    try:
        if codeexport() == 0:
            time1 = datetime.now().strftime('%H:%M:%S')
            # 编译命令
            CODE_BUILD_COMMAND = "mvn clean install -Pzmsy_test -DskipTests"
            # 更换工作目录
            os.chdir(export_path)
            # 运行编译命令
            build_status = Popen(CODE_BUILD_COMMAND,
                                 shell=True, stdout=PIPE, stderr=PIPE)
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
            time_diff = datetime.strptime(
                time2, FMT) - datetime.strptime(time1, FMT)
            if build_status.returncode == 0:
                print "\033[33m编译用时:\033[0m" + "%s" % time_diff
                print "\033[32mBuild syzm_test Is successful\033[0m"
                messages = "build code success"
                recordlog().info(messages)
            else:
                print "\033[32mBuild syzm_test Is Failed\033[0m"
                messages = "build code Failed"
                recordlog().info(messages)
                print stderr
            return build_status.returncode
    except KeyboardInterrupt:
        print "\033[32m 退出编译\033[0m"


# 文件处理
def codewar(version, project_name, code_time):
    if codebuild() == 0:
        print "\033[32m项目包处理.请等待...........\033[0m"
        # 项目名称
        CODE_WAR_NAME = "sy-cybershop-%s-3.1.1-SNAPSHOT" % project_name
        PROJECT_PATH = "%s/%s/%s/%s/%s" % (PROJECT_REPOSITORY, project_name, code_time, version, CODE_WAR_NAME)
        if not os.path.exists(PROJECT_PATH):
            os.makedirs(PROJECT_PATH)
        # 项目包生成路径
        PROJECT_WAR_PATH = "%s/cybershop-%s/target/%s" % (
            export_path, project_name, CODE_WAR_NAME) + ".war"
        # 直接将项目包解压到项目目录
        try:
            zip_ref = zipfile.ZipFile(PROJECT_WAR_PATH, 'r')
            zip_ref.extractall(PROJECT_PATH)
            zip_ref.close()
            messages = "project handle success %s" % CODE_WAR_NAME
            recordlog().info(messages)
        except IOError:
            print "\033[31m%s Is Not Exists Please Run bulid\033[0m" % PROJECT_WAR_PATH
    else:
        sys.exit(1)


# 推送项目文件
def pushproject(project_name):
    print "\033[32m等待项目文件推送......\033[0m"
    # 使用ansible rsync模块直接推送到远端
    push_project_directory = "%s/%s" % (PROJECT_REPOSITORY, project_name)
    push_command = """ansible-playbook /etc/ansible/roles/push_v1.yml --extra-vars "hosts=%s src_dir=%s dest_dir=%s" """ % (project_name, push_project_directory, PROJECT_REPOSITORY)
    code_push = Popen(push_command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = code_push.communicate()
    messages = "project push to remote Server success "
    recordlog().info(messages)
    print stdout


# 部署项目
def deployproject(project_name, code_time, svn_number, tags_name):
    print "\033[32m项目正在部署重启.....\033[0m"
    # ansible 处理软连接、重启项目、检测（脚本输出）项目状态
    ansible_path = "ansible-playbook"
    repository_path = "%s/%s" % (PROJECT_REPOSITORY, project_name)
    other_vars = "hosts=%s project_name=%s repository=%s time=%s svn_number=%s" % (project_name, project_name, repository_path, code_time, svn_number)
    playbook_path = "/etc/ansible/roles/syzm.yml"
    deploy_command = """%s %s --tags %s --extra-vars "%s" """ % (ansible_path, playbook_path, tags_name, other_vars)
    code_deploy = Popen(deploy_command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = code_deploy.communicate()
    print stdout
    if code_deploy.returncode == 0:
        messages = "project deploy successful "
        recordlog().info(messages)
        messages_success = "%s#%s#%s" % (code_time, svn_number, project_name)
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


def rollbackdeploy(svn_number, project_name, tags_name):
    for number in checkdeploy():
        pro_name = checkdeploy()[number]['p_name']
        if number == svn_number and project_name == pro_name:
            code_time = checkdeploy()[number]['d_time']
            ansible_path = "ansible-playbook"
            repository_path = "%s/%s" % (PROJECT_REPOSITORY, project_name)
            other_vars = "hosts=%s project_name=%s repository=%s time=%s svn_number=%s" % (project_name, project_name, repository_path, code_time, svn_number)
            playbook_path = "/etc/ansible/roles/syzm.yml"
            rollback_command = """%s %s --tags %s --extra-vars "%s" """ % (ansible_path, playbook_path, tags_name, other_vars)
            rollback_code = Popen(rollback_command, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = rollback_code.communicate()
            print stdout
            if rollback_code.returncode == 0:
                messages = "project rollback successful svn_number is %s" % svn_number
                recordlog().info(messages)
        else:
            messages_stout = "%s is Not Fount" % svn_number
            sys.stdout.write('%s\r' % messages_stout)


def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="EG: '%(prog)s'  deploy or rollback syzm test")
    parser.add_argument('-n', '--number', default='latest', help='input svn number')
    parser.add_argument('-p', '--project', choices=['web', 'rest-api', 'dubbo-index', 'dubbo-price', 'wap', 'dps'], help='input project name')
    parser.add_argument('-o', '--operate', choices=['rollback', 'deploy'])
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def main():
    args = check_arg(sys.argv[1:])
    # 时间  年-月-日
    CODE_TIME = datetime.now().strftime("%Y-%m-%d")
    if args.operate == 'rollback':
        rollbackdeploy(svn_number=args.number,
                       project_name=args.project, tags_name=args.operate)
    if args.operate == 'deploy':
        messages = "deploy svn number:%s-deploy project:%s" % (
            args.number, args.project)
        recordlog().info(messages)
        codeupdate(number=args.number)
        if args.project != 'wap':
            codewar(version=args.number, project_name=args.project, code_time=CODE_TIME)
            pushproject(project_name=args.project)
            deployproject(project_name=args.project, code_time=CODE_TIME, svn_number=args.number, tags_name=args.operate)
        else:
            if codeexport() == 0:
                static_deploy.handlestaticfiles(version=args.number, project_name=args.project, code_time=CODE_TIME)
                pushproject(project_name=args.project)
                deployproject(project_name=args.project, code_time=CODE_TIME, svn_number=args.number, tags_name=args.operate)
if __name__ == '__main__':
    main()
