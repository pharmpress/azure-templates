#!/usr/bin/env python

import os
import subprocess
import re
import pwd


def run_get_output(cmd, chk_err=True, log_cmd=False):
    if log_cmd:
        print(cmd)
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError, e:
        if chk_err and log_cmd:
            print('CalledProcessError.  Error Code is ' + str(e.returncode))
            print('CalledProcessError.  Command string was ' + e.cmd)
            print('CalledProcessError.  Command result was ' + (e.output[:-1]).decode('latin-1'))
        return e.returncode, e.output.decode('latin-1')
    return 0, output.decode('latin-1')


def run(cmd, chk_err=True):
    return run_get_output(cmd, chk_err)[0]


def get_mount_point(a_device):
    mount_list = run_get_output("mount")[1]
    if mount_list and a_device:
        for entry in mount_list.split('\n'):
            if re.search(a_device, entry):
                tokens = entry.split()
                # Return the 3rd column of this line
                return tokens[2] if len(tokens) > 2 else None
    return None


def change_owner(filepath, user):
    try:
        p = pwd.getpwnam(user)
        if p is not None:
            if not os.path.exists(filepath):
                print("Path does not exist: {0}".format(filepath))
            else:
                os.chown(filepath, p[2], p[3])
    except:
        pass


def create_dir(dir_path, user, mode):
    try:
        os.makedirs(dir_path, mode)
    except:
        pass
    change_owner(dir_path, user)


device = "/dev/sdc"
mount_point = "/mnt/data"
fs = "ext3"

if get_mount_point(device):
    print("ActivateResourceDisk: " + device + "1 is already mounted.")
else:
    create_dir(mount_point, "root", 0755)
    partition = device + "1"

    # Check partition type
    ret = run_get_output("parted {0} print".format(device))

    if ret[0] == 0:
        # Get partitions.
        parts = filter(lambda x: re.match("^\s*[0-9]+", x), ret[1].split("\n"))
    else:
        parts = []

    # If there are more than 1 partitions, remove all partitions
    # and create a new one using the entire disk space.
    if len(parts) > 1:
        for i in range(1, len(parts) + 1):
            run("parted {0} rm {1}".format(device, i))
        parts = []

    if len(parts) == 0:
        print("Create partition and format")
        run("parted {0} mklabel msdos mkpart primary 0% 100%".format(device))
        run("mkfs." + fs + " " + partition + " -F")

    existingFS = run_get_output("sfdisk -q -c " + device + " 1", chk_err=False)[1].rstrip()
    if existingFS == "7":
        run("sfdisk -c " + device + " 1 83")
        run("mkfs." + fs + " " + partition)

    if run("mount " + partition + " " + mount_point, chk_err=False):
        # If mount failed, try to format the partition and mount again
        print("Failed to mount resource disk. Retry mounting.")
        run("mkfs." + fs + " " + partition + " -F")
        if run("mount " + partition + " " + mount_point):
            print("ActivateResourceDisk: Failed to mount resource disk (" + partition + ").")
    print("Resource disk (" + partition + ") is mounted at " + mount_point + " with fstype " + fs)
