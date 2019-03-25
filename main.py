#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:26:27 2018

@author: Ivar Thokle Hovden

Check the GitHub page for dependencies.

Recommended standalone run:
mkdir ../epi_corrections_out_yyyy_mm_dd && python3 main.py 2>&1 | tee ../epi_corrections_out_yyyy_mm_dd/pipeline_report_yyyy_mm_dd.txt

for instance
mkdir ../epi_corrections_out_2019_01_18 && python3 main.py 2>&1 | tee ../epi_corrections_out_2019_01_18/pipeline_report_2019_01_18.txt

First a folder named epi_corrections_out is created in the parent
directory of the epi_corrections GitHub repository 
(one directory up from the GitHub repository location).
Then the program is run and its stdout and sterr log 
is saved to a file in the epi_corrections_out directory.

The input folder to the program is DICOM_directory,
which is also one directory up from the GitHub repository location.

Running the pipeline in this way enshures that both stdout and strerr
are shown in the command line while at the same time they are saved to 
file for later debuging. Note that since the pipeline uses 
multiprocessing, the order of output messages in the file and
terminal output are not in a strictly specified order when comparing
outputs from multiple runs.
This is because multiple processes are competing on resources on the OS,
and the OS scheduler's choices of resource allocation for each processes
are not fixed and dependent on other processes in the operating system. 
It is a preemptive dynamic scheduler (dynamic priority scheduling).
"""

import multiprocessing as mp
from search import get_blip_pairs
from utils import create_directory_if_not_exists, \
                    dcm2niix_pipeline, \
                    epi_hmc_fsfast_script_wrapper, \
                    epi_hmc_elastix_script_wrapper, \
                    epi_hmc_nICE_prepare_dir_script_wrapper, \
                    epi_hmc_nICE_copy_back_script_wrapper, \
                    topup_pipeline, \
                    topup_pipeline_init, \
                    epic_pipeline, \
                    epic_pipeline_init, \
                    report_listener, \
                    print_detected_data, \
                    make_directory_folders_EPIC_friendly
import sys

def main():

    # NB! replace_spaces_with__ = True will
    # modify the folder and file names
    # in the input DICOM directory
    # since EPIC does not work with
    # any spaces in file names and paths.
    # Need to be True for EPIC to work. 
    # Will modify the folder and file names in DICOM_directory
    replace_spaces_with__ = False
    
    #run_dcm2niix = True
    run_dcm2niix = False
    
    # EPI head motion correction
    #run_epi_hmc = True
    run_epi_hmc = False
    
    #epi_nICE_hmc_not_done = True
    epi_nICE_hmc_not_done = False
    
    run_topup = True
    #run_topup = False
    
    run_epic = True
    #run_epic = False
    
    # No spaces. Can be a date [yyyy_mm_dd]
    run_output_directory_suffix = "2019_04_25_372114315"
    
    # Original DICOM folder from Matlab anonymization
    # and defacing script.
    DICOM_directory = "../DICOM_372114315_no_spaces"
    
    if replace_spaces_with__:
        # Replaces all spaces (" ") with "_" in all
        # folders and file names in 
        make_directory_folders_EPIC_friendly(DICOM_directory)    
    
    # Output folder. This program shall not output
    # or modify data in any other directory except
    # in this folder. However, error log
    # (from mri_robust_register failure)
    # has been observed in the epi_corrections
    # repository folder.
    corrections_base_directory = "../epi_corrections_out_" + \
                                            run_output_directory_suffix

    # Folder for EPI NIFTI pairs converted by
    # dcm2niix script (the script's output directory)
    # from .dcm files in DICOM_directory
    EPI_NIFTI_directory = corrections_base_directory + "/EPI"
    
    # Folder for FLAIR 3D NIFTI converted by
    # dcm2niix script (the script's output directory)
    # from .dcm files in DICOM_directory
    FLAIR_3D_NIFTI_directory = corrections_base_directory + "/FLAIR_3D"

    if run_dcm2niix:
        #"""
        # dcm2niix NIFTI conversion start
        # 
        # using script/dicom_to_niix_same_folder_structure.sh
        
        # Convert EPI data using the keyword epi
        create_directory_if_not_exists(EPI_NIFTI_directory)
        
        dcm2niix_pipeline(DICOM_directory, \
                          EPI_NIFTI_directory, \
                          "epi")
        # Convert FLAIR 3D data using the beyword "flair 3d"
        create_directory_if_not_exists(FLAIR_3D_NIFTI_directory)
        dcm2niix_pipeline(DICOM_directory, \
                          FLAIR_3D_NIFTI_directory, \
                          "flair_3d")        
        # dcm2niix conversion end
        #"""

    if run_epi_hmc:
        # Head motion correction.
        
        # This is not recommended for DSC, since corrects to the mean of the entire dynamic series.
        #epi_hmc_fsfast_script_wrapper(EPI_NIFTI_directory)
        
        # Better for DSC since it coregisters to the first dynamic image.
        #epi_hmc_elastix_script_wrapper(EPI_NIFTI_directory)
        
        # The most correct head motion correction is NordicICE Barch head motion correction.
        # This coregisters to the mean baseline image, which is selected to be the mean
        # of the dynamuc images __before__ the start of the contrast bolus passage.
        # (suited for perfusion data).
        if epi_nICE_hmc_not_done:
            epi_hmc_nICE_prepare_dir_script_wrapper(EPI_NIFTI_directory)
            print("----------------")
            print("----------------")
            print("Run NordicICE (head) Motion correction Batch Analysis on the nICE prepared NIFTI EPI data: " + \
                  corrections_base_directory + "/" + "EPI_for_nICE_batch_head_motion_correction")
            print("----------------")
            print("----------------")
            print()
            
            print(",then set epi_nICE_hmc_not_done and run_dcm2niix to False and re-run.")
            print("Exiting pipeline.")
            sys.exit(0)
        elif not epi_nICE_hmc_not_done:
            epi_hmc_nICE_copy_back_script_wrapper(EPI_NIFTI_directory)

    if run_topup or run_epic:
        # Detect EPI pairs in EPI_NIFTI_directory
        
        # Important assumptions:
        # GE_blip_nii_pairs and SE_blip_nii_pairs
        # each are lists of tuples on the form:
        
        # [( blip-down (negative (FSL TOPUP) or reverse (EPIC) or "strethed" along y / AP) 
        # , blip-up (positive (FSL TOPUP) or forward (EPIC) or "compressed" along y / AP) ), (,), ...]
        
        # This definition is compatible with the specific dcm2niix used: dcm2niix_ogeier
        # that is compiled to avoid reorienting images during the conversion
        # from patient to scanner coordinate system.
        
        # EPI pairs.
        # The two lists is are used later for topup and EPIC.
        
        #GE_blip_nii_pairs, SE_blip_nii_pairs = get_blip_pairs(EPI_NIFTI_directory)
        GE_blip_nii_pairs, SE_blip_nii_pairs = get_blip_pairs(EPI_NIFTI_directory)
        
        print_detected_data(GE_blip_nii_pairs, SE_blip_nii_pairs)
        
        # Complete list of tuples with EPI pairs to correct for
        # magnetic susceptibility distortions
        EPI_pairs_to_correct = GE_blip_nii_pairs + SE_blip_nii_pairs
        
    if run_topup:
        # FSL TOPUP EPI correction section start
        
        # Output directory for FSL topup pipeline
        TOPUP_directory = corrections_base_directory + "/TOPUP"
        
        # Directory for final FSL topup corrected EPIs 
        # (positive phase encoded, blip up).
        EPI_NIFTI_applytopup_directory = corrections_base_directory + "/EPI_applytopup"
        create_directory_if_not_exists(EPI_NIFTI_applytopup_directory)
        
        # Manager queue for report writer process
        manager = mp.Manager()
        
        # Report queue
        q = manager.Queue()
        
        # Multiprocessing pool of 8 workers (= number of physical CPU cores)
        p = mp.Pool(8, topup_pipeline_init, \
                    initargs=(q, EPI_NIFTI_directory, \
                              FLAIR_3D_NIFTI_directory, \
                              TOPUP_directory, \
                              EPI_NIFTI_applytopup_directory), \
                    maxtasksperchild=1)
        
        # Put report listener to work first
        p.apply_async(report_listener, args=(q, TOPUP_directory))
        
        # Run topup pipeline on chunks of EPI pairs concurrently,
        # working on GE pairs first.
        p.starmap(topup_pipeline, EPI_pairs_to_correct)
        
        q.put('kill')
        p.close()
        
        # FSL TOPUP EPI correction section end

    if run_epic:
        # EPIC EPI correction section start
        # Assuming converted NIFTI files are in EPI_NIFTI_directory
                
        # Output directory for EPIC pipeline
        EPIC_directory = corrections_base_directory + "/EPIC"
        create_directory_if_not_exists(EPIC_directory)
        
        # Directory for final FSL topup corrected EPIs 
        # (positive phase encoded, blip up).
        EPI_NIFTI_applyepic_directory = corrections_base_directory + "/EPI_applyepic"
        create_directory_if_not_exists(EPI_NIFTI_applyepic_directory)
                
        # Manager queue for report writer process
        manager = mp.Manager()
        
        # Report queue
        q = manager.Queue()
        
        # Multiprocessing pool of 8 workers (= number of physical CPU cores)
        p = mp.Pool(8, epic_pipeline_init, \
                    initargs=(q, EPI_NIFTI_directory, \
                              FLAIR_3D_NIFTI_directory, \
                              EPIC_directory, \
                              EPI_NIFTI_applyepic_directory), \
                    maxtasksperchild=1)
        
        # Put report listener to work first
        p.apply_async(report_listener, args=(q, EPIC_directory, "epic"))
        
        # Run topup pipeline on chunks of EPI pairs concurrently,
        # working on GE pairs first.
        p.starmap(epic_pipeline, EPI_pairs_to_correct)
        
        q.put('kill')
        p.close()
        # EPIC EPI correction section end

if __name__ == '__main__':
    main()
