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
Cyborg FPGA driver implementation.
"""


class FPGADriver(object):
    """Base class for FPGA drivers.

       This is just a virtual FPGA drivers interface.
       Vedor should implement their specific drivers.
    """

    @classmethod
    def create(cls, args):
        for sclass in cls.__subclasses__():
            if args['vendor'] == sclass.VENDOR:
                return sclass(args)
        raise LookupError("Not find the FPGA driver for vendor %s"
                          % args.get('vendor'))

    def __init__(self, args):
        pass

    def discover(self):
        raise NotImplementedError()

    def program(self, device_path, image):
        raise NotImplementedError()
