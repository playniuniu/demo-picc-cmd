#!/env/bin/python3
# -*- coding: utf-8 -*-
import argparse
import config
from lib.WeblogicTools import WeblogicTools
from lib.SSHClient import SSHClient


def add_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="weblogic server ip",
                        metavar="target", required=True, dest="ip")
    parser.add_argument("-u", help="weblogic server username",
                        metavar="user", required=True, dest="username")
    parser.add_argument("-p", help="weblogic server password",
                        metavar="password", required=True, dest="password")
    parser.add_argument("-w", help="upload config file to weblogic",
                        action="store_true", dest="upload")
    args = parser.parse_args()
    # return vars(args)
    return args


def run():
    args = add_argparse()
    ssh_client = SSHClient(args.ip, args.username, args.password)
    weblogic_tools = WeblogicTools(ssh_client)
    if args.upload:
        weblogic_tools.upload_configfile(config.WEBLOGIC_FILE)
    else:
        config_file = weblogic_tools.get_configfile(config.WEBLOGIC_FILE)
        weblogic_tools.format_output(config_file)


if __name__ == '__main__':
    run()
