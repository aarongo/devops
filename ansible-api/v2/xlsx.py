
from task import MyRunner
a = MyRunner()
books = ['/Users/lonny/Documents/Ansible_Book/playbooks/a.yml',
         '/Users/lonny/Documents/Ansible_Book/playbooks/b.yml']
for playbook in books:
    print a.run_playbooks(host_list=['172.31.0.253', '172.31.1.250'],
                          playbook_path=playbook)
