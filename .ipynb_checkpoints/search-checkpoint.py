#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:39:38 2018

@author: ivar
"""

# Uncovering all NIFTI files and folder structures to be corrected
import os
from utils import determine_e1_or_e2, \
    determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE

def get_blip_pairs(NIFTI_folder_name = "NIFTI"):

    # GE_blip_nii_pairs and SE_blip_nii_pairs
    # have the following structure 
    # [('NIFTI/path/to/negative_phase_encoding_direction.nii', 'NIFTI/path/to/positive_phase_encoding_direction.nii'), (,) , .. ]
    
    # assuming e1.nii is GE and e2.nii is SE
    
    # assuming prescan corresponds to corr_SENSE
    # and scan corresponds to SENSE
    
    # assuming prescan and corr_SENSE are always positive phase encoding directions
    # and scan and SENSE negative phase encoding directions
    
    # Empty lists for relative directory path + filename.nii to be corrected
    
    GE_prescan = []
    GE_scan = []
    
    GE_corr_SENSE = []
    GE_SENSE = []
    
    GE_not_corr = []
    GE_corr = []
    
    SE_prescan =[]
    SE_scan = []
    
    SE_corr_SENSE = []
    SE_SENSE = []
    
    SE_not_corr = []
    SE_corr = []
    
    num_directories_bypassed = 0
    
    # NIFTI directory traversal. The NIFTI directory 
    # is the output of dicom_to_niix_same_folder_structure.sh
    # conversion script (from DICOM files) using dcm2niix 1.0.20180622
    
    directoryTree = [tuple3 for tuple3 in os.walk(NIFTI_folder_name)]
    
    
    #for dirpath, dirnames, filenames in directoryTree:
        
    for i in range(len(directoryTree)):
        
        dirpath, dirnames, filenames = directoryTree[i]
        
        # Start, two available folders check
        
        # os.walk iterates top-down as default. 
        
        # With the assumed folder structure
        # it visits the folders according to this example:
        
        # Iteration 1: Show EPI-blip-down-folder and EPI-blip-up-folder
        # Iteration 2: Visit either EPI-blip-down-folder or EPI-blip-up-folder
        # to show its contents.
        
        # This means that os.walk will always visit the directory
        # with the blip-up and blip-down folders in ONE ITERATION
        # BEFORE visiting one of the folders.
        
        # The two available folders check enshures that only
        # directories corresponding to Iteration 1 in the 
        # example with exactly two folders are visited
        # by the script. When there exist two folders,
        # they are assumed to be the blip-down and blip-up 
        # folders (this should be assured if they are the only folders)
        # with the string "epi" as part of lowercase versions of folder names
        # in the original DICOM directory structure. 
        # If this is assured, dicom_to_niix_same_folder_structure.sh
        # will only convert those folders to .nii format into a near equal
        # folder structure. The difference is that the relative path from
        # root of script starts with the folder NIFTI instead of the 
        # orignal folder DICOM containing the original .dcm folder structure.
        
        # A single folder shown when os.walk is
        # in the iteration analog to Iteration 1 where
        # "epi" is part of the the name (incase-sesitive), is bypassed
        # from furhter subdirectory traversal.
        # This is done by skipping the newxt iteration that would have followed, 
        # where the .nii files for the single epi folder would 
        # have been accessed/shown by os.walk.
        
        # Assume that the two available folders check
        # enshures that only .nii files associated with
        # two different EPI phase encoding directions
        # are included for corretion.
        
        if i > 0:
            prevdirpath, prevdirnames, _ = directoryTree[i-1]
            if len(prevdirnames) != 2 and prevdirnames and \
            "epi" in prevdirnames[0].lower():
                print("WARNING: The folder " + prevdirnames[0] + \
                      " is the only folder in the directory")
                print(prevdirpath)
                print("Assuming it does not have a companying folder \
                with opposite phase endoded EPI recording.")
                print("Conclusion: Skipping data in " + prevdirnames[0])
                num_directories_bypassed += 1
                continue
    
        # End, two available folders check 
    
        # Enshure not empty list traversal
        if filenames:
    
            for file in filenames:
                
                # Enshure only .nii files
                if file[-len(".nii"):] == ".nii":
                    
                    
                    # Gradient Echo files    
    
                    if determine_e1_or_e2(file) == "e1" and \
                    determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "prescan":
                        # GE positive phase encoded
                        GE_prescan += [os.path.join(dirpath, file)]
    
                    elif determine_e1_or_e2(file) == "e1" and \
                    determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "scan":
                        # GE negative phase encoded
                        GE_scan += [os.path.join(dirpath, file)]
    
                    elif determine_e1_or_e2(file) == "e1" and \
                    determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "corr_SENSE":
                        # GE positive phase encoded
                        GE_corr_SENSE += [os.path.join(dirpath, file)]
    
                    elif determine_e1_or_e2(file) == "e1" and \
                    determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "SENSE":
                        # GE negative phase encoded
                        GE_SENSE += [os.path.join(dirpath, file)]
                    
                    # EDIT: The below special case is excluded,
                    # since it included a file that was not a dynamic (DSC) sequence
                    # (although having correct phase encoding compared to other DSC).
                    # Although (first dynamic) topup and epic works for this case, 
                    # it will cause nICE to be unable to produce perfusion images
                    # for this data in a later analysis, and then causing other errors
                    # such as multiple perfusion images being copied back
                    # wrong image directories (step 7 in notebook 1; 
                    # after performing nICE perfusion analysis).
                    
                    # the two last are for a special case
                    # with a EPI pair recording
                    # where corr seems to be negative phase
                    # encoded and the other file name has nothing
                    # in it's name that is specified and seems to
                    # be positive phase encoded recording.
                    #elif determine_e1_or_e2(file) == "e1" and \
                    #determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "not_corr":
                    #    # GE positive phase encoded
                    #    GE_not_corr += [os.path.join(dirpath, file)]
    
                    #elif determine_e1_or_e2(file) == "e1" and \
                    #determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "corr":
                    #    # GE negative phase encoded
                    #    GE_corr += [os.path.join(dirpath, file)]
    
                        
                    # Spin Echo files
    
                    elif determine_e1_or_e2(file) == "e2" and \
                    determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "prescan":
                        # SE positive phase encoded
                        SE_prescan += [os.path.join(dirpath, file)]
    
                    elif determine_e1_or_e2(file) == "e2" and \
                    determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "scan":
                        # SE negative phase encoded
                        SE_scan += [os.path.join(dirpath, file)]
    
                    elif determine_e1_or_e2(file) == "e2" and \
                    determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "corr_SENSE":
                        # SE positive phase encoded
                        SE_corr_SENSE += [os.path.join(dirpath, file)]
    
                    elif determine_e1_or_e2(file) == "e2" and \
                    determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "SENSE":
                        # SE negative phase encoded
                        SE_SENSE += [os.path.join(dirpath, file)]
    
                    # EDIT: The below special case is excluded,
                    # since it included a file that was not a dynamic (DSC) sequence
                    # (although having correct phase encoding compared to other DSC).
                    # Although (first dynamic) topup and epic works for this case, 
                    # it will cause nICE to be unable to produce perfusion images
                    # for this data in a later analysis, and then causing other errors
                    # such as multiple perfusion images being copied back
                    # wrong image directories (step 7 in notebook 1; 
                    # after performing nICE perfusion analysis).
    
                    # the two last are for a special case
                    # with a EPI pair recording
                    # where corr seems to be negative phase
                    # encoded and the other file name has nothing
                    # in it's name that is specified and seems to
                    # be positive phase encoded recording.                    
                    #elif determine_e1_or_e2(file) == "e2" and \
                    #determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "not_corr":
                    #    # positive phase encoded
                    #    SE_not_corr += [os.path.join(dirpath, file)]
    
                    #elif determine_e1_or_e2(file) == "e2" and \
                    #determine_prescan_or_scan_or_wip_or_corr_SENSE_or_SENSE(file) == "corr":
                    #    # negative phase encoded
                    #    SE_corr += [os.path.join(dirpath, file)]
    
                        
    print("----------------------------------------------------------------")
    
                
    print("1. Equal number of GE and SE prescan and scan included: ", end="")
    print(len(GE_prescan) == len(GE_scan) == len(SE_prescan) == len(SE_scan))
    print("2. Equal number of GE and SE corr_SENSE and SENSE included: ", end="")
    print(len(GE_corr_SENSE) == len(GE_SENSE) == len(SE_corr_SENSE) == len(SE_SENSE))
    print("3. Equal number of GE and SE not_corr and corr included: ", end="")
    print(len(GE_not_corr) == len(GE_corr) == len(SE_not_corr) == len(SE_corr))
    
    
    # Finally, make GE and SE list of 2D tuples of relative path + filename.nii
    # for blip-down (negative (FSL TOPUP), forward (EPIC), "compressed" along y / AP) 
    # - blip-up (positive (FSL TOPUP), reverse (EPIC), "stretched" along y / AP) EPI pairs.
    # The two lists is are used later for topup and EPIC.
    GE_blip_nii_pairs = list(zip(GE_scan, GE_prescan)) + \
        list(zip(GE_SENSE, GE_corr_SENSE)) + list(zip(GE_corr, GE_not_corr))
    SE_blip_nii_pairs = list(zip(SE_scan, SE_prescan)) + \
        list(zip(SE_SENSE, SE_corr_SENSE)) + list(zip(SE_corr, SE_not_corr))
    
    print("4. Equal number of GE and SE prescan+corr_SENSE+not_corr and scan+SENSE+corr included: ", end="")
    print(len(GE_blip_nii_pairs) == len(SE_blip_nii_pairs))
    
    print("----------------------------------------------------------------")
    
    print("Important assumptions:")
    print("* Assuming the following content of a NIFTI file")
    print("according to the following string as part of its file name:")
    print("e1.nii is GE and e2.nii is SE")
    print("* Assuming file and directory names including the string prescan")
    print("correspond to file and directory names including the string corr_SENSE")
    print("* Assuming file and directory names including the string scan")
    print("correspond to file and directory names including the string SENSE")
    print("* Assuming file and directory names including no special string")
    print("but is placed correctly according to the directory to compare to")
    print("correspond to file and directory names including the string corr")
    print("* 1., 2. and 3. and 4. must be True")
    print("* prescan, corr_SENSE and not_corr: Negative phase encoded direction EPI (blip-down)")
    print("* scan, SENSE and corr: Positive phase encoded direction EPI (blip-up)")
    print("* prescan and corr_SENSE EPI have generally fewer number of temporal \
    recordings than scan and SENSE EPI")
    
    print("----------------------------------------------------------------")
    
    print("Report when all assumptions are fullfilled:")
    print("* Number of GE and SE prescan-scan pairs found: %i" % len(GE_prescan))
    print("* Number of GE and SE corr_SENSE-SENSE pairs found: %i" % len(GE_corr_SENSE))
    print("* Number of GE and SE not_corr-corr pairs found: %i" % len(GE_not_corr))
    print("* Total number of GE and SE blip-down - blip-up pairs: %i" % len(GE_blip_nii_pairs))
    print("* Total number of GE and SE blip-down - blip-up pairs: %i + %i = %i" % \
          (len(GE_prescan), len(GE_corr_SENSE), len(GE_prescan) + len(GE_corr_SENSE) + len(GE_not_corr)) )
    print("* Number of directories bypassed since no detection of opposite phase encoded EPI pairs: %i" % \
          num_directories_bypassed)
    print("Sanity check: %i should be the original number of EPI blip-down-blip-up folders\n \
    inside the input directy to this script, with directory root folder name: %s.\n \
    This should be the output directory of dicom_to_niix_same_folder_structure.sh beforehand." % \
          (len(GE_blip_nii_pairs) + num_directories_bypassed, NIFTI_folder_name))
    
    return GE_blip_nii_pairs, SE_blip_nii_pairs
