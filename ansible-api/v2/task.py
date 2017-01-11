# -*- coding: utf-8 -*-
import os
import sys
import json
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible import constants as C


class ResultCallback(CallbackBase):

    # ansible 运行时的返回结果处理
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    # 当ansible 运行时无法到达时返回结果
    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    # 当 ansible 成功时返回
    def v2_runner_on_ok(self, result,  *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    # 当 ansible 失败时返回
    def v2_runner_on_failed(self, result,  *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class MyRunner(object):

    # 定义运行 playbooks传入主机列表 和 playbooks路径列表
    def run_playbooks(self, host_list, playbook_path):
        # 管理变量的类,包括主机,组,扩展等变量
        variable_manager = VariableManager()
        # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
        loader = DataLoader()
        # 根据 inventory 加载对应变量
        inventory = Inventory(
            loader=loader, variable_manager=variable_manager,
            host_list=host_list)

        if not os.path.exists(playbook_path):
            print '[INFO] The playbook does not exist'
            sys.exit()
        # playbooks 运行时的变量相当于本地的 ansible.cfg 文件
        Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts',
                                         'syntax', 'connection', 'module_path',
                                         'forks', 'remote_user',
                                         'private_key_file', 'ssh_common_args',
                                         'ssh_extra_args', 'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method',
                                         'become_user', 'verbosity', 'check'])
        options = Options(listtags=False, listtasks=False, listhosts=False,
                          syntax=False, connection='ssh', module_path=None,
                          forks=100, remote_user='root', private_key_file=None,
                          ssh_common_args=None, ssh_extra_args=None,
                          sftp_extra_args=None, scp_extra_args=None,
                          become=True, become_method=None, become_user='root',
                          verbosity=None, check=False)

        # This can accomodate various other command line arguments.`
        # 运行 playbooks 时的额外参数
        # variable_manager.extra_vars = {'hosts': 'mywebserver'}
        # 可以使用密码进行连接
        passwords = {}

        # 运行 playbooks
        pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory,
                                variable_manager=variable_manager, loader=loader,
                                options=options, passwords=passwords)

        results = pbex.run()
        return results

    def Order_Run(self, host_list, module_name, module_args):

        variable_manager = VariableManager()
        loader = DataLoader()
        inventory = Inventory(
            loader=loader, variable_manager=variable_manager, host_list=host_list)
        Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts',
                                         'syntax', 'connection', 'module_path',
                                         'forks', 'remote_user', 'private_key_file',
                                         'ssh_common_args', 'ssh_extra_args',
                                         'sftp_extra_args', 'scp_extra_args',
                                         'become', 'become_method', 'become_user',
                                         'verbosity', 'check'])
        options = Options(listtags=False, listtasks=False, listhosts=False,
                          syntax=False, connection='ssh', module_path=None,
                          forks=100, remote_user='root', private_key_file=None,
                          ssh_common_args=None, ssh_extra_args=None,
                          sftp_extra_args=None, scp_extra_args=None,
                          become=True, become_method=None, become_user='root',
                          verbosity=None, check=False)
        passwords = {}

        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[
                dict(action=dict(module=module_name, args=module_args))]
        )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        tqm = None
        callback = ResultCallback()
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                stdout_callback=callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )

            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
        results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in callback.host_ok.items():
            results_raw['success'][host] = result._result

        for host, result in callback.host_failed.items():
            results_raw['failed'][host] = result._result

        for host, result in callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result
        return json.dumps(results_raw)
