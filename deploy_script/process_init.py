#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.compile

import handle_files
import handle_process
import argparse
import sys
import time
import datetime


def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="EG: '%(prog)s'  -p start|stop|status|restart|log|deploy")
    parser.add_argument('-p', '--process', default='log',
                        help='Input One of the \
                        {start|stop|status|restart|log|deploy}')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.1')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def main():
    args = check_arg(sys.argv[1:])
    if args.process == "start":
        handle_process.process_init()
    elif args.process == "stop":
        handle_process.process_kill()
    elif args.process == "status":
        handle_process.process_status()
    elif args.process == "log":
        handle_process.process_log_info()
    elif args.process == "restart":
        handle_process.process_kill()
        time.sleep(10)
        handle_process.process_init()
    elif args.process == "deploy":
        handle_files.process_judgment_dir()
        print "\033[32mWaitting Unzip project\033[0m" + "." * 10
        start_time = datetime.datetime.now()
        handle_files.process_source()
        end_time = datetime.datetime.now()
        print "\033[32mPorject Unzip End-time(s):%s\033[0m" \
              % (end_time - start_time).seconds
        handle_process.process_kill()
        handle_files.process_link()
        handle_process.process_init()


if __name__ == '__main__':
    main()
