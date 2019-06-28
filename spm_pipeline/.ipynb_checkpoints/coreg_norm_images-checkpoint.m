function coreg_norm_images(epi_corrections_out_dir)

% Note: This script is very specific on the output directory structure from the epi corrections pipeline.

% 1. Specify directories.
%%
% Multiple copies of this file will be resliced and saved to a separate file.
% NOTE: THIS NEEDS TO BE CHANGED
regions_file = '/media/loek/HDD3TB1/apps/spm12/tpm/labels_Neuromorphometrics.nii';

%epi_corrections_out_dir = '../../epi_corrections_out_2019_04_25';

%FLAIR_3D_struct_array = dir(strcat(epi_corrections_out_dir, '/FLAIR_3D/*/*/*/*.nii'));
FLAIR_3D_struct_array = dir(strcat(epi_corrections_out_dir, '/FLAIR_3D/**/*.nii'));

%EPI_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_raw_DSC/*/*/*/*.nii'));
EPI_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_raw_DSC/**/*.nii'));
EPI_struct_array = EPI_struct_array(~contains({EPI_struct_array.folder}, 'perf'));

%EPI_applytopup_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applytopup/*/*/*/*applytopup_postp.nii'));
EPI_applytopup_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applytopup/**/*applytopup_postp.nii'));
%EPI_applytopup_orf_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applytopup/*/*/*/*field_postp.nii'));
EPI_applytopup_orf_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applytopup/**/*field_postp.nii'));

%EPI_applyepic_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/*/*/*/*applyepic.nii'));
EPI_applyepic_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/**/*applyepic.nii'));
%EPI_applyepic_df_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/*/*/*/*field_e*.nii'));
EPI_applyepic_df_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/**/*field_e*.nii'));

%MNI_region_maps_struct_array = dir(strcat(epi_corrections_out_dir, '/MNI_region_maps/*.nii'));

%%
% 2. Run settings.
%%
disp('Valid EPI dirs [1: Valid, 0: Not Valid]:');
valid_check = {length({EPI_struct_array.name})/2 == length({EPI_applytopup_struct_array.name})/2 , length({EPI_struct_array.name})/2 == length({EPI_applyepic_struct_array.name})/2};
valid = all(cell2mat(valid_check)');
 if valid
     disp('Valid clean EPI dirs');
 else
     disp('Not clean Valid EPI dirs');
     return;
 end
 
run_everything = true;
%run_everything = false;

if run_everything == false
    disp('--run_everything is set to false; will only print detected data--')
else
    disp('--run_everything is set to true; will start complete pipeline with parfor multiprocessing--')
end

%%
% 3. Running pipeline.
% Pipeline overview:
% For raw, topup, and epic corrected images, do:
% - Low res -> High res coreg est reslice : out: upsampled first dynamic DSC .
% - Normalize est : out: deformation field
% - Normalize write : out: DSC first dynamic + topup/epic field + perfusion
% maps in MNI space.
% - Coreg est : out : brain regions files in perfusion MNI space.

% Update: parfor parallelization did not allow to be run within a function,
% thus the code sadly needs to be replicated three times -> Use section
% folding.
%%
% 3a. Raw data.
%%
disp("--Running coreg + MNI nomraliation pipeline on raw data + Perfusion images--");
%coreg_norm_pipeline(run_everything, EPI_struct_array, [], FLAIR_3D_struct_array, 'EPI_raw_DSC');
EPI_folder_name = 'EPI_raw_DSC';
EPI_corrected = false;
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    % 1. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    [FLAIR_3D_folder, FLAIR_3D_file_name, FLAIR_3D_file] = ...
        find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, ...
        FLAIR_3D_struct_array, EPI_folder_name, 'FLAIR_3D');
    
    if EPI_corrected
        field_struct_array = EPI_field_struct_array(i);
    
        field = strcat(field_struct_array.folder, '/', ...
            field_struct_array.name);
    end
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    if EPI_corrected
        disp(strcat('Loop ', int2str(i), ':', field));
    end
    
    disp(strcat('Loop ', int2str(i), ':', FLAIR_3D_file));
    
    % --------------------------------
    
    % --------------------------------
    
    % 2. Low res. (DSC first dynamic volume, src) -> low res. (FLAIR 3D, ref)
    % coregistration; estimate and reslice.
    
    % Flair 3D as ref file
    ref_file = FLAIR_3D_file;
    ref = strcat(ref_file, ',1');
    
    % First dynamic volume as src file.
    
    % Make a copy of the file to work on.
    src_file = strcat(DSC_file);
    src_file_copied = ...
        strcat(DSC_struct_array.folder, '/_coregest_', ...
        DSC_struct_array.name);
    
    if run_everything
        copyfile(src_file, src_file_copied);
    end
    
    src = strcat(src_file_copied, ',1');
    
    % Get the perfusion files
    DSC_file_name = DSC_struct_array.name;
    perfusion_dir_string = ...
        strcat(DSC_struct_array.folder, '/', ...
        DSC_file_name(1:length(DSC_file_name)-length('.nii')), '_perf');
    
    perfusion_struct_array = ...
        dir(strcat(perfusion_dir_string, '/*.nii'));
    
    % A list containing all files to reslice.
    if EPI_corrected
        to_reslice = ...
            cell(1, length(perfusion_struct_array)+1);
    else
        to_reslice = ...
            cell(1, length(perfusion_struct_array));
    end
    
    for j = 1:length(perfusion_struct_array)
        perfusion_maps_struct_array = ...
            perfusion_struct_array(j);
    
        perfusion_file = ...
            strcat(perfusion_maps_struct_array.folder, '/', ...
            perfusion_maps_struct_array.name);
    
        perfusion_file_copied = ...
            strcat(perfusion_maps_struct_array.folder, '/_coregest_', ...
            perfusion_maps_struct_array.name);
    
        if run_everything
            copyfile(perfusion_file, perfusion_file_copied);
        end
        to_reslice{j} = ...
            strcat(perfusion_file_copied, ',1');
    end
    
    if EPI_corrected
        % The off-resonance field (topup) or deformation field (epic)
        field_copied = ...
            strcat(field_struct_array.folder, '/_coregest_', ...
            field_struct_array.name);
    
        if run_everything
            copyfile(field, field_copied);
        end
        
        to_reslice{length(perfusion_struct_array)+1} = ...
            strcat(field_copied, ',1');
    
    end
    
    % Transpose. Necessary for matlabbatch .
    to_reslice = to_reslice';
    
    % other
    other = to_reslice;
    
    if run_everything
        %coreg_est_reslice_function(ref, src, other, 4); % 4.order b-spline interpolation
        coreg_est_reslice_function(ref, src, other, 1); % Trilinear interpolation
        %coreg_est_reslice_function(ref, src, other, 0); % Nearest
        %neighbour interpolation
    end
    
    % --------------------------------
    
    % --------------------------------
    
    % 3. Normalization into MNI space.
    % This creates a deformation field (y) for the flair.
    % The deformation field is then used to transform the coregistered
    % volumes (dsc first dynamic, topup/epic fields and perfusion maps) into MNI space.
    
    % 3a. Estimate deformation
    % space. Outputs (y_<flair file name>).
    
    nrun = 1; % enter the number of runs here
    jobfile = {'norm_est_job.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(0, nrun);
    
    flair = strcat(FLAIR_3D_folder, '/', FLAIR_3D_file_name);
    
    % Since the code is run in parallell, multiple threads should not
    % access the same file at the same location. However, they can
    % access the same file copied to different locations.
    
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
    flair_copied = strcat(DSC_struct_array.folder, '/', ...
        type, '_', FLAIR_3D_file_name);
    
    if run_everything
    
        copyfile(flair, flair_copied);
    
    end
    
    vol = strcat(flair_copied, ',1');
    
    inputs{1, nrun} = cellstr(vol);
    
    if run_everything
        % Run
        spm('defaults', 'FMRI');
        spm_jobman('run', jobs, inputs{:});
    end
    
    % 3b. Use estimated deformation field (y) to transform the relevant
    % volumes into MNI space (write).
    
    nrun = 1;
    jobfile = {'norm_write_job.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(2, nrun);
    
    % Estimated deformation field
    def = strcat(DSC_struct_array.folder, '/y_', ...
        type, '_', FLAIR_3D_file_name);
    
    inputs{1, 1} = cellstr(def);
    
    if EPI_corrected
        to_resample = cell(1, 1+length(perfusion_struct_array)+1);
    else
        to_resample = cell(1, 1+length(perfusion_struct_array));
    end 
    
    to_resample{1} = ...
        strcat(DSC_struct_array.folder, '/r_coregest_', ...
        DSC_struct_array.name, ',1');
    
    % Fill in the coregistered perfusion maps
    for j = 1:length(perfusion_struct_array)
        perfusion_maps_struct_array = ...
            perfusion_struct_array(j);
        
        pefusion_file_copied_coregistered = ...
            strcat(perfusion_maps_struct_array.folder, '/r_coregest_', ...
            perfusion_maps_struct_array.name);
    
        to_resample{1+j} = ...
            strcat(pefusion_file_copied_coregistered, ',1');
    end
    
    if EPI_corrected
        % The coregistered off-resonance field (topup) or deformation field (epic)
        to_resample{1+length(perfusion_struct_array)+1} = ...
            strcat(field_struct_array.folder, '/r_coregest_', ...
            field_struct_array.name, ',1');
    end
    
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
    
    % 4. Coreg reslice MNI regions file to perfusion MNI space
    % using estimated deformation field from 3a.
    
    % The file consisting brain regions in MNI space should be resliced
    % to perfusion MNI space so that pixel-perfect masking of brain 
    % regions can be done later on for instance rCBV.
    % However, unlinke the other resliced images in 2., this reslice should
    % use Nearest Neighbour interpolation to achieve pixel-perfect
    % masking of brain regions.
    
    % Image defining space; estimated deformation field from 3a.
    ref = strcat(DSC_struct_array.folder, '/y_', ...
        type, '_', FLAIR_3D_file_name, ',1');
    
    % A list containing all files to reslice.
    to_reslice = cell(1, 1);
    
    if run_everything
        % Determine of gradient echo (e1) or spin echo (e2).
        type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
        % Copy the regions file so that it can be resliced.
        regions_file_copied = strcat(DSC_struct_array.folder, '/_', ...
            type, '_labels_Neuromorphometrics.nii');
    
        copyfile(regions_file, regions_file_copied);
        
        % Add regions_file_copied to the to_reslice list.
        to_reslice{1} = strcat(regions_file_copied, ',1');
    end
    
    % Transpose. Necessary for matlabbatch .
    to_reslice = to_reslice';
    
    % other
    src = to_reslice;
    
    if run_everything
        coreg_reslice_function(ref, src, 0); % Nearest neighbour interpolation
    end
    % --------------------------------
end
%%
% 3a. TOPUP data.
%%
disp("--Running coreg + MNI nomraliation pipeline on TOPUP corrected data + Perfusion images + Fields--");
%coreg_norm_pipeline(run_everything, EPI_applytopup_struct_array, EPI_applytopup_orf_struct_array, FLAIR_3D_struct_array, 'EPI_applytopup');
%run_everything = true;
EPI_struct_array = EPI_applytopup_struct_array;
EPI_field_struct_array = EPI_applytopup_orf_struct_array;
EPI_folder_name = 'EPI_applytopup';
EPI_corrected = true;
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    % 1. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    [FLAIR_3D_folder, FLAIR_3D_file_name, FLAIR_3D_file] = ...
        find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, ...
        FLAIR_3D_struct_array, EPI_folder_name, 'FLAIR_3D');
    
    if EPI_corrected
        field_struct_array = EPI_field_struct_array(i);
    
        field = strcat(field_struct_array.folder, '/', ...
            field_struct_array.name);
    end
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    if EPI_corrected
        disp(strcat('Loop ', int2str(i), ':', field));
    end
    
    disp(strcat('Loop ', int2str(i), ':', FLAIR_3D_file));
    
    % --------------------------------
    
    % --------------------------------
    
    % 2. Low res. (DSC first dynamic volume, src) -> low res. (FLAIR 3D, ref)
    % coregistration; estimate and reslice.
    
    % Flair 3D as ref file
    ref_file = FLAIR_3D_file;
    ref = strcat(ref_file, ',1');
    
    % First dynamic volume as src file.
    
    % Make a copy of the file to work on.
    src_file = strcat(DSC_file);
    src_file_copied = ...
        strcat(DSC_struct_array.folder, '/_coregest_', ...
        DSC_struct_array.name);
    
    if run_everything
        copyfile(src_file, src_file_copied);
    end
    
    src = strcat(src_file_copied, ',1');
    
    % Get the perfusion files
    DSC_file_name = DSC_struct_array.name;
    perfusion_dir_string = ...
        strcat(DSC_struct_array.folder, '/', ...
        DSC_file_name(1:length(DSC_file_name)-length('.nii')), '_perf');
    
    perfusion_struct_array = ...
        dir(strcat(perfusion_dir_string, '/*.nii'));
    
    % A list containing all files to reslice.
    if EPI_corrected
        to_reslice = ...
            cell(1, length(perfusion_struct_array)+1);
    else
        to_reslice = ...
            cell(1, length(perfusion_struct_array));
    end
    
    for j = 1:length(perfusion_struct_array)
        perfusion_maps_struct_array = ...
            perfusion_struct_array(j);
    
        perfusion_file = ...
            strcat(perfusion_maps_struct_array.folder, '/', ...
            perfusion_maps_struct_array.name);
    
        perfusion_file_copied = ...
            strcat(perfusion_maps_struct_array.folder, '/_coregest_', ...
            perfusion_maps_struct_array.name);
    
        if run_everything
            copyfile(perfusion_file, perfusion_file_copied);
        end
        to_reslice{j} = ...
            strcat(perfusion_file_copied, ',1');
    end
    
    if EPI_corrected
        % The off-resonance field (topup) or deformation field (epic)
        field_copied = ...
            strcat(field_struct_array.folder, '/_coregest_', ...
            field_struct_array.name);
    
        if run_everything
            copyfile(field, field_copied);
        end
        
        to_reslice{length(perfusion_struct_array)+1} = ...
            strcat(field_copied, ',1');
    
    end
    
    % Transpose. Necessary for matlabbatch .
    to_reslice = to_reslice';
    
    % other
    other = to_reslice;
    
    if run_everything
        %coreg_est_reslice_function(ref, src, other, 4); % 4.order b-spline interpolation
        coreg_est_reslice_function(ref, src, other, 1); % Trilinear interpolation
        %coreg_est_reslice_function(ref, src, other, 0); % Nearest
        %neighbour interpolation
    end
    
    % --------------------------------
    
    % --------------------------------
    
    % 3. Normalization into MNI space.
    % This creates a deformation field (y) for the flair.
    % The deformation field is then used to transform the coregistered
    % volumes (dsc first dynamic, topup/epic fields and perfusion maps) into MNI space.
    
    % 3a. Estimate deformation
    % space. Outputs (y_<flair file name>).
    
    nrun = 1; % enter the number of runs here
    jobfile = {'norm_est_job.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(0, nrun);
    
    flair = strcat(FLAIR_3D_folder, '/', FLAIR_3D_file_name);
    
    % Since the code is run in parallell, multiple threads should not
    % access the same file at the same location. However, they can
    % access the same file copied to different locations.
    
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
    flair_copied = strcat(DSC_struct_array.folder, '/', ...
        type, '_', FLAIR_3D_file_name);
    
    if run_everything
    
        copyfile(flair, flair_copied);
    
    end
    
    vol = strcat(flair_copied, ',1');
    
    inputs{1, nrun} = cellstr(vol);
    
    if run_everything
        % Run
        spm('defaults', 'FMRI');
        spm_jobman('run', jobs, inputs{:});
    end
    
    % 3b. Use estimated deformation field (y) to transform the relevant
    % volumes into MNI space (write).
    
    nrun = 1;
    jobfile = {'norm_write_job.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(2, nrun);
    
    % Estimated deformation field
    def = strcat(DSC_struct_array.folder, '/y_', ...
        type, '_', FLAIR_3D_file_name);
    
    inputs{1, 1} = cellstr(def);
    
    if EPI_corrected
        to_resample = cell(1, 1+length(perfusion_struct_array)+1);
    else
        to_resample = cell(1, 1+length(perfusion_struct_array));
    end 
    
    to_resample{1} = ...
        strcat(DSC_struct_array.folder, '/r_coregest_', ...
        DSC_struct_array.name, ',1');
    
    % Fill in the coregistered perfusion maps
    for j = 1:length(perfusion_struct_array)
        perfusion_maps_struct_array = ...
            perfusion_struct_array(j);
        
        pefusion_file_copied_coregistered = ...
            strcat(perfusion_maps_struct_array.folder, '/r_coregest_', ...
            perfusion_maps_struct_array.name);
    
        to_resample{1+j} = ...
            strcat(pefusion_file_copied_coregistered, ',1');
    end
    
    if EPI_corrected
        % The coregistered off-resonance field (topup) or deformation field (epic)
        to_resample{1+length(perfusion_struct_array)+1} = ...
            strcat(field_struct_array.folder, '/r_coregest_', ...
            field_struct_array.name, ',1');
    end
    
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
    
    % 4. Coreg reslice MNI regions file to perfusion MNI space
    % using estimated deformation field from 3a.
    
    % The file consisting brain regions in MNI space should be resliced
    % to perfusion MNI space so that pixel-perfect masking of brain 
    % regions can be done later on for instance rCBV.
    % However, unlinke the other resliced images in 2., this reslice should
    % use Nearest Neighbour interpolation to achieve pixel-perfect
    % masking of brain regions.
    
    % Image defining space; estimated deformation field from 3a.
    ref = strcat(DSC_struct_array.folder, '/y_', ...
        type, '_', FLAIR_3D_file_name, ',1');
    
    % A list containing all files to reslice.
    to_reslice = cell(1, 1);
    
    if run_everything
        % Determine of gradient echo (e1) or spin echo (e2).
        type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
        % Copy the regions file so that it can be resliced.
        regions_file_copied = strcat(DSC_struct_array.folder, '/_', ...
            type, '_labels_Neuromorphometrics.nii');
    
        copyfile(regions_file, regions_file_copied);
        
        % Add regions_file_copied to the to_reslice list.
        to_reslice{1} = strcat(regions_file_copied, ',1');
    end
    
    % Transpose. Necessary for matlabbatch .
    to_reslice = to_reslice';
    
    % other
    src = to_reslice;
    
    if run_everything
        coreg_reslice_function(ref, src, 0); % Nearest neighbour interpolation
    end
    % --------------------------------
end
%%
% 3a. EPIC data.
%%
disp("--Running coreg + MNI nomraliation pipeline on EPIC corrected data + Perfusion images + Fields--");
%coreg_norm_pipeline(run_everything, EPI_applyepic_struct_array, EPI_applyepic_df_struct_array, FLAIR_3D_struct_array, 'EPI_applyepic');
%run_everything = true;
EPI_struct_array = EPI_applyepic_struct_array;
EPI_field_struct_array = EPI_applyepic_df_struct_array;
EPI_folder_name = 'EPI_applyepic';
EPI_corrected = true;
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    % 1. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    [FLAIR_3D_folder, FLAIR_3D_file_name, FLAIR_3D_file] = ...
        find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, ...
        FLAIR_3D_struct_array, EPI_folder_name, 'FLAIR_3D');
    
    if EPI_corrected
        field_struct_array = EPI_field_struct_array(i);
    
        field = strcat(field_struct_array.folder, '/', ...
            field_struct_array.name);
    end
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    if EPI_corrected
        disp(strcat('Loop ', int2str(i), ':', field));
    end
    
    disp(strcat('Loop ', int2str(i), ':', FLAIR_3D_file));
    
    % --------------------------------
    
    % --------------------------------
    
    % 2. Low res. (DSC first dynamic volume, src) -> low res. (FLAIR 3D, ref)
    % coregistration; estimate and reslice.
    
    % Flair 3D as ref file
    ref_file = FLAIR_3D_file;
    ref = strcat(ref_file, ',1');
    
    % First dynamic volume as src file.
    
    % Make a copy of the file to work on.
    src_file = strcat(DSC_file);
    src_file_copied = ...
        strcat(DSC_struct_array.folder, '/_coregest_', ...
        DSC_struct_array.name);
    
    if run_everything
        copyfile(src_file, src_file_copied);
    end
    
    src = strcat(src_file_copied, ',1');
    
    % Get the perfusion files
    DSC_file_name = DSC_struct_array.name;
    perfusion_dir_string = ...
        strcat(DSC_struct_array.folder, '/', ...
        DSC_file_name(1:length(DSC_file_name)-length('.nii')), '_perf');
    
    perfusion_struct_array = ...
        dir(strcat(perfusion_dir_string, '/*.nii'));
    
    % A list containing all files to reslice.
    if EPI_corrected
        to_reslice = ...
            cell(1, length(perfusion_struct_array)+1);
    else
        to_reslice = ...
            cell(1, length(perfusion_struct_array));
    end
    
    for j = 1:length(perfusion_struct_array)
        perfusion_maps_struct_array = ...
            perfusion_struct_array(j);
    
        perfusion_file = ...
            strcat(perfusion_maps_struct_array.folder, '/', ...
            perfusion_maps_struct_array.name);
    
        perfusion_file_copied = ...
            strcat(perfusion_maps_struct_array.folder, '/_coregest_', ...
            perfusion_maps_struct_array.name);
    
        if run_everything
            copyfile(perfusion_file, perfusion_file_copied);
        end
        to_reslice{j} = ...
            strcat(perfusion_file_copied, ',1');
    end
    
    if EPI_corrected
        % The off-resonance field (topup) or deformation field (epic)
        field_copied = ...
            strcat(field_struct_array.folder, '/_coregest_', ...
            field_struct_array.name);
    
        if run_everything
            copyfile(field, field_copied);
        end
        
        to_reslice{length(perfusion_struct_array)+1} = ...
            strcat(field_copied, ',1');
    
    end
    
    % Transpose. Necessary for matlabbatch .
    to_reslice = to_reslice';
    
    % other
    other = to_reslice;
    
    if run_everything
        %coreg_est_reslice_function(ref, src, other, 4); % 4.order b-spline interpolation
        coreg_est_reslice_function(ref, src, other, 1); % Trilinear interpolation
        %coreg_est_reslice_function(ref, src, other, 0); % Nearest
        %neighbour interpolation
    end
    
    % --------------------------------
    
    % --------------------------------
    
    % 3. Normalization into MNI space.
    % This creates a deformation field (y) for the flair.
    % The deformation field is then used to transform the coregistered
    % volumes (dsc first dynamic, topup/epic fields and perfusion maps) into MNI space.
    
    % 3a. Estimate deformation
    % space. Outputs (y_<flair file name>).
    
    nrun = 1; % enter the number of runs here
    jobfile = {'norm_est_job.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(0, nrun);
    
    flair = strcat(FLAIR_3D_folder, '/', FLAIR_3D_file_name);
    
    % Since the code is run in parallell, multiple threads should not
    % access the same file at the same location. However, they can
    % access the same file copied to different locations.
    
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
    flair_copied = strcat(DSC_struct_array.folder, '/', ...
        type, '_', FLAIR_3D_file_name);
    
    if run_everything
    
        copyfile(flair, flair_copied);
    
    end
    
    vol = strcat(flair_copied, ',1');
    
    inputs{1, nrun} = cellstr(vol);
    
    if run_everything
        % Run
        spm('defaults', 'FMRI');
        spm_jobman('run', jobs, inputs{:});
    end
    
    % 3b. Use estimated deformation field (y) to transform the relevant
    % volumes into MNI space (write).
    
    nrun = 1;
    jobfile = {'norm_write_job.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(2, nrun);
    
    % Estimated deformation field
    def = strcat(DSC_struct_array.folder, '/y_', ...
        type, '_', FLAIR_3D_file_name);
    
    inputs{1, 1} = cellstr(def);
    
    if EPI_corrected
        to_resample = cell(1, 1+length(perfusion_struct_array)+1);
    else
        to_resample = cell(1, 1+length(perfusion_struct_array));
    end 
    
    to_resample{1} = ...
        strcat(DSC_struct_array.folder, '/r_coregest_', ...
        DSC_struct_array.name, ',1');
    
    % Fill in the coregistered perfusion maps
    for j = 1:length(perfusion_struct_array)
        perfusion_maps_struct_array = ...
            perfusion_struct_array(j);
        
        pefusion_file_copied_coregistered = ...
            strcat(perfusion_maps_struct_array.folder, '/r_coregest_', ...
            perfusion_maps_struct_array.name);
    
        to_resample{1+j} = ...
            strcat(pefusion_file_copied_coregistered, ',1');
    end
    
    if EPI_corrected
        % The coregistered off-resonance field (topup) or deformation field (epic)
        to_resample{1+length(perfusion_struct_array)+1} = ...
            strcat(field_struct_array.folder, '/r_coregest_', ...
            field_struct_array.name, ',1');
    end
    
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
    
    % 4. Coreg reslice MNI regions file to perfusion MNI space
    % using estimated deformation field from 3a.
    
    % The file consisting brain regions in MNI space should be resliced
    % to perfusion MNI space so that pixel-perfect masking of brain 
    % regions can be done later on for instance rCBV.
    % However, unlinke the other resliced images in 2., this reslice should
    % use Nearest Neighbour interpolation to achieve pixel-perfect
    % masking of brain regions.
    
    % Image defining space; estimated deformation field from 3a.
    ref = strcat(DSC_struct_array.folder, '/y_', ...
        type, '_', FLAIR_3D_file_name, ',1');
    
    % A list containing all files to reslice.
    to_reslice = cell(1, 1);
    
    if run_everything
        % Determine of gradient echo (e1) or spin echo (e2).
        type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
        % Copy the regions file so that it can be resliced.
        regions_file_copied = strcat(DSC_struct_array.folder, '/_', ...
            type, '_labels_Neuromorphometrics.nii');
    
        copyfile(regions_file, regions_file_copied);
        
        % Add regions_file_copied to the to_reslice list.
        to_reslice{1} = strcat(regions_file_copied, ',1');
    end
    
    % Transpose. Necessary for matlabbatch .
    to_reslice = to_reslice';
    
    % other
    src = to_reslice;
    
    if run_everything
        coreg_reslice_function(ref, src, 0); % Nearest neighbour interpolation
    end
    % --------------------------------
end
%%
disp("--coreg + MNI nomraliation pipeline finished--");
end
