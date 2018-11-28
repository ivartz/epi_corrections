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
from registration import highres_to_lowres_registration

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

def extract_string_after_last_backslash(stringeling):
    # Use to extract file name from path + file name (file)
    # or to extract the last folder name in a path .
    #
    # Finds the first index of "/" in the reversed
    # order of stringeling string.
    # Then converts the reversed index to normal index.
    i = len(stringeling) - stringeling[::-1].index("/")
    # The part of stringeling that is after the last /
    # is the remaining part of stringeling
    # after index i .
    return stringeling[i:]

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

def create_directory_if_not_exists(output_directory):    
        while True:
            try:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                else:
                    print("create_directory_if_not_exists: %s \
                          already exists, not creating" % output_directory)
                break
            except OSError as e:
                if e.errno != os.errno.EEXIST:
                    raise
                # There might be a race condition, sleeping for 50 ms
                # to try again later
                sleep(0.05)
                pass

def determine_output_directory(root_folder_name, \
                          NIFTI_folder_name, \
                          blip_down_file, \
                          blip_up_file, \
                          blip_down_file_name, \
                          blip_up_file_name):
    output_directory = root_folder_name + \
        longest_common_substring_from_beginning(blip_down_file, \
                                                blip_up_file)[len(NIFTI_folder_name):] + \
                    determine_prescan_or_scan_or_corr_SENSE_or_SENSE(blip_down_file_name) + "_" + \
                    determine_prescan_or_scan_or_corr_SENSE_or_SENSE(blip_up_file_name)
        
    return output_directory

def split_and_merge_first_temporary_for_topup(output_directory, \
                                    blip_down_file, \
                                    blip_up_file):
    
    # Splitting part
    blip_down_file_name = extract_string_after_last_backslash(blip_down_file)
    blip_up_file_name = extract_string_after_last_backslash(blip_up_file)
    
    extract_first_temporary_window_and_save(output_directory, \
                                              blip_down_file, \
                                              blip_down_file_name)
                                              
    extract_first_temporary_window_and_save(output_directory, \
                                              blip_up_file, \
                                              blip_up_file_name)
            
    blip_down_temporary_window_file_name = \
        determine_blip_file_name_for_window_topup("blip_down", \
                                            blip_down_file_name, \
                                            blip_up_file_name)
    
    blip_down_temporary_window_file = output_directory + "/" + \
        blip_down_temporary_window_file_name
    
    print("blip_down_temporary_window_file: %s" % \
          blip_down_temporary_window_file)
    
    blip_up_temporary_window_file_name = \
        determine_blip_file_name_for_window_topup("blip_up", \
                                            blip_down_file_name, \
                                            blip_up_file_name)
    
    blip_up_temporary_window_file = output_directory + "/" + \
        blip_up_temporary_window_file_name
    
    print("blip_up_temporary_window_file: %s" % \
          blip_up_temporary_window_file)

    # FSL topup specific operations: add dulicate top and bottom slice
    # along z-axis, since the topup algorithm will remove top and bottom slice.
    blip_down_temporary_window_file_prep = add_duplicate_slices(output_directory, blip_down_temporary_window_file_name)
    blip_up_temporary_window_file_prep = add_duplicate_slices(output_directory, blip_up_temporary_window_file_name)
    
    
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
    blip_down_blip_up_temporary_window_file = output_directory + "/" + \
        blip_down_blip_up_temporary_window_file_name
    
    # prepend relative path to make blip_down_blip_up_temporary_window_file_raw
    blip_down_blip_up_temporary_window_file_raw = output_directory + "/" + \
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

def find_corresponding_flair_3d_file_for_epi_pair_output_directory(output_directory, \
                            TOPUP_folder_name, \
                            FLAIR_3D_NIFTI_folder_name):
    # Find corresponding (already converted to NIFTI)
    # FLAIR 3D image in FLAIR_3D_NIFTI_folder_name
    # if it exists. Return "not found" elsewise.
    output_folder = extract_string_after_last_backslash(output_directory)
    
    
    
    corresponding_matched_flair_3d_directory_if_exists = \
                                FLAIR_3D_NIFTI_folder_name + \
                                output_directory[len(TOPUP_folder_name):-len(output_folder)]
    
    directoryTree = \
    [tuple3 for tuple3 in os.walk(corresponding_matched_flair_3d_directory_if_exists)]
    
    if not directoryTree:
        # It seems like that no corresponding matching flair folder exists,
        # returning "not found"
        return "not found"
    
    # TODO: Better error handling.
    # TODO: More robust way of finding
    # correct flair folder and file.
    
    # This way of extracting folder name is experimental.
    flair_3d_folder = [l[1] for l in directoryTree][0][0]
    
    if not "flair" in flair_3d_folder.lower():
        # The detected folder does not have
        # flair in the lower case version
        # of the folder name.
        # Assuming not flair found.
        return "not found"
    
    # This way of extracting file name is experimental.
    flair_3d_file_name = [l[2] for l in directoryTree][-1][0]

    if not "flair" in flair_3d_file_name.lower():
        # The detected file name  does not have
        # flair in the lower case version
        # of the file name.
        # Assuming not flair found.
        return "not found"
    
    corresponding_flair_3d_file_directory_if_exists = \
    corresponding_matched_flair_3d_directory_if_exists + \
    flair_3d_folder + "/" + flair_3d_file_name
    
    return corresponding_flair_3d_file_directory_if_exists

def calculate_volume_similarity_measures(volume_1, \
                                         volume_2, \
                                         volume_pair_desc="Corr. neg. and pos. phase EPIs"):
    
    # TODO: Add structural similarity index
    # and other novel similarity measures.
    
    header = volume_pair_desc + " Correlation Coefficient (CC)," + \
                volume_pair_desc + " Correlation Ratio (CR)," + \
                volume_pair_desc + " L1-norm based Correlation Ratio (L1CR)," + \
                volume_pair_desc + " Mutual Information (MI)," + \
                volume_pair_desc + " Normalized Mutual Inrofmation (NMI)"
    
    report = ""
    
    similarity = Similarity()
    similarity.inputs.volume1 = volume_1
    similarity.inputs.volume2 = volume_2
    similarity.inputs.metric = 'cc'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")] + ","
    
    similarity = Similarity()
    similarity.inputs.volume1 = volume_1
    similarity.inputs.volume2 = volume_2
    similarity.inputs.metric = 'cr'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")] + ","
    
    similarity = Similarity()
    similarity.inputs.volume1 = volume_1
    similarity.inputs.volume2 = volume_2
    similarity.inputs.metric = 'crl1'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")] + ","
    
    similarity = Similarity()
    similarity.inputs.volume1 = volume_1
    similarity.inputs.volume2 = volume_2
    similarity.inputs.metric = 'mi'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")] + ","
    
    similarity = Similarity()
    similarity.inputs.volume1 = volume_1
    similarity.inputs.volume2 = volume_2
    similarity.inputs.metric = 'nmi'
    report += str(similarity.run().outputs)[len("similarity =  "):-len("\n")]
    
    return header, report

def evaluate_topup_performance(output_directory, \
                               blip_down_window_file, \
                               blip_up_window_file, \
                               corrected_4D_file, \
                               TOPUP_folder_name, \
                               FLAIR_3D_NIFTI_folder_name):
    
    # Source:
    # https://nipype.readthedocs.io/en/latest/interfaces/generated/interfaces.nipy/utils.html
    
    corrected_4D_file_name = extract_string_after_last_backslash(corrected_4D_file)
    
    split_along_temporary_axis_and_save(output_directory, \
                                              corrected_4D_file ,\
                                              corrected_4D_file_name)
    
    # Splitting corrected_4D_file_name in split_along_temporary_axis_and_save
    # is expected to create two .nii files, each having names equal to 
    # corrected_4D_file_name but with appended a four 
    # digit long temporal identifier at the end of the file name.
    corrected_blip_down_file = corrected_4D_file[:-len(".nii")] + "_0000.nii"
    corrected_blip_down_file_name = extract_string_after_last_backslash(corrected_blip_down_file)
    corrected_blip_up_file = corrected_4D_file[:-len(".nii")] + "_0001.nii"
    corrected_blip_up_file_name = extract_string_after_last_backslash(corrected_blip_up_file)
    
    # FSL topup fix: since duplicate slices were added to the 
    # uncorrected 4D file that was used with topup, 
    # corrected_4D_file remains shifted one slice upwards 
    # even with these slices removed by the topup algorithm.
    # 
    # A solution to shifting the corrected data back to original 
    # position along z axims seems to be to replace the 
    # geometrical header information of the corrected blip down
    # and blip up .nii files with the geometrical header
    # information of the original uncorrected .nii files:
    #
    # Replace geometry info in header of corrected_blip_down_file
    # and corrected_blip_up_file with geometry info in header
    # of blip_down_window_file and blip_up_window_file respectively 
    # (non-corrected temporary window files)
    # The header geometrical information of
    # corrected_blip_down_file amd corrected_blip_up_file
    # is changed after running the two following commands.
    copy_header(blip_down_window_file, corrected_blip_down_file)
    copy_header(blip_up_window_file, corrected_blip_up_file)
    
    # Find corresponding (already converted to NIFTI)
    # FLAIR 3D image in FLAIR_3D_NIFTI_folder_name
    # if it exists. Return "not found" elsewise.
    flair_3d_file = find_corresponding_flair_3d_file_for_epi_pair_output_directory(output_directory, \
                                                                                   TOPUP_folder_name, \
                                                                                   FLAIR_3D_NIFTI_folder_name)
    flair_3d_file_name = extract_string_after_last_backslash(flair_3d_file)
    
    # Overview of file name and file (file directory + file name) 
    # for raw and corrected EPI as well as corresponding flair 3d.
    raw_epi_file_names_overview = "Neg. phase enc. EPI: " + \
                extract_string_after_last_backslash(blip_down_window_file)  + \
                ";Pos. phase enc. EPI: " + \
                extract_string_after_last_backslash(blip_up_window_file)
    raw_epi_files_overview = "Neg. phase enc. EPI: " + \
                blip_down_window_file  + \
                ";Pos. phase enc. EPI: " + \
                blip_up_window_file
    corr_epi_file_names_overview = "Neg. phase enc. EPI: " + \
                corrected_blip_down_file_name  + \
                ";Positive phase encoded EPI: " + \
                corrected_blip_up_file_name
    corr_epi_files_overview = "Neg. phase enc. EPI: " + \
                corrected_blip_down_file  + \
                ";Pos. phase enc. EPI: " + \
                corrected_blip_up_file
    flair_file_name_overview = "FLAIR 3D: " + \
                flair_3d_file_name
    flair_file_overview = "FLAIR 3D: " + \
                flair_3d_file
    
    # Raw
    # Compute similarity measures between non-corrected blips
    raw_blips_similarities_header, \
    raw_blips_similarities_report = \
    calculate_volume_similarity_measures(blip_down_window_file, \
                                         blip_up_window_file, \
                                         volume_pair_desc="Raw neg. to pos. phase EPI")
    # Corr
    # Compute similarity measures between corrected blips
    corrected_blips_similarities_header, \
    corrected_blips_similarities_report = \
    calculate_volume_similarity_measures(corrected_blip_down_file, \
                                         corrected_blip_up_file, \
                                         volume_pair_desc="Corr. neg. to pos. phase EPI")
    # Raw to Corr neg
    # Compute similarity measures between (raw) non-corrected 
    # and corrected blip down EPIs
    raw_and_corrected_blip_down_similarities_header, \
    raw_and_corrected_blip_down_similarities_report = \
    calculate_volume_similarity_measures(blip_down_window_file, \
                                         corrected_blip_down_file, \
                                         volume_pair_desc="Raw to corr. neg. phase EPI")
    # Raw to corr pos
    # Compute similarity measures between (raw) non-corrected 
    # and corrected blip up EPIs
    raw_and_corrected_blip_up_similarities_header, \
    raw_and_corrected_blip_up_similarities_report = \
    calculate_volume_similarity_measures(blip_up_window_file, \
                                         corrected_blip_up_file, \
                                         volume_pair_desc="Raw to corr. pos. phase EPI")

    # Perform FreeSurfer high res -> low res robust registrations
    # and then perform corresponding similarity measures
    # as previously.
    # The following files are downsampled flair 3d versions
    # with voxels (data points) only where the corresponding EPI
    # has voxels.
    registration_directory = \
                        output_directory + \
                        "/registration"
    create_directory_if_not_exists(registration_directory)
    
    # --- Raw neg
    # flair and corrected pos. EPI
    flair_3d_registrated_to_raw_neg_file = \
                highres_to_lowres_registration(flair_3d_file, \
                                               blip_down_window_file, \
                                               registration_directory, \
                                               "flair_3d_registrated_to_raw_neg")
    # Compute similarity measures between registrated (downscaled FLAIR 3D,
    # the high res in registration) and the low res EPI.
    flair_3d_registrated_to_raw_neg_and_raw_neg_similarities_header, \
    flair_3d_registrated_to_raw_neg_and_raw_neg_similarities_report = \
    calculate_volume_similarity_measures(flair_3d_registrated_to_raw_neg_file, \
                                         blip_down_window_file, \
                                         volume_pair_desc="FLAIR 3D (reg.) to raw. neg. phase EPI")
    # --- Raw pos
    # flair and corrected pos. EPI
    flair_3d_registrated_to_raw_pos_file = \
                highres_to_lowres_registration(flair_3d_file, \
                                               blip_up_window_file, \
                                               registration_directory, \
                                               "flair_3d_registrated_to_raw_pos")
    # Compute similarity measures between registrated (downscaled FLAIR 3D,
    # the high res in registration) and the low res EPI.
    flair_3d_registrated_to_raw_pos_and_raw_pos_similarities_header, \
    flair_3d_registrated_to_raw_pos_and_raw_pos_similarities_report = \
    calculate_volume_similarity_measures(flair_3d_registrated_to_raw_pos_file, \
                                         blip_up_window_file, \
                                         volume_pair_desc="FLAIR 3D (reg.) to raw. pos. phase EPI")
    # --- Corr neg
    # flair and corrected neg. EPI
    flair_3d_registrated_to_corr_neg_file = \
                highres_to_lowres_registration(flair_3d_file, \
                                               corrected_blip_down_file, \
                                               registration_directory, \
                                               "flair_3d_registrated_to_corr_neg")
    # Compute similarity measures between registrated (downscaled FLAIR 3D,
    # the high res in registration) and the low res EPI.
    flair_3d_registrated_to_corr_neg_and_corr_neg_similarities_header, \
    flair_3d_registrated_to_corr_neg_and_corr_neg_similarities_report = \
    calculate_volume_similarity_measures(flair_3d_registrated_to_corr_neg_file, \
                                         corrected_blip_down_file, \
                                         volume_pair_desc="FLAIR 3D (reg.) to corr. neg. phase EPI")
    # --- Corr pos
    # flair and corrected pos. EPI
    flair_3d_registrated_to_corr_pos_file = \
                highres_to_lowres_registration(flair_3d_file, \
                                               corrected_blip_up_file, \
                                               registration_directory, \
                                               "flair_3d_registrated_to_corr_pos")
    # Compute similarity measures between registrated (downscaled FLAIR 3D,
    # the high res in registration) and the low res EPI.
    flair_3d_registrated_to_corr_pos_and_corr_pos_similarities_header, \
    flair_3d_registrated_to_corr_pos_and_corr_pos_similarities_report = \
    calculate_volume_similarity_measures(flair_3d_registrated_to_corr_pos_file, \
                                         corrected_blip_up_file, \
                                         volume_pair_desc="FLAIR 3D (reg.) to corr. pos. phase EPI")

    
    
    
    # Finally, generate the total similarity report for this EPI pair and flair 3d.
    header = raw_blips_similarities_header + "," + \
                corrected_blips_similarities_header + "," + \
                raw_and_corrected_blip_down_similarities_header + "," + \
                raw_and_corrected_blip_up_similarities_header + "," + \
                flair_3d_registrated_to_raw_neg_and_raw_neg_similarities_header + "," + \
                flair_3d_registrated_to_raw_pos_and_raw_pos_similarities_header + "," + \
                flair_3d_registrated_to_corr_neg_and_corr_neg_similarities_header + "," + \
                flair_3d_registrated_to_corr_pos_and_corr_pos_similarities_header + "," + \
                "Raw EPI File Names" + "," + \
                "Raw EPI Files" + "," + \
                "Corr. EPI File Names" + "," + \
                "Corr. EPI Files" + "," + \
                "FLAIR 3D File Name" + "," + \
                "FLAIR 3D File"
                
    report = raw_blips_similarities_report + "," + \
                corrected_blips_similarities_report + "," + \
                raw_and_corrected_blip_down_similarities_report + "," + \
                raw_and_corrected_blip_up_similarities_report + "," + \
                flair_3d_registrated_to_raw_neg_and_raw_neg_similarities_report + "," + \
                flair_3d_registrated_to_raw_pos_and_raw_pos_similarities_report + "," + \
                flair_3d_registrated_to_corr_neg_and_corr_neg_similarities_report + "," + \
                flair_3d_registrated_to_corr_pos_and_corr_pos_similarities_report + "," + \
                raw_epi_file_names_overview + "," + \
                raw_epi_files_overview + "," + \
                corr_epi_file_names_overview + "," + \
                corr_epi_files_overview + "," + \
                flair_file_name_overview + "," + \
                flair_file_overview
    
    # TODO
    # blip pair similarity measures
    # Find corresponding structural image
    # if found:
    #   FreeSurfer coregistration measures
    #   in addition to saving similarity measures from coregistration
    #   to report string, images, fields, etc describing he coregistration
    #   are saved on the output_directory with describing file names.
    # if not found:
    #   fill in empty values or 
    #   corresponding structural image etc
    # all performance measures are collected in one large
    # report string.
    # Report string is saved along with header and title
    # information.
    # Additionally, report string is sent into a queue
    # resulting it being appended to a file containing 
    # all report strings across subjects.
    
    # "" since we want to skip a line between title and header
    # in the file
    data = [header, report]
    
    for d in data:
        print(d)
    
    report_name = corrected_4D_file[:-len(".nii")] + "_performance_metrics.txt"   
    
    with open(report_name , 'w') as f:
        for line in data:
            f.write("%s\n" % line)
    
    # Return report so that topup_pipeline cam put it in a summary queue.
    # Put the report to the queue along with the nifti file.
    return report + "|" + header

def print_detected_data(GE_pairs, SE_pairs):
    for g in GE_pairs:
        print(g[0])
        print(g[1])    
    for s in SE_pairs:
        print(s[0])
        print(s[1])

def topup_pipeline(blip_down_file, blip_up_file):

    blip_down_file_name = extract_string_after_last_backslash(blip_down_file)
    
    print("blip_down_file_name: %s" % blip_down_file_name)
    
    blip_up_file_name = extract_string_after_last_backslash(blip_up_file)
    
    print("blip_up_file_name: %s" % blip_up_file_name)
    
    output_directory = determine_output_directory(topup_pipeline.TOPUP_folder_name, \
                              topup_pipeline.EPI_NIFTI_folder_name, \
                              blip_down_file, \
                              blip_up_file, \
                              blip_down_file_name, \
                              blip_up_file_name)
        
    print("output_directory: %s" % output_directory)
    
    #print("DBG: create if not exists: %s" % output_directory)
    
    create_directory_if_not_exists(output_directory)
    
    
    merged_image_for_topup_compute_file, \
    merged_image_file_raw, \
    blip_down_file_first_temp_window_moved, \
    blip_up_file_first_temp_window_moved = split_and_merge_first_temporary_for_topup(output_directory, \
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
    
    corrected_4D_file_postp = remove_first_and_last_slices_and_save(output_directory, \
                                                                    extract_string_after_last_backslash(corrected_4D_file))
    
    report = evaluate_topup_performance(output_directory, \
                                        blip_down_file_first_temp_window_moved, \
                                        blip_up_file_first_temp_window_moved, \
                                        corrected_4D_file_postp, \
                                        topup_pipeline.TOPUP_folder_name, \
                                        topup_pipeline.FLAIR_3D_NIFTI_folder_name)

    topup_pipeline.q.put(report)
    #"""
    
def topup_pipeline_init(q, EPI_NIFTI_folder_name, \
                        FLAIR_3D_NIFTI_folder_name,\
                        TOPUP_folder_name):
    topup_pipeline.q = q
    topup_pipeline.EPI_NIFTI_folder_name = EPI_NIFTI_folder_name
    topup_pipeline.FLAIR_3D_NIFTI_folder_name = FLAIR_3D_NIFTI_folder_name
    topup_pipeline.TOPUP_folder_name = TOPUP_folder_name

def listen_to_queue_and_write_to_file(q, report_file):
    # This operation report_file
    # in append mode, or creates it 
    # if it does not exist.
    # In this case it does not exist
    # every time this funtion is called,
    # so report_file is always created
    # at this point.
    f = open(report_file, 'a')
    while True:
        # Wait for topup 
        # performance evaluate
        # report from any of 
        # the topup pipeline
        # processes.
        m = q.get()
        if m == 'kill':
            break
        # Write the header of the
        # file is empty (just created).
        elif os.stat(report_file).st_size == 0:
            header = m.split("|")[1]
            f.write(str(header) + '\n')
        # Write the report.
        report = m.split("|")[0]
        f.write(str(report) + '\n')
        f.flush()
    f.close()
    
    
    """
    try:
        f = open(report_file, 'a')
        # Inner while loop 1
        while True:
            # Wait for topup 
            # performance evaluate
            # report from any of 
            # the topup pipeline
            # processes.
            m = q.get()
            if m == 'kill':
                break
            # The header is expected
            # to be already written
            # to report_file by 
            # outer while loop 2
            report = m.split(";")[0]
            f.write(str(report) + '\n')
            f.flush()
        f.close()
        return False
    except NameError:
        # f = open(report_file, 'a')
        # reported that the
        # report_file
        # file doesn't exist,
        # which means that 
        # the file needs to be 
        # created and the file
        # header needs to be
        # received and written
        # to the created file
        # exactly once.
        
        # This command creates
        # report_file .
        f = open(report_file, 'w')
        # Inner while loop 2
        while True:
            # Wait for topup 
            # performance evaluate
            # report from any of 
            # the topup pipeline
            # processes.
            m = q.get()
            if m == 'kill':
                break
            else:
                # Assumong this is data 
                # from any of the processes
                # running topup_pipeline .
                # First write header to file
                header = m.split(";")[1]
                # Then write the report data
                report = m.split(";")[0]
                f.write(str(header) + '\n')
                f.write(str(report) + '\n')
                f.flush()
                # Break out enshures 
                # that inner while 
                # loop 2 is not run
                # anymore, and the
                # report_listener 
                # process goes to 
                # the inner while 
                # loop 1 with the 
                # help of outer
                # while loop.
                break
        f.close()
        return True
    """

def report_listener(q, output_folder_name, correction="topup"):
    '''listens for messages on the q, writes to file. '''
    
    if correction == "topup":
        report_file = output_folder_name + "/" + "topup_performance_metrics.txt"
    elif correction == "epic":    
        report_file = output_folder_name + "/" + "epic_performance_metrics.txt"
    
    create_directory_if_not_exists(output_folder_name)
    
    # Outer while loop
    #while listen_to_queue_and_write_to_file(q, report_file):
    #    continue
    listen_to_queue_and_write_to_file(q, report_file)

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
