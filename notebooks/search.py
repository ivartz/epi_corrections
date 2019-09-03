import os

def find_cbv_files(corrections_base_directory):

    # Gradient Echo nrCBV (e1)

    raw_cbv_files_e1 = \
    [tuple3[0] + "/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_raw_DSC") \
     if ("wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" in  tuple3[2] and "_e1_" in tuple3[0])]

    topup_cbv_files_e1 = \
    [tuple3[0] + "/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_applytopup") \
     if ("wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" in  tuple3[2] and "_e1_" in tuple3[0])]

    epic_cbv_files_e1 = \
    [tuple3[0] + "/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_applyepic") \
     if ("wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" in  tuple3[2] and "_e1_" in tuple3[0])]

    # Spin Echo nrCBV (e2)

    raw_cbv_files_e2 = \
    [tuple3[0] + "/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_raw_DSC") \
     if ("wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" in  tuple3[2] and "_e2_" in tuple3[0])]

    topup_cbv_files_e2 = \
    [tuple3[0] + "/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_applytopup") \
     if ("wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" in  tuple3[2] and "_e2_" in tuple3[0])]

    epic_cbv_files_e2 = \
    [tuple3[0] + "/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_applyepic") \
     if ("wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii" in  tuple3[2] and "_e2_" in tuple3[0])]
    
    return raw_cbv_files_e1, topup_cbv_files_e1, epic_cbv_files_e1, raw_cbv_files_e2, topup_cbv_files_e2, epic_cbv_files_e2

def find_field_files(corrections_base_directory):

    # Gradient Echo based

    topup_field_files_e1 = []
    for tuple3 in os.walk(corrections_base_directory + "/EPI_applytopup"):
        for filename in tuple3[2]:
            if "_e1_0000_prep_topup_field_postp.nii" in filename and "wr_" in filename:
                topup_field_files_e1 += [tuple3[0] + "/" + filename]


    epic_field_files_e1 = [tuple3[0] + "/wr_coregest_displacement_field_e1.nii" \
                            for tuple3 in os.walk(corrections_base_directory + "/EPI_applyepic") \
                            if "wr_coregest_displacement_field_e1.nii" in tuple3[2]]
    
    # Spin Echo based

    topup_field_files_e2 = []
    for tuple3 in os.walk(corrections_base_directory + "/EPI_applytopup"):
        for filename in tuple3[2]:
            if "_e2_0000_prep_topup_field_postp.nii" in filename and "wr_" in filename:
                topup_field_files_e2 += [tuple3[0] + "/" + filename]

    epic_field_files_e2 = [tuple3[0] + "/wr_coregest_displacement_field_e2.nii" \
                            for tuple3 in os.walk(corrections_base_directory + "/EPI_applyepic") \
                            if "wr_coregest_displacement_field_e2.nii" in tuple3[2]]
    
    return topup_field_files_e1, epic_field_files_e1, topup_field_files_e2, epic_field_files_e2

def find_label_files(corrections_base_directory):

    # Gradient Echo nrCBV (e1)

    raw_label_files_e1 = \
    [tuple3[0] + "/r_e1_labels_Neuromorphometrics.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_raw_DSC") \
     if ("r_e1_labels_Neuromorphometrics.nii" in  tuple3[2])]

    topup_label_files_e1 = \
    [tuple3[0] + "/r_e1_labels_Neuromorphometrics.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_applytopup") \
     if ("r_e1_labels_Neuromorphometrics.nii" in  tuple3[2])]

    epic_label_files_e1 = \
    [tuple3[0] + "/r_e1_labels_Neuromorphometrics.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_applyepic") \
     if ("r_e1_labels_Neuromorphometrics.nii" in  tuple3[2])]

    # Spin Echo nrCBV (e2)
    
    raw_label_files_e2 = \
    [tuple3[0] + "/r_e2_labels_Neuromorphometrics.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_raw_DSC") \
     if ("r_e2_labels_Neuromorphometrics.nii" in  tuple3[2])]

    topup_label_files_e2 = \
    [tuple3[0] + "/r_e2_labels_Neuromorphometrics.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_applytopup") \
     if ("r_e2_labels_Neuromorphometrics.nii" in  tuple3[2])]

    epic_label_files_e2 = \
    [tuple3[0] + "/r_e2_labels_Neuromorphometrics.nii" \
     for tuple3 in os.walk(corrections_base_directory + "/EPI_applyepic") \
     if ("r_e2_labels_Neuromorphometrics.nii" in  tuple3[2])]
    
    return raw_label_files_e1, topup_label_files_e1, epic_label_files_e1, raw_label_files_e2, topup_label_files_e2, epic_label_files_e2

def find_segment_files(segment_base_directory):
    segment_files = \
    [tuple3[0] + "/mni/rSegmentation.nii" \
     for tuple3 in os.walk(segment_base_directory) \
     if ("mni" in  tuple3[1])]
    return segment_files