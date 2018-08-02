import sys
from .get_config_path import LabConfigHandler
from .create_lab_config import remove_unsupported


def customize_lab8_config(tmp_file):
    """Removes lines related to Rec2"""

    with open(tmp_file, 'r+') as f:
        f_lines = f.readlines()
        for line in f_lines:
            if line.strip().split(' ')[0] == 'ge-0/0/9':
                line_index = f_lines.index(line)
                del(f_lines[line_index:line_index + 8])
                break
        for line in f_lines:
            if line.strip().split(' ')[0] == 'routing-options':
                line_index = f_lines.index(line)
                del(f_lines[line_index:line_index + 5])
                break
        for line in f_lines:
            if line.strip().split(' ')[0] == 'protocols':
                line_index = f_lines.index(line)
                del(f_lines[line_index:line_index + 14])
                break
        for line in f_lines:
            if line.strip().split(' ')[0] == 'policy-options':
                line_index = f_lines.index(line)
                del(f_lines[line_index:line_index + 13])
                break
        content = "".join(f_lines)
        f.seek(0)
        f.truncate()
        f.write(content)
    return tmp_file


"""Creates custom config for lab8
Original configs from the bootcamp are designed for separate routers
This script allows avoid creating separate routers 
Instead it creates config file for vrdevice with several logical systems
"""


def change_interfaces(interface, content):
    """Changes interface id in the content (config)

    :param int interface: interface id, e.g. 2
    :param list content: config content
    :return: list content: changed config
    """
    for line in content:
        line_splitted = line.strip().split(' ')
        # print(line_splitted)

        try:
            # print(line_splitted[0].split('/')[0])

            # interfaces section
            if line_splitted[0].split('/')[0] == 'ge-0':
                line_index = content.index(line)
                # print(content[line_index])
                content[line_index] = str("    ge-0/0/" + str(interface) + ' ' + "{\n")
                # print(content[line_index])
            # protocols pim section
            elif line_splitted[1].split('/')[0] == 'ge-0':
                line_index = content.index(line)
                # print(content[line_index])
                content[line_index] = str("        interface ge-0/0/" + str(interface) + '.0' + ";\n")
                # print(content[line_index])
                break
        except Exception as e:
            # print(e)
            continue

    return content


def interfaces_lab8(conf, content):
    """Specifies interface ids for the config files"""
    interface_number = 0

    if conf == 'Rec1.conf':
        interface_number = 2
    elif conf == 'Rec3.conf':
        interface_number = 4
    elif conf == 'Rec4.conf':
        interface_number = 5
    elif conf == 'Rec2.conf':
        interface_number = 9

    if interface_number == 0:
        return content
    else:
        return change_interfaces(interface_number, content)


def prepare_one_config(dir, conf):
    """Processes one config file"""

    if conf == 'Rec2.conf':
        # Special case!
        # There is no config for Rec2 in the bootcamp package as it is implemented on vrdevice
        # However, as Rec2 does not function properly on vrdevice
        # (does not send IGMP v2 reports for 224.2.2.2), we make it manually from Rec3.conf
        # AND don't forget to exclude same statements from "Rec2-vr.conf"
        config_path = str(dir + '/' + 'Rec3.conf')
    else:
        config_path = str(dir + '/' + conf)
    # print('processing config: ', config_path)

    with open(config_path, 'r') as c:
        # get the config except first two lines like these ones
        #   "## Last changed: 2011-07-27 18:02:14 UTC"
        #   "version 10.3D0;"
        c_lines = c.readlines()[2:]

        # remove "system" section
        # print('removing "system" section')
        line_index = 0
        for line in c_lines:
            if line.startswith("}"):
                line_index = c_lines.index(line)
                # print(line, line_index)
                break
        del(c_lines[:line_index+1])

        # remove interface descriptions as they lead to "syntax error" when committing under logical systems
        # print("removing interface descriptions")
        for line in c_lines:
            if line.lstrip().startswith("description"):
                c_lines.remove(line)

        # change interface id
        # print("changing interface id")
        c_lines = interfaces_lab8(conf, c_lines)

        content = "".join(c_lines)

        # Special case!
        # See details above
        if conf == 'Rec2.conf':
            content = content.replace('172.27.1.3', '172.27.1.2')
            content = content.replace('224.3.3.3', '224.2.2.2')

        return content


def prepare_custom_config(lab, host, configs):
    """Creates custom config from several config files."""

    _conf_dir = LabConfigHandler(lab, host).lab_dir

    print('Preparing custom config')
    tmp_file = '/tmp/' + str(host) + '.' + 'custom.lab' + lab
    with open(tmp_file, 'w') as f:
        f.write('logical-systems {\n')

        # create separate logical system for each config and the configs there
        for config in configs:

            # create logical system
            logical_system_name = config.split(".")[0].lower()
            f.write(str(logical_system_name + " {\n"))

            # write config
            f.write(prepare_one_config(_conf_dir, config))

            # closing respective logical system
            f.write('}\n')

        # closing logical-systemS
        f.write('}\n')

    # remove unsupported statements from the config
    remove_unsupported(tmp_file)

    return tmp_file



