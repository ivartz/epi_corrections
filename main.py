#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:26:27 2018

@author: ivar
"""

from search import get_blip_pairs

from utils import extract_file_name, \
    determine_output_path, \
    create_directory_if_not_exists, \
    split_and_merge_first_temporary
    
from fsl import topup_compute
    
NIFTI_folder_name = "../NIFTI"

TOPUP_folder_name = "../TOPUP"

#GE_blip_nii_pairs, SE_blip_nii_pairs = get_blip_pairs(NIFTI_folder_name)

#blip_down_file = '../NIFTI/Anonymized/DEFACED_IVS/274299819/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_prescan/94900_GE-SE_EPI_SSH_v1_32CH_V2_prescan_901_e1.nii'
#blip_up_file = '../NIFTI/Anonymized/DEFACED_IVS/274299819/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_scan/94900_GE-SE_EPI_SSH_v1_32CH_V2_scan_1001_e1.nii'

#blip_down_file = '../NIFTI/Anonymized/DEFACED_IVS/1931166645/DAY_0000/No_DeFacing_WIP GE-SE EPI SSH_v1_32CH_corr SENSE/104935_WIP_GE-SE_EPI_SSH_v1_32CH_corr_SENSE_701_e1.nii'
#blip_up_file = '../NIFTI/Anonymized/DEFACED_IVS/1931166645/DAY_0000/No_DeFacing_WIP GE-SE EPI SSH_v1_32CH SENSE/104935_WIP_GE-SE_EPI_SSH_v1_32CH_SENSE_801_e1.nii'
#
blip_down_file = '../NIFTI/Anonymized/DEFACED_IVS/5464565466/DAY_0000/No_DeFacing_GE-SE EPI SSH_16CH/115533_GE-SE_EPI_SSH_16CH_2001_e1.nii'
blip_up_file = '../NIFTI/Anonymized/DEFACED_IVS/5464565466/DAY_0000/No_DeFacing_GE-SE EPI SSH_16CH_corr/115533_GE-SE_EPI_SSH_16CH_corr_1901_e1.nii'


blip_down_file_name = extract_file_name(blip_down_file)

print("blip_down_file_name: %s" % blip_down_file_name)

blip_up_file_name = extract_file_name(blip_up_file)

print("blip_up_file_name: %s" % blip_up_file_name)


output_path = determine_output_path(TOPUP_folder_name, \
                          NIFTI_folder_name, \
                          blip_down_file, \
                          blip_up_file, \
                          blip_down_file_name, \
                          blip_up_file_name)
    
print("output_path: %s" % output_path)

create_directory_if_not_exists(output_path)

merged_image_for_topup_compute = split_and_merge_first_temporary(output_path, \
                                    blip_down_file, \
                                    blip_up_file, \
                                    blip_down_file_name , \
                                    blip_up_file_name)

print(merged_image_for_topup_compute)

topup_datain = "topup_config/aquisition_parameters.txt"
topup_config = "topup_config/b02b0.cnf"

# Finally, compute the off-resonance field and correct the EPI pair in
# merged_image_for_topup_compute according to this field
topup_compute(merged_image_for_topup_compute, \
              topup_datain, \
              topup_config)

"""
#def topup(blip_down_file, blip_up_file):
    #common_data_dir = find_common_folder_for_blip_down_blip_up_EPI_data(blip_down_file, blip_up_file)
    
common_dir = find_common_folder_for_blip_down_blip_up_EPI_data(blip_down_file, \
                                                               blip_up_file)

process_msg_prefix = "PID %i: " % os.getpid()

# Enshure that the input is correct 1:
# Asumption: The mother folder a given scan collection has always "day"
# in it's lowercase version of folder name.
if not "day" in common_dir.lower():
    print(process_msg_prefix + " Error: it seems that common_dir is wrong: \
    " + common_dir + " , aborting process")
    sys.exit(1)



# Enshure that the input is correct 2:
# Enshure that echo sequences match between the files (GE or SE)
if not determine_e1_or_e2(blip_down_file_name) == \
    determine_e1_or_e2(blip_up_file_name):
    print(process_msg_prefix + " Error: Could not verify \
    matching echo sequence EPI pair (GE or SE), aborting process")
    sys.exit(1)
"""