import xlsxwriter

workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()

a = {'172.31.0.253': {'host_name': 'salt-master', 'disk_total': 50,
                      'cpu_total': 4, 'mem_total': 7760,
                      'server_type': 'VMware Virtual Platform',
                      'swap_total': 4095, 'os_type': 'CentOS6.4',
                      'os_kernel': '2.6.32-358.el6.x86_64',
                      'cpu_type': 'Intel(R) Xeon(R) CPU           X5650  @ 2.67GHz'},
     '10.90.3.110': {'host_name': 'custom', 'disk_total': 298, 'cpu_total': 8,
                     'mem_total': 7769, 'server_type': 'MS-7758',
                     'swap_total': 7951, 'os_type': 'CentOS7.2.1511',
                     'os_kernel': '3.10.0-327.10.1.el7.x86_64',
                     'cpu_type': 'Intel(R) Xeon(R) CPU E31230 @ 3.20GHz'}}
# print "ipaddress:%s" % ip
# print "物理内存容量:%s" % mem_total + "MB"
# print "虚拟内容容量:%s" % swap_total + "MB"
# print "CPU型号:%s" % cpu_type
# print "CPU核心数:%s" % cpu_total
# print "操作系统类型:%s" % os_type
# print "硬盘总容量:%s" % disk_total + "GB"
# print "服务器型号:%s" % server_type
# print "服务器主机名:%s" % host_name
# print "操作系统内核型号:%s" % os_kernel
# print "-----------------我是分割线----------------"
