#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:47:08 2018

@author: ivar
"""
import os
import sys
from subprocess import call, Popen, PIPE, run
import shlex
#import shlex, subprocess

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

def source(script, update=True):
    """
    http://pythonwise.blogspot.fr/2010/04/sourcing-shell-script.html (Miki Tebeka)
    http://stackoverflow.com/questions/3503719/#comment28061110_3505826 (ahal)
    """
    proc = Popen(
        ['bash', '-c', 'set -a && source {} && env -0'.format(script)], 
        stdout=PIPE, shell=False)
    output, err = proc.communicate()
    output = output.decode('utf8')
    env = dict((line.split("=", 1) for line in output.split('\x00') if line))
    if update:
        os.environ.update(env)
    return env

def run_shell_command_with_environment(full_command, source_script):
    """
    https://stackoverflow.com/questions/20669558/how-to-make-subprocess-called-with-call-popen-inherit-environment-variables
    """
    process_msg_prefix = "PID %i: " % os.getpid()
    try:
        print("run_shell_command_with_environment: %s" % full_command)
        args = shlex.split(full_command)
        env = {}
        env.update(os.environ)
        env.update(source(source_script))
        retcode = run(args, env=env).returncode
        if retcode < 0:
            print(process_msg_prefix + "Child was \
            terminated by signal", -retcode, file=sys.stderr)
        #else:
        #    print(process_msg_prefix + "fslsplit: Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print(process_msg_prefix + "Error: Child execution \
        failed:", e, file=sys.stderr)
