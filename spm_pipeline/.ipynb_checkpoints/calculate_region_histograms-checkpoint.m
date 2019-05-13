function region_histograms = calculate_region_histograms(volume_file_string, region_file_string)
    % volume_file : file path + / + file name for the volume for which to
    % calculate region histograms (in MNI space)
    % region_file : file path + / + file name for the (resliced into volume_file MNI space
    % as image defining space) labels_Neuromorphometrics.nii 
    % (from <spm dir>/tpm/labels_Neuromorphometrics.nii)
    
    %{
    Description region_file:
    Maximum probability tissue labels derived from the 
    ``MICCAI 2012 Grand Challenge and Workshop on Multi-Atlas Labeling'' 
    (https://masi.vuse.vanderbilt.edu/workshop2012/index.php/Challenge_Details). 
    These data were released under the Creative Commons Attribution-NonCommercial 
    (CC BY-NC) with no end date. Users should credit the MRI scans as originating 
    from the OASIS project (http://www.oasis-brains.org/) and the labeled data as 
    "provided by Neuromorphometrics, Inc. (http://Neuromorphometrics.com/) under academic subscription".  
    These references should be included in all workshop and final publications.
    %}
    volume_file_string = '/media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections_out_2019_04_25_372114315/EPI_applytopup/372114315/DAY_0000/No_DeFacing_GE-SE_EPI_SSH_v1_32CH_V2_scan/145923_GE-SE_EPI_SSH_v1_32CH_V2_scan_1001_e1_prep_topup_applytopup_postp_perf/wr_coregest_Normalized rCBV map -Leakage corrected.nii';
    
    region_file_string = '/media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections_out_2019_04_25_372114315/rlabels_Neuromorphometrics.nii';
    
    disp(volume_file_string);
    disp(region_file_string);
    
    volume_data = niftiread(volume_file_string);
    disp(size(volume_data));
    region_data = niftiread(region_file_string);
    disp(size(region_data));
    
    reion_values = unique(region_data);
    disp(reion_values);
    
end