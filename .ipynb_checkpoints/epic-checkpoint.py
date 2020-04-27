#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  17 15:58:51 2019

@author: ivar
"""

import os
from execute import run_shell_command, \
                    run_shell_command_with_environment

def convert_nii_to_mgz(nii_file):

    process_msg_prefix = "PID %i: " % os.getpid()
    
    mgz_file = nii_file[:-len(".nii")] + ".mgz"
    
    full_command = 'mri_convert ' + \
        '"' + nii_file + '"' + ' ' + \
        '"' + mgz_file + '"'

    run_shell_command(full_command)
        
    print(process_msg_prefix + "convert_nii_to_mgz: Successfully converted " + \
                  nii_file + " to " + \
                  mgz_file)
    
    return mgz_file

def convert_mgz_to_nii(mgz_file):

    process_msg_prefix = "PID %i: " % os.getpid()
    
    nii_file = mgz_file[:-len(".mgz")] + ".nii"
    
    full_command = 'mri_convert ' + \
        '"' + mgz_file + '"' + ' ' + \
        '"' + nii_file + '"'

    run_shell_command(full_command)
        
    print(process_msg_prefix + "convert_mgz_to_nii: Successfully converted " + \
                  mgz_file + " to " + \
                  nii_file)
    
    return nii_file

def epic_compute(forward_epi_mgz_file, \
                 reverse_epi_mgz_file, \
                 output_directory):

    process_msg_prefix = "PID %i: " % os.getpid()
    
    displacement_mgz_file_name = "displacement_field.mgz"
    displacement_mgz_file = output_directory + "/" + displacement_mgz_file_name
    
    # NB! In additional to making displacement_field.mgz , this compiled
    # version of EPIC makes:
    # - fB0uw.mgz for corrected / unwarped pos. / forward EPI mgz
    # - rB0uw.mgz for corrected / unwarped neg. / reverse EPI mgz
    # - avgEIP.mgz for average 
    # - difEIP.mgz for difference
    
    forward_epi_corrected_mgz_file = output_directory + "/" + "fB0uw.mgz"
    reverse_epi_corrected_mgz_file = output_directory + "/" + "rB0uw.mgz"
    
    source_script = 'epic_src/SetUpEpic.sh'
    
    full_command = 'epic_src/bin/epic ' + \
        '-f ' + '"' + forward_epi_mgz_file + '"' + ' ' + \
        '-r ' + '"' + reverse_epi_mgz_file + '"' + ' ' + \
        '-od ' + '"' + output_directory + '"' + ' ' + \
        '-do ' + '"' + displacement_mgz_file_name + '"'        

    #full_command = pre_command + ' && ' + command

    run_shell_command_with_environment(full_command, source_script)
        
    print(process_msg_prefix + "epic_compute: Successfully computed " + \
                  displacement_mgz_file + " " + \
                  "from forward/pos. phase encoded EPI " + \
                  displacement_mgz_file + " and reverse/neg. phase encoded EPI " + \
                  reverse_epi_mgz_file)
    
    # TODO: also return avgEIP.mgz and difEIP.mgz files
    return forward_epi_corrected_mgz_file, \
            reverse_epi_corrected_mgz_file, \
            displacement_mgz_file

def epic_apply_reverse(reverse_epi_mgz_file, \
                       reverse_epi_mgz_file_name, \
                       displacement_mgz_file, \
                       output_directory):
    
    process_msg_prefix = "PID %i: " % os.getpid()
    
    reverse_epi_corrected_mgz_file_name = \
        reverse_epi_mgz_file_name[:-len(".mgz")] + \
        "_applyepic.mgz"
    
    source_script = 'epic_src/SetUpEpic.sh'
    
    full_command = 'epic_src/bin/applyEpic ' + \
        '-r ' + '"' + reverse_epi_mgz_file + '"' + ' ' + \
        '-d ' + '"' + displacement_mgz_file + '"' + ' ' + \
        '-ro ' + '"' + reverse_epi_corrected_mgz_file_name + '"' + ' ' + \
        '-od ' + '"' + output_directory + '"'
        #'-od ' + '"/' + output_directory + '"' # (A '/' must precede the text name of the directory.)

    #full_command = pre_command + ' && ' + command

    run_shell_command_with_environment(full_command, source_script)
        
    reverse_epi_corrected_mgz_file = \
        output_directory + "/" + reverse_epi_corrected_mgz_file_name
    
    print(process_msg_prefix + "epic_apply_reverse: Successfully unwarped DSC EPI " + \
                  reverse_epi_mgz_file + " " + \
                  "into DSC EPI " + \
                  reverse_epi_corrected_mgz_file + " " + \
                  "using displacement field " + \
                  displacement_mgz_file)
    
    return reverse_epi_corrected_mgz_file
