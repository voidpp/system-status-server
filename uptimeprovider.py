
import re

from dataproviderbase import DataProviderBase

class UptimeProvider(DataProviderBase):
    def __init__(self):
        self.pattern = re.compile('([0-9\.]{2,}) ([0-9\.]{2,})')

    def fetch(self):

        output = ''
        with open('/proc/uptime') as file:
            output = file.read()

        matches = self.pattern.search(output)

        if matches is None:
            print "Regex search failed. Output: '%s'" % output
            return dict()

        return dict(
            uptime = float(matches.group(1))
        )
