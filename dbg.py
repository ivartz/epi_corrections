#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 15:47:55 2018

@author: ivar
"""

from search import get_blip_pairs


    
NIFTI_folder_name = "../NIFTI"

GE_blip_nii_pairs, SE_blip_nii_pairs = get_blip_pairs(NIFTI_folder_name)

#blip_down_file = '../NIFTI/Anonymized/DEFACED_IVS/274299819/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_prescan/94900_GE-SE_EPI_SSH_v1_32CH_V2_prescan_901_e1.nii'
#blip_up_file = '../NIFTI/Anonymized/DEFACED_IVS/274299819/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_scan/94900_GE-SE_EPI_SSH_v1_32CH_V2_scan_1001_e1.nii'

#blip_down_file = '../NIFTI/Anonymized/DEFACED_IVS/1931166645/DAY_0000/No_DeFacing_WIP GE-SE EPI SSH_v1_32CH_corr SENSE/104935_WIP_GE-SE_EPI_SSH_v1_32CH_corr_SENSE_701_e1.nii'
#blip_up_file = '../NIFTI/Anonymized/DEFACED_IVS/1931166645/DAY_0000/No_DeFacing_WIP GE-SE EPI SSH_v1_32CH SENSE/104935_WIP_GE-SE_EPI_SSH_v1_32CH_SENSE_801_e1.nii'

blip_down_file = '../NIFTI/Anonymized/DEFACED_IVS/5464565466/DAY_0000/No_DeFacing_GE-SE EPI SSH_16CH/115533_GE-SE_EPI_SSH_16CH_2001_e1.nii'
blip_up_file = '../NIFTI/Anonymized/DEFACED_IVS/5464565466/DAY_0000/No_DeFacing_GE-SE EPI SSH_16CH_corr/115533_GE-SE_EPI_SSH_16CH_corr_1901_e1.nii'


print(GE_blip_nii_pairs[-1])