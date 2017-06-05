#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.compile


import os
import zipfile
import datetime

# set process directory vars
DEPLOY_ENV = "mobile"
DEPLOY_WAR = "cybershop-%s-0.0.1-SNAPSHOT.war" % DEPLOY_ENV
UPLOAD_WAR_DIRECTORY = "/software/source_files"
DEPLOY_TMP = "/software/deploy_tmp/"
DEPLOY_REALY = "/software/deploy_%s/" % DEPLOY_ENV
STATIC_DIRECTORY = "/data/www"
PICTURE_DIRECTORY = "/software/picture"
# Set process Diectory Vars end
# Set Process Used dir
Source_Path = "%s/%s" % (UPLOAD_WAR_DIRECTORY, DEPLOY_WAR)
now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
Last_File = "%s%s-%s" % (DEPLOY_TMP, DEPLOY_WAR.split('.war')[0], now_time)
# Set process Used End


def process_judgment_dir():
    # 判断目录是否存在
    if not os.path.exists(UPLOAD_WAR_DIRECTORY):
        os.makedirs(UPLOAD_WAR_DIRECTORY)
    elif not os.path.exists(DEPLOY_TMP):
        os.makedirs(DEPLOY_TMP)
    elif not os.path.exists(DEPLOY_REALY):
        os.makedirs(DEPLOY_REALY)
    else:
        print "\033[32mUsed Dir Is exists\033[0m"


def process_source():
    """
        1.解压部署文件
        2.创建图片存放目录
    """
    ret = 0
    # 图片目录创建
    Last_File_Pic = "%s/assets" % Last_File
    if not os.path.exists(Last_File):
        # 创建程序目录
        os.makedirs(Last_File)
        # 创建图片目录
        os.makedirs(Last_File_Pic)
        try:
            zip_ref = zipfile.ZipFile(Source_Path, 'r')
            zip_ref.extractall(Last_File)
            zip_ref.close()
            ret = 1
            return ret
        except IOError:
            print "\033[31m%s Is Not Exists Please send Files\033[0m" \
                % DEPLOY_WAR.split('.war')[0]
        return ret


def process_link():
    if process_source() == 1:
        # 创建项目启动所需链接
        dest_pic = "%s/assets/upload" % Last_File
        dest_static = "%s/www" % Last_File
        os.symlink(PICTURE_DIRECTORY, dest_pic)
        os.symlink(STATIC_DIRECTORY, dest_static)
        # 创建项目启动所需链接----END
        # 创建启动程序链接
        dest_deploy_path = "%s%s" % (DEPLOY_REALY, DEPLOY_WAR.split('.war')[0])
        os.symlink(Last_File, dest_deploy_path)
        if os.path.islink(dest_deploy_path):
            print "\033[32mCrate Link Process Is Scueeful\033[0m"
        # 创建启动程序链接----END
