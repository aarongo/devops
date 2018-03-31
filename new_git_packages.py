#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'Edward.Liu'
# dateTime:  '15/12/9'
#   motto:  'Good memory as bad written'
import datetime, time
import os
import shutil
import subprocess
from subprocess import PIPE, Popen
import tarfile
import sys


class Packages(object):
    def __init__(self):
        self.git_checkout_path = "/software/git_checkout_path/core"
        self.export_path = "/software/git_checkout_path/carrefour_export/"
        self.Project_Directory_F = "%scybershop-front/target" % self.export_path
        self.Project_Directory_B = "%scybershop-web/target" % self.export_path
        # add mobile
        self.Project_Directory_M = "%scybershop-mobile/target" % self.export_path
        self.Upload_Directory = "/software/registry/"
        self.Project_Directory_F_Name = "cybershop-front-0.0.1-SNAPSHOT.war"
        self.Project_Directory_B_Name = "cybershop-web-0.0.1-SNAPSHOT.war"
        # add Mobile
        self.Project_Directory_M_Name = "cybershop-mobile-0.0.1-SNAPSHOT.war"
        self.density_name = ['pro', 'demo', 'ptest', 'newpro']
        self.bulid_home = "/software/maven3.0.5/bin/mvn"
        self.date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H')
        self.branch_name = 'master'

    # git Update
    def codeupdate(self):
        print "\33[32m等待更新项目\033[0m"
        try:
            os.chdir(self.git_checkout_path)
            SVN_UPDATE_COMMAND = "/usr/local/git/bin/git pull"
            code_update = Popen(SVN_UPDATE_COMMAND, shell=True,
                                stdout=PIPE, stderr=PIPE)
            while True:
                # 编译显示信息
                update_info = "\033[32mRunupdate-->Time:\033[0m" + \
                              datetime.datetime.now().strftime('%H:%M:%S')
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
                print "\033[32mUpdate glwc_online Is successful\033[0m"
            else:
                print "\033[32mUpdate glwc_online Is Failed\033[0m"
                print stderr
                sys.exit(1)
        except KeyboardInterrupt:
            print "\033[31m退出更新\033[0m"

    # svn export
    def codeexport(self):
        print "\033[32m等待检出目录........\033[0m"
        if os.path.exists(self.export_path):
            shutil.rmtree(self.export_path)
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
        # 检出 SVN 工作目录
        export_command = "/usr/local/git/bin/git archive %s | tar -x -C %s" % (self.branch_name, self.export_path)
        FNULL = open(os.devnull, 'w')
        # 更换工作目录
        os.chdir(self.git_checkout_path)
        ret_code = subprocess.call(
            export_command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        if ret_code == 0:
            print "code export success"
        return ret_code

    # get git last number
    def get_version(self):
        command = """git log --pretty=format:"%h" -1"""
        os.chdir(self.git_checkout_path)
        ret_code = subprocess.Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        if ret_code == 0:
            print "get git version success"
        stdout, stderr = ret_code.communicate()
        return stdout

    def Bulid(self):
        global env
        # 编译项目(分环境)
        # 获取生成项目的文件名-- get
        bulided_File_Path_F = "%s/%s" % (self.Project_Directory_F, self.Project_Directory_F_Name)
        # ---get end
        # 编译环境选择--- select---> Maven
        for index, value in enumerate(self.density_name):
            print index, "Carrefour" + "---->" + value
        try:
            while True:
                Chose_ENV = raw_input("\033[32mChose Density Environment:\033[0m")
                if Chose_ENV.isdigit():
                    Chose_ENV = int(Chose_ENV)
                    env = self.density_name[Chose_ENV]
                    try:
                        if self.density_name[Chose_ENV] == 'pro':
                            os.chdir(self.export_path)
                            bulid_command = "%s clean install -PcarrefourPro -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            print "\033[32m--------------------Create TarFiles--------------------\033[0m"
                            self.Files_Handle()
                            break
                        elif self.density_name[Chose_ENV] == 'demo':
                            os.chdir(self.export_path)
                            bulid_command = "%s clean install -Pcarrefour -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            print "\033[32m--------------------Create TarFiles--------------------\033[0m"
                            self.Files_Handle()
                            break
                        elif self.density_name[Chose_ENV] == 'ptest':
                            os.chdir(self.export_path)
                            bulid_command = "%s clean install -PcarrefourPtest -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            print "\033[32m--------------------Create TarFiles--------------------\033[0m"
                            self.Files_Handle()
                            break
                        elif self.density_name[Chose_ENV] == 'newpro':
                            os.chdir(self.export_path)
                            bulid_command = "%s clean install -PcarrefourProNew -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            print "\033[32m--------------------Create TarFiles--------------------\033[0m"
                            self.Files_Handle()
                            break
                    except IndexError:
                        print "\033[31mSelect error\033[0m"
        except KeyboardInterrupt:
            print "\033[32m Quit\033[0m"
            # select----Maven--->END

    def Files_Handle(self):
        # 生成文件处理
        # 文件压缩----tar
        Tmp_density_dir = "/software/%s%s-%s" % (env, self.get_version(), self.date_time)
        os.makedirs(Tmp_density_dir) 
        source_fiels = ["%s/%s" % (self.Project_Directory_F, self.Project_Directory_F_Name),
                        "%s/%s" % (self.Project_Directory_B, self.Project_Directory_B_Name),
                        "%s/%s" % (self.Project_Directory_M, self.Project_Directory_M_Name)]
        for i in range(3):
            shutil.move(source_fiels[i], Tmp_density_dir)
        # 创建压缩包
        os.chdir("/software")
        tarfile_name = "%s.tar.gz" % Tmp_density_dir.split('/')[2]
        tar = tarfile.open(tarfile_name, "w:gz")
        tar.add(Tmp_density_dir.split('/')[2])
        tar.close()
        # 创建压缩包---end
        if os.path.exists(tarfile_name):
            print "\033[32m----------Delete Temporary Files%s----------\033[0m" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
            shutil.rmtree(Tmp_density_dir)
            shutil.move(tarfile_name, self.Upload_Directory)
            Upload_Files_Name = "%s%s" % (self.Upload_Directory, tarfile_name)
            print "\033[32mSuccessful Download address:http://182.50.117.44:8081/%s\033[0m" % tarfile_name
        else:
            print "\033[31m----------Create archive Is Failed%s----------\033[0m" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')

    def usage(self):
        script_name = "packages.py"
        print "\033[31m*****************************************\033[0m"
        print "\033[31m|------------Packages Useage------------|\033[0m"
        print "\033[32m|------------./%s--------------|\033[0m" % script_name
        print "\033[32m|------------<path>/%s---------|\033[0m" % script_name
        print "\033[32m|----------脚本执行过程1步人工干预------|\033[0m"
        print "\033[32m|----------1.选择需要打包的环境---------|\033[0m"
        print "\033[32m|----------2.复制输出下载链接进行下载---|\033[0m"
        print "\033[31m******************************************\033[0m"


if __name__ == '__main__':
    Run_packages = Packages()
    Run_packages.usage()
    # Run_packages.codeupdate()
    #if Run_packages.codeexport() == 0:
    Run_packages.Bulid()
    # else:
    #     print "检出不成功!!!"
    #     sys.exit(1)

