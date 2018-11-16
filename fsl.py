#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:51:51 2018

@author: ivar
"""

import os
from execute import run_shell_command

# Splitting NIFTI files along time axis and moving to destination for correction

def extract_first_temporary_window_and_save(output_path, \
                                              blip_file, \
                                              blip_file_name):
    # blip_file is the relative path from script root + file name
    # blip_file_name is the file name only
    
    process_msg_prefix = "PID %i: " % os.getpid()
    
    output_base_name = output_path + "/" + blip_file_name[:-len(".nii")] + "_"
    
    pre_command = 'FSLOUTPUTTYPE=NIFTI'
    command = 'fslroi ' + '"' + blip_file + '"' + ' ' + '"' + \
        output_base_name + '0000"' + ' 0 1'
    full_command = pre_command + ' && ' + command

    run_shell_command(full_command)
        
    print(process_msg_prefix + "extract_first_temporary_window_and_save: Successfully extracted " + \
                  " first temporary window of " + \
                  blip_file + " into directory " + \
                  output_path + \
                  " using fslroi in subprocess shell call")

def split_along_temporary_axis_and_save(output_path, \
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
        
    print(process_msg_prefix + "extract_first_temporary_window_and_save: Successfully split " + \
                  blip_file + " into directory " + output_path + \
                 " using fslsplit in subprocess shell call")

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

def add_duplicate_slices(output_path, file_name):
    
    process_msg_prefix = "PID %i: " % os.getpid()

    output_base = file_name[:-len(".nii")]
    output_zmin = output_base + '_zmin'
    output_zmax = output_base + '_zmax'
    output_prep = output_base + '_prep_topup'
    output_prep_file = output_path + "/" + output_prep + ".nii"
    
    pre_command = 'cd ' + '"' + output_path + '"' + \
                    ' && FSLOUTPUTTYPE=NIFTI && xdim=$(fslval ' + \
                    '"' + file_name + '"' + ' dim1) && ydim=$(fslval ' + \
                    '"' + file_name + '"' + ' dim2) && zdim=$(fslval ' + \
                    '"' + file_name + '"' + ' dim3)'
    # This command will extract the 2D lowest slice along z axis
    # to the file output_zmin.nii
    output_zmin_command = 'fslroi ' + '"' + file_name + '"' + \
        ' '  + '"' + output_zmin + '"' + \
        ' ' + '0 $xdim' + \
        ' ' + '0 $ydim' + \
        ' ' + '0 1'
    # This command will extract the 2D highest slice along z axis
    # to the file output_zmax.nii
    output_zmax_command = 'fslroi ' + '"' + file_name + '"' + \
        ' '  + '"' + output_zmax + '"' + \
        ' ' + '0 $xdim' + \
        ' ' + '0 $ydim' + \
        ' ' + '$((zdim-1)) 1'
    # This command will merge the two extracted 2D slices 
    # output_zmin.nii and output_zmax.nii to file ,
    # to the file output_prep.nii
    output_prep_command = 'fslmerge -z ' + '"' + output_prep + '"' + \
        ' '  + '"' + output_zmin + '"' + \
        ' '  + '"' + file_name + '"' + \
        ' '  + '"' + output_zmax + '"'
    # Concatenate all the commands into a one-liner command (a large string string to be evaluated in a shell environment)
    full_command = pre_command + ' && ' + output_zmin_command + ' && ' + output_zmax_command + ' && ' + output_prep_command
      
    run_shell_command(full_command)
    
    print(process_msg_prefix + "Successfully merged " + \
              "duplicate zmin and zmax slices to " + \
              output_path + "/" + file_name + \
              ", thereby creating " + \
              output_prep_file + \
              " for FSL topup")
    
    return output_prep_file

def remove_first_and_last_slices_and_save(output_path, file_name):
    
    process_msg_prefix = "PID %i: " % os.getpid()

    output_base = file_name[:-len(".nii")]
    output_file_name = output_base + '_postp'
    output_file = output_path + "/" + output_file_name + ".nii"
    
    pre_command = 'cd ' + '"' + output_path + '"' + \
                    ' && FSLOUTPUTTYPE=NIFTI && xdim=$(fslval ' + \
                    '"' + file_name + '"' + ' dim1) && ydim=$(fslval ' + \
                    '"' + file_name + '"' + ' dim2) && zdim=$(fslval ' + \
                    '"' + file_name + '"' + ' dim3)'
    # This command will extract the 2D lowest slice along z axis
    # to the file output_zmin.nii
    command = 'fslroi ' + '"' + file_name + '"' + \
        ' '  + '"' + output_file_name + '"' + \
        ' ' + '0 $xdim' + \
        ' ' + '0 $ydim' + \
        ' ' + '1 $((zdim-2))'

    # Concatenate all the commands into a one-liner command (a large string string to be evaluated in a shell environment)
    full_command = pre_command + ' && ' + command
      
    run_shell_command(full_command)
    
    print(process_msg_prefix + "Successfully removed " + \
              "first and last z slice from" + \
              output_path + "/" + file_name + \
              ", and saved to" + \
              output_file)
    
    return output_file