from junspbootcamp.tools.yml_parser import parse_yml
from junspbootcamp.tools.create_base_config import prepare_base_config
from junspbootcamp.tools.create_lab_config import create_lab_config
from junspbootcamp.tools.create_lab8_config import prepare_custom_config
from junspbootcamp.tools.install_script import install_script
from junspbootcamp.tools.load_config_pyez import load_cfg_pyez
from junspbootcamp.tools.disable_unused_interfaces import get_interfaces
from junspbootcamp.tools.disable_unused_interfaces import disable_unused_interfaces


class Loader:
    """Modifies and loads config(s) to vMXs"""

    def __init__(self):
        """Constructor"""

        # private attributes
        parsed_loader_yml = parse_yml()
        self._hosts = parsed_loader_yml.get('hosts')
        self._auth = parsed_loader_yml.get('auth')
        self._user = self._auth.get('user')
        self._auth_method = self._auth.get('method')
        if self._auth_method == 'password':
            self._pass = self._auth.get('password')
        else:
            self._pass = False

    def prepare_environment(self):
        pass

    def _create_base_config(self, host):
        """Creates base config from the template

        :param host: hostname of the device
        :type host: string
        """
        _mgmt_ip = self._hosts.get(host)
        if _mgmt_ip:
            _base_conf_filename = prepare_base_config(host, _mgmt_ip)
            return _base_conf_filename
        else:
            print('Cannot get management IP from loader.yml')
            print('Ensure that hostnames in config.yml are in lower case')
            return None

    def load_base_config(self, host):
        """Replaces existing network element config with the one based on template

        :param host: hostname of the device
        :type host: string
        """
        _conf = self._create_base_config(host)
        if _conf:
            _user = self._auth.get('user')
            _pass = self._auth.get('password')
            load_cfg_pyez(host, _conf, _user, _pass, mode='overwrite')
        else:
            return None

    @staticmethod
    def _create_lab_config(lab, host):
        """Removes unsupported lines from original config.

        E.g. Juniper's configs for JNCIE SP bootcamp are created for SRX devices.
        There is "security" section there, which is not supported by vMX - config load fails.
        NOTE: The task is solved in remove_unsupported.py -
        routine integration with other modules is to be done
        :param config:
        :return:
        """
        create_lab_config(lab, host)

    def load_lab_config(self, lab, host):
        """Merges existing network element config with lab config

        :param int lab: lab number
        :param str host: hostname of the device
        """
        _conf = create_lab_config(lab, host)
        # we want only interfaces used in the lab to be used, the rest disabled
        interfaces_to_use = get_interfaces(_conf)

        _user = self._auth.get('user')
        _pass = self._auth.get('password')
        load_cfg_pyez(host, _conf, _user, _pass, mode='merge')

        # Checking if custom configs should be loaded
        #
        # lab 8 (Multicast) requires additional devices as multicast receivers
        if lab == str(8) and host == 'vrdevice':
            # create custom config for the device
            configs = ['Rec1.conf', 'Rec3.conf', 'Rec4.conf']
            _conf = prepare_custom_config(lab, host, configs)
            interfaces_to_use = interfaces_to_use + get_interfaces(_conf)
            # load created config to the device
            load_cfg_pyez(host, _conf, _user, _pass, mode='merge')

            # load multiping.slax script
            install_script(lab, host, _user, _pass, 'multiping.slax', '/var/db/scripts/op/')

        #
        try:
            disable_unused_interfaces(host, _user, _pass, interfaces_to_use)
        except Exception as e:
            print('Cannot disable unused interfaces due to an error, ')
            print('however this is not critical - you can proceed further')
            # TO IMPLEMENT LATER - LOG THE EXCEPTION
            print(e)

    def load_one_device(self, lab, host):
        ip = self._hosts.get(host)
        print('')
        print('Processing', host, 'with IP address', ip)
        self.load_base_config(host)
        self.load_lab_config(lab, host)
        print('Done with', host)
        print('======================')

    def load_all_devices(self, lab):
        """
        Load configs for all devices in the lab.

        First, it replaces current config with base configuration,
        specific to your lab (SSH keys, etc.)
        Second, it replaces devices' configs with the ones from some directory
        (e.g. provided with JNCIE bootcamp course).
        """
        hosts_sorted = sorted(self._hosts)
        hosts_done = list()
        print('')
        print('+++++++++++++')
        print('Processing ALL devices:', ", ".join(hosts_sorted))
        for host in hosts_sorted:
            self.load_one_device(lab, host)
            hosts_done.append(host)
        print('')
        print('Done with', ", ".join(hosts_done))
        print('+++++++++++++')
        print('')
