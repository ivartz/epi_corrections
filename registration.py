#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 17:10:25 2018

@author: ivar
"""
import os
from execute import run_shell_command

def highres_to_lowres_registration(highres_file, \
                                   lowres_file, \
                                   output_directory, \
                                   registration_desc):
    # wraps around FreeSurfer's 
    # mri_robust_register .
    # Returns the mapmov output file.
    
    process_msg_prefix = "PID %i: " % os.getpid()

    options = "--nosym --noinit --satit --iscale --verbose 2"
    
    lta_file = output_directory + \
                        "/" + \
                        registration_desc + \
                        "_lta.lta"
    mapmov_file = output_directory + \
                        "/" + \
                        registration_desc + \
                        "_mapmov.nii"
    mapmovhdr_file = output_directory + \
                        "/" + \
                        registration_desc + \
                        "_mapmovhdr.nii"
    weights_file = output_directory + \
                        "/" + \
                        registration_desc + \
                        "_weights.nii"
    bash_run_log_file = output_directory + \
                        "/" + \
                        registration_desc + \
                        "_bash_run_log.txt"                        
    bash_run_log_command = "2>&1 | tee"

    full_command = 'mri_robust_register ' + \
                '--mov "' + highres_file + '" ' + \
                '--dst "' + lowres_file + '" ' + \
                '--lta "' + lta_file + '" ' + \
                '--mapmov "' + mapmov_file + '" ' + \
                '--mapmovhdr "' + mapmovhdr_file + '" ' + \
                '--weights "' + weights_file + '" ' + \
                options + ' ' + \
                bash_run_log_command + ' ' + \
                '"' + bash_run_log_file + '"'

    run_shell_command(full_command)
    
    print(process_msg_prefix + "Ran mri_robust_register " + \
          "with registration_desc: " + \
          registration_desc + " "\
          "with --mov " + \
          highres_file + " " + \
          "and --dst " + \
          lowres_file)
    
    return mapmov_file