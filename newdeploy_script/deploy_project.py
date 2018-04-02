#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author EdwardLiu

from subprocess import Popen, PIPE
from config_base import Read_Conf as readconfig
import yaml
import logging.config
import ast


class Deploy_Project(object):

    def __init__(self, hosts, project_name, conf=readconfig().o_conf()):

        self.repository = conf.get("repository", "path")
        # 个例 实现
        """
        当 ansible 中的主机组名称与部署输入的项目名称不一致时,调用该参数
        """
        self.hosts = hosts
        self.project_name = project_name
        self.conf_path = conf.get("log_path", "conf_path")
        self.log_path = "{0}/{1}".format(conf.get("strong", "strong_path"), "stdout.log")

    # 记录日志,后续部署调用该日志进行项目部署
    def write_log(self):
        log_conf = "{0}/logging.yml".format(self.conf_path)
        with open(log_conf, 'r') as f_conf:
            dict_conf = yaml.load(f_conf)
        logging.config.dictConfig(dict_conf)

        logger = logging.getLogger('deployed')
        return logger

    # 推送项目文件
    def push_project(self):

        print "\033[32m项目文件推送......\033[0m"

        # 使用ansible rsync模块直接推送到远端
        push_project_directory = "%s/%s" % (self.repository, self.project_name)

        playbooks_path = "/etc/ansible/roles/push.yml"

        push_command = """ansible-playbook {0} --extra-vars "hosts={1} src_dir={2} dest_dir={3}" """.format(playbooks_path, self.hosts, push_project_directory, self.repository)

        code_push = Popen(push_command, shell=True, stdout=PIPE, stderr=PIPE)

        stdout, stderr = code_push.communicate()

        print stdout

        messages = "project push {0} to remote Server {1} success".format(self.project_name, self.project_name)

        self.write_log().info(messages)

        return code_push.returncode

    # 检测以部署的项目
    def deploy_log(self):

        file_object = open(self.log_path, 'rU')

        try:
            lines = file_object.readlines()

            # 最近一次编译结果--并且直接转换成字典
            result = ast.literal_eval(lines[-1].split('  -  ')[3])
        finally:
            file_object.close()

        data = result[self.project_name]

        # 返回的是需要部署的路径
        return data

    # 部署项目
    def deploy_project(self, tags_name):
        print "\033[32m项目正在部署重启.....\033[0m"

        # ansible 处理软连接、重启项目、检测（脚本输出）项目状态
        ansible_path = "ansible-playbook"

        other_vars = "hosts={0} project_name={1} deploy_file={2}".format(self.hosts, self.project_name, self.deploy_log())

        # 后续是否提出该选项做为公共配置项
        playbook_path = "/etc/ansible/roles/ejl_deploy.yml"

        deploy_command = """{0} {1} --tags {2} --extra-vars "{3}" """.format(ansible_path, playbook_path, tags_name, other_vars)

        code_deploy = Popen(deploy_command, shell=True, stdout=PIPE, stderr=PIPE)

        stdout, stderr = code_deploy.communicate()

        print stdout

        messages = "project deploy {0} success".format(self.project_name)

        self.write_log().info(messages)