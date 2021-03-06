
import psutil
import subprocess
import re
from collections import namedtuple

from .dataproviderbase import DataProviderBase

partition = namedtuple('partition', ['device', 'label', 'mount', 'used', 'total', 'free', 'percent'])

class HDDProvider(DataProviderBase):

    def __init__(self):
        self.label_pattern = re.compile(r'(\/dev\/[a-z0-9A-Z\/]{3,}) on .+ \[(.+)\]')

    def fetch(self):

        data = self.get_full_stat(self.get_labels())

        return dict(
            hdd = [r._asdict() for r in data]
        )

    def get_labels(self):
        try:
            mounts = subprocess.check_output(['mount','-l']).decode('utf8')
        except subprocess.CalledProcessError:
            return {}
        disks = {}
        for line in mounts.split('\n'):
            res = self.label_pattern.match(line)
            if res is None:
                continue
            disks[res.group(1)] = res.group(2)
        return disks

    def get_full_stat(self, labels):
        partitions = psutil.disk_partitions()

        data = []

        for part in partitions:
            usage = psutil.disk_usage(part.mountpoint)

            data.append(partition(
                part.device,
                labels.get(part.device, ''),
                part.mountpoint,
                usage.used,
                usage.total,
                usage.free,
                usage.percent,
            ))

        return data
