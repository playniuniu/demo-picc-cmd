# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from lib.Logger import Logger


class ParseWeblogicConfig:

    xmlns = {"ns": "http://www.bea.com/ns/weblogic/920/domain"}

    def __init__(self, xmlfile):
        self._xmlfile = xmlfile
        self.logger = Logger('ParseWeblogicConfig').get_logger()

    def parse(self, ip="127.0.0.1"):
        try:
            tree = ET.parse(self._xmlfile)
        except FileNotFoundError:
            self.logger.error("File {} not found!".format(self._xmlfile))
            return {}

        root = tree.getroot()
        parse_res = {
            "domain_name": self.get_domain_name(root),
            "domain_version": self.get_domain_version(root),
            "adminserver": self.get_admin_server(root),
            "server_list": self.get_server_list(root),
        }
        parse_res_all = self.parse_self(parse_res, ip)
        return parse_res_all

    def parse_self(self, data, ip):
        server_name = "UNKNOWN"
        server_type = "UNKNOWN"
        server_list = data['server_list']
        for el in server_list:
            if el['ip'] == ip:
                server_name = el['name']

        if server_name != "UNKNOWN":
            if server_name == data['adminserver']:
                server_type = "AdminServer"
            else:
                server_type = "ManagedServer"

        data.update({
            "host_name": server_name,
            "host_type": server_type
        })
        return data

    def get_server_list(self, root):
        server_list = []
        for child in root.findall('ns:server', self.xmlns):
            server_name = child.find('ns:name', self.xmlns)
            server_address = child.find('ns:listen-address', self.xmlns)
            server_port = child.find('ns:listen-port', self.xmlns)
            
            if server_port is not None:
                parse_server_port = server_port.text
            else:
                parse_server_port = "7001"
                

            server_list.append({
                "name": server_name.text,
                "ip": server_address.text,
                "port": parse_server_port
            })

        return server_list

    def get_admin_server(self, root):
        for child in root.findall('ns:admin-server-name', self.xmlns):
            if child.tag:
                return child.text

        return None

    def get_domain_name(self, root):
        for child in root.findall('ns:name', self.xmlns):
            if child.tag:
                return child.text

        return None

    def get_domain_version(self, root):
        for child in root.findall('ns:domain-version', self.xmlns):
            if child.tag:
                return child.text

        return None


if __name__ == "__main__":
    weblogic_file = "../file/config.xml"
    parseobj = ParseWeblogicConfig(weblogic_file)
    print(parseobj.parse())
