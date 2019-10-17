function coreg_reslice_lrmerged_neurom(epi_corrections_out_dir)

% Note: This script is very specific on the output directory structure from the epi corrections pipeline.

% Run
% In Command Window
% epi_corrections_out_dir = '../../epi_corrections_out_2019_07_02';
% coreg_reslice_lrmerged_neurom(epi_corrections_out_dir);

% 1. Specify directories.
%%
% Multiple copies of this file will be resliced and saved to a separate file.
% NOTE: THIS NEEDS TO BE CHANGED
regions_file = '/media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections_out_2019_07_02/labels_Neuromorphometrics_lrmerged.nii';
%regions_file = strcat(epi_corrections_out_dir, '/labels_Neuromorphometrics_lrmerged.nii');

EPI_json_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_raw_DSC/**/*.json'));

EPI_applytopup_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applytopup/**/*applytopup_postp.nii'));
EPI_applytopup_struct_array = EPI_applytopup_struct_array(~contains({EPI_applytopup_struct_array.name}, 'coregest'));

EPI_applyepic_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/**/*applyepic.nii'));
EPI_applyepic_struct_array = EPI_applyepic_struct_array(~contains({EPI_applyepic_struct_array.name}, 'coregest'));

%MNI_region_maps_struct_array = dir(strcat(epi_corrections_out_dir, '/MNI_region_maps/*.nii'));

%%
% 2. Run settings.
%%

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
% - Coreg est : out : brain regions files in perfusion MNI space.

% Update: parfor parallelization did not allow to be run within a function,
% thus the code sadly needs to be replicated three times -> Use section
% folding.
%%
% 3a. Raw data.
%%
disp("--Running coreg reslice pipeline on raw data--");
%coreg_norm_pipeline(run_everything, EPI_struct_array, [], FLAIR_3D_struct_array, 'EPI_raw_DSC');
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_json_struct_array)
    % --------------------------------
    % 1. Get the files
    DSC_struct_array = EPI_json_struct_array(i);
    
    DSC_struct_array.name = strrep(DSC_struct_array.name, 'json','nii');
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    % --------------------------------
    
    % --------------------------------
    
    % 4. Coreg reslice MNI regions file to perfusion MNI space
    % using final first dynamic DSC file.
    
    % The file consisting brain regions in MNI space should be resliced
    % to perfusion MNI space so that pixel-perfect masking of brain 
    % regions can be done later on for instance rCBV.
    % However, unlinke the other resliced images in 2., this reslice should
    % use Nearest Neighbour interpolation to achieve pixel-perfect
    % masking of brain regions.
    
    % Image defining space.
    ref = ...
    strcat(DSC_struct_array.folder, '/wr_coregest_', ...
    DSC_struct_array.name, ',1');

    % A list containing all files to reslice.
    to_reslice = cell(1, 1);
    
    if run_everything
        % Determine of gradient echo (e1) or spin echo (e2).
        type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
        % Copy the regions file so that it can be resliced.
        regions_file_copied = strcat(DSC_struct_array.folder, '/_', ...
            type, '_labels_Neuromorphometrics_lrmerged.nii');
        
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
disp("--Running coreg reslice pipeline on TOPUP corrected data--");
%coreg_norm_pipeline(run_everything, EPI_applytopup_struct_array, EPI_applytopup_orf_struct_array, FLAIR_3D_struct_array, 'EPI_applytopup');
%run_everything = true;
EPI_struct_array = EPI_applytopup_struct_array;
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    % 1. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    % --------------------------------
    
    % --------------------------------
    
    % 4. Coreg reslice MNI regions file to perfusion MNI space
    % using final first dynamic DSC file.
    
    % The file consisting brain regions in MNI space should be resliced
    % to perfusion MNI space so that pixel-perfect masking of brain 
    % regions can be done later on for instance rCBV.
    % However, unlinke the other resliced images in 2., this reslice should
    % use Nearest Neighbour interpolation to achieve pixel-perfect
    % masking of brain regions.
    
    % Image defining space.
    ref = ...
    strcat(DSC_struct_array.folder, '/wr_coregest_', ...
    DSC_struct_array.name, ',1');

    % A list containing all files to reslice.
    to_reslice = cell(1, 1);
    
    if run_everything
        % Determine of gradient echo (e1) or spin echo (e2).
        type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
        % Copy the regions file so that it can be resliced.
        regions_file_copied = strcat(DSC_struct_array.folder, '/_', ...
            type, '_labels_Neuromorphometrics_lrmerged.nii');
    
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
disp("--Running coreg reslice pipeline on EPIC corrected data--");
%coreg_norm_pipeline(run_everything, EPI_applyepic_struct_array, EPI_applyepic_df_struct_array, FLAIR_3D_struct_array, 'EPI_applyepic');
%run_everything = true;
EPI_struct_array = EPI_applyepic_struct_array;
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    % --------------------------------
    % 1. Get the files
    DSC_struct_array = EPI_struct_array(i);
    
    DSC_file = strcat(DSC_struct_array.folder, '/', ...
        DSC_struct_array.name);
    
    disp(strcat('Loop ', int2str(i), ':', DSC_file));
    
    % --------------------------------
    
    % --------------------------------
    
    % 4. Coreg reslice MNI regions file to perfusion MNI space
    % using final first dynamic DSC file.
    
    % The file consisting brain regions in MNI space should be resliced
    % to perfusion MNI space so that pixel-perfect masking of brain 
    % regions can be done later on for instance rCBV.
    % However, unlinke the other resliced images in 2., this reslice should
    % use Nearest Neighbour interpolation to achieve pixel-perfect
    % masking of brain regions.
    
    % Image defining space.
    ref = ...
    strcat(DSC_struct_array.folder, '/wr_coregest_', ...
    DSC_struct_array.name, ',1');

    % A list containing all files to reslice.
    to_reslice = cell(1, 1);
    
    if run_everything
        % Determine of gradient echo (e1) or spin echo (e2).
        type = determine_e1_or_e2_DSC(DSC_struct_array.name);
    
        % Copy the regions file so that it can be resliced.
        regions_file_copied = strcat(DSC_struct_array.folder, '/_', ...
            type, '_labels_Neuromorphometrics_lrmerged.nii');
    
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
disp("--coreg reslice pipeline finished--");
end
