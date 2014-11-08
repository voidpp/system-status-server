
import re
import subprocess

from dataproviderbase import DataProviderBase

class LoadProvider(DataProviderBase):
    def __init__(self):
        self.pattern = re.compile('load average: ([0-9\.]{2,}), ([0-9\.]{2,}), ([0-9\.]{2,})')

    def fetch(self):
        try:
            output = subprocess.Popen('uptime', stdout=subprocess.PIPE).communicate()[0].strip()
        except Exception as e:
            print e
            return dict()

        matches = self.pattern.search(output)

        if matches is None:
            print "Regex search failed. Output: '%s'" % output
            return dict()

        return dict(
            load = [
                float(matches.group(1)),
                float(matches.group(2)),
                float(matches.group(3))
            ]
        )
