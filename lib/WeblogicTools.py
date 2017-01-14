# -*- coding: utf-8 -*-
from pathlib import Path
from lib.Logger import Logger
from lib.ParseWeblogicConfig import ParseWeblogicConfig


class WeblogicTools:

    SHELL_CMD = 'find /home/ -name "stopWebLogic.sh" -not -path "*/samples/*"'

    def __init__(self, ssh_client):
        self.ssh_client = ssh_client
        self.weblogic_dict = {}
        self.logger = Logger('WeblogicTools').get_logger()

    def parse_configxml_path(self, search_path):
        search_path_obj = Path(search_path)
        domain_path = search_path_obj.parents[1]
        self.logger.debug("Domain path: {}".format(domain_path))
        config_file_path = domain_path.joinpath('config/config.xml')
        return str(config_file_path)

    def get_remote_configxml_path(self):
        res, status = self.ssh_client.execute(self.SHELL_CMD)

        if not status:
            self.logger.error(
                "Cannot excute command {}".format(self.SHELL_CMD))
            return None

        if len(res) > 1:
            self.logger.error("Find multi position, Abort!")
            return None

        search_path = res[0].strip()
        return self.parse_configxml_path(search_path)

    def download_configfile(self, local_path):
        remote_path = self.get_remote_configxml_path()
        if remote_path:
            return self.ssh_client.transfile(local_path, remote_path, "download")
        else:
            self.logger.info("stop download file to {}".format(local_path))
            return False

    def upload_configfile(self, local_path):
        remote_path = self.get_remote_configxml_path()
        if remote_path:
            return self.ssh_client.transfile(local_path, remote_path, "upload")
        else:
            self.logger.info("stop upload file from {}".format(local_path))
            return False

    def get_configfile(self, local_path):
        if not self.download_configfile(local_path):
            self.logger.error("Cannot get config.xml file!")
            return {}

        self.weblogic_dict = ParseWeblogicConfig(local_path).parse(
            self.ssh_client.ip)

        return self.weblogic_dict

    def format_output(self, data):
        if data:
            print(data)


if __name__ == "__main__":
    from lib.SSHClient import SSHClient
    ssh_client = SSHClient("172.0.0.155", "root", "picc123456")
    weblogic_tools = WeblogicTools(ssh_client)
    config_dict = weblogic_tools.get_configfile("../file/config.xml")
    weblogic_tools.format_output(config_dict)
