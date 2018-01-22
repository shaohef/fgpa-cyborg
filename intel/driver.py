# Copyright 2018 Intel, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
Cyborg Intel FPGA driver implementation.
"""

# from cyborg.accelerator.drivers.fpga.base import FPGADriver
from fpga.base import FPGADriver
from sysinfo import fpga_tree


class IntelFPGADriver(FPGADriver):
    """Base class for FPGA drivers.

       This is just a virtual FPGA drivers interface.
       Vedor should implement their specific drivers.
    """
    VENDOR = "intel"

    def __init__(self, args):
        pass

    def discover(self):
        return fpga_tree()

    def program(self, device_path, image):
        raise NotImplementedError("The program function of Intel FPGA "
                                  "dirver is not implemented.")
