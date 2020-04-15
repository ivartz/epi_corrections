function coreg_native_template_and_warp_rois(epi_corrections_out_dir)

% Note: This script is very specific on the output directory structure from the epi corrections pipeline.

% 1. Specify directories.
%%
% Multiple copies of this file will be resliced and saved to a separate file.
% NOTE: THIS NEEDS TO BE CHANGED
epi_corrections_out_dir = '../../epi_corrections_out_2019_07_02_native';

template_file = '/media/loek/HDD3TB1/data/MNI152/mni_icbm152_lin_nifti/icbm_avg_152_t2_tal_lin.nii';

regions_file = strcat(epi_corrections_out_dir, '/labels_Neuromorphometrics_lrmerged.nii');

%here
EPI_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_raw_DSC/**/*.nii'));
EPI_struct_array = EPI_struct_array(~contains({EPI_struct_array.folder}, 'perf'));

%assignin('base', 'EPI_struct_array', EPI_struct_array);

%here
EPI_applytopup_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applytopup/**/*applytopup_postp.nii'));

%assignin('base', 'EPI_applytopup_struct_array', EPI_applytopup_struct_array);

%here
EPI_applyepic_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/**/*applyepic.nii'));

%assignin('base', 'EPI_applyepic_struct_array', EPI_applyepic_struct_array);

logfile = strcat(epi_corrections_out_dir, '/gtrunlog.txt');

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

% Update: parfor parallelization did not allow to be run within a function,
% thus the code sadly needs to be replicated three times -> Use section
% folding.
%%
% 3a. Raw data.
%%
disp("--Running coreg native template + ROI reslice pipeline on raw data");
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    
    % 1a. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    % --------------------------------
    
    % 1b. Determine gradient echo (e1) or spin echo (e2)
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    % The numvber of runs of each job call
    nrun = 1; % enter the number of runs here
    
    % -------------------------------
    
    % 2. High res. (T2 MNI152 template file, src) to low res. 
    % (DSC first dynamic volume, ref)
    % coregistration; estimate and reslice.
    
    % First dynamic DSC as ref file
    ref_file = DSC_file;
    ref = strcat(ref_file, ',1');
    
    % T2 MNI152 template as src file.
    
    % Make a copy of the file to work on.
    src_file = template_file;
    src_file_copied = ...
        strcat(DSC_struct_array.folder, '/', ...
        'gtrois_', type, '/icbm_avg_152_t2_tal_lin.nii');
    
    if run_everything
        mkdir(strcat(DSC_struct_array.folder, ...
            '/gtrois_', type));
        copyfile(src_file, src_file_copied);
    end
    
    src = strcat(src_file_copied, ',1');
    
    regions_file_copied= strcat(DSC_struct_array.folder, '/gtrois_', ...
        type, '/labels_Neuromorphometrics_lrmerged.nii');
    
    if run_everything
        copyfile(regions_file, regions_file_copied);
    end
    
    % The ROIs file and tumor segments file are taken in as other
    other = {
        regions_file_copied
        };

    if run_everything
        coreg_est_reslice_function(ref, src, other, 0); % Nearest
        %neighbour interpolation
    end
    
    % --------------------------------
    
    % Cleaning up, deleting files we don't need any more
    if run_everything
        disp('The following files will be deleted');
        disp(regions_file_copied);
        delete(regions_file_copied);
        disp(src_file_copied);
        delete(src_file_copied);
    end
    
	% --------------------------------
    
end
%%
% 3a. TOPUP data.
%%
disp("--Running coreg native template + ROI reslice pipeline on TOPUP corrected data");
EPI_struct_array = EPI_applytopup_struct_array;
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    
    % 1a. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    % --------------------------------
    
    % 1b. Determine gradient echo (e1) or spin echo (e2)
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    % The numvber of runs of each job call
    nrun = 1; % enter the number of runs here
    
    % -------------------------------
    
    % 2. High res. (T2 MNI152 template file, src) to low res. 
    % (DSC first dynamic volume, ref)
    % coregistration; estimate and reslice.
    
    % First dynamic DSC as ref file
    ref_file = DSC_file;
    ref = strcat(ref_file, ',1');
    
    % T2 MNI152 template as src file.
    
    % Make a copy of the file to work on.
    src_file = template_file;
    src_file_copied = ...
        strcat(DSC_struct_array.folder, '/', ...
        'gtrois_', type, '/icbm_avg_152_t2_tal_lin.nii');
    
    if run_everything
        mkdir(strcat(DSC_struct_array.folder, ...
            '/gtrois_', type));
        copyfile(src_file, src_file_copied);
    end
    
    src = strcat(src_file_copied, ',1');
    
    regions_file_copied= strcat(DSC_struct_array.folder, '/gtrois_', ...
        type, '/labels_Neuromorphometrics_lrmerged.nii');
    
    if run_everything
        copyfile(regions_file, regions_file_copied);
    end
    
    % The ROIs file and tumor segments file are taken in as other
    other = {
        regions_file_copied
        };

    if run_everything
        coreg_est_reslice_function(ref, src, other, 0); % Nearest
        %neighbour interpolation
    end
    
    % --------------------------------
    
    % Cleaning up, deleting files we don't need any more
    if run_everything
        disp('The following files will be deleted');
        disp(regions_file_copied);
        delete(regions_file_copied);
        disp(src_file_copied);
        delete(src_file_copied);
    end
    
	% --------------------------------
end
%%
% 3a. EPIC data.
%%
disp("--Running coreg native template + ROI reslice pipeline on EPIC corrected data");
EPI_struct_array = EPI_applyepic_struct_array;
% Code within parfor loop is equal to the code within the other parfor loops
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    
    % 1a. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    % --------------------------------
    
    % 1b. Determine gradient echo (e1) or spin echo (e2)
    type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    % The numvber of runs of each job call
    nrun = 1; % enter the number of runs here
    
    % -------------------------------
    
    % 2. High res. (T2 MNI152 template file, src) to low res. 
    % (DSC first dynamic volume, ref)
    % coregistration; estimate and reslice.
    
    % First dynamic DSC as ref file
    ref_file = DSC_file;
    ref = strcat(ref_file, ',1');
    
    % T2 MNI152 template as src file.
    
    % Make a copy of the file to work on.
    src_file = template_file;
    src_file_copied = ...
        strcat(DSC_struct_array.folder, '/', ...
        'gtrois_', type, '/icbm_avg_152_t2_tal_lin.nii');
    
    if run_everything
        mkdir(strcat(DSC_struct_array.folder, ...
            '/gtrois_', type));
        copyfile(src_file, src_file_copied);
    end
    
    src = strcat(src_file_copied, ',1');
    
    regions_file_copied= strcat(DSC_struct_array.folder, '/gtrois_', ...
        type, '/labels_Neuromorphometrics_lrmerged.nii');
    
    if run_everything
        copyfile(regions_file, regions_file_copied);
    end
    
    % The ROIs file and tumor segments file are taken in as other
    other = {
        regions_file_copied
        };

    if run_everything
        coreg_est_reslice_function(ref, src, other, 0); % Nearest
        %neighbour interpolation
    end
    
    % --------------------------------
    
    % Cleaning up, deleting files we don't need any more
    if run_everything
        disp('The following files will be deleted');
        disp(regions_file_copied);
        delete(regions_file_copied);
        disp(src_file_copied);
        delete(src_file_copied);
    end
    
	% --------------------------------
end
%%
disp("--coreg native template + ROI reslice pipeline finished--");
end