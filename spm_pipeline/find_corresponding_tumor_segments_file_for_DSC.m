function [matched_folder, matched_name, matched_folder_and_name] = find_corresponding_tumor_segments_file_for_DSC(DSC_file, onco_dir, segments_struct_array)
    
    s = what(onco_dir);
    ONCOHabitats_full_path = s.path;
    
    for i = 1:length(segments_struct_array)
        
        segment_dir = segments_struct_array(i).folder;
        
        startind_segment_reldir = length(segment_dir) - strfind(reverse(segment_dir), reverse(ONCOHabitats_full_path));
        
        segment_reldir = segment_dir(startind_segment_reldir+3:length(segment_dir));
        
        ind_segment_reldir_first_slash = strfind(segment_reldir, '/');
        
        patient_id = segment_reldir(1:ind_segment_reldir_first_slash-1);
        
        if contains(DSC_file, patient_id)
            %disp('BINGO!');
            matched_folder = segment_dir;
            matched_name = segments_struct_array(i).name;
            matched_folder_and_name = strcat(matched_folder, '/', matched_name);
            %disp(matched_folder_and_name);
            
        end
    end
end
