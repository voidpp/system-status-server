#!/usr/bin/env python

import argparse
import os

from infodaemon import InfoDaemon

parser = argparse.ArgumentParser()
parser.add_argument("command", help = "command", choices = ['start', 'stop', 'restart', 'status'])

args = parser.parse_args()

curr = os.getcwd()

daemon = InfoDaemon(os.path.join(curr, 'server.pid'), 'config.json', os.path.join(curr, 'server.log'))

command = getattr(daemon, args.command)

print(command())
