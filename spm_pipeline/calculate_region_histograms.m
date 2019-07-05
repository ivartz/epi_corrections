function [region_values, region_histograms] = calculate_region_histograms(volume_data, ...
                                                regions_data, ...
                                                hist_num_cells, ...
                                                hist_min, ...
                                                hist_max)
    
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
    %volume_file_string = ...
    % '/media/ivar/Shared/sf-virtualbox/IVS EPI Basline/epi_corrections_out_2019_04_25_372114315/EPI_applytopup/372114315/DAY_0000/No_DeFacing_GE-SE_EPI_SSH_v1_32CH_V2_scan/145923_GE-SE_EPI_SSH_v1_32CH_V2_scan_1001_e1_prep_topup_applytopup_postp_perf/wr_coregest_Normalized rCBV map -Leakage corrected.nii';
    
    %regions_file_string = ...
    % '/media/ivar/Shared/sf-virtualbox/IVS EPI Basline/epi_corrections_out_2019_04_25_372114315/rlabels_Neuromorphometrics.nii';
    
    % Read the volume
    %volume_data = niftiread(volume_file_string);
    
    % Read the region atlas
    %regions_data = niftiread(regions_file_string);
    
    % Get the header.
    %volume_info = niftiinfo(volume_file_string);
    
    % Any region that is not 0 is the brain.
    %regions_brain_mask = regions_data ~= 0;
    
    % Mask for Regions outsite of the brain.
    regions_nonbrain_mask = regions_data == 0;

    % Mask of the possible NaN values in volume.
    %volume_nan_mask = isnan(volume_data);
    
    % Setting possible NaN values in volume to 0 .
    %volume_data(volume_nan_mask) = single(0);
    
    % Setting non-brain regions to 0 .
    %volume_data(regions_nonbrain_mask) = single(0);
    
    % Setting non-brain regions to nan
    volume_data(regions_nonbrain_mask) = nan;
    
    % Volume zero mask
    volume_zero_mask = volume_data == 0;
    
    % Setting zeros in the volume to nan
    volume_data(volume_zero_mask) = nan;
 
    % A vector containing all unique values in 
    % regions_data.
    region_values = unique(regions_data);    
    
    % The resolution in the histograms to calculate.
    %num_hist_cells = 60;
    
    % A matrix to contain all region histograms.
    region_histograms = zeros(length(region_values)-1, hist_num_cells);
        
    % Predefined histogram edges    
    edges = hist_min:((hist_max - hist_min)/hist_num_cells):hist_max;
    
    for i = 2:length(region_values)
                
        % Create ROI
        mask = 1 == (regions_data == region_values(i));

        % Get data in ROI
        region_data = volume_data.*single(mask);
        
        % Se the regions outside of the mask to nan
        % values
        region_data(~mask) = nan;

        %assignin('base','region_data', region_data);
        
        % Create histogram
        [N, ~] = histcounts(region_data(~isnan(region_data)), edges); 
        %N = histcounts(region_data);
        
        %plot(edges(1:length(edges)-1), N);
        
        %disp(max(edges(:)));
        
        % Insert the histogram at the correct row.
        region_histograms(i-1, :) = N;
    end
    
    % Remove the first entry in region_values, 
    % since this is 0; the values outside of the brain.
    region_values = region_values(2:end);
end