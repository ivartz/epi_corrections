function [region_values, CBV_region_histograms] = get_region_histograms(all_CBV_struct_array, ...
                                                            all_regions_struct_array, ...
                                                            num_regions, ...
                                                            hist_num_cells, ...
                                                            hist_min_value, ...
                                                            hist_max_value)
    num_CBVs = length(all_CBV_struct_array);
    % All histograms stored in this matrix.
    CBV_region_histograms = zeros(num_CBVs, num_regions, hist_num_cells);
    for i = 1:num_CBVs
        % Get the CBV struct.
        CBV_struct_array = all_CBV_struct_array(i);

        % Get the CBV file string.
        CBV_file = strcat(CBV_struct_array.folder, '/', CBV_struct_array.name);

        % Read the CBV
        volume_data = niftiread(CBV_file);

        % Get the regions struct
        regions_struct_array = all_regions_struct_array(i);

        % Get the regions file string
        regions_file = strcat(regions_struct_array.folder, '/', regions_struct_array.name);

        % Read the regions file
        regions_data = niftiread(regions_file);

        % Compute histograms.
        [region_values, region_histograms] = calculate_region_histograms(...
            volume_data, ...
            regions_data, ...
            hist_num_cells, ...
            hist_min_value, ...
            hist_max_value);

        CBV_region_histograms(i, :, :) = region_histograms;
    end
end