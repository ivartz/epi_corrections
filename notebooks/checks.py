from search import find_label_files
from utils import load_nifti
import numpy as np

def check_if_equal_number_of_label_files(corrections_base_directory):
    [raw_label_files_e1, \
     topup_label_files_e1, \
     epic_label_files_e1, \
     raw_label_files_e2, \
     topup_label_files_e2, \
     epic_label_files_e2] = find_label_files("../" + corrections_base_directory)
    
    print("Equal number of detected label files for raw (uncorrected), topup, and epic correction methods: %r" % \
          (len(raw_label_files_e1) == \
           len(raw_label_files_e2) == \
           len(topup_label_files_e1) == \
           len(topup_label_files_e2) == \
           len(epic_label_files_e1) == \
           len(epic_label_files_e2)))
    print("Number of subject in each labels file: %i" % len(raw_label_files_e1))
    
    return [raw_label_files_e1, \
            topup_label_files_e1, \
            epic_label_files_e1, \
            raw_label_files_e2, \
            topup_label_files_e2, \
            epic_label_files_e2]

def check_if_all_region_sets_are_identical_for_method(label_files):    
    equal = []
    for i in range(len(label_files)-1):
        label_data, _, _ = \
            load_nifti(label_files[i])
        label_data_next, _, _ = \
            load_nifti(label_files[i+1])
        equal += [np.all(label_data == label_data_next)]
    
    print("All regions are identical for correction method: %r" % np.all(equal))
    
def check_if_two_region_sets_are_identical(regions_1, regions_2):
    regions_data_1, _, _ = \
        load_nifti(regions_1)
    regions_data_2, _, _ = \
        load_nifti(regions_2)
    equal = np.all(regions_data_1 == regions_data_2)
    
    print("All regions are equal for pair: %r" % equal)