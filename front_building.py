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
        self.Front_Home_Path = "/software/build_home/carrefour-app"
        self.Export_Code_Path = "/software/build_home/carrefour-app_export"
        self.Build_After_Path = "/software/build_home/build_after"
        self.Git_Path = "/usr/local/git/bin/git"
        self.Npm_Path = "/root/.nvm/versions/node/v6.11.4/bin/npm"
        self.Bower_Path = "/root/.nvm/versions/node/v6.11.4/bin/bower"
        self.Gulp_Path = "/root/.nvm/versions/node/v6.11.4/bin/gulp"
        self.Build_Way = "package"
        self.Build_Project = "wxshop"
        self.Build_Environment = "production"

    # 删除分之
    def Delete_branch(self):
        # 删除除 master 外的所有的本地分之---明天做细化
        os.chdir(self.Front_Home_Path)
        check_branch = "%s branch | wc -l" % self.Git_Path
        if check_branch != "1":
            Delete_branch = """%s checkout master && %s branch | grep -v "master" | xargs %s branch -D""" % (
            self.Git_Path, self.Git_Path, self.Git_Path)
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
    def Build_Front_Code(self, branch_name):
        build_cmd = ["%s install " % self.Npm_Path, "%s --allow-root install" % self.Bower_Path,
                     "%s package -t %s -e %s" % (self.Gulp_Path, self.Build_Project, self.Build_Environment)]
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
    def Build_After(self, branch_name):
        if self.Build_Front_Code(branch_name) == 0:
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

    """
    如果输入分支存在列表中不进行更新直接获取列表中的进行操作, 如果未在列表中进行项目更新检出以及编译
    """

    # 增加输入分之判断

    def Version_verification(self, branch_name):

        dirs = os.listdir(self.Build_After_Path)

        if branch_name in dirs:
            u_path = "{0}/{1}".format(self.Build_After_Path, branch_name)
            return u_path
        else:
            print "\033[32m输入分支不存在\033[0m"
            return 1

    # 增加公用目录时间排序方法--升序
    def Sequence(self, branch_name):


        # 需要排序的目录
        if self.Version_verification(branch_name) != 1:

            DIR = self.Version_verification(branch_name)

            def compare(x, y):
                stat_x = os.stat(DIR + "/" + x)
                stat_y = os.stat(DIR + "/" + y)
                if stat_x.st_ctime < stat_y.st_ctime:
                    return -1
                elif stat_x.st_ctime > stat_y.st_ctime:
                    return 1
                else:
                    return 0

            iterms = os.listdir(DIR)

            iterms.sort(compare)

            final = "{0}/{1}".format(DIR, iterms[-1])


            # 返回最近一次部署后路径
            return final

        else:
            return 1


class Maven_Tools(object):
    def __init__(self):
        self.git_checkout_path = "/software/git_checkout_path/core"
        self.export_path = "/software/git_checkout_path/carrefour_export"
        self.After_Dist_Path = "cybershop-mobile/src/main/webapp/mobile"
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
    def Maven_Build_Before(self, p_list):
        print p_list
        print type(p_list)
        after_d_inside = "%s/%s/www" % (self.export_path, self.After_Dist_Path)
        after_d_outside = "%s/%s/wwwTest" % (self.export_path, self.After_Dist_Path)
        if os.path.exists(after_d_inside) or os.path.exists(after_d_outside):
            shutil.rmtree(after_d_inside)
            shutil.rmtree(after_d_outside)
        if len(p_list) != 2:
            print "\033[31m前端构建不成功!\033[0m"
            exit(1)
        else:
            for path in p_list:
                if self.branch_name in path:
                    shutil.copytree(path, after_d_inside)
                    print after_d_inside
                else:
                    shutil.copytree(path, after_d_outside)
                    print after_d_outside


# 处理执行参数
def check_arg(args=None):
    parser = argparse.ArgumentParser(description="EG: '%(prog)s' Build Front Code")
    parser.add_argument('-b', '--branch', help='input git branch')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def Front_Build_Handle(branch_name):
    Front_Build = Build_Tools()
    after_path_list = []

    for name in branch_name:
        if Front_Build.Sequence(name) == 1:
            Front_Build.Delete_branch()
            Front_Build.Swith_branch(name)
            Front_Build.Front_Code_Update()
            after_path_list.append(Front_Build.Build_After(name))
        else:
            after_path_list.append(Front_Build.Sequence(name))
    return after_path_list


def Maven_Build_Hanle(branch_name):
    M_Build = Maven_Tools()
    M_Build.Code_Update()
    if M_Build.Code_Export():
        M_Build.Maven_Build_Before(Front_Build_Handle(branch_name))


def main():
    args = check_arg(sys.argv[1:])
    branch = ["master", args.branch]
    Maven_Build_Hanle(branch)


if __name__ == '__main__':
    main()
