#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:47:08 2018

@author: ivar
"""
import os
import sys
from subprocess import call

def run_shell_command(full_command):
    process_msg_prefix = "PID %i: " % os.getpid()
    try:
        print("run_shell_command: %s" % full_command)
        retcode = call(full_command, shell=True)
        if retcode < 0:
            print(process_msg_prefix + "Child was \
            terminated by signal", -retcode, file=sys.stderr)
        #else:
        #    print(process_msg_prefix + "fslsplit: Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print(process_msg_prefix + "Error: Child execution \
        failed:", e, file=sys.stderr)
