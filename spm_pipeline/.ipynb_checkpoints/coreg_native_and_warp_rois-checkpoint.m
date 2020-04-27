function coreg_native_and_warp_rois(epi_corrections_out_dir)

% Note: This script is very specific on the output directory structure from the epi corrections pipeline.

% 1. Specify directories.
%%
% Multiple copies of this file will be resliced and saved to a separate file.
% NOTE: THIS NEEDS TO BE CHANGED
epi_corrections_out_dir = '../../epi_corrections_out_2019_07_02_native';

%regions_file = '/media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections_out_2019_07_02_native/labels_Neuromorphometrics_lrmerged.nii';

regions_file = strcat(epi_corrections_out_dir, '/labels_Neuromorphometrics_lrmerged.nii');

onco_dir = strcat(epi_corrections_out_dir, '/ONCOHabitats_tumor_segments_from_flair_native');

%here
FLAIR_3D_struct_array = dir(strcat(epi_corrections_out_dir, '/FLAIR_3D/**/*.nii'));

%here
EPI_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_raw_DSC/**/*.nii'));
EPI_struct_array = EPI_struct_array(~contains({EPI_struct_array.folder}, 'perf'));

%here
EPI_applytopup_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applytopup/**/*applytopup_postp.nii'));

%here
EPI_applyepic_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/**/*applyepic.nii'));

tumor_segments_struct_array = dir(strcat(epi_corrections_out_dir, ...
    '/ONCOHabitats_tumor_segments_from_flair_native/**/results/native/Segmentation_Flair_space.nii'));

logfile = strcat(epi_corrections_out_dir, '/runlog.txt');

diary off;
if (exist(logfile, 'file'))
    delete(logfile);
end
%diary on;
diary(logfile);

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
     %return;
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

% Update: parfor parallelization did not allow to be run within a function,
% thus the code sadly needs to be replicated three times -> Use section
% folding.
%%
% 3a. Raw data.
%%
disp("--Running coreg + ROI warp pipeline on raw data");
%coreg_norm_pipeline(run_everything, EPI_struct_array, [], FLAIR_3D_struct_array, 'EPI_raw_DSC');
EPI_folder_name = 'EPI_raw_DSC';
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    
    % 1a. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    [~, FLAIR_3D_file_name, FLAIR_3D_file] = ...
        find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, ...
        FLAIR_3D_struct_array, EPI_folder_name, 'FLAIR_3D');
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    disp(strcat('Loop ', int2str(i), ':', FLAIR_3D_file));
    
    % --------------------------------
    
    % 1b. Determine gradient echo (e1) or spin echo (e2)
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    % The numvber of runs of each job call
    nrun = 1; % enter the number of runs here
    
    % -------------------------------
    
    % 2. Estimate the warping of native Flair into MNI space.
    % This creates a deformation field (y) for the flair
    % Outputs (y_<flair file name>).
    
    jobfile = {'norm_est_job.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(1, nrun);
    
    % Since the code is run in parallell, multiple threads should not
    % access the same file at the same location. However, they can
    % access the same file copied to different locations
    
    flair_copied = strcat(DSC_struct_array.folder, '/', ...
        type, '_', FLAIR_3D_file_name);
    
    vol = strcat(flair_copied, ',1');
    
    inputs{1, nrun} = cellstr(vol);
    
    if run_everything
        % Copy
        copyfile(FLAIR_3D_file, flair_copied);
        % Run
        spm('defaults', 'FMRI');
        spm_jobman('run', jobs, inputs{:});
    end
    
    % --------------------------------    
    
    % 3. Invert the deformation field so that it can later be used to 
    % to transform MNI ROIs into native Flair space
    
    % The deformation field from the MNI normalization, estimate step
    def = strcat(DSC_struct_array.folder, '/y_', ...
        type, '_', FLAIR_3D_file_name);
    
    % The space in which to take the inverse is the original Flair
    space = flair_copied;
    
    % The file name of the inverted deformation
    def_inv_fname = strcat('inverse_y_', ...
        type, '_', FLAIR_3D_file_name);
    
    % The directory to save the inverted file
    savedir = DSC_struct_array.folder;
    
    if run_everything
        % Run
        compute_inverse(def, space, def_inv_fname, savedir);
    end
    
    % --------------------------------
    
    % 4. Apply the inverse deformation on the ROIs,
    % creating ROIs in native Flair space
    
    % The inverted deformation file
    def_inv = strcat(DSC_struct_array.folder, '/y_', def_inv_fname);
    
    % The ROIs in MNI space
    % Copy the MNI regions file to the correct DSC dir
    regions_file_copied = strcat(DSC_struct_array.folder, '/_', ...
        type, '_labels_Neuromorphometrics_lrmerged.nii');
    
    % The directory to save the ROIs in native Flair space
    savedir = DSC_struct_array.folder;
    
    if run_everything
        % Copy
        copyfile(regions_file, regions_file_copied);
        % Run
        apply_inverse(def_inv, regions_file_copied, savedir);
    end
    
    % 5. High res. (FLAIR 3D, src) to low res. (DSC first dynamic volume, ref)
    % coregistration; estimate and reslice.
    
    % First dynamic DSC as ref file
    ref_file = DSC_file;
    ref = strcat(ref_file, ',1');
    
    % Flair as src file.
    
    % Make a copy of the file to work on.
    src_file = flair_copied;
    src_file_copied = ...
        strcat(DSC_struct_array.folder, '/_coregest_', ...
        type, '_', FLAIR_3D_file_name);
    
    if run_everything
        copyfile(src_file, src_file_copied);
    end
    
    src = strcat(src_file_copied, ',1');
    
    regions_file_copied_warped = strcat(DSC_struct_array.folder, '/yinvapplied_', ...
        type, '_labels_Neuromorphometrics_lrmerged.nii');
    
    % Find corresponding segments file
    [~, ~, tumor_segments_file] = ...
        find_corresponding_native_flair_tumor_segments_file_for_DSC(DSC_file, onco_dir, tumor_segments_struct_array)
    
    disp(strcat('Loop ', int2str(i), ':', tumor_segments_file));
    
    tumor_segments_file_copied = ...
        strcat(DSC_struct_array.folder, ...
        '/', type, '_tumor_segments.nii');
    
    if run_everything
        copyfile(tumor_segments_file, tumor_segments_file_copied);
    end
    
    % The ROIs file and tumor segments file are taken in as other
    other = {
        tumor_segments_file_copied
        regions_file_copied_warped
        };

    if run_everything
        %coreg_est_reslice_function(ref, src, other, 4); % 4.order b-spline interpolation
        %coreg_est_reslice_function(ref, src, other, 1); % Trilinear interpolation
        coreg_est_reslice_function(ref, src, other, 0); % Nearest
        %neighbour interpolation
    end
    
    % --------------------------------
    
    % Cleaning up, deleting files we don't need any more
    if run_everything
        disp('The following files will be deleted');
        disp(tumor_segments_file_copied);
        delete(tumor_segments_file_copied);
        disp(src_file_copied);
        delete(src_file_copied);
        disp(regions_file_copied);
        delete(regions_file_copied);
        disp(def_inv);
        delete(def_inv);
        disp(def);
        delete(def);
        disp(flair_copied);
        delete(flair_copied);
    end
    
	% --------------------------------
    
end
%%
% 3a. TOPUP data.
%%
disp("--Running coreg + ROI warp pipeline on TOPUP corrected data");
%coreg_norm_pipeline(run_everything, EPI_applytopup_struct_array, EPI_applytopup_orf_struct_array, FLAIR_3D_struct_array, 'EPI_applytopup');
EPI_struct_array = EPI_applytopup_struct_array;
EPI_folder_name = 'EPI_applytopup';
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    
    % 1a. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    [~, FLAIR_3D_file_name, FLAIR_3D_file] = ...
        find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, ...
        FLAIR_3D_struct_array, EPI_folder_name, 'FLAIR_3D');
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    disp(strcat('Loop ', int2str(i), ':', FLAIR_3D_file));
    
    % --------------------------------
    
    % 1b. Determine gradient echo (e1) or spin echo (e2)
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    % The numvber of runs of each job call
    nrun = 1; % enter the number of runs here
    
    % -------------------------------
    
    % 2. Estimate the warping of native Flair into MNI space.
    % This creates a deformation field (y) for the flair
    % Outputs (y_<flair file name>).
    
    jobfile = {'norm_est_job.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(1, nrun);
    
    % Since the code is run in parallell, multiple threads should not
    % access the same file at the same location. However, they can
    % access the same file copied to different locations
    
    flair_copied = strcat(DSC_struct_array.folder, '/', ...
        type, '_', FLAIR_3D_file_name);
    
    vol = strcat(flair_copied, ',1');
    
    inputs{1, nrun} = cellstr(vol);
    
    if run_everything
        % Copy
        copyfile(FLAIR_3D_file, flair_copied);
        % Run
        spm('defaults', 'FMRI');
        spm_jobman('run', jobs, inputs{:});
    end
    
    % --------------------------------    
    
    % 3. Invert the deformation field so that it can later be used to 
    % to transform MNI ROIs into native Flair space
    
    % The deformation field from the MNI normalization, estimate step
    def = strcat(DSC_struct_array.folder, '/y_', ...
        type, '_', FLAIR_3D_file_name);
    
    % The space in which to take the inverse is the original Flair
    space = flair_copied;
    
    % The file name of the inverted deformation
    def_inv_fname = strcat('inverse_y_', ...
        type, '_', FLAIR_3D_file_name);
    
    % The directory to save the inverted file
    savedir = DSC_struct_array.folder;
    
    if run_everything
        % Run
        compute_inverse(def, space, def_inv_fname, savedir);
    end
    
    % --------------------------------
    
    % 4. Apply the inverse deformation on the ROIs,
    % creating ROIs in native Flair space
    
    % The inverted deformation file
    def_inv = strcat(DSC_struct_array.folder, '/y_', def_inv_fname);
    
    % The ROIs in MNI space
    % Copy the MNI regions file to the correct DSC dir
    regions_file_copied = strcat(DSC_struct_array.folder, '/_', ...
        type, '_labels_Neuromorphometrics_lrmerged.nii');
    
    % The directory to save the ROIs in native Flair space
    savedir = DSC_struct_array.folder;
    
    if run_everything
        % Copy
        copyfile(regions_file, regions_file_copied);
        % Run
        apply_inverse(def_inv, regions_file_copied, savedir);
    end
    
    % 5. High res. (FLAIR 3D, src) to low res. (DSC first dynamic volume, ref)
    % coregistration; estimate and reslice.
    
    % First dynamic DSC as ref file
    ref_file = DSC_file;
    ref = strcat(ref_file, ',1');
    
    % Flair as src file.
    
    % Make a copy of the file to work on.
    src_file = flair_copied;
    src_file_copied = ...
        strcat(DSC_struct_array.folder, '/_coregest_', ...
        type, '_', FLAIR_3D_file_name);
    
    if run_everything
        copyfile(src_file, src_file_copied);
    end
    
    src = strcat(src_file_copied, ',1');
    
    regions_file_copied_warped = strcat(DSC_struct_array.folder, '/yinvapplied_', ...
        type, '_labels_Neuromorphometrics_lrmerged.nii');
    
    % Find corresponding segments file
    [~, ~, tumor_segments_file] = ...
        find_corresponding_native_flair_tumor_segments_file_for_DSC(DSC_file, onco_dir, tumor_segments_struct_array)
    
    disp(strcat('Loop ', int2str(i), ':', tumor_segments_file));
    
    tumor_segments_file_copied = ...
        strcat(DSC_struct_array.folder, ...
        '/', type, '_tumor_segments.nii');
    
    if run_everything
        copyfile(tumor_segments_file, tumor_segments_file_copied);
    end
    
    % The ROIs file and tumor segments file are taken in as other
    other = {
        tumor_segments_file_copied
        regions_file_copied_warped
        };

    if run_everything
        %coreg_est_reslice_function(ref, src, other, 4); % 4.order b-spline interpolation
        %coreg_est_reslice_function(ref, src, other, 1); % Trilinear interpolation
        coreg_est_reslice_function(ref, src, other, 0); % Nearest
        %neighbour interpolation
    end
    
    % --------------------------------
    
    % Cleaning up, deleting files we don't need any more
    if run_everything
        disp('The following files will be deleted');
        disp(tumor_segments_file_copied);
        delete(tumor_segments_file_copied);
        disp(src_file_copied);
        delete(src_file_copied);
        disp(regions_file_copied);
        delete(regions_file_copied);
        disp(def_inv);
        delete(def_inv);
        disp(def);
        delete(def);
        disp(flair_copied);
        delete(flair_copied);
    end
    
	% --------------------------------
    
end
%%
% 3a. EPIC data.
%%
disp("--Running coreg + ROI warp pipeline on EPIC corrected data");
EPI_struct_array = EPI_applyepic_struct_array;
EPI_folder_name = 'EPI_applyepic';
% Code within parfor loop is equal to the code within the other parfor loops
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    
    % 1a. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    [~, FLAIR_3D_file_name, FLAIR_3D_file] = ...
        find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, ...
        FLAIR_3D_struct_array, EPI_folder_name, 'FLAIR_3D');
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    disp(strcat('Loop ', int2str(i), ':', FLAIR_3D_file));
    
    % --------------------------------
    
    % 1b. Determine gradient echo (e1) or spin echo (e2)
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    % The numvber of runs of each job call
    nrun = 1; % enter the number of runs here
    
    % -------------------------------
    
    % 2. Estimate the warping of native Flair into MNI space.
    % This creates a deformation field (y) for the flair
    % Outputs (y_<flair file name>).
    
    jobfile = {'norm_est_job.m'};
    jobs = repmat(jobfile, 1, nrun);
    inputs = cell(1, nrun);
    
    % Since the code is run in parallell, multiple threads should not
    % access the same file at the same location. However, they can
    % access the same file copied to different locations
    
    flair_copied = strcat(DSC_struct_array.folder, '/', ...
        type, '_', FLAIR_3D_file_name);
    
    vol = strcat(flair_copied, ',1');
    
    inputs{1, nrun} = cellstr(vol);
    
    if run_everything
        % Copy
        copyfile(FLAIR_3D_file, flair_copied);
        % Run
        spm('defaults', 'FMRI');
        spm_jobman('run', jobs, inputs{:});
    end
    
    % --------------------------------    
    
    % 3. Invert the deformation field so that it can later be used to 
    % to transform MNI ROIs into native Flair space
    
    % The deformation field from the MNI normalization, estimate step
    def = strcat(DSC_struct_array.folder, '/y_', ...
        type, '_', FLAIR_3D_file_name);
    
    % The space in which to take the inverse is the original Flair
    space = flair_copied;
    
    % The file name of the inverted deformation
    def_inv_fname = strcat('inverse_y_', ...
        type, '_', FLAIR_3D_file_name);
    
    % The directory to save the inverted file
    savedir = DSC_struct_array.folder;
    
    if run_everything
        % Run
        compute_inverse(def, space, def_inv_fname, savedir);
    end
    
    % --------------------------------
    
    % 4. Apply the inverse deformation on the ROIs,
    % creating ROIs in native Flair space
    
    % The inverted deformation file
    def_inv = strcat(DSC_struct_array.folder, '/y_', def_inv_fname);
    
    % The ROIs in MNI space
    % Copy the MNI regions file to the correct DSC dir
    regions_file_copied = strcat(DSC_struct_array.folder, '/_', ...
        type, '_labels_Neuromorphometrics_lrmerged.nii');
    
    % The directory to save the ROIs in native Flair space
    savedir = DSC_struct_array.folder;
    
    if run_everything
        % Copy
        copyfile(regions_file, regions_file_copied);
        % Run
        apply_inverse(def_inv, regions_file_copied, savedir);
    end
    
    % 5. High res. (FLAIR 3D, src) to low res. (DSC first dynamic volume, ref)
    % coregistration; estimate and reslice.
    
    % First dynamic DSC as ref file
    ref_file = DSC_file;
    ref = strcat(ref_file, ',1');
    
    % Flair as src file.
    
    % Make a copy of the file to work on.
    src_file = flair_copied;
    src_file_copied = ...
        strcat(DSC_struct_array.folder, '/_coregest_', ...
        type, '_', FLAIR_3D_file_name);
    
    if run_everything
        copyfile(src_file, src_file_copied);
    end
    
    src = strcat(src_file_copied, ',1');
    
    regions_file_copied_warped = strcat(DSC_struct_array.folder, '/yinvapplied_', ...
        type, '_labels_Neuromorphometrics_lrmerged.nii');
    
    % Find corresponding segments file
    [~, ~, tumor_segments_file] = ...
        find_corresponding_native_flair_tumor_segments_file_for_DSC(DSC_file, onco_dir, tumor_segments_struct_array)
    
    disp(strcat('Loop ', int2str(i), ':', tumor_segments_file));
    
    tumor_segments_file_copied = ...
        strcat(DSC_struct_array.folder, ...
        '/', type, '_tumor_segments.nii');
    
    if run_everything
        copyfile(tumor_segments_file, tumor_segments_file_copied);
    end
    
    % The ROIs file and tumor segments file are taken in as other
    other = {
        tumor_segments_file_copied
        regions_file_copied_warped
        };

    if run_everything
        %coreg_est_reslice_function(ref, src, other, 4); % 4.order b-spline interpolation
        %coreg_est_reslice_function(ref, src, other, 1); % Trilinear interpolation
        coreg_est_reslice_function(ref, src, other, 0); % Nearest
        %neighbour interpolation
    end
    
    % --------------------------------
    
    % Cleaning up, deleting files we don't need any more
    if run_everything
        disp('The following files will be deleted');
        disp(tumor_segments_file_copied);
        delete(tumor_segments_file_copied);
        disp(src_file_copied);
        delete(src_file_copied);
        disp(regions_file_copied);
        delete(regions_file_copied);
        disp(def_inv);
        delete(def_inv);
        disp(def);
        delete(def);
        disp(flair_copied);
        delete(flair_copied);
    end
    
	% --------------------------------
    
end
%%
disp("--coreg + ROI warp pipeline finished--");
end
