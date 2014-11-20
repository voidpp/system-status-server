
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
        print("[%s]:[%s]:[%s]" % (self.date_time_string(), self.client_address[0], self.requestline))

        data = dict()

        for provider in providers:
            data.update(provider.fetch())

        self.set_content(json.dumps(data))

class InfoServer(object):
    def __init__(self, config_file):

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


    def serve(self):

        providers.append(UptimeProvider())
        providers.append(LoadProvider())

        address = self.config['listen']['address'] if 'address' in self.config['listen'] else '0.0.0.0'
        port = self.config['listen']['port']

        SocketServer.TCPServer.allow_reuse_address = True

        httpd = SocketServer.TCPServer((address, port), InfoHTTPHandler)
        httpd.serve_forever()


class InfoDaemon(Daemon):
    def __init__(self, pid_file, config_file, log_file = '/dev/null'):

        self.server = InfoServer(config_file)

        if self.server.config is None:
            return

        super(InfoDaemon, self).__init__(pid_file, '/dev/null', log_file, log_file)

    def run(self):

        if self.server.config is None:
            return

        self.server.serve()
