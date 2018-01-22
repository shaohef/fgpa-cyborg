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

import os
import glob

SYS_FPGA = "/sys/class/fpga"

def all_fpgas():
    # glob.glob1("/sys/class/fpga", "*")
    return glob.glob("/sys/class/fpga/*")

def all_vf_fpgas():
    return [dev.rsplit("/", 2)[0] for dev in
            glob.glob("/sys/class/fpga/*/device/physfn")]

def all_pf_fpgas():
    return list(set(all_fpgas()) - set(all_vf_fpgas()))


DEVICE_FILE = {"sriov_numvfs": "sriov_numvfs",
               "reset": "reset",
               "iommu_group": "iommu_group",
               "enable": "enable", 
               "uevent": "uevent",
               "numa_node": "numa_node",
               "class": "class",
               "resource": "resource",
               "dma_mask_bits": "dma_mask_bits",
               "subsystem": "subsystem",
               "vendor": "vendor_id",
               "firmware_node": "firmware_node",
               "irq": "irq",
               "resource0_wc": "resource0_wc",
               "driver_override": "driver_override",
               "local_cpus": "local_cpus",
               "msi_bus": "msi_bus",
               "resource0": "resource0",
               "d3cold_allowed": "d3cold_allowed",
               "fpga": "fpga",
               "resource2_wc": "resource2_wc",
               "consistent_dma_mask_bits": "consistent_dma_mask_bits",
               "config": "config",
               "local_cpulist": "local_cpulist",
               "resource2": "resource2",
               "subsystem_vendor": "subsystem_vendor",
               "iommu": "iommu",
               "modalias": "modalias",
               "device": "product_id",
               "remove": "remove",
               "virtfn0": "virtfn0",
               "broken_parity_status": "broken_parity_status",
               "power": "power",
               "sriov_totalvfs": "sriov_totalvfs",
               "driver": "driver",
               "rescan": "rescan",
               "subsystem_device": "subsystem_device"}

def fpgas():
    DEVICE = "device"
    PF = "physfn"
    VF = "virtfn*"
    devs = []
    for root, dirs, files  in os.walk(SYS_FPGA, topdown=True):
        for d in dirs:
            fpga_path = os.path.join(SYS_FPGA, d)
            dpath = os.path.realpath(os.path.join(fpga_path, DEVICE))
            bdf = os.path.basename(dpath)
            fpga = {"path": fpga_path, "function": "",
                    "bdf": bdf, "assignable": "", "pf_bdf": ""}
            if glob.glob0(dpath, PF):
                fpga["function"] = "vf"
                fpga["assignable"] = True
                fpga["pf_bdf"] = os.path.basename(os.path.realpath(os.path.join(dpath, PF)))
            elif glob.glob1(dpath, VF):
                fpga["function"] = "pf"
                fpga["assignable"] = False
            else:
                fpga["function"] = "pf"
                fpga["assignable"] = True
            devs.append(fpga)
    return devs


class IntelFPGADriver(FPGADriver):
    """Base class for FPGA drivers.

       This is just a virtual FPGA drivers interface.
       Vedor should implement their specific drivers.
    """
    VENDOR = "intel"

    def __init__(self, args):
        pass

    def discover(self):
        raise NotImplementedError("The discover function of Intel FPGA "
                                  "dirver is not implemented.")

    def program(self, device_path, image):
        raise NotImplementedError("The program function of Intel FPGA "
                                  "dirver is not implemented.")
