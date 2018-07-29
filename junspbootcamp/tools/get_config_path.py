import sys
import os
from .yml_parser import parse_yml


class LabConfigHandler:
    """Gets absolute path of network element config file."""

    def __init__(self, lab, hostname):
        """
        Constructor

        :param lab: lab number.
        :param hostname: name of network element; \
            only first two letters of the name analyzed.
        """

        # Initialize inputs
        self._lab_number = lab
        self._element = hostname
        self._dir_dictionary = parse_yml().get('dir')

        # We don't know the path yet - set it to None
        self._absolute_path = None
        # We haven't created path to the directory from config yet
        self._config_dir = None
        # We don't know the filename yet
        self._config_filename = None

    def _get_lab_dir(self):
        """Creates absolute path of the config directory from user inputs in YAML file."""
        if self._lab_number:
            _lab = self._lab_number
            _dir = self._dir_dictionary
            if 0 < int(self._lab_number) < 10:
                _lab = str(0) + str(_lab)
            lab_config_dir = _dir.get('top_dir') + "/" + \
                             _dir.get('subdir_level_1') + \
                             _lab + "/" + \
                             _dir.get('subdir_level_2')
            self._config_dir = lab_config_dir
            return self._config_dir
        else:
            print('Please provide lab number as CLI argument or in loader.yml')

    def _get_config_filename(self):
        """Searches for a config file in config directory"""
        # Getting list of filenames in the lab directory
        lab_dir = self._get_lab_dir()
        file_list = os.listdir(lab_dir)
        # Looking for a filename, where first two letters are the same as the router name
        dev = self._element.lower()
        for filename in file_list:
            # print('Checking', filename, 'where first symbols are', filename[:2])
            if dev[:2] == filename.lower()[:2] and filename.split('.')[1] == 'config':
                print('returning', filename)
                #return filename
                self._config_filename = filename
                break
        if self._config_filename:
            return self._config_filename
        else:
            for filename in file_list:
                if dev[:2] == filename.lower()[:2] and filename.split('.')[1] == 'conf':
                    # print('returning', filename)
                    self._config_filename = filename
                    break
                # Special case for lab 8, when filename for vrdevice is rec2-vr.conf
                elif dev[:2] == filename.lower()[5:7] and filename.split('.')[1] == 'conf':
                    # print('returning', filename)
                    self._config_filename = filename
                    break
            return self._config_filename

    def _get_full_path(self):
        """Creates absolute path from config directory and filename"""
        _lab_directory = self._get_lab_dir()
        _config_file = self._get_config_filename()
        if _lab_directory:
            if _config_file:
                self._absolute_path = str(_lab_directory + "/" + _config_file)
        return self._absolute_path

    @property
    def lab_dir(self):
        """Returns absolute path to the config file"""
        lab_dir = self._get_lab_dir()
        return lab_dir

    @property
    def path(self):
        """Returns absolute path to the config file"""
        path = self._get_full_path()
        return path


def main():
    """Allows using script with CLI arguments"""
    if len(sys.argv) != 3:
        print('Please provide exactly two script parameters:')
        print('1) lab number ')
        print('2) network element hostname')
        print('First two letters of the hostname will be compared with config file names')
        sys.exit(1)
    else:
        lab_number = sys.argv[1]
        hostname = sys.argv[2]
        print(LabConfigHandler(lab_number, hostname).path)


if __name__ == '__main__':
    main()
