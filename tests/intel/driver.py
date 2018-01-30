import unittest
import os
import mock
from fpga.intel.driver import IntelFPGADriver
from fpga.intel import sysinfo
import subprocess


class TestIntelFPGADriver(unittest.TestCase):

    def setUp(self):
        self.syspath = sysinfo.SYS_FPGA
        sysinfo.SYS_FPGA = "/sys/class/fpga"
        dirname = os.path.dirname(os.path.realpath(__file__))
        sysinfo.SYS_FPGA = os.path.join(
            os.path.dirname(dirname), "data",
            sysinfo.SYS_FPGA.split("/", 1)[-1])

    def tearDown(self):
        sysinfo.SYS_FPGA = self.syspath

    def test_discover(self):
        expect = [{'function': 'pf', 'assignable': False, 'pr_num': '1',
                   'vendor_id': '0x8086', 'devices': '0000:5e:00.0',
                   'regions': [{'function': 'vf', 'assignable': True,
                                'product_id': '0xbcc1',
                                'parent_devices': '0000:5e:00.0',
                                'path': '%s/intel-fpga-dev.2' % sysinfo.SYS_FPGA ,
                                'vendor_id': '0x8086',
                                'devices': '0000:5e:00.1'}],
                   'parent_devices': '',
                   'path': '%s/intel-fpga-dev.0' % sysinfo.SYS_FPGA,
                   'product_id': '0xbcc0'},
                  {'function': 'pf', 'assignable': True, 'pr_num': '0',
                   'vendor_id': '0x8086', 'devices': '0000:be:00.0',
                   'parent_devices': '',
                   'path': '%s/intel-fpga-dev.1' % sysinfo.SYS_FPGA,
                   'product_id': '0xbcc0'}]

        intel = IntelFPGADriver()
        fpgas = intel.discover()
        self.assertEqual(2, len(fpgas))
        self.assertEqual(fpgas, expect)

    @mock.patch.object(subprocess, 'Popen', autospec=True)
    def test_intel_program(self, mock_popen):

        class p(object):

            returncode = 0

            def wait(self): pass

        b = "0x5e"
        d = "0x00"
        f = "0x0"
        expect_cmd = ['sudo', 'fpgaconf', '-b', b,
                      '-d', d, '-f', f, '/path/image']
        mock_popen.return_value = p()
        intel = IntelFPGADriver()
        # program VF
        fpgas = intel.program("0000:5e:00.1", "/path/image")
        mock_popen.assert_called_with(expect_cmd, stdout=subprocess.PIPE)

        # program PF
        fpgas = intel.program("0000:5e:00.0", "/path/image")
        mock_popen.assert_called_with(expect_cmd, stdout=subprocess.PIPE)
