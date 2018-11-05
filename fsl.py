#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:51:51 2018

@author: ivar
"""

import os
from execute import run_shell_command

# Splitting NIFTI files along time axis and moving to destination for correction

def split_NIFTI_file_along_time_axis_and_move(output_path, \
                                              blip_file, \
                                              blip_file_name):
    # blip_file is the relative path from script root + file name
    # blip_file_name is the file name only
    
    process_msg_prefix = "PID %i: " % os.getpid()
    
    output_base_name = output_path + "/" + blip_file_name[:-len(".nii")] + "_"

    pre_command = 'FSLOUTPUTTYPE=NIFTI'
    command = 'fslsplit ' + '"' + blip_file + '"' + ' ' + '"' + \
        output_base_name + '"' + ' -t'
    full_command = pre_command + ' && ' + command

    run_shell_command(full_command)
    
    print(process_msg_prefix + "Successfully split " + \
                  blip_file + " into directory " + output_path + \
                 " using fslsplit in subprocess shell call")

# fslmerge

# Discarding adding empty top and bottom slice along z-axis for now.
# Future fix.

def merge_blip_down_blip_up_first_temporary_window(blip_down_blip_up_temporary_window_file, \
                                                  blip_down_temporary_window_file, \
                                                  blip_up_temporary_window_file):
    # Merge nii files of different phase 
    
    # Assuming that fslsplit correctly appended
    # 0000 for the first temporary window 
    # at the end of the file name
    
    # Assuming that corresponding data
    # for both blip directions already
    # exist in output_path
    
    process_msg_prefix = "PID %i: " % os.getpid()
    
    pre_command = 'FSLOUTPUTTYPE=NIFTI'
    command = 'fslmerge -t ' + '"' + blip_down_blip_up_temporary_window_file + \
        '"' + ' ' + '"' + blip_down_temporary_window_file + \
        '"' + ' ' + '"' + blip_up_temporary_window_file + '"'
    full_command = pre_command + ' && ' + command
    
    run_shell_command(full_command)
    
    print(process_msg_prefix + "Successfully merged " + \
              blip_down_temporary_window_file + " with " + \
              blip_up_temporary_window_file + " into the file " + \
              blip_down_blip_up_temporary_window_file + \
              " using fslmerge in subprocess shell call")

def topup_compute(merged_image_for_topup_compute_file, \
                  datain, config):
    
    process_msg_prefix = "PID %i: " % os.getpid()

    output_base_name = merged_image_for_topup_compute_file[:-len(".nii")]
    out_name = output_base_name + "_generic_out"
    fout_name = output_base_name + "_field"
    iout_name = output_base_name + "_corrected"
    
    pre_command = 'FSLOUTPUTTYPE=NIFTI'
    command = 'topup --imain=' + '"' + merged_image_for_topup_compute_file + \
        '"' + ' ' + '--datain='  + '"' + datain + \
        '"' + ' ' + '--config=' + '"' + config + \
        '"' + ' ' + '--out='  + '"' + out_name + \
        '"' + ' ' + '--fout='  + '"' + fout_name + \
        '"' + ' ' + '--iout='  + '"' + iout_name + '"'
    full_command = pre_command + ' && ' + command
    
    run_shell_command(full_command)
    
    print(process_msg_prefix + "Successfully computed off-resonance field " + \
              fout_name + " based on " + \
              merged_image_for_topup_compute_file + " and used it to correct " + \
              merged_image_for_topup_compute_file + " into " + \
              iout_name)
    
    return iout_name + ".nii"