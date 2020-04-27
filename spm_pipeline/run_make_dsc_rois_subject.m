function run_make_dsc_rois_subject(i, ...
    EPI_struct_array, ...
    EPI_folder_name, ...
    onco_dir, ...
    mni_tumor_segments_struct_array, ...
    flair_tumor_segments_struct_array, ...
    FLAIR_3D_struct_array, ...
    regions_file, ...
    run_everything)
	% 1. Get the files
    % DSC
    DSC_struct_array = EPI_struct_array(i);
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    % Tumor regions in MNI space
    [~, ~, mni_tumor_segments_file] = ...
        find_corresponding_tumor_segments_file_for_DSC(DSC_file, onco_dir, mni_tumor_segments_struct_array);
    
    % Tumor regions in FLAIR space
    [~, ~, flair_tumor_segments_file] = ...
        find_corresponding_tumor_segments_file_for_DSC(DSC_file, onco_dir, flair_tumor_segments_struct_array);
    
    % FLAIR
    [~, ~, FLAIR_3D_file] = ...
        find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, ...
        FLAIR_3D_struct_array, EPI_folder_name, 'FLAIR_3D');
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    disp(strcat('Loop ', int2str(i), ':', mni_tumor_segments_file));
    disp(strcat('Loop ', int2str(i), ':', flair_tumor_segments_file));
    disp(strcat('Loop ', int2str(i), ':', FLAIR_3D_file));
    
    % 2. Determine gradient echo (e1) or spin echo (e2) DSC
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
    disp(strcat('Loop ', int2str(i), ': DSC type: ', type));
    
    % 3. Make not ground truth brain and tumor regions
    % (using tumor rois in mni space)
    if run_everything
        make_dsc_rois_subject(type, DSC_file, regions_file, mni_tumor_segments_file);
    end
    
    % 4. Make ground truth brain and tumor regions
    % (using tumor rois in flair space)
    if run_everything
        make_gt_dsc_rois_subject(type, DSC_file, FLAIR_3D_file, regions_file, flair_tumor_segments_file);
    end   
end