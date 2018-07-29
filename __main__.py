import sys
from junspbootcamp.loader import Loader


def main():
    """
    Allows using script with CLI arguments

    Usage:
    python loader.py lab_number [hostname]
    1) If only lab_number provided, replaces all configs for all devices in the lab
    2) If lab_number and hostname provided, replaces config for one device
    """

    _host = None

    if len(sys.argv) == 2:
        _lab_number = sys.argv[1]
    elif len(sys.argv) == 3:
        _lab_number = sys.argv[1]
        _host = sys.argv[2]
    else:
        print('Please provide CLI arguments:')
        _lab_number = input('lab number: 1, 2, ... 11: ')
        _host = input('resolvable hostname (r1, r2, r3, r4, r5, vrdevice): ')

    # first script parameter (lab number) should be 1 to 11
    if 1 <= int(_lab_number) <= 11:
        # second script parameter should be one of [r1, r2, r3, r4, r5, vrdevice]
        _valid_hostnames = ['r1', 'r2', 'r3', 'r4', 'r5', 'vr', 'vrdevice']
        if _host.lower() in _valid_hostnames:
            x = Loader()
            if _host:
                x.load_base_config(_host)
                x.load_lab_config(_lab_number, _host)
            else:
                x.load_all_configs(_lab_number)
    else:
        print('Invalid input')
        sys.exit(1)


if __name__ == '__main__':
    main()