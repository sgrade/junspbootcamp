from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP
from jnpr.junos.exception import ConnectError
from .get_config_path import LabConfigHandler


def install_script(lab, hostname, host_address, username, password, script, path):
    """Loads multiping.slax script (only for lab8 (Multicast))"""

    print('Loading', script)

    # If password is provided in loader.yml
    if password:
        try:
            dev = Device(host=host_address, user=username, password=password, gather_facts=False)
            dev.open()
        except ConnectError as err:
            print("Cannot connect to device: {0}".format(err))
            return
    # If password set to False in loader.yml (ssh key is used)
    else:
        try:
            dev = Device(host=host_address, user=username, password=None, gather_facts=False)
            dev.open()
        except ConnectError as err:
            print("Cannot connect to device: {0}".format(err))
            return

    local_path = LabConfigHandler(lab, hostname).lab_dir
    f = str(local_path + '/' + script)
    try:
        # Default progress messages
        with SCP(dev, progress=True) as scp1:
            scp1.put(f, remote_path=path)

    except Exception as err:
        print(err)
        return
    else:
        dev.close()
