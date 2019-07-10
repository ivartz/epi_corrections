function coreg_reslice_oncohabitats_segmentaiton_mni(epi_corrections_out_dir, ONCOHabitats_results_folder)
% ONCOHabitats_results_folder : Assumed to exist within epi_corrections_out_dir

%epi_corrections_out_dir = ...
%    '../../epi_corrections_out_2019_07_02';
%ONCOHabitats_results_folder = ...
%    'ONCOHabitats_results';

run_everything = true;
%run_everything = false;

% Based on a check in correction_assessment_part_1.ipynb, 
% all resliced labels files were verified to be equal. Thus, only the first
% one is sufficient for defining an image space for coreg reslice.
EPI_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/EPI_raw_DSC/**/r_e1_labels_Neuromorphometrics.nii'));

% Image defining space.
ref = strcat(EPI_struct_array(1).folder, ...
    '/', EPI_struct_array(1).name, ',1');

segmentations_compressed_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/', ONCOHabitats_results_folder, ...
    '/**/mni/Segmentation.nii.gz'));

parfor i = 1:length(segmentations_compressed_struct_array)
    segments_file_compressed = ...
        strcat(segmentations_compressed_struct_array(i).folder, ...
        '/', segmentations_compressed_struct_array(i).name);
    if run_everything
        to_decompress = segments_file_compressed;
        gunzip_function(to_decompress);
    end
end

segmentations_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/', ONCOHabitats_results_folder, ...
    '/**/mni/Segmentation.nii'));

parfor i = 1:length(segmentations_struct_array)
    % Coreg reslice ONCOHabitats segments files to perfusion MNI space
    % using a representative image defining space.
    
    % A list containing all files to reslice.
    to_reslice = cell(1, 1);
    
    segments_file= ...
        strcat(segmentations_struct_array(i).folder, ...
        '/', segmentations_struct_array(i).name);
    
    % Add regions_file_copied to the to_reslice list.
    to_reslice{1} = strcat(segments_file, ',1');
    
    % Transpose. Necessary for matlabbatch .
    to_reslice = to_reslice';
    
    % other
    src = to_reslice;
    
    disp(strcat('Loop ', int2str(i), ':', segments_file));
    
    if run_everything
        coreg_reslice_function(ref, src, 0); % Nearest neighbour interpolation
    end
end
end