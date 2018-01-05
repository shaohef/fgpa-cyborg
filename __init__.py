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

import os
import glob


__import__('pkg_resources').declare_namespace(__name__)
__import__(".".join([__package__, 'base']))


def load_fpga_vendor_driver():
    files = glob.glob(os.path.join(os.path.dirname(__file__), "*/driver*"))
    modules = set(map(lambda s: s.rsplit(".")[0].replace("/", "."), files))
    for m in modules:
        try:
            __import__(m, globals(), locals(), [''])
            print("Succefully to load fpga vendor driver: %s." % m)
        except ImportError as e:
            print("Failed to load fpga vendor driver: %s. Details: %s"
                  % (m, e))


load_fpga_vendor_driver()
