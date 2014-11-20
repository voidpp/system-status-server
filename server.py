#!/usr/bin/env python

import argparse
import os

from infodaemon import InfoDaemon, InfoServer

parser = argparse.ArgumentParser()
start_group = parser.add_mutually_exclusive_group(required = True)
start_group.add_argument("command", help = "command", choices = ['start', 'stop', 'restart', 'status'], nargs='?')
start_group.add_argument("-c", "--console", help = "run in the console, not forking", action='store_true')
parser.add_argument("--config", help = "config file", type = str, default = 'config.json')

args = parser.parse_args()

if args.console:

    server = InfoServer(args.config)

    server.serve()

else:
    curr = os.getcwd()

    daemon = InfoDaemon(os.path.join(curr, 'server.pid'), args.config, os.path.join(curr, 'server.log'))

    command = getattr(daemon, args.command)

    print(command())
