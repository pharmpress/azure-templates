#!/usr/bin/env bash

umount /mnt/data
printf "p\nd 1\nw\np" |  fdisk /dev/sdc
rmdir /mnt/data
