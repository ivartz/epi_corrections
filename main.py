#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:26:27 2018

@author: ivar

Check the GitHub page for dependencies.

Recommended standalone run:
mkdir ../epi_corrections_out && python3 main.py 2>&1 | tee ../epi_corrections_out/pipeline_report_yyyy_mm_dd.txt

for instance
mkdir ../epi_corrections_out && python3 main.py 2>&1 | tee ../epi_corrections_out/pipeline_report_2018_11_23.txt

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
                    topup_pipeline, \
                    topup_pipeline_init, \
                    report_listener, \
                    print_detected_data

def main():

    # Original DICOM folder from Matlab anonymization
    # and defacing script.
    DICOM_directory = "../DICOM"
    
    # Output folder. This program shall not output
    # or modify data in any other directory except
    # in this folder. However, error log
    # (from mri_robust_register failure)
    # has been observed in the epi_corrections
    # repository folder.
    corrections_base_directory = "../epi_corrections_out_2019_01_04"

    # Folder for EPI NIFTI pairs converted by
    # dcm2niix script (the script's output directory)
    # from .dcm files in DICOM_directory
    EPI_NIFTI_directory = corrections_base_directory + "/EPI"
    
    # Folder for FLAIR 3D NIFTI converted by
    # dcm2niix script (the script's output directory)
    # from .dcm files in DICOM_directory
    FLAIR_3D_NIFTI_directory = corrections_base_directory + "/FLAIR_3D"

    # Output directory for FSL topup pipeline
    TOPUP_directory = corrections_base_directory + "/TOPUP"
    
    # Directory for final FSL topup corrected EPIs 
    # (positive phase encoded, blip up).
    EPI_NIFTI_applytopup_directory = corrections_base_directory + "/EPI_applytopup"
    create_directory_if_not_exists(EPI_NIFTI_applytopup_directory)
    
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
                      "flair 3d")

    #"""
    # Detect EPI pairs in EPI_NIFTI_directory
    #GE_blip_nii_pairs, SE_blip_nii_pairs = get_blip_pairs(EPI_NIFTI_directory)
    GE_blip_nii_pairs, SE_blip_nii_pairs = get_blip_pairs(EPI_NIFTI_directory)
    
    print_detected_data(GE_blip_nii_pairs, SE_blip_nii_pairs)
    
    # Complete list of tuples with EPI pairs to correct for
    # magnetic susceptibility distortions
    EPI_pairs_to_correct = GE_blip_nii_pairs + SE_blip_nii_pairs
    
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
    #"""

if __name__ == '__main__':
    main()
