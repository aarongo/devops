#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: liuyulong@co-mall.com


"""
    三亚中免静态资源部署
    1. 代码更新 (依赖主文件)
    2. 数据传送  自定义方法
    3. 服务重启 (依赖主文件)
"""

import os
import shutil

# 代码 export 目录
CODE_EXPORT = "/software/code_export"
# 代码 export 名称
CODE_EXPORT_NAME = "syzm_test"
# 项目名称
STATIC_PROJECT_NAME = "cybershop-wap"
# 静态资源路径
STATIC_PAHT = "/src/main/webapp"
WAP_STATIC_PATH = "%s/%s/%s/%s" % (CODE_EXPORT, CODE_EXPORT_NAME, STATIC_PROJECT_NAME, STATIC_PAHT)
# 编译后代码存放路径
PROJECT_REPOSITORY = "/software/project_repository"


def handlestaticfiles(version, project_name, code_time):
    # 静态资源项目文件处理
    # 项目名称
    CODE_WAR_NAME = "sy-cybershop-%s-3.1.1-SNAPSHOT" % project_name
    PROJECT_PATH = "%s/%s/%s/%s" % (PROJECT_REPOSITORY, code_time, version, CODE_WAR_NAME)
    if not os.path.exists(PROJECT_PATH):
        os.makedirs(PROJECT_PATH)
    # 处理静态资源文件
    directory_list = ['wap', 'WEB-INF']
    for dir_name in directory_list:
        print "\033[32mStarting Copy %s......\033[0m" % dir_name
        src_path = "%s/%s" % (WAP_STATIC_PATH, dir_name)
        dest_path = "%s/%s" % (PROJECT_PATH, dir_name)
        try:
            shutil.copytree(src=src_path, dst=dest_path)
        except OSError:
            shutil.rmtree(path=dest_path)
            shutil.copytree(src=src_path, dst=dest_path)
