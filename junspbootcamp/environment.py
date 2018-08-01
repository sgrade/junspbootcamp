from junspbootcamp.tools.yml_parser import parse_yml
import paramiko


class Environment:

    def __init__(self, config='config.yml'):
        self._server = parse_yml(config).get('server')['ip-address']

    @property
    def server(self):
        """Get server as defined in config.yml"""
        return self._server

    @server.setter
    def server(self, value):
        self._server = value


