from .yml_parser import parse_yml
from .get_config_path import LabConfigHandler



class InterfaceHandler:

    def __init__(self, lab, host, config):
        """parse loader config"""

        parsed_loader_yml = parse_yml()
        self.lab = lab
        self.host = host
        self.config = config
        self.dir = LabConfigHandler(lab, host)

    def get_used_interfaces(self):
        """parse device config and return a list of interfaces used in the lab"""
        pass

    def get_all_interfaces(self):
        """connects to a device and gets complete interface list"""
        pass

    def filter_ge_interfaces(self):
        """gets interface list and returns list of ge (Gigabit Ethernet) interfaces"""
        pass
