import sys
import shutil
from .get_config_path import LabConfigHandler


def remove_unsupported(conf):
    """Removes config parts, that are not supported by vMX"""

    # vMX does not support the following
    unsupported_statement = """security {
        forwarding-options {
            family {
                inet6 {
                    mode packet-based;
                }
                mpls {
                    mode packet-based;
                }
                iso {
                    mode packet-based;
                }
            }
        }
    }"""

    # Remove LACP on ae interfaces as vMX does not support LACP on Linux bridges
    # TO BE IMPLEMENTED

    # there might be more than one occurence of unsupported statement in the file
    for i in range(0, 5):

        with open(conf, 'r+') as c:
            c_lines = c.readlines()
            c_lines_stripped = [line.strip() for line in c_lines]

            try:
                start_index = c_lines_stripped.index("security {")
                section_length = len(unsupported_statement.split('\n'))
                end_index = start_index + section_length

                updated_content = ("".join(c_lines[:start_index] + c_lines[end_index:]))

                c.seek(0)
                c.truncate(0)
                c.write(updated_content)

            except Exception as e:
                # print(e, i)
                break

        i += 1


def prepare_lab_config(lab, host):
    """
    Creates base device config from base template.

    Replaces the IP_ADDR in the template with the device's IP address
    :param ip_address: device management IP address
    :return: base config file name
    """

    _conf = LabConfigHandler(lab, host).path

    # copy the config to temp directory
    print('Preparing lab config')
    tmp_file = '/tmp/' + str(host) + '.lab'
    shutil.copyfile(_conf, tmp_file)

    # further operations will be with the tmp config to avoid breaking original config
    # print('Lab config copied to:', tmp_file)
    remove_unsupported(tmp_file)

    return tmp_file


if __name__ == "__main__":
    # create_lab_config(lab_number, hostname)
    if len(sys.argv) == 3:
        _lab_number = sys.argv[1]
        _host = sys.argv[2]
        prepare_lab_config(_lab_number, _host)
    else:
        print('Please provide CLI arguments: lab number and hostname')
        print('allowed lab numbers: 1, 2, ... 11')
        print('allowed host names: r1, r2, r3, r4, r5, vrdevice')
