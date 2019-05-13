function [matched_folder, matched_name, matched_folder_and_name] = find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, FLAIR_3D_struct_array, TOPUP_or_EPIC_folder_name, FLAIR_3D_NIFTI_folder_name)

    matched_folder = '';
    matched_name = '';

    dsc_dir = DSC_struct_array.folder;
    
    startind_dsc_reldir = strfind(dsc_dir, TOPUP_or_EPIC_folder_name);
    
    dsc_reldir = dsc_dir(startind_dsc_reldir:length(dsc_dir));
    
    dsc_reldir_to_match = dsc_reldir(length(TOPUP_or_EPIC_folder_name)+2:length(dsc_reldir));
    
    %disp(dsc_reldir_to_match);
    
    max_match_length = 0;
    
    for i = 1:length(FLAIR_3D_struct_array)
        
        flair_dir = FLAIR_3D_struct_array(i).folder;
        
        %disp(flair_dir)
        
        startind_flair_reldir = strfind(flair_dir, FLAIR_3D_NIFTI_folder_name);
        
        flair_reldir = flair_dir(startind_flair_reldir:length(flair_dir));
        
        flair_reldir_to_match = flair_reldir(length(FLAIR_3D_NIFTI_folder_name)+2:length(flair_reldir));
        
        %disp(flair_reldir_to_match);
        
        match_length = 0;
        
        for j = 1:length(flair_reldir_to_match)
            if flair_reldir_to_match(j) == dsc_reldir_to_match(j)
                match_length = match_length + 1;
            end
        end
        
        if match_length > max_match_length
            max_match_length = match_length;
            matched_folder = flair_dir;
            % assume only one flair 3d .nii file
            matched_name = FLAIR_3D_struct_array(i).name;
        end
        
        %disp(max_match_length);
    end
    
    matched_folder_and_name = strcat(matched_folder, '/', matched_name);
    
end