#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author EdwardLiu


"""
仓库地址: http://gitlab.product.co-mall:10080/frontend/carrefour-app.git
编译结果输出:
    构建master分支 输出到 cybershop-mobile\src\main\webapp\mobile\www
    构建指定分支  输出到 cybershop-mobile\src\main\webapp\mobile\wwwTest
前端编译过程:
	1. 本地安装 node, npm, gulp, ruby, sass, bower
		node,npm+ruby:
			详见本地 node 和 ruby 安装文档
		gulp + bower:
			npm install -g gulp
			npm install -g bower
		asaa:
			gem install sass	
	2. 检出项目
		git clone http://xxxxxxxxx/xx.git
	3. 进入项目打包
		1. npm install (根据项目里的 package.json 进行安装项目依赖)
		2. bower --allow-root install install (根据项目里的 bower.json 进行安装项目内部依赖)
		3. gulp package -t wxshop -e production (根据项目里 package.json里的标签进行项目打包)
	4. 拷贝编译好的文件
		1. 项目目录下 dist拷贝到 maven 项目中
	5. maven 项目编译前调用打包脚本进行项目更新与检出后 将前端编译好的文件拷贝到指定目录下
	6. maven 项目进行编译, 
"""
import os
from subprocess import PIPE, Popen, call, STDOUT
from datetime import datetime
import sys
import shutil
import argparse


class Build_Tools(object):
    # 定义全局使用变量
    def __init__(self):
        self.Front_Home_Path = "/software/syzm_front_repo/cdfg-app"
        self.Export_Code_Path = "/software/syzm_front_repo/cdfg-app_export"
        self.Build_After_Path = "/software/syzm_front_repo/build_after"
        self.Git_Path = "/usr/local/git/bin/git"
        self.yarn_path = "/root/.nvm/versions/node/v8.9.3/bin/yarn"
        self.Build_Way = "package"
        self.Build_Environment = "production"

    # 删除分之
    def Delete_branch(self):
        # 删除除 master 外的所有的本地分之---明天做细化
        os.chdir(self.Front_Home_Path)
        check_branch = "%s branch | wc -l" % self.Git_Path
        if check_branch != "1":
            Delete_branch = """%s checkout master && %s branch | grep -v "master" | xargs %s branch -D""" % (self.Git_Path, self.Git_Path, self.Git_Path)
            delete_code = call(Delete_branch, shell=True)
            if delete_code == 0:
                print "delete branch success"

    # 切换 GIT分之
    def Swith_branch(self, branch_name):
        # git 直接切换分之
        if branch_name != 'master':
            swith_cmd = "%s checkout --track origin/%s" % (self.Git_Path, branch_name)
            branch_swith = Popen(swith_cmd, shell=True, stdout=PIPE, stderr=PIPE)
            while True:
                # 显示信息
                update_info = "\033[32mRuncheckout-->Time:\033[0m" + datetime.now().strftime('%H:%M:%S')
                # 获取输出
                newline = branch_swith.stdout.readline()
                # 如果没有输出就退出
                if newline == '' and branch_swith.poll() is not None:
                    break
                # 打印信息
                sys.stdout.write('%s\r' % update_info)
                # 刷新打印缓存
                sys.stdout.flush()
            stdout, stderr = branch_swith.communicate()
            if branch_swith.returncode == 0:
                print "\033[32mCheckout Branch: %s Is successful\033[0m" % branch_name
            else:
                print "\033[32mCheckout Branch: %s Is Failed\033[0m"
                print stderr
                sys.exit(1)
        else:
            print "\033[32m当前分支以是Master 不需要切换.....\033[0m"

    # 更新代码
    def Front_Code_Update(self):
        print "\33[32m更新项目.......\033[0m"
        try:
            os.chdir(self.Front_Home_Path)
            update_cmd = "%s pull" % self.Git_Path
            code_update = Popen(update_cmd, shell=True, stdout=PIPE, stderr=PIPE)
            while True:
                # 编译显示信息
                update_info = "\033[32mRunupdate-->Time:\033[0m" + datetime.now().strftime('%H:%M:%S')
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
            if code_update.returncode == 0:
                print "\033[32mUpdate Code Is successful\033[0m"
            else:
                print "\033[32mUpdate Code Is Failed\033[0m"
                print stderr
                sys.exit(1)
        except KeyboardInterrupt:
            print "\033[31m退出更新\033[0m"

    # 检出代码
    def Front_Code_Export(self, branch_name):
        print "\033[32m等待检出目录........\033[0m"
        if os.path.exists(self.Export_Code_Path):
            shutil.rmtree(self.Export_Code_Path)
            os.makedirs(self.Export_Code_Path)
        else:
            os.makedirs(self.Export_Code_Path)
        export_cmd = "%s archive %s | tar -x -C %s" % (self.Git_Path, branch_name, self.Export_Code_Path)
        r_null = open(os.devnull, 'w')
        # 更换工作目录
        os.chdir(self.Front_Home_Path)
        ret_code = call(export_cmd, shell=True, stdout=r_null, stderr=STDOUT)
        if ret_code == 0:
            print "\033[32m 检出目录成功.....\033[0m"
            return ret_code

    # 前端代码打包
    def Build_Front_Code(self, branch_name, project):
        build_cmd = ["%s install " % self.Npm_Path, "%s build -t %s -e %s" % (self.yarn_path, project, self.Build_Environment)]
        build_return_code = 0
        try:
            if self.Front_Code_Export(branch_name=branch_name) == 0:
                print "\033[32mBuilding %s.....\033[0m" % branch_name
                for cmd in build_cmd:
                    time1 = datetime.now().strftime('%H:%M:%S')
                    # 编译命令
                    # 更换工作目录
                    os.chdir(self.Export_Code_Path)
                    # 运行编译命令
                    build_status = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                    # 显示编译进度---使用时间作为记录标识
                    while True:
                        # 编译显示信息
                        build_info = "\033[32mRunBuilding-->Time:\033[0m" + datetime.now().strftime('%H:%M:%S')
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
                        print "\033[32mBuild Code Is successful cmd is %s\033[0m" % cmd
                    else:
                        print "\033[32mBuild code Is Failed cmd is %s\033[0m" % cmd
                        print stderr
                    build_return_code += build_status.returncode
            return build_return_code
        except KeyboardInterrupt:
            print "\033[32m 退出编译\033[0m"

    # 编译后文件处理
    def Build_After(self, branch_name, project):
        if self.Build_Front_Code(branch_name, project) == 0:
            print "\033[32m整理编译后文件....\033[0m"
            # 时间  年-月-日
            after_time = datetime.now().strftime("%Y-%m-%d-%H-%M")
            """
                # 处理前端代码编译后对生成文件的处理
                1. 将编译好的文件根据分之名与时间进行区分
                2. 将区分后的目录拷贝到maven 项目对应目录下
            """
            after_path_src = "%s/%s" % (self.Export_Code_Path, "dist")
            after_path = "%s/%s" % (self.Build_After_Path, branch_name)
            if os.path.exists(after_path):
                after_path_dest = "%s/%s" % (after_path, after_time)
                shutil.copytree(after_path_src, after_path_dest)
                return after_path_dest
            else:
                os.makedirs(after_path)
                after_path_dest = "%s/%s" % (after_path, after_time)
                shutil.copytree(after_path_src, after_path_dest)
                return after_path_dest


class Maven_Tools(object):
    def __init__(self):
        self.git_checkout_path = "/software/git_code_registroy/ld"
        self.export_path = "/software/git_code_export/ld_export"
        self.branch_name = 'master'

    # git Update
    def Code_Update(self):
        print "\33[32m等待更新Maven项目\033[0m"
        try:
            os.chdir(self.git_checkout_path)
            cmd = "/usr/local/git/bin/git pull"
            code_update = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            while True:
                # 编译显示信息
                update_info = "\033[32mRunupdate-->Time:\033[0m" + datetime.now().strftime('%H:%M:%S')
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
            if code_update.returncode == 0:
                print "\033[32mUpdate Maven Project carrefour_online Is successful\033[0m"
            else:
                print "\033[32mUpdate Maven Project carrefour_online Is Failed\033[0m"
                print stderr
                sys.exit(1)
        except KeyboardInterrupt:
            print "\033[31m退出更新\033[0m"

    # git export
    def Code_Export(self):
        print "\033[32m等待检出Maven Project目录........\033[0m"
        if os.path.exists(self.export_path):
            shutil.rmtree(self.export_path)
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
        # 检出 SVN 工作目录
        export_command = "/usr/local/git/bin/git archive %s | tar -x -C %s" % (self.branch_name, self.export_path)
        FNULL = open(os.devnull, 'w')
        # 更换工作目录
        os.chdir(self.git_checkout_path)
        ret_code = call(export_command, shell=True, stdout=FNULL, stderr=STDOUT)
        if ret_code == 0:
            print "Maven Project code export success"
            return True
        else:
            return False

    # 处理前端项目文件
    def Maven_Build_Before(self, path, project):

        After_Dist_Path = "cybershop-%s/src/main/webapp" % project

        after_d_inside = ""

        if project == "wap":

            after_d_inside = "%s/%s/wap" % (self.export_path, After_Dist_Path)

        elif project == "wxshop":

            after_d_inside = "%s/%s/wxshop" % (self.export_path, After_Dist_Path)

        if os.path.exists(after_d_inside):

            shutil.rmtree(after_d_inside)

        else:

            shutil.copytree(path, after_d_inside)


# 处理执行参数
def check_arg(args=None):
    parser = argparse.ArgumentParser(description="EG: '%(prog)s' Build Front Code")
    parser.add_argument('-b', '--branch', help='input git branch')
    parser.add_argument('-p', '--project', help='project name')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def Front_Build_Handle(branch_name, project):

    Front_Build = Build_Tools()

    Front_Build.Delete_branch()

    Front_Build.Swith_branch(branch_name)

    Front_Build.Front_Code_Update()

    path = Front_Build.Build_After(branch_name, project)

    return path


def Maven_Build_Hanle(branch_name, project):
    M_Build = Maven_Tools()
    M_Build.Code_Update()
    if M_Build.Code_Export():
        M_Build.Maven_Build_Before(Front_Build_Handle(branch_name, project), project)


def main():
    args = check_arg(sys.argv[1:])
    branch = args.branch
    project = args.project
    Maven_Build_Hanle(branch, project)


if __name__ == '__main__':
    main()
