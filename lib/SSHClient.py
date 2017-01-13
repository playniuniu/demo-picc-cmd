# -*- coding: utf-8 -*-
import paramiko
from lib.Logger import Logger


class SSHClient():

    def __init__(self, ip, username, password, port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.ssh_client = None
        self.sftp_client = None
        self.logger = Logger('SSHClient').get_logger()

    def init_ssh_client(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.load_system_host_keys()
            self.ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                self.ip, self.port, self.username, self.password, timeout=5)
            return True
        except Exception as e:
            self.logger.error(
                "SSH connect to {}:{} error: {}".format(self.ip, self.port, e))
            return False

    def init_sftp_client(self):
        try:
            sftp_trans = paramiko.Transport((self.ip, self.port))
            sftp_trans.connect(username=self.username, password=self.password)
            self.sftp_client = paramiko.SFTPClient.from_transport(sftp_trans)
            return True
        except Exception as e:
            self.logger.error(
                "SFTP connect to {}:{} error: {}".format(self.ip, self.port, e))
            return False

    def execute(self, cmd):
        command_result = []
        command_status = False

        if self.init_ssh_client():
            try:
                std_in, std_out, std_err = self.ssh_client.exec_command(cmd)
                std_out_data = std_out.readlines()
                if std_out_data:
                    self.logger.debug("Execute \"{}\" success!".format(cmd))
                    command_result = std_out_data
                    command_status = True
                else:
                    self.logger.error("Execute \"{}\" error!".format(cmd))
                    command_result = std_err.readlines()
                    command_status = False
            except Exception as e:
                self.logger.error(
                    "Execute command {} error: {}".format(cmd, e))
            finally:
                self.ssh_client.close()
                self.ssh_client = None

        return command_result, command_status

    def transfile(self, local_path, remote_path, direction="upload"):
        trans_status = False

        if self.init_sftp_client():
            try:
                if direction == "upload":
                    self.sftp_client.put(local_path, remote_path)
                    self.logger.info(
                        "Upload file {} success!".format(local_path))
                else:
                    self.sftp_client.get(remote_path, local_path)
                    self.logger.debug(
                        "Download file {} success!".format(remote_path))

                trans_status = True

            except Exception as e:
                self.logger.error("Trans {} error: {}".format(direction, e))

            finally:
                self.sftp_client.close()
                self.sftp_client = None

        return trans_status


if __name__ == '__main__':
    def unit_test():
        test_command = "ifconfig -a"
        test_locale_file = "__init__.py"
        test_remote_path = "/root/test.py"
        test_locale_path = "./test.py"

        ssh_test = SSHClient("172.0.0.155", "root", "picc123456")

        print("Command test: -------------\n")

        std_out, status = ssh_test.execute(test_command)
        for line in std_out:
            print(line, end="")

        print("Command test end: -------------\n")

        print("Upload test: -------------\n")
        ssh_test.transfile(test_locale_file, test_remote_path, "upload")
        print("Upload test end: -------------\n")

        print("Download test: -------------\n")
        ssh_test.transfile(test_locale_path, test_remote_path, "download")
        print("Download test end: -------------\n")

    unit_test()
