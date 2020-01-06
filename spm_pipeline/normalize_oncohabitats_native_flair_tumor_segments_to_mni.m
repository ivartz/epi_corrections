function normalize_oncohabitats_native_flair_tumor_segments_to_mni(epi_corrections_out_dir, ONCOHabitats_results_folder)
% ONCOHabitats_results_folder : Assumed to exist within epi_corrections_out_dir

%epi_corrections_out_dir = ...
%    '../../epi_corrections_out_2019_07_02';
%ONCOHabitats_results_folder = ...
%    'ONCOHabitats_tumor_segments_from_flair_native';

run_everything = true;
%run_everything = false;

deformations_struct_array = dir(strcat(epi_corrections_out_dir, '/**/y_*.nii'));

segmentations_compressed_struct_array = ...
    dir(strcat(epi_corrections_out_dir, ...
    '/', ONCOHabitats_results_folder, ...
    '/**/native/Segmentation_Flair_space.nii.gz'));

if run_everything
    parfor i = 1:length(segmentations_compressed_struct_array)
        segments_file_compressed = ...
            strcat(segmentations_compressed_struct_array(i).folder, ...
            '/', segmentations_compressed_struct_array(i).name);
        
        to_decompress = segments_file_compressed;
        gunzip_function(to_decompress);
    end
    
    segmentations_struct_array = ...
        dir(strcat(epi_corrections_out_dir, ...
        '/', ONCOHabitats_results_folder, ...
        '/**/native/Segmentation_Flair_space.nii'));
end

parfor i = 1:length(deformations_struct_array)
    % MNI normalize ONCOHabitats segments files to perfusion MNI space
    % using a representative image defining space.
    
    % --------------------------------
    % 1. Get the files
    
    deformation_struct_array = deformations_struct_array(i);
    deformation_folder = deformations_struct_array(i).folder;
    deformation_name = deformations_struct_array(i).name;
    deformation_file = strcat(deformation_folder, '/', deformation_name);
    
    [segment_folder, segment_file_name, segment_file] = ...
        find_corresponding_native_flair_tumor_segment_for_MNI_def_field(...
        strcat(epi_corrections_out_dir,'/',ONCOHabitats_results_folder), ...
        deformation_struct_array, ...
        segmentations_struct_array);
    
    %disp(strcat('Loop ', int2str(i), ': ', deformation_file));
    %disp(strcat('Loop ', int2str(i), ': ', segment_file));
    
    %disp(deformation_file);
    %disp(segment_file);
    % --------------------------------
    
    % --------------------------------
        
    % 3. Normalization into MNI space.
    % Existing deformation fields are used to transform the coregistered
    % tumor segments into MNI space.

    % 3b. Use estimated deformation field (y) to transform the relevant
    % volumes into MNI space (write).

    nrun = 1;
    jobfile = {'norm_write_job_knn.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(2, nrun);

    % Use previously estimated deformation field
    inputs{1, 1} = cellstr(deformation_file);

    to_resample = cell(1, 1);

    to_resample{1} = strcat(segment_file, ',1');

    % transpose
    to_resample = to_resample';

    % images to write
    inputs{2, 1} = cellstr(to_resample);

    if run_everything
        spm('defaults', 'FMRI');
        spm_jobman('run', jobs, inputs{:});
    end
    % --------------------------------
    
    % --------------------------------
    % Move MNI normalized segments to mni folder
    segment_file_normalized = strcat(segment_folder, '/w',segment_file_name);
    disp(strcat('Loop ', int2str(i), ': ', segment_file_normalized));
    segment_file_normalized_moved = strcat(segment_folder(1:length(segment_folder)-length('native')), 'mni/Segmentation.nii');
    disp(strcat('Loop ', int2str(i), ': ', segment_file_normalized_moved));
    if run_everything
        movefile(segment_file_normalized, segment_file_normalized_moved);
    end
    % --------------------------------
end