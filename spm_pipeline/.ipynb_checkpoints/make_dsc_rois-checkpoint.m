function make_dsc_rois(epi_corrections_out_dir)
% 1. Specify directories.
%%
% Dataset directory
%epi_corrections_out_dir = '../../epi_corrections_out_2019_07_02_native';

% T2-FLAIR
FLAIR_3D_struct_array = ...
    dir(strcat(epi_corrections_out_dir, '/FLAIR_3D/**/*.nii'));

% Uncorrected DSC and rCBV
EPI_struct_array = ...
    dir(strcat(epi_corrections_out_dir, '/EPI_raw_DSC/**/*.nii'));
EPI_struct_array = ...
    EPI_struct_array(~contains({EPI_struct_array.folder}, 'perf'));

% TOPUP corrected DSC and rCBV
EPI_applytopup_struct_array = dir(strcat(epi_corrections_out_dir, ...
    '/EPI_applytopup/**/*applytopup_postp.nii'));

% EPIC corrected DSC and rCBV
EPI_applyepic_struct_array = ...
    dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/**/*applyepic.nii'));

% Custom made brain regions file in MNI space: Left and right parts merged
regions_file = strcat(epi_corrections_out_dir, '/mniregions.nii');

% Tumor segments (necrotic, enhancing and edema) in T2-FLAIR and MNI space
onco_dir = strcat(epi_corrections_out_dir, ...
    '/ONCOHabitats');

mni_tumor_segments_struct_array = dir(strcat(onco_dir, ...
    '/**/results/mni/Segmentation.nii'));

flair_tumor_segments_struct_array = dir(strcat(onco_dir, ...
    '/**/results/native/Segmentation_Flair_space.nii'));

% File for logging this script
logfile = strcat(epi_corrections_out_dir, '/makedscroisrunlog.txt');

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
valid_check = {length({EPI_struct_array.name})/2 == ...
    length({EPI_applytopup_struct_array.name})/2 , ...
    length({EPI_struct_array.name})/2 == ...
    length({EPI_applyepic_struct_array.name})/2};
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
disp("--Running pipeline for uncorrected data----");
%coreg_norm_pipeline(run_everything, EPI_struct_array, [], FLAIR_3D_struct_array, 'EPI_raw_DSC');
EPI_folder_name = 'EPI_raw_DSC';
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    run_make_dsc_rois_subject(i, ...
        EPI_struct_array, ...
        EPI_folder_name, ...
        onco_dir, ...
        mni_tumor_segments_struct_array, ...
        flair_tumor_segments_struct_array, ...
        FLAIR_3D_struct_array, ...
        regions_file, ...
        run_everything)
%     % 1. Get the files
%     % DSC
%     DSC_struct_array = EPI_struct_array(i);
%     DSC_file = strcat(DSC_struct_array.folder, '/', ...
%         DSC_struct_array.name);
%     
%     % Tumor regions in MNI space
%     [~, ~, mni_tumor_segments_file] = ...
%         find_corresponding_tumor_segments_file_for_DSC(DSC_file, onco_dir, mni_tumor_segments_struct_array);
%     
%     % Tumor regions in FLAIR space
%     [~, ~, flair_tumor_segments_file] = ...
%         find_corresponding_tumor_segments_file_for_DSC(DSC_file, onco_dir, flair_tumor_segments_struct_array);
%     
%     % FLAIR
%     [~, ~, FLAIR_3D_file] = ...
%         find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, ...
%         FLAIR_3D_struct_array, EPI_folder_name, 'FLAIR_3D');
%     
%     disp(strcat('Loop ', int2str(i), ':', DSC_file));
%     disp(strcat('Loop ', int2str(i), ':', mni_tumor_segments_file));
%     disp(strcat('Loop ', int2str(i), ':', flair_tumor_segments_file));
%     disp(strcat('Loop ', int2str(i), ':', FLAIR_3D_file));
%     
%     % 2. Determine gradient echo (e1) or spin echo (e2) DSC
%     type = determine_e1_or_e2_DSC(DSC_struct_array.name);
%     
%     disp(strcat('Loop ', int2str(i), ': DSC type: ', type));
%     
%     % 3. Make not ground truth brain and tumor regions
%     % (using tumor rois in mni space)
%     if run_everything
%         make_dsc_rois_subject(type, DSC_file, regions_file, mni_tumor_segments_file);
%     end
%     
%     % 4. Make ground truth brain and tumor regions
%     % (using tumor rois in flair space)
%     if run_everything
%         make_gt_dsc_rois_subject(type, DSC_file, FLAIR_3D_file, regions_file, flair_tumor_segments_file);
%     end    
end
%%
% 3b. TOPUP data.
%%
disp("--Running pipeline for TOPUP corrected data----");
%coreg_norm_pipeline(run_everything, EPI_applytopup_struct_array, EPI_applytopup_orf_struct_array, FLAIR_3D_struct_array, 'EPI_applytopup');
EPI_struct_array = EPI_applytopup_struct_array;
EPI_folder_name = 'EPI_applytopup';
% Code within parfor loop is equal to the code within the other parfor loops.
parfor i = 1:length(EPI_struct_array)
    run_make_dsc_rois_subject(i, ...
        EPI_struct_array, ...
        EPI_folder_name, ...
        onco_dir, ...
        mni_tumor_segments_struct_array, ...
        flair_tumor_segments_struct_array, ...
        FLAIR_3D_struct_array, ...
        regions_file, ...
        run_everything)
end
%%
% 3c. EPIC data.
%%
disp("--Running pipeline for EPIC corrected data----");
EPI_struct_array = EPI_applyepic_struct_array;
EPI_folder_name = 'EPI_applyepic';
% Code within parfor loop is equal to the code within the other parfor loops
parfor i = 1:length(EPI_struct_array)
    run_make_dsc_rois_subject(i, ...
        EPI_struct_array, ...
        EPI_folder_name, ...
        onco_dir, ...
        mni_tumor_segments_struct_array, ...
        flair_tumor_segments_struct_array, ...
        FLAIR_3D_struct_array, ...
        regions_file, ...
        run_everything)
end
%%
disp("----Pipeline finished----");
end
