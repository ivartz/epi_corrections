from search import find_label_files
from utils import load_nifti

def find_files(corrections_base_directory):

    [raw_label_files_e1, \
     topup_label_files_e1, \
     epic_label_files_e1, \
     raw_label_files_e2, \
     topup_label_files_e2, \
     epic_label_files_e2] = find_label_files("../" + corrections_base_directory)
    # A check
    print("Equal number of detected label files for raw (uncorrected), topup, and epic correction methods: %r" % \
          (len(raw_label_files_e1) == \
           len(raw_label_files_e2) == \
           len(topup_label_files_e1) == \
           len(topup_label_files_e2) == \
           len(epic_label_files_e1) == \
           len(epic_label_files_e2)))
    print("Number of subject label files: %i" % len(raw_label_files_e1)
          
    return [raw_label_files_e1, \
            topup_label_files_e1, \
            epic_label_files_e1, \
            raw_label_files_e2, \
            topup_label_files_e2, \
            epic_label_files_e2]
      
def check_equal_masks(raw_label_files_e1, \
                      topup_label_files_e1, \
                      epic_label_files_e1, \
                      raw_label_files_e2, \
                      topup_label_files_e2, \
                      epic_label_files_e2):
    # Checks that all label files have equal pixels.
    # This takes forever.
    equal = []
    for i in range(45):
        for j in range(45):
            for k in range(45):
                for l in range(45):
                    for m in range(45):
                        for n in range(45):

                            raw_label_data_e1, _, _ = \
                            load_nifti(raw_label_files_e1[i])
                            raw_label_data_e2, _, _ = \
                            load_nifti(raw_label_files_e2[j])

                            topup_label_data_e1, _, _ = \
                            load_nifti(topup_label_files_e1[k])
                            topup_label_data_e2, _, _ = \
                            load_nifti(topup_label_files_e2[l])

                            epic_label_data_e1, _, _ = \
                            load_nifti(epic_label_files_e1[m])
                            epic_label_data_e2, _, _ = \
                            load_nifti(epic_label_files_e2[n])

                            equal += \
                            [np.all(raw_label_data_e1 == raw_label_data_e1) == \
                             np.all(topup_label_data_e1 == topup_label_data_e2) == \
                             np.all(epic_label_data_e1 == epic_label_data_e2)]
    print("All resliced label files are actually equal: %r" % np.all(equal))
