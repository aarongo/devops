#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author EdwardLiu


from subprocess import Popen, PIPE
import os

workspace = "/software/workspace/project-local/project"


def get_result():
    os.chdir(workspace)
    git_command = "/usr/bin/git log --name-only -1"
    result = Popen(git_command, stdin=PIPE,
                   stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = result.communicate()
    # 去除列表中的空元素
    stdout_list = [line for line in stdout.split('\n') if line.strip() != '']
    project_name = stdout_list[-1].split('/')[0]
    process_name = stdout_list[-1].split('/')[1]
    # 定义存放字典--存放对应项目与程序关联
    project_process = {
        "project_name": project_name,
        "process_name": process_name
    }
    return project_process


def push_config(yml_path, hosts):
    push_command = """ansible-playbook  %s --extra-vars "hosts_run=%s" """ % (
        yml_path, hosts)
    result = Popen(push_command, stdin=PIPE,
                   stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = result.communicate()
    print stdout


if __name__ == '__main__':
    nginx_push_role = "/etc/ansible/channel/%s_config.yml" % get_result().get("process_name")
    push_config(yml_path=nginx_push_role, hosts=hosts)
