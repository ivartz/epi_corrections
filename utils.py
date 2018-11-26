#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:27:16 2018

@author: ivar
"""

import os
import sys
from time import sleep
from nipype.interfaces.nipy.utils import Similarity
from execute import run_shell_command
from fsl import topup_compute, \
    extract_first_temporary_window_and_save, \
    merge_blip_down_blip_up_first_temporary_window, \
    add_duplicate_slices, \
    split_along_temporary_axis_and_save, \
    remove_first_and_last_slices_and_save, \
    copy_header

def remove_substring_after_last_slash(string_with_slashes):
    # Index for last "/" in string_with_slashes
    last_slash_index = len(string_with_slashes) - 1 - string_with_slashes[::-1].index("/")
    
    # Chars after last "/" are removed
    return string_with_slashes[:last_slash_index]

def longest_common_substring_from_beginning(string1, string2):
    if string1[0] != string2[0]:
        return ""
    
    if len(string1) < len(string2):
        index_differ = [i for i in range(len(string1)) if string1[:i] == string2[:i]][-1]
        longest_common_substring_from_beginning =  string1[:index_differ]
        
    else:
        index_differ = [i for i in range(len(string2)) if string2[:i] == string1[:i]][-1]
        longest_common_substring_from_beginning =  string2[:index_differ]
    return longest_common_substring_from_beginning

def find_common_folder_for_blip_down_blip_up_EPI_data(blip_down_file, blip_up_file):
    # Example:
    # if blip_down_file:
    # 'NIFTI/Anonymized/DEFACED_IVS/1269262582/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_prescan/142048_GE-SE_EPI_SSH_v1_32CH_V2_prescan_901_e1.nii'
    # and blip_down_file:
    # 'NIFTI/Anonymized/DEFACED_IVS/1269262582/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_scan/142048_GE-SE_EPI_SSH_v1_32CH_V2_scan_1001_e1.nii'
    # Shall return:
    # 'NIFTI/Anonymized/DEFACED_IVS/1269262582/DAY_0000'
    common_path = longest_common_substring_from_beginning(blip_down_file, blip_up_file)
    return remove_substring_after_last_slash(common_path)

def extract_file_name(path_and_file_name):
    # Finds the first index of "/" in the reversed
    # order string or path_and_file_name.
    # Then converts the reversed index to normal index.
    i = len(path_and_file_name) - path_and_file_name[::-1].index("/")
    # File name is the last part of path_and_file_name
    # after index i
    return path_and_file_name[i:]

def determine_e1_or_e2(file_name):
    if file_name[-len("e1.nii"):] == "e1.nii":
        # e1 is GE
        return "e1"
    elif file_name[-len("e1.nii"):] == "e2.nii":
        # e2 is SE
        return "e2"
    else:
        print("PID %i: Error, could not determine e1 (GE) or e2 (SE) \
        from file_name, aborting process" % os.getpid())
        sys.exit(1)

def determine_prescan_or_scan_or_corr_SENSE_or_SENSE(file_name):
    if "prescan" in file_name.lower():
        return "prescan"
    elif "scan" in file_name.lower():
        return "scan"
    elif "corr_sense" in file_name.lower():
        return "corr_SENSE"
    elif "sense" in file_name.lower():
        return "SENSE"

    # the two lasts elifs
    # are special cases.
    # Should be removed
    # for clean data
    
    elif "corr" in file_name.lower():
        # expected positive 
        # phase encoded
        return "corr"

    elif ".nii" in file_name.lower():
        # expected negative
        # phase encoded
        return "not_corr"

    else:
        print("PID %i: Error, could not determine prescan or scan or \
        corr_SENSE or SENSE from file_name, aborting process" % os.getpid())
        print(file_name)
        sys.exit(1)
    
def determine_merged_blips_file_name_topup(blip_down_file_name, \
                                     blip_up_file_name, \
                                    temporary_window_number="0000", \
                                    prep=True):
    # The returned name must correspond to the naming scheme
    # followed by the use of fslsplit in the script.
    
    if not determine_e1_or_e2(blip_down_file_name) == \
    determine_e1_or_e2(blip_up_file_name):
        print("PID %i: Error, the arguments blip_down_file_name and \
        blip_up_file_name in the determine_merged_blips_file_name_topup \
        function coud not be identified with the same echo sequence \
        (e1 (GE) or e2 (SE)), aborting process" % os.getpid())
        sys.exit(1)
    
    blip_down_type = determine_prescan_or_scan_or_corr_SENSE_or_SENSE(blip_down_file_name)
    blip_up_type = determine_prescan_or_scan_or_corr_SENSE_or_SENSE(blip_up_file_name)
    echo_type = determine_e1_or_e2(blip_down_file_name)

    blip_down_blip_up_longest_common_substring_from_beginning = \
        longest_common_substring_from_beginning(blip_down_file_name, \
                                                blip_up_file_name)

    blip_down_number_before_echo_type_in_name = \
        blip_down_file_name[len(blip_down_blip_up_longest_common_substring_from_beginning + \
           blip_down_type) + 1:][:-(len(echo_type + ".nii") + 1)]

    blip_up_number_before_echo_type_in_name = \
        blip_up_file_name[len(blip_down_blip_up_longest_common_substring_from_beginning + \
           blip_up_type) + 1:][:-(len(echo_type + ".nii") + 1)]

    if prep:
        file_ending = "_prep_topup.nii"
    else:
        file_ending = ".nii"

    merged_blips_file_name = \
        blip_down_blip_up_longest_common_substring_from_beginning + \
        blip_down_type + "_" + \
        blip_up_type + "_" + \
        blip_down_number_before_echo_type_in_name + "_" + \
        blip_up_number_before_echo_type_in_name + "_" + \
        determine_e1_or_e2(blip_down_file_name) + "_" + \
        temporary_window_number + file_ending
    
    return merged_blips_file_name

def determine_blip_file_name_for_window_topup(blip_direction , \
                                        blip_down_file_name, \
                                        blip_up_file_name, \
                                        temporary_window_number="0000"):
    
    process_msg_prefix = "PID %i: " % os.getpid()
    
    if blip_direction == "blip_down":    
        return blip_down_file_name[:-len(determine_e1_or_e2(blip_down_file_name) + ".nii")] + \
        determine_e1_or_e2(blip_down_file_name) + "_" + \
        temporary_window_number + ".nii"
    
    elif blip_direction == "blip_up":
        return blip_up_file_name[:-len(determine_e1_or_e2(blip_up_file_name) + ".nii")] + \
        determine_e1_or_e2(blip_up_file_name) + "_" + \
        temporary_window_number + ".nii"
    
    else:
        print(process_msg_prefix + " Error: determine_blip_file_name_for_window_topup: \
        the argument blip_direction is not correctly set")
        sys.exit(1)

def create_directory_if_not_exists(output_path):    
        while True:
            try:
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                else:
                    print("create_directory_if_not_exists: %s \
                          already exists, not creating" % output_path)
                break
            except OSError as e:
                if e.errno != os.errno.EEXIST:
                    raise
                # There might be a race condition, sleeping for 50 ms
                # to try again later
                sleep(0.05)
                pass

def determine_output_path(root_folder_name, \
                          NIFTI_folder_name, \
                          blip_down_file, \
                          blip_up_file, \
                          blip_down_file_name, \
                          blip_up_file_name):
    output_path = root_folder_name + \
        longest_common_substring_from_beginning(blip_down_file, \
                                                blip_up_file)[len(NIFTI_folder_name):] + \
                    determine_prescan_or_scan_or_corr_SENSE_or_SENSE(blip_down_file_name) + "_" + \
                    determine_prescan_or_scan_or_corr_SENSE_or_SENSE(blip_up_file_name)
        
    return output_path

def split_and_merge_first_temporary_for_topup(output_path, \
                                    blip_down_file, \
                                    blip_up_file):
    
    # Splitting part
    blip_down_file_name = extract_file_name(blip_down_file)
    blip_up_file_name = extract_file_name(blip_up_file)
    
    extract_first_temporary_window_and_save(output_path, \
                                              blip_down_file, \
                                              blip_down_file_name)
                                              
    extract_first_temporary_window_and_save(output_path, \
                                              blip_up_file, \
                                              blip_up_file_name)
            
    blip_down_temporary_window_file_name = \
        determine_blip_file_name_for_window_topup("blip_down", \
                                            blip_down_file_name, \
                                            blip_up_file_name)
    
    blip_down_temporary_window_file = output_path + "/" + \
        blip_down_temporary_window_file_name
    
    print("blip_down_temporary_window_file: %s" % \
          blip_down_temporary_window_file)
    
    blip_up_temporary_window_file_name = \
        determine_blip_file_name_for_window_topup("blip_up", \
                                            blip_down_file_name, \
                                            blip_up_file_name)
    
    blip_up_temporary_window_file = output_path + "/" + \
        blip_up_temporary_window_file_name
    
    print("blip_up_temporary_window_file: %s" % \
          blip_up_temporary_window_file)

    # FSL topup specific operations: add dulicate top and bottom slice
    # along z-axis, since the topup algorithm will remove top and bottom slice.
    blip_down_temporary_window_file_prep = add_duplicate_slices(output_path, blip_down_temporary_window_file_name)
    blip_up_temporary_window_file_prep = add_duplicate_slices(output_path, blip_up_temporary_window_file_name)
    
    
    # Merging part
    
    # determine file name for merged file that is prepated for topup
    # prepared means that the file has added duplicate zmin and zmax slices
    blip_down_blip_up_temporary_window_file_name = \
        determine_merged_blips_file_name_topup(blip_down_file_name, \
                                         blip_up_file_name)

    # determine file name for merged file that is not prepared
    # for topup. 
    # not prepated means that the file shall not have duplicate
    # slices added, and that it is a direct merge.
    # The point for having this is for later easier coregistration.
    # Coregistration for measure of correctness of FSL topup 
    # distortion correction.
    blip_down_blip_up_temporary_window_file_name_raw = \
        determine_merged_blips_file_name_topup(blip_down_file_name, \
                                         blip_up_file_name, \
                                         prep=False)

        
    print("blip_down_blip_up_temporary_window_file_name: %s" % \
          blip_down_blip_up_temporary_window_file_name)
    
    # prepend relative path to make blip_down_blip_up_temporary_window_file
    blip_down_blip_up_temporary_window_file = output_path + "/" + \
        blip_down_blip_up_temporary_window_file_name
    
    # prepend relative path to make blip_down_blip_up_temporary_window_file_raw
    blip_down_blip_up_temporary_window_file_raw = output_path + "/" + \
        blip_down_blip_up_temporary_window_file_name_raw
    
    print("blip_down_blip_up_temporary_window_file: %s" % \
          blip_down_blip_up_temporary_window_file)    
    
    # merge together the volumes with added duplicate slices
    merge_blip_down_blip_up_first_temporary_window(blip_down_blip_up_temporary_window_file, \
                                                      blip_down_temporary_window_file_prep, \
                                                      blip_up_temporary_window_file_prep)
    # merge together the volumes with no added duplicate slices
    # for later ease of performance comparison
    merge_blip_down_blip_up_first_temporary_window(blip_down_blip_up_temporary_window_file_raw, \
                                                      blip_down_temporary_window_file, \
                                                      blip_up_temporary_window_file)

    return blip_down_blip_up_temporary_window_file, \
            blip_down_blip_up_temporary_window_file_raw, \
            blip_down_temporary_window_file, \
            blip_up_temporary_window_file


#def evaluate_topup_performance_init(q):
#    evaluate_topup_performance.q = q

def evaluate_topup_performance(output_path, \
                               blip_down_window_file, \
                               blip_up_window_file, \
                               corrected_4D_file):
    
    # Source:
    # https://nipype.readthedocs.io/en/latest/interfaces/generated/interfaces.nipy/utils.html
    
    corrected_4D_file_name = extract_file_name(corrected_4D_file)
    
    split_along_temporary_axis_and_save(output_path, \
                                              corrected_4D_file ,\
                                              corrected_4D_file_name)
    
    # This works because we know that _0000.nii and _0001.nii
    # differ after fslsplit
    corrected_blip_down_file = corrected_4D_file[:-len(".nii")] + "_0000.nii"
    corrected_blip_down_file_name = extract_file_name(corrected_blip_down_file)
    corrected_blip_up_file = corrected_4D_file[:-len(".nii")] + "_0001.nii"
    corrected_blip_up_file_name = extract_file_name(corrected_blip_up_file)
    
    # Replace geometry info in header of corrected_blip_down_file
    # and corrected_blip_up_file with geometry info in header
    # of blip_down_window_file and blip_up_window_file respectively 
    # (non-corrected temporary window files)
    
    copy_header(blip_down_window_file, corrected_blip_down_file)
    copy_header(blip_up_window_file, corrected_blip_up_file)
    
    title = corrected_blip_down_file_name  + " and " + corrected_blip_up_file_name
    header = "Correlation Coefficient (CC),Correlation Ratio (CR),L1-norm based Correlation Ratio (L1CR),Mutual Information (MI),Normalized Mutual Inrofmation (NMI)"
    
    report = ""
    
    similarity = Similarity()
    similarity.inputs.volume1 = corrected_blip_down_file
    similarity.inputs.volume2 = corrected_blip_up_file
    similarity.inputs.metric = 'cc'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")] + ","
    
    similarity = Similarity()
    similarity.inputs.volume1 = corrected_blip_down_file
    similarity.inputs.volume2 = corrected_blip_up_file
    similarity.inputs.metric = 'cr'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")] + ","
    
    similarity = Similarity()
    similarity.inputs.volume1 = corrected_blip_down_file
    similarity.inputs.volume2 = corrected_blip_up_file
    similarity.inputs.metric = 'crl1'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")] + ","
    
    similarity = Similarity()
    similarity.inputs.volume1 = corrected_blip_down_file
    similarity.inputs.volume2 = corrected_blip_up_file
    similarity.inputs.metric = 'mi'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")] + ","
    
    similarity = Similarity()
    similarity.inputs.volume1 = corrected_blip_down_file
    similarity.inputs.volume2 = corrected_blip_up_file
    similarity.inputs.metric = 'nmi'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")]
        
    # "" since we want to skip a line between title and header
    # in the file
    data = [title, "", header, report]
    
    for d in data:
        print(d)
    
    report_name = corrected_4D_file[:-len(".nii")] + "_similarity.txt"   
    
    with open(report_name , 'w') as f:
        for line in data:
            f.write("%s\n" % line)
    
    # Return report so that topup_pipeline cam put it in a summary queue.
    # Put the report to the queue along with the nifti file.
    return report + "," + corrected_4D_file

def print_detected_data(GE_pairs, SE_pairs):
    for g in GE_pairs:
        print(g[0])
        print(g[1])    
    for s in SE_pairs:
        print(s[0])
        print(s[1])

def topup_pipeline(blip_down_file, blip_up_file):

    blip_down_file_name = extract_file_name(blip_down_file)
    
    print("blip_down_file_name: %s" % blip_down_file_name)
    
    blip_up_file_name = extract_file_name(blip_up_file)
    
    print("blip_up_file_name: %s" % blip_up_file_name)
    
    output_path = determine_output_path(topup_pipeline.TOPUP_folder_name, \
                              topup_pipeline.NIFTI_folder_name, \
                              blip_down_file, \
                              blip_up_file, \
                              blip_down_file_name, \
                              blip_up_file_name)
        
    print("output_path: %s" % output_path)
    
    #print("DBG: create if not exists: %s" % output_path)
    
    create_directory_if_not_exists(output_path)
    
    
    merged_image_for_topup_compute_file, \
    merged_image_file_raw, \
    blip_down_file_first_temp_window_moved, \
    blip_up_file_first_temp_window_moved = split_and_merge_first_temporary_for_topup(output_path, \
                                                                          blip_down_file , \
                                                                          blip_up_file)    
    #"""
    topup_datain = "topup_config/aquisition_parameters.txt"
    topup_config = "topup_config/b02b0.cnf"
    
    # Finally, compute the off-resonance field and correct the EPI pair in
    # merged_image_for_topup_compute according to this field
    corrected_4D_file = topup_compute(merged_image_for_topup_compute_file, \
                                      topup_datain, \
                                      topup_config)
    
    corrected_4D_file_postp = remove_first_and_last_slices_and_save(output_path, \
                                                                    extract_file_name(corrected_4D_file))
    
    report = evaluate_topup_performance(output_path, \
                                        blip_down_file_first_temp_window_moved, \
                                        blip_up_file_first_temp_window_moved, \
                                        corrected_4D_file_postp)

    topup_pipeline.q.put(report)
    #"""
    
def topup_pipeline_init(q, NIFTI_folder_name, TOPUP_folder_name):
    topup_pipeline.q = q
    topup_pipeline.NIFTI_folder_name = NIFTI_folder_name
    topup_pipeline.TOPUP_folder_name = TOPUP_folder_name
    
def report_listener(q, TOPUP_folder_name):
    '''listens for messages on the q, writes to file. '''
    report_file = TOPUP_folder_name + "/" + "corrected_blips_similarities.txt"    
    
    header = "Correlation Coefficient (CC),Correlation Ratio (CR),L1-norm based Correlation Ratio (L1CR),Mutual Information (MI),Normalized Mutual Inrofmation (NMI),Blip-up Blip-down File Name"

    create_directory_if_not_exists(TOPUP_folder_name)

    f = open(report_file, 'w') 
    f.write(str(header) + '\n')
    f.flush()
    f.close()

    f = open(report_file, 'a') 
    while 1:
        m = q.get()
        if m == 'kill':
            break
        f.write(str(m) + '\n')
        f.flush()
    f.close()

def dcm2niix_script_wrapper(dicom_root_folder, \
                            nifti_output_folder, \
                            directory_keyword, \
                            log_file):
    process_msg_prefix = "PID %i: " % os.getpid()

    command = 'bash scripts/dicom_to_niix_same_folder_structure.sh' + \
                ' "' + dicom_root_folder + '"' + \
                ' "' + nifti_output_folder + '"' + \
                ' "' + directory_keyword + '" 2>&1 | tee' + \
                ' "' + log_file + '"'
    
    run_shell_command(command)

    print(process_msg_prefix + "dcm2niix_script_wrapper: Given not already existing " + \
                  "converted files, successfully converted " + \
                  ".dcm files in " + dicom_root_folder + \
                  " having folder name including keyword (after taking lowercase) " + \
                  directory_keyword + \
                  " to " +  nifti_output_folder + \
                  " using scripts/dicom_to_niix_same_folder_structure.sh in subprocess shell call." + \
                  " log file: " + log_file)

def dcm2niix_pipeline(DICOM_folder_name, \
                      NIFTI_folder_name, \
                      keyword):
    
    conversion_log_file = NIFTI_folder_name + \
    "/DICOM to NIFTI conversion report with keyword " + \
    keyword + ".txt"
    
    dcm2niix_script_wrapper(DICOM_folder_name, \
                            NIFTI_folder_name, \
                            keyword, \
                            conversion_log_file)
