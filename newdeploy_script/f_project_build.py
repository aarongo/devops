#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/4/6 下午2:23
# @Author : EdwardLiu
# @Site : 
# @File : f_project_build.py

from datetime import datetime
import os
from config_base import Read_Conf as readconfig
from handle_git import Custom_Git as git


class Front_Project(object):

    def __init__(self, conf=readconfig().o_conf()):




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