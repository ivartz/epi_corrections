#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 15:47:55 2018

@author: ivar
"""

#from search import get_blip_pairs


    
#NIFTI_folder_name = "../NIFTI"

#GE_blip_nii_pairs, SE_blip_nii_pairs = get_blip_pairs(NIFTI_folder_name)


#blip_down_file = '../NIFTI/Anonymized/DEFACED_IVS/274299819/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_prescan/94900_GE-SE_EPI_SSH_v1_32CH_V2_prescan_901_e1.nii'
#blip_up_file = '../NIFTI/Anonymized/DEFACED_IVS/274299819/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_scan/94900_GE-SE_EPI_SSH_v1_32CH_V2_scan_1001_e1.nii'

#blip_down_file = '../NIFTI/Anonymized/DEFACED_IVS/1931166645/DAY_0000/No_DeFacing_WIP GE-SE EPI SSH_v1_32CH_corr SENSE/104935_WIP_GE-SE_EPI_SSH_v1_32CH_corr_SENSE_701_e1.nii'
#blip_up_file = '../NIFTI/Anonymized/DEFACED_IVS/1931166645/DAY_0000/No_DeFacing_WIP GE-SE EPI SSH_v1_32CH SENSE/104935_WIP_GE-SE_EPI_SSH_v1_32CH_SENSE_801_e1.nii'
#
#blip_down_file = '../NIFTI/Anonymized/DEFACED_IVS/5464565466/DAY_0000/No_DeFacing_GE-SE EPI SSH_16CH/115533_GE-SE_EPI_SSH_16CH_2001_e1.nii'
#blip_up_file = '../NIFTI/Anonymized/DEFACED_IVS/5464565466/DAY_0000/No_DeFacing_GE-SE EPI SSH_16CH_corr/115533_GE-SE_EPI_SSH_16CH_corr_1901_e1.nii'


#print(GE_blip_nii_pairs[-1])

#from fsl import split_NIFTI_file_along_time_axis_and_move
#from nipype.algorithms.metrics import Similarity
#
## Original
#orig = "/media/ivar/Shared/sf-virtualbox/IVS EPI Basline/TOPUP/Anonymized/DEFACED_IVS/274299819/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_prescan_scan/94900_GE-SE_EPI_SSH_v1_32CH_V2_prescan_scan_901_1001_e1_0000.nii"
#
## FSL topup corrected
#corr = "/media/ivar/Shared/sf-virtualbox/IVS EPI Basline/TOPUP/Anonymized/DEFACED_IVS/274299819/DAY_0000/No_DeFacing_GE-SE EPI SSH_v1_32CH_V2_prescan_scan/94900_GE-SE_EPI_SSH_v1_32CH_V2_prescan_scan_901_1001_e1_0000_corrected.nii"
#
#
#split_NIFTI_file_along_time_axis_and_move
#
#similarity = Similarity()
#similarity.inputs.volume1 = orig
#similarity.inputs.volume2 = corr
#similarity.inputs.metric = 'cc'
#print(str(similarity.run().outputs))
#
#similarity = Similarity()
#similarity.inputs.volume1 = orig
#similarity.inputs.volume2 = corr
#similarity.inputs.metric = 'cr'
#print(similarity.run().outputs)
#
#similarity = Similarity()
#similarity.inputs.volume1 = orig
#similarity.inputs.volume2 = corr
#similarity.inputs.metric = 'crl1'
#print(similarity.run().outputs)
#
#similarity = Similarity()
#similarity.inputs.volume1 = orig
#similarity.inputs.volume2 = corr
#similarity.inputs.metric = 'mi'
#print(similarity.run().outputs)
#
#similarity = Similarity()
#similarity.inputs.volume1 = orig
#similarity.inputs.volume2 = corr
#similarity.inputs.metric = 'nmi'
#print(similarity.run().outputs)

#report_file = "../TOPUP" + "/" + "corrected_blips_similarities.txt"
#
#header = "Correlation Coefficient (CC),Correlation Ratio (CR),L1-norm based Correlation Ratio (L1CR),Mutual Information (MI),Normalized Mutual Inrofmation (NMI),Blip-up Blip-down File Name"
#
##with open(report_file, 'w') as f:
##    f.write("%s\n" % header)
#
#f = open(report_file, 'w') 
#f.write(str(header) + '\n')
#f.flush()
#f.close()
#
#
#"""
#f = open(report_file, 'wb') 
#while 1:
#    m = q.get()
#    if m == 'kill':
#        f.write('killed')
#        break
#    f.write(str(m) + '\n')
#    f.flush()
#f.close()
"""