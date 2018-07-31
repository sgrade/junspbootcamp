from jnpr.junos import Device
from jnpr.junos.utils.config import Config


def get_interfaces(config):
    """parses device config and returns a list of interfaces used in this config"""
    interface_list = list()
    with open(config) as c:
        c_lines = c.readlines()
        line_index = 0
        curly_braces_count = 1
        for line in c_lines:
            if line.lstrip().startswith("interfaces"):
                line_index = c_lines.index(line)
                continue
            if line_index > 0:
                line_index += 1
                if curly_braces_count > 0:
                    if line.rstrip().endswith("{"):
                        curly_braces_count += 1
                        if line.strip().split('-')[0] == 'ge':
                            interface_list.append(line.strip().split(' ')[0])
                    elif line.rstrip().endswith("}"):
                        curly_braces_count -= 1
                else:
                    # there might be several "interfaces" sections in the config
                    # e.g. in case we use logical systems
                    if line_index < len(c_lines):
                        curly_braces_count = 1
                        continue
                    else:
                        break
    return interface_list


def get_number_of_ports():
    """returns int number-of-ports from the template"""
    with open('junspbootcamp/templates/base_template') as t:
        t_lines = t.readlines()
        for line in t_lines:
            if line.strip().startswith('number-of-ports'):
                return int(line.strip().split(' ')[1][:-1])


def disable_unused_interfaces(host, _user, _pass, interface_list):
    """ Disables interfaces, which are not used in the lab"""

    print("Disabling interfaces, which are not used in the lab")

    number_of_ports = get_number_of_ports()

    dev = Device(host).open()
    with Config(dev) as cu:
        i = 0
        while i < number_of_ports:
            interface = 'ge-0/0/' + str(i)
            interface_disable_string = 'set interfaces ' + interface + ' disable'
            if interface in interface_list:
                i += 1
                continue
            else:
                cu.load(interface_disable_string, format='set')
                i += 1
        # cu.pdiff()
        cu.commit()

    dev.close()
