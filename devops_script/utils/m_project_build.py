#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

"""后端项目编译"""
import os
import shutil
import sys
from datetime import datetime
from subprocess import PIPE, Popen

from config_base import Read_Conf as readconfig
from write_logs import Write_Logs as logs


class Maven_Build(object):

    def __init__(self, name, conf=readconfig().o_conf()):
        self.code_export = conf.get("repo", "repo_export_path")
        self.maven_environment = conf.get("build-options", "env")
        self.project_name = conf.get('will_deployed', 'name')
        self.branch_name = name
        self.repository = conf.get("repository", "path")
        # 生成部署文件的名称拼接
        self.head_name = "{0}".format(conf.get("project", "name"))
        self.version = "{0}".format(conf.get("project", "version"))
        self.snapshot = "{0}".format(conf.get("project", "snapshot"))
        # 拼接完成
        self.maven_bin = conf.get("system", "mvn_bin")
        # war 包存放位置
        self.deploy_path = conf.get("deploy", "path")

    # 拷贝前端文件到后端项目-合并其后端项目文件
    def Transfer_File(self):

        # 后端项目文件路径
        backend_file_path = "{0}/{1}/{2}/{3}/{4}/{5}".format(self.code_export, "cybershop-mobile", 'src', 'main',
                                                             'webapp', 'mobile')

        # 前端文件目录
        front_file_path = "{0}".format(self.repository)

        # 前端文件名
        front_name = ['wx_www', 'tm_group']

        for name in front_name:

            if name == 'wx_www':

                path = "{0}/{1}".format(front_file_path, name)

                shutil.copytree(path, "{0}/{1}".format(backend_file_path, "www"))

            else:

                path = "{0}/{1}".format(front_file_path, name)

                shutil.copytree(path, "{0}/{1}".format(backend_file_path, "group"))

    # 代码编译
    def Maven_Code_Build(self):
        try:
            time1 = datetime.now().strftime('%H:%M:%S')
            # 编译命令
            build_cmd = "{0} clean install -P{1} -Dmaven.test.skip=true".format(self.maven_bin, self.maven_environment)
            # 更换工作目录
            os.chdir(self.code_export)
            # 运行编译命令
            build_status = Popen(build_cmd, shell=True, stdout=PIPE, stderr=PIPE)
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
                print ("\033[33m编译用时:\033[0m" + "%s" % time_diff)
                print ("\033[32mBuild Project Is successful\033[0m")
            else:
                print ("\033[32mBuild Project Is Failed\033[0m")
                print stderr
            return build_status.returncode
        except KeyboardInterrupt:
            print "\033[32m 退出编译\033[0m"

    # 文件处理
    '''
    （1）处理所有需要部署的项目文件处理， 存放到统一目录
    （2）只生成带部署war包、不做任何处理
    （3）将结果记录到日志中
    （4）war包存放的位置有且只存在同名唯一文件
    （5）该目录可提供外部下载
    '''

    def Files_Handle(self):

        # 收集所有输出结果
        result = {}

        if self.Maven_Code_Build() == 0:

            print "\033[32m项目安装包处理.请等待...........\033[0m"

            for name in self.project_name.split(','):
                # 项目包名称
                deploy_name = "{0}-{1}-{2}-{3}".format(self.head_name, name, self.version, self.snapshot)

                if not os.path.exists(self.deploy_path):

                    os.makedirs(self.deploy_path)

                # 项目包生成路径
                deploy_files_path = "%s/cybershop-%s/target/%s" % (self.code_export, name, deploy_name) + ".war"

                # 生成的路径
                save_path = "{0}/{1}.{2}".format(self.deploy_path, deploy_name, "war")

                # 删除已经存在的部署文件
                """
                处理原方法删除目录的产生只会处理最后一个文件
                """
                if os.path.exists(save_path):

                    os.remove(save_path)

                shutil.copy(deploy_files_path, self.deploy_path)

                result[name] = save_path

        else:

            result = {"status": "failed"}

        # 返回所有结果或者记录到日志中
        logs().write_log("builded").info(result)
