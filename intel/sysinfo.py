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

import os
import glob


SYS_FPGA = "/sys/class/fpga"
DEVICE = "device"
PF = "physfn"
VF = "virtfn*"

DEVICE_FILE_MAP = {"vendor": "vendor_id",
                   "device": "product_id",
                   "sriov_numvfs": "pr_num"}
DEVICE_FILE_HANDLER = {}
DEVICE_EXPOSED = ["vendor", "device", "sriov_numvfs"]


def all_fpgas():
    # glob.glob1("/sys/class/fpga", "*")
    return glob.glob(os.path.join(SYS_FPGA, "*"))


def all_vf_fpgas():
    return [dev.rsplit("/", 2)[0] for dev in
            glob.glob(os.path.join(SYS_FPGA, "*/device/physfn"))]


def all_pure_pf_fpgas():
    return [dev.rsplit("/", 2)[0] for dev in
            glob.glob(os.path.join(SYS_FPGA, "*/device/virtfn0"))]


def target_symbolic_map():
    maps = {}
    for f in glob.glob(os.path.join(SYS_FPGA, "*/device")):
        maps[os.path.realpath(f)] = os.path.dirname(f)
    return maps


def all_vfs_in_pf_fpgas(pf_path):
    maps = target_symbolic_map()
    vfs = glob.glob(os.path.join(pf_path, "device/virtfn*"))
    return [maps[os.path.realpath(vf)] for vf in vfs]


def all_pf_fpgas():
    return [dev.rsplit("/", 2)[0] for dev in
            glob.glob(os.path.join(SYS_FPGA, "*/device/sriov_totalvfs"))]


def fpga_device(path):
    infos = {}
    def read_line(filename):
        with open(filename) as f:
            return f.readline().strip()

    # NOTE "In 3.x, os.path.walk is removed in favor of os.walk."
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename in DEVICE_EXPOSED:
                key = DEVICE_FILE_MAP.get(filename) or filename
                if key in DEVICE_FILE_HANDLER and callable(
                        DEVICE_FILE_HANDLER(key)):
                    infos[key] = DEVICE_FILE_HANDLER(key)(
                       os.path.join(dirpath, filename))
                else:
                    infos[key] = read_line(os.path.join(dirpath, filename))
    return infos


def fpga_tree():

    def gen_fpga_infos(path, vf=True):
        dpath = os.path.realpath(os.path.join(path, DEVICE))
        bdf = os.path.basename(dpath)
        func = "vf" if vf else "pf"
        pf_bdf = os.path.basename(
            os.path.realpath(os.path.join(dpath, PF))) if vf else ""
        fpga = {"path": path, "function": func,
                "devices": bdf, "assignable": True,
                "parent_devices": pf_bdf}
        d_info = fpga_device(dpath)
        fpga.update(d_info)
        return fpga

    devs = []
    pure_pfs = all_pure_pf_fpgas()
    for pf in all_pf_fpgas():
        fpga = gen_fpga_infos(pf, False)
        if pf in pure_pfs:
            fpga["assignable"] = False
            fpga["regions"] = []
            vfs = all_vfs_in_pf_fpgas(pf)
            for vf in vfs:
                vf_fpga = gen_fpga_infos(vf, True)
                fpga["regions"].append(vf_fpga)
        devs.append(fpga)
    return devs
