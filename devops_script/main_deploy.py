#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

import argparse
import sys
import os
import shutil
import zipfile
from tqdm import tqdm
tqdm.monitor_interval = 0
from datetime import datetime

import requests

from conf.config_base import Read_Conf as readconfig
from libs.deploy_project import Deploy_Project
from conf.write_logs import Write_Logs as logs


def download_file(project):

    conf = readconfig().o_conf()

    # 生成时间
    generate_time = datetime.now().strftime('%Y-%m-%d-%H-%M')

    # 生成部署文件的名称拼接
    head_name = "{0}".format(conf.get("project", "name"))

    version = "{0}".format(conf.get("project", "version"))

    snapshot = "{0}".format(conf.get("project", "snapshot"))

    # 下载文件选项
    download_url = conf.get("download", "url")

    download_save_path = conf.get("download", "tmp_path")

    download_deploy_path = conf.get("download", "deploy_path")

    # 待部署文件存放位置
    files_name = "{0}-{1}-{2}-{3}".format(head_name, project, version, snapshot)

    base_url = "{0}/{1}".format(download_url, files_name) + ".war"

    deploy_path = "{0}".format(download_deploy_path) + "/" + "{0}".format(project) + "/" + "{0}".format(generate_time) + "/" + "{0}".format(files_name)

    # 下载保存的文件名称及路径
    save_path = "{0}/{1}".format(download_save_path, project)

    save_name = "{0}".format(files_name) + ".zip"

    if not os.path.exists(download_save_path):

        os.makedirs(download_save_path)

    elif not os.path.exists(download_deploy_path):

        os.makedirs(download_deploy_path)

    elif not os.path.exists(save_path):

        os.makedirs(save_path)

    # 下载文件

    print ("download {0}.war file".format(files_name))

    try:

        r = requests.get(base_url, stream=True)

        content_size = int(r.headers['Content-Length']) / 1024

        with open("{0}/{1}".format(save_path, save_name), 'wb') as f:

            print "total: ", content_size, 'k'

            for data in tqdm(iterable=r.iter_content(1024), total=content_size, unit='k'):

                f.write(data)

            print "done " + save_name

        # 方法返回数据
        results = {
            "status": r.status_code,
            "save_path": save_path,
            "save_name": save_name,
            "deploy_path": deploy_path,
        }

        return results

    except requests.ConnectTimeout:

        messages = "Timeout"

        return messages

    except requests.ConnectionError:

        messages = "connection"

        return messages

    except requests.HTTPError:

        messages = "httperror"

        return messages

    except KeyboardInterrupt:

        exit(1)


# unpack 压缩文件
def unpack_file(project):

    down = download_file(project)

    # 文件存放位置
    file_path = down['save_path']

    # 待解压的文件名
    tar_file = down['save_name']

    # 解压到指定目录
    death_dir = down['deploy_path']

    if not os.path.exists(death_dir):

        os.makedirs(death_dir)

    if down['status'] == 200:

        t = zipfile.ZipFile("{0}/{1}".format(file_path, tar_file), "r")

        t.extractall(path=death_dir)

        t.close()

    shutil.rmtree(file_path)

    # 增加下载文件后对文件处理结果, 路径记录到日志中,在后续部署过程中进行调用部署
    messages = "{0}".format(death_dir)

    logs().write_log(write_way='unpack').info(messages)

    return death_dir


def push_deploy(hosts, name, tags):

    # 初始化部署函数
    deploy = Deploy_Project(hosts, name)

    # 推送部署文件
    deploy.push_project()

    # 项目部署
    deploy.deploy_project(tags)


def check_arg(args=None):
    parser = argparse.ArgumentParser(description="EG: '%(prog)s'  build maven project")
    parser.add_argument('-p', '--project_name', choices=['wx', 'teamshop', 'restapi', 'erpdocke', 'web'], help='deploy project name')
    parser.add_argument('-t', '--tags', default='deploy', choices=['deploy', 'rollback'], help='deploy way')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


# 针对项目名称与部署文件不对应
def project_name_handle(project_name):

    if project_name == "restapi":

        project = "mobile"

    elif project_name == "wxshop":

        project = "mobile"

    elif project_name == "wx":

        project = "mobile"

    elif project_name == "teamshop":

        project = "mobile"

    elif project_name == "erpdocke":

        project = "api"

    else:

        project = project_name

    return project


def main():

    # 获取所有参数
    args = check_arg(sys.argv[1:])

    hosts = args.project_name

    project_name = project_name_handle(args.project_name)

    tags_name = args.tags

    unpack_file(project_name)

    push_deploy(hosts, project_name, tags_name)


if __name__ == '__main__':

    main()
