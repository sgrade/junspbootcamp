import fileinput
import shutil
import sys
import os


def prepare_base_config(host, ip_address):
    """
    Creates base device config from base template.

    Replaces the IP_ADDR in the template with the device's IP address
    :param ip_address: device management IP address
    :return: base config file name
    """

    print('Preparing base config')

    work_dir = os.getcwd()
    base_template = work_dir+'/junspbootcamp/templates/base_template'

    # copy essential template to a tmp directory
    # print('Filling template with the IP address:', ip_address)
    tmp_file = '/tmp/' + host + '.base'
    shutil.copyfile(base_template, tmp_file)

    # writing the IP address instead of the ip_addr place holder
    for line in fileinput.input([tmp_file], inplace=True):
        print(line.replace('IP_ADDR', str(ip_address)), end='')

    return tmp_file


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide CLI arguments: hostname and IP address')
        sys.exit(1)
    hostname = sys.argv[1]
    address = sys.argv[2]
    prepare_base_config(hostname, address)

