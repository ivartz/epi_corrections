function [matched_folder, matched_name, matched_folder_and_name] = find_corresponding_native_flair_tumor_segments_file_for_DSC(DSC_file, onco_dir, segments_struct_array)
    
    s = what(onco_dir);
    ONCOHabitats_tumor_segments_from_flair_native_full_path = s.path;

%     ONCOHabitats_tumor_segments_from_flair_native_full_path = ...
%         '/media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections_out_2019_07_02_native/ONCOHabitats_tumor_segments_from_flair_native';
% 
%     DSC_file = ...
%         '/media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections_out_2019_07_02_native/EPI_applyepic_test/Anonymized/DEFACED_IVS/37852448/DAY_0000/No_DeFacing_WIP_GE-SE_EPI_SSH_v1_32CH_SENSE/135702_WIP_GE-SE_EPI_SSH_v1_32CH_SENSE_1001_e1_applyepic.nii';
%     
%     epi_corrections_out_dir = '../../epi_corrections_out_2019_07_02_native';
%     
%     segments_struct_array = dir(strcat(epi_corrections_out_dir, ...
%         '/ONCOHabitats_tumor_segments_from_flair_native/**/results/native/Segmentation_Flair_space.nii'));
    
    for i = 1:length(segments_struct_array)
        
        segment_dir = segments_struct_array(i).folder;
        
        %disp(DSC_file);
        
        %disp(segment_dir);
        
        startind_segment_reldir = length(segment_dir) - strfind(reverse(segment_dir), reverse(ONCOHabitats_tumor_segments_from_flair_native_full_path));
        
        segment_reldir = segment_dir(startind_segment_reldir+3:length(segment_dir));
        
        ind_segment_reldir_first_slash = strfind(segment_reldir, '/');
        
        patient_id = segment_reldir(1:ind_segment_reldir_first_slash-1);
        
        %disp(patient_id);
        
        if contains(DSC_file, patient_id)
            %disp('BINGO!');
            matched_folder = segment_dir;
            matched_name = segments_struct_array(i).name;
            matched_folder_and_name = strcat(matched_folder, '/', matched_name);
            %disp(matched_folder_and_name);
            
        end

    end
end
