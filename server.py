#!/usr/bin/env python

import argparse
import os

from infodaemon import InfoDaemon, InfoServer

root_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
start_group = parser.add_mutually_exclusive_group(required = True)
start_group.add_argument("command", help = "command", choices = ['start', 'stop', 'restart', 'status'], nargs='?')
start_group.add_argument("-c", "--console", help = "run in the console, not forking", action='store_true')
parser.add_argument("--config", help = "config file", type = str, default = 'config.json')

args = parser.parse_args()

config = os.path.join(root_path, args.config)

if args.console:

    server = InfoServer(config)

    server.serve()

else:
    daemon = InfoDaemon(os.path.join(root_path, 'server.pid'), config, os.path.join(root_path, 'server.log'))

    command = getattr(daemon, args.command)

    print(command())
