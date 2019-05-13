function [hist_min_value, hist_max_value] = get_global_min_max_no_outliers(...
    regions_data,...
    EPI_raw_CBV_struct_array, ...
    EPI_applytopup_CBV_struct_array, ...
    EPI_applyepic_CBV_struct_array)
    
    hist_min_value = single(0);
    hist_max_value = single(0);
    
    regions_nonbrain_mask = regions_data == 0;
    
    % -- Raw CBV ---
    
    for i = 1:length(EPI_raw_CBV_struct_array)
    % Get the CBV struct.
    CBV_struct_array = EPI_raw_CBV_struct_array(i);
    
    % Get the CBV file string.
    CBV_file = strcat(CBV_struct_array.folder, '/', CBV_struct_array.name);
 
    % Read the CBV
    volume_data = niftiread(CBV_file);
    
    % set non-brain as nan
    volume_data(regions_nonbrain_mask) = nan;
    
    % Remove outliers from volume_data
    % An outlier is a value that is more than three scaled median absolute deviations (MAD)
    volume_data = rmoutliers(volume_data(~isnan(volume_data)), 'median');
    %volume_data = rmoutliers(volume_data(:));
    
    if min(volume_data(:)) < hist_min_value
        hist_min_value = min(volume_data(:));
    end
    
    if max(volume_data(:)) > hist_max_value
        hist_max_value = max(volume_data(:));
    end
    end
    
    % -- topup CBV ---
    
    for i = 1:length(EPI_applytopup_CBV_struct_array)
    % Get the CBV struct.
    CBV_struct_array = EPI_applytopup_CBV_struct_array(i);
    
    % Get the CBV file string.
    CBV_file = strcat(CBV_struct_array.folder, '/', CBV_struct_array.name);
 
    % Read the CBV
    volume_data = niftiread(CBV_file);
    
    % set non-brain as nan
    volume_data(regions_nonbrain_mask) = nan;
    
    % Remove outliers from volume_data
    % An outlier is a value that is more than three scaled median absolute deviations (MAD)
    volume_data = rmoutliers(volume_data(~isnan(volume_data)), 'median');
    %volume_data = rmoutliers(volume_data(:));
    
    if min(volume_data(:)) < hist_min_value
        hist_min_value = min(volume_data(:));
    end
    
    if max(volume_data(:)) > hist_max_value
        hist_max_value = max(volume_data(:));
    end
    end
    
    % -- epic CBV ---
    
    for i = 1:length(EPI_applyepic_CBV_struct_array)
    % Get the CBV struct.
    CBV_struct_array = EPI_applyepic_CBV_struct_array(i);
    
    % Get the CBV file string.
    CBV_file = strcat(CBV_struct_array.folder, '/', CBV_struct_array.name);
 
    % Read the CBV
    volume_data = niftiread(CBV_file);
    
    % set non-brain as nan
    volume_data(regions_nonbrain_mask) = nan;
    
    % Remove outliers from volume_data
    % An outlier is a value that is more than three scaled median absolute deviations (MAD)
    volume_data = rmoutliers(volume_data(~isnan(volume_data)), 'median');
    %volume_data = rmoutliers(volume_data(:));
    
    if min(volume_data(:)) < hist_min_value
        hist_min_value = min(volume_data(:));
    end
    
    if max(volume_data(:)) > hist_max_value
        hist_max_value = max(volume_data(:));
    end
    end
end