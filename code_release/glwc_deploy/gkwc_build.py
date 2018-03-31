#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

import logging
import logging.config
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from subprocess import Popen, PIPE


# code 存放位置
CODE_WORKSPACE = "/software/git_code_registroy/code"
# 代码 export 目录
CODE_EXPORT = "/software/git_code_export"
# 代码 export 名称
CODE_EXPORT_NAME = "gkwc_online"
# export 路径
export_path = "%s/%s" % (CODE_EXPORT, CODE_EXPORT_NAME)
# 编译后代码存放路径及推送目录
PROJECT_REPOSITORY = "/software/project_repository"


# 部署记录日志
def recordlog():
    loger_path = "/software/script/logger.conf"
    logging.config.fileConfig(loger_path)
    logger = logging.getLogger("glwc")
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


# 更新代码
def codeupdate():
    print "\33[32m等待更新项目\033[0m"
    try:
        os.chdir(CODE_WORKSPACE)
        GIT_UPDATE_COMMAND = "/usr/bin/git pull"
        code_update = Popen(GIT_UPDATE_COMMAND, shell=True,
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
            print "\033[32mUpdate glwc_online Is successful\033[0m"
            messages = "update code success"
            recordlog().info(messages)
        else:
            print "\033[32mUpdate glwc_online Is Failed\033[0m"
            print stderr
            sys.exit(1)
    except KeyboardInterrupt:
        print "\033[31m退出更新\033[0m"


# 获取代码最新版本号
def get_version():
    command = """git log --pretty=format:"%h" -1"""
    os.chdir(CODE_WORKSPACE)
    ret_code = subprocess.Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    if ret_code == 0:
        messages = "get git version success"
        recordlog().info(messages)
    stdout, stderr = ret_code.communicate()
    return stdout


# 检出代码
def codeexport(branch_name):
    print "\033[32m等待检出目录........\033[0m"
    if os.path.exists(export_path):
        shutil.rmtree(export_path)
    if not os.path.exists(export_path):
        os.makedirs(export_path)
    # 检出 SVN 工作目录
    export_command = "/usr/bin/git archive %s | tar -x -C %s" % (
        branch_name, export_path)
    FNULL = open(os.devnull, 'w')
    # 更换工作目录
    os.chdir(CODE_WORKSPACE)
    ret_code = subprocess.call(
        export_command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    if ret_code == 0:
        messages = "code export success"
        recordlog().info(messages)
    return ret_code


# 处理 front gulp 编译问题
def gulp_handle():
    source_dir_name = "/software/node_modules"
    dest_dir_name = "%s/cybershop-front/src/main/websrc/node_modules" % export_path
    shutil.copytree(source_dir_name, dest_dir_name)
    if os.path.isdir(dest_dir_name):
        return "OK"
    else:
        print "handle project front is Failed"
        return "Failed"


# 代码编译
def codebuild(branch_name):
    try:
        if codeexport(branch_name=branch_name) == 0 and gulp_handle() == "OK":
            time1 = datetime.now().strftime('%H:%M:%S')
            # 编译命令
            CODE_BUILD_COMMAND = "mvn clean install -Ponline -Dmaven.test.skip=true"
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
                print "\033[32mBuild glwc_online Is successful\033[0m"
                messages = "build code success"
                recordlog().info(messages)
            else:
                print "\033[32mBuild glwc_online Is Failed\033[0m"
                messages = "build code Failed"
                recordlog().info(messages)
                print stderr
            return build_status.returncode
    except KeyboardInterrupt:
        print "\033[32m 退出编译\033[0m"


# 处理所有待编译的文件
def codewar(b_name, version, project_name, code_time):
    if codebuild(branch_name=b_name) == 0:
        for p_name in project_name:
            print "\033[32m项目包(%s)处理.请等待...........\033[0m" % p_name
            # 项目名称
            CODE_WAR_NAME = "cybershop-%s-2.2.0" % p_name
            PROJECT_PATH = "%s/%s/%s/%s/%s" % (PROJECT_REPOSITORY,
                                               p_name, code_time, version, CODE_WAR_NAME)
            if not os.path.exists(PROJECT_PATH):
                os.makedirs(PROJECT_PATH)
            # 项目包生成路径
            PROJECT_WAR_PATH = "%s/cybershop-%s/target/%s" % (
                export_path, p_name, CODE_WAR_NAME) + ".war"
            # 直接将项目包解压到项目目录
            try:
                zip_ref = zipfile.ZipFile(PROJECT_WAR_PATH, 'r')
                zip_ref.extractall(PROJECT_PATH)
                zip_ref.close()
                messages = "project handle success %s" % CODE_WAR_NAME
                recordlog().info(messages)
                print "\033[32m项目包(%s)处理完成!!!\033[0m" % p_name
            except IOError:
                print "\033[31m%s Is Not Exists Please Run bulid\033[0m" % PROJECT_WAR_PATH
        else:
            sys.exit(1)

if __name__ == '__main__':
    project_list = ['web', 'front', 'web-merchant']
    # 时间  年-月-日
    CODE_TIME = datetime.now().strftime("%Y-%m-%d")
    codeupdate()
    codewar(b_name='master', version=get_version(), project_name=project_list, code_time=CODE_TIME)