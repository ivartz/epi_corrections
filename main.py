#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:26:27 2018

@author: ivar
"""

from multiprocessing import Pool
from search import get_blip_pairs
from utils import topup_pipeline, NIFTI_folder_name, print_detected_data

# Detect EPI pairs in input directory
GE_blip_nii_pairs, SE_blip_nii_pairs = get_blip_pairs(NIFTI_folder_name)

print_detected_data(GE_blip_nii_pairs, SE_blip_nii_pairs)

EPI_pairs_to_correct = GE_blip_nii_pairs + SE_blip_nii_pairs

# Multiprocessing pool of 8 workers
p = Pool(processes=8, maxtasksperchild=1)

# Run topup pipeline on chunks of EPI pairs concurrently,
# working on GE pairs first.
_ = p.starmap(topup_pipeline, EPI_pairs_to_correct[0:8])
