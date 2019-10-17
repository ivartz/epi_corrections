function [region_values,...
    hist_edges,...
    raw_e1_CBV_region_histograms,...
    raw_e1_CBV_dirs,...
    raw_e2_CBV_region_histograms,...
    raw_e2_CBV_dirs,...
    topup_e1_CBV_region_histograms,...
    topup_e1_CBV_dirs,...
    topup_e2_CBV_region_histograms,...
    topup_e2_CBV_dirs,...
    epic_e1_CBV_region_histograms,...
    epic_e1_CBV_dirs,...
    epic_e2_CBV_region_histograms,...
    epic_e2_CBV_dirs] =...
    get_all_region_histograms(epi_corrections_out_dir, hist_num_cells, ...
    hist_min_value, hist_max_value, region_req_covered_frac, min_roi_region)

% Number of histogram cells; resolution of histograms.
%hist_num_cells = 64;

% Maximum probability tissue labels nifti
% files in <spm_dir>/tpm/labels_Neuromorphometrics.nii (MNI), but resliced
% to same voxel resolution as the DSC data using SPM (still MNI space).

EPI_raw_e1_regions_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_raw_DSC/**/r_e1_labels_Neuromorphometrics_lrmerged.nii'));
EPI_raw_e2_regions_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_raw_DSC/**/r_e2_labels_Neuromorphometrics_lrmerged.nii'));
EPI_applytopup_e1_regions_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applytopup/**/r_e1_labels_Neuromorphometrics_lrmerged.nii'));
EPI_applytopup_e2_regions_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applytopup/**/r_e2_labels_Neuromorphometrics_lrmerged.nii'));
EPI_applyepic_e1_regions_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applyepic/**/r_e1_labels_Neuromorphometrics_lrmerged.nii'));
EPI_applyepic_e2_regions_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applyepic/**/r_e2_labels_Neuromorphometrics_lrmerged.nii'));

% Get CBV from raw EPI structs
EPI_raw_e1_CBV_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_raw_DSC/**/*e1*/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii'));
raw_e1_CBV_dirs = struct2cell(EPI_raw_e1_CBV_struct_array);
raw_e1_CBV_dirs = raw_e1_CBV_dirs(2, :);
EPI_raw_e2_CBV_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_raw_DSC/**/*e2*/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii'));
raw_e2_CBV_dirs = struct2cell(EPI_raw_e2_CBV_struct_array);
raw_e2_CBV_dirs = raw_e2_CBV_dirs(2, :);
% Get CBV from TOPUP corrected EPI structs
EPI_applytopup_e1_CBV_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applytopup/**/*e1*/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii'));
topup_e1_CBV_dirs = struct2cell(EPI_applytopup_e1_CBV_struct_array);
topup_e1_CBV_dirs = topup_e1_CBV_dirs(2, :);
EPI_applytopup_e2_CBV_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applytopup/**/*e2*/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii'));
topup_e2_CBV_dirs = struct2cell(EPI_applytopup_e2_CBV_struct_array);
topup_e2_CBV_dirs = topup_e2_CBV_dirs(2, :);
% Get CBV from EPIC corrected EPI structs
EPI_applyepic_e1_CBV_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applyepic/**/*e1*/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii'));
epic_e1_CBV_dirs = struct2cell(EPI_applyepic_e1_CBV_struct_array);
epic_e1_CBV_dirs = epic_e1_CBV_dirs(2, :);
EPI_applyepic_e2_CBV_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applyepic/**/*e2*/wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii'));
epic_e2_CBV_dirs = struct2cell(EPI_applyepic_e2_CBV_struct_array);
epic_e2_CBV_dirs = epic_e2_CBV_dirs(2, :);

% Get global min and max value of CBV maps, so
% that histograms can be compared.
%[hist_min_value, hist_max_value] = get_global_min_max_no_outliers(...
%    regions_data,...
%    EPI_raw_CBV_struct_array, ...
%    EPI_applytopup_CBV_struct_array, ...
%    EPI_applyepic_CBV_struct_array);

% From looking at histograms
%hist_min_value = 0;
%hist_max_value = 12;

%disp('Global min is:');
%disp(hist_min_value);
%disp('Global max is:');
%disp(hist_max_value);

% The number of regions in the regions data 
% is the number of unique values except 0.
%num_regions = length(unique(regions_data)) - 1;
%num_regions = 134; % This is the number of brain regions in the MNI regions template form SPM
num_regions = 71; % This is the number of unique regions in resliced MNI regions file 
% (except 0) where left and right parts have been merged

% The histogram edges that is used
hist_edges = hist_min_value:((hist_max_value - hist_min_value)/hist_num_cells):hist_max_value;

% --- Calculate histograms for raw CBV
% e1
[~, raw_e1_CBV_region_histograms] = get_region_histograms(EPI_raw_e1_CBV_struct_array, ...
                                                            EPI_raw_e1_regions_struct_array, ...
                                                            num_regions, ...
                                                            hist_num_cells, ...
                                                            hist_min_value, ...
                                                            hist_max_value, ...
                                                            region_req_covered_frac, ...
                                                            min_roi_region);
% e2
[~, raw_e2_CBV_region_histograms] = get_region_histograms(EPI_raw_e2_CBV_struct_array, ...
                                                            EPI_raw_e2_regions_struct_array, ...
                                                            num_regions, ...
                                                            hist_num_cells, ...
                                                            hist_min_value, ...
                                                            hist_max_value, ...
                                                            region_req_covered_frac, ...
                                                            min_roi_region);
% --- Calculate histograms for TOPUP CBV
% e1
[~, topup_e1_CBV_region_histograms] = get_region_histograms(EPI_applytopup_e1_CBV_struct_array, ...
                                                            EPI_applytopup_e1_regions_struct_array, ...
                                                            num_regions, ...
                                                            hist_num_cells, ...
                                                            hist_min_value, ...
                                                            hist_max_value, ...
                                                            region_req_covered_frac, ...
                                                            min_roi_region);
% e2
[~, topup_e2_CBV_region_histograms] = get_region_histograms(EPI_applytopup_e2_CBV_struct_array, ...
                                                            EPI_applytopup_e2_regions_struct_array, ...
                                                            num_regions, ...
                                                            hist_num_cells, ...
                                                            hist_min_value, ...
                                                            hist_max_value, ...
                                                            region_req_covered_frac, ...
                                                            min_roi_region);

% --- Calculate histograms for EPIC CBV
% e1
[~, epic_e1_CBV_region_histograms] = get_region_histograms(EPI_applyepic_e1_CBV_struct_array, ...
                                                            EPI_applyepic_e1_regions_struct_array, ...
                                                            num_regions, ...
                                                            hist_num_cells, ...
                                                            hist_min_value, ...
                                                            hist_max_value, ...
                                                            region_req_covered_frac, ...
                                                            min_roi_region);
% e2
[region_values, epic_e2_CBV_region_histograms] = get_region_histograms(EPI_applyepic_e2_CBV_struct_array, ...
                                                            EPI_applyepic_e2_regions_struct_array, ...
                                                            num_regions, ...
                                                            hist_num_cells, ...
                                                            hist_min_value, ...
                                                            hist_max_value, ...
                                                            region_req_covered_frac, ...
                                                            min_roi_region);

disp('The size of raw_e1_CBV_region_histograms is:')
disp(size(raw_e1_CBV_region_histograms));
disp('The size of raw_e2_CBV_region_histograms is:')
disp(size(raw_e2_CBV_region_histograms));
disp('The size of topup_e1_CBV_region_histograms is:')
disp(size(topup_e1_CBV_region_histograms));
disp('The size of topup_e2_CBV_region_histograms is:')
disp(size(topup_e2_CBV_region_histograms));
disp('The size of epic_e1_CBV_region_histograms is:')
disp(size(epic_e1_CBV_region_histograms));
disp('The size of epic_e2_CBV_region_histograms is:')
disp(size(epic_e2_CBV_region_histograms));

end