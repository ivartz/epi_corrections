#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:26:27 2018

@author: ivar
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
