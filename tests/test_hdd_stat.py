import unittest
from unittest.mock import patch
from collections import namedtuple

from system_status_server.hddprovider import HDDProvider, partition

hdd = HDDProvider()

sdiskpart = namedtuple('sdiskpart', ['device', 'mountpoint'])
sdiskusage = namedtuple('sdiskusage', ['total', 'used', 'free', 'percent'])

class TestStat(unittest.TestCase):

    def test_parse_labels(self):
        # Arrange
        mount_result = \
        b"/dev/sdc1 on /media/f486fea4-2050-4d7a-ba46-911425d08d08 type ext4 (rw,noexec,relatime,user_xattr,barrier=1,data=ordered,jqfmt=vfsv0,usrjquota=aquota.user,grpjquota=aquota.group,_netdev) [Hyperion]\n" + \
        b"/dev/sdf1 on /media/a22a5778-7d36-4445-a906-985ce07a1a5f type ext4 (rw,noexec,relatime,user_xattr,barrier=1,data=ordered,jqfmt=vfsv0,usrjquota=aquota.user,grpjquota=aquota.group,_netdev) [Janus]\n" + \
        b"/dev/mmcblk0p2 on / type ext4 (rw,noatime,errors=remount-ro) [trusty]\n"

        # Act
        with patch('subprocess.check_output', return_value = mount_result):
            labels = hdd.get_labels()

        # Assert
        self.assertDictEqual(labels, {'/dev/sdc1': 'Hyperion', '/dev/sdf1': 'Janus', '/dev/mmcblk0p2': 'trusty'})

    def test_get_full_stat(self):
        # Arrange
        partitions = [
            sdiskpart('/dev/sdc1', '/media/f486fea4'),
            sdiskpart('/dev/sdf1', '/media/a22a5778'),
            sdiskpart('/dev/mmcblk0p2', '/'),
        ]
        usages = {
            '/media/f486fea4': sdiskusage(100, 20, 80, 20),
            '/media/a22a5778': sdiskusage(200, 130, 70, 65),
            '/': sdiskusage(10, 6, 4, 6),
        }
        labels = {'/dev/sdc1': 'Hyperion', '/dev/sdf1': 'Janus', '/dev/mmcblk0p2': 'trusty'}

        # Act
        with patch('psutil.disk_partitions', return_value = partitions):
            with patch('psutil.disk_usage', lambda p: usages[p]):
                data = hdd.get_full_stat(labels)

        # Assert
        expected = [
            partition('/dev/sdc1', 'Hyperion', '/media/f486fea4', 20, 100, 80, 20),
            partition('/dev/sdf1', 'Janus', '/media/a22a5778', 130, 200, 70, 65),
            partition('/dev/mmcblk0p2', 'trusty', '/', 6, 10, 4, 6),
        ]

        self.assertListEqual(data, expected)
