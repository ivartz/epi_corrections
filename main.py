#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:26:27 2018

@author: ivar

Recommended standalone run:
python3 main.py 2>&1 | tee reports/pipeline_report_yyyy_mm_dd.txt
for instance

python3 main.py 2>&1 | tee reports/pipeline_report_2018_11_23.txt

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
from utils import topup_pipeline, \
                    topup_pipeline_init, \
                    report_listener, \
                    print_detected_data

def main():
    # Input directory from dcm2niix script (the script's output directory)
    NIFTI_folder_name= "../NIFTI_TEST"
    # Output directory for FSL topup pipeline
    TOPUP_folder_name = "../TOPUP_TEST"

    # Detect EPI pairs in input directory
    GE_blip_nii_pairs, SE_blip_nii_pairs = get_blip_pairs(NIFTI_folder_name)
    
    print_detected_data(GE_blip_nii_pairs, SE_blip_nii_pairs)
    
    # Complete list of tuples with EPI pairs to correct for
    # magnetic susceptibility distortions
    EPI_pairs_to_correct = GE_blip_nii_pairs + SE_blip_nii_pairs
    
    
    
    
    
    # Manager queue for report writer process
    manager = mp.Manager()
    
    # Report queue
    q = manager.Queue()
    
    # Multiprocessing pool of 8 workers (= number of physical CPU cores)
    p = mp.Pool(8, topup_pipeline_init, initargs=(q, NIFTI_folder_name, TOPUP_folder_name), maxtasksperchild=1)
    
    # Put report listener to work first
    p.apply_async(report_listener, args=(q, TOPUP_folder_name))
    
    # Run topup pipeline on chunks of EPI pairs concurrently,
    # working on GE pairs first.
    p.starmap(topup_pipeline, EPI_pairs_to_correct)
    
    q.put('kill')
    p.close()





if __name__ == '__main__':
    main()
