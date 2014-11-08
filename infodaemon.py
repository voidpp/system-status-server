
import time
import json
import SocketServer

from daemon import Daemon
from httphandler import HTTPHandler

from uptimeprovider import UptimeProvider
from loadprovider import LoadProvider

providers = []

class InfoHTTPHandler(HTTPHandler):
    def do_GET(self):
        data = dict()

        for provider in providers:
            data.update(provider.fetch())

        self.set_content(json.dumps(data))

class InfoDaemon(Daemon):
    def __init__(self, pid_file, config_file, log_file = '/dev/null'):

        self.config = dict()

        try:
            with open(config_file) as file:
                self.config = json.loads(file.read())
        except ValueError as e:
            print(e)
            return

        if 'listen' not in self.config:
            print("'listen' node not found in the config")
            self.config = None

        if 'port' not in self.config['listen']:
            print("'port' value not found in the listen node")
            self.config = None

        super(InfoDaemon, self).__init__(pid_file, '/dev/null', log_file, log_file)

    def run(self):

        if self.config is None:
            return

        providers.append(UptimeProvider())
        providers.append(LoadProvider())

        address = self.config['listen']['address'] if 'address' in self.config['listen'] else '0.0.0.0'
        port = self.config['listen']['port']

        httpd = SocketServer.TCPServer((address, port), InfoHTTPHandler)
        httpd.serve_forever()
