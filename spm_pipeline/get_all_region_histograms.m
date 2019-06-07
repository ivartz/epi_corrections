function [region_values,...
    hist_edges,...
    raw_CBV_region_histograms,...
    topup_CBV_region_histograms,...
    epic_CBV_region_histograms] =...
    get_all_region_histograms(epi_corrections_out_dir)

% Number of histogram cells; resolution of histograms.
hist_num_cells = 60;

% % To be commended out when used as a function.
% epi_corrections_out_dir = ...
%     '/media/ivar/Shared/sf-virtualbox/IVS EPI Basline/epi_corrections_out_2019_04_25_372114315';

% Assuming this exists. This is the maximum probability tissue labels nifti
% file in <spm_dir>/tpm/labels_Neuromorphometrics.nii (MNI), but resliced
% to same voxel resolution as the DSC data using SPM (still MNI space).
regions_file_string = ...
    strcat(epi_corrections_out_dir, '/', 'rlabels_Neuromorphometrics.nii');

% Read the region atlas
regions_data = niftiread(regions_file_string);

% Get CBV from raw EPI structs
EPI_raw_CBV_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_raw_DSC/*/*/*/*/wr_coregest_Normalized rCBV map -Leakage corrected.nii'));

% Get CBV from TOPUP corrected EPI structs
EPI_applytopup_CBV_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applytopup/*/*/*/*/wr_coregest_Normalized rCBV map -Leakage corrected.nii'));

% Get CBV from EPIC corrected EPI structs
EPI_applyepic_CBV_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applyepic/*/*/*/*/wr_coregest_Normalized rCBV map -Leakage corrected.nii'));

% Get global min and max value of CBV maps, so
% that histograms can be compared.
[hist_min_value, hist_max_value] = get_global_min_max_no_outliers(...
    regions_data,...
    EPI_raw_CBV_struct_array, ...
    EPI_applytopup_CBV_struct_array, ...
    EPI_applyepic_CBV_struct_array);

disp(hist_min_value);
disp(hist_max_value);

% The histogram edges that is used
hist_edges = hist_min_value:((hist_max_value - hist_min_value)/hist_num_cells):hist_max_value;

% The number of regions in the regions data 
% is the number of unique values except 0.
num_regions = length(unique(regions_data)) - 1;    

% --- Calculate histograms for raw CBV
num_raw_CBV = length(EPI_raw_CBV_struct_array);
% All histograms stored in this matrix.
raw_CBV_region_histograms = zeros(num_raw_CBV, num_regions, hist_num_cells);
for i = 1:num_raw_CBV
    % Get the CBV struct.
    CBV_struct_array = EPI_raw_CBV_struct_array(i);
    
    % Get the CBV file string.
    CBV_file = strcat(CBV_struct_array.folder, '/', CBV_struct_array.name);
 
    % Read the CBV
    volume_data = niftiread(CBV_file);

    % Compute histograms.
    [region_values, region_histograms] = calculate_region_histograms(...
        volume_data, ...
        regions_data, ...
        hist_num_cells, ...
        hist_min_value, ...
        hist_max_value);
    
    raw_CBV_region_histograms(i, :, :) = region_histograms;
end

% --- Calculate histograms for TOPUP CBV
num_topup_CBV = length(EPI_applytopup_CBV_struct_array);
% All histograms stored in this matrix.
topup_CBV_region_histograms = zeros(num_topup_CBV, num_regions, hist_num_cells);
for i = 1:num_topup_CBV
    % Get the CBV struct.
    CBV_struct_array = EPI_applytopup_CBV_struct_array(i);
    
    % Get the CBV file string.
    CBV_file = strcat(CBV_struct_array.folder, '/', CBV_struct_array.name);
 
    % Read the CBV
    volume_data = niftiread(CBV_file);

    % Compute histograms.
    [region_values, region_histograms] = calculate_region_histograms(...
        volume_data, ...
        regions_data, ...
        hist_num_cells, ...
        hist_min_value, ...
        hist_max_value);
    
    topup_CBV_region_histograms(i, :, :) = region_histograms;
end

% --- Calculate histograms for EPIC CBV
num_epic_CBV = length(EPI_applyepic_CBV_struct_array);
% All histograms stored in this matrix.
epic_CBV_region_histograms = zeros(num_epic_CBV, num_regions, hist_num_cells);
for i = 1:num_epic_CBV
    % Get the CBV struct.
    CBV_struct_array = EPI_applyepic_CBV_struct_array(i);
    
    % Get the CBV file string.
    CBV_file = strcat(CBV_struct_array.folder, '/', CBV_struct_array.name);
 
    % Read the CBV
    volume_data = niftiread(CBV_file);

    % Compute histograms.
    [region_values, region_histograms] = calculate_region_histograms(...
        volume_data, ...
        regions_data, ...
        hist_num_cells, ...
        hist_min_value, ...
        hist_max_value);
    
    epic_CBV_region_histograms(i, :, :) = region_histograms;
end

%disp(size(raw_CBV_region_histograms));
%disp(size(topup_CBV_region_histograms));
%disp(size(epic_CBV_region_histograms));

end