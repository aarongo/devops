# -*- coding: utf-8 -*-
from task import MyRunner
import json
import xlsxwriter


# a = MyRunner()
# print a.run_playbooks(host_list=['172.31.0.253', '172.31.1.250'],
#                     playbooks_path='/Users/lonny/Documents/Ansible_Book/playbooks/a.yml')


def base_info(host):
    get_resluts = MyRunner().Order_Run(host_list=host,
                                       module_name='setup', module_args='')
    resluts = {}

    data = json.loads(get_resluts)
    for ip in host:
        get_results = data['success'][ip]['ansible_facts']
        mem_total = get_results['ansible_memtotal_mb']
        swap_total = get_results['ansible_swaptotal_mb']
        cpu_type = get_results['ansible_processor'][-1].encode('utf-8')
        cpu_total = get_results['ansible_processor_vcpus']
        os_type = "".join((get_results['ansible_distribution'], get_results[
            'ansible_distribution_version'])).encode('utf-8')
        disk_total = sum([int(get_results["ansible_devices"][i]["sectors"]) *
                          int(get_results["ansible_devices"][i][
                              "sectorsize"]) / 1024 / 1024 / 1024
                          for i in get_results["ansible_devices"] if i[0:2] in ("sd", "ss")])
        server_type = get_results["ansible_product_name"].encode('utf-8')
        host_name = get_results["ansible_hostname"].encode('utf-8')
        os_kernel = get_results["ansible_kernel"].encode('utf-8')
        resluts[ip] = {u'物理内存容量(MB)': mem_total,
                       u'虚拟内容容量(MB)': swap_total, u'CPU型号': cpu_type,
                       u'CPU核心数': cpu_total, u'操作系统类型': os_type,
                       u'硬盘总容量(GB)': disk_total, u'服务器型号': server_type,
                       u'主机名': host_name, u'操作系统内核型号': os_kernel}
    return resluts


def covent_excel(data):
    workbook = xlsxwriter.Workbook('systeminfo.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    # 设置A1 字段
    headings = [u'IP地址', u'统计信息', u'结果']
    # 设置 A1字段属性
    format1 = workbook.add_format()  # 实例化属性类
    # 设置属性
    format1.set_bold()  # 加粗
    format1.set_font_color('#000000')  # 颜色
    format1.set_align('center')  # 字体居中
    format1.set_align('vcenter')  # 方向居中
    worksheet.write_row('A1', headings, format1)  # 设置 A1
    format = workbook.add_format()
    format.set_font_size(12)
    format.set_align('center')
    format.set_align('vcenter')
    worksheet.set_column('A:A', 15)  # 设置字段宽度
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 45)
    for key in data.keys():
        row += 1
        worksheet.write(row, col, key, format)
        for item, value in data[key].iteritems():
            worksheet.write(row, col + 1, item, format)
            worksheet.write(row, col + 2, value, format)
            row += 1

    workbook.close()


def main():
    host_list = ['172.31.0.253', '10.90.3.110',
                 '172.31.10.100', '172.31.1.252']
    # run convent execl
    print base_info(host=host_list)
    covent_excel(base_info(host=host_list))


if __name__ == '__main__':
    main()
