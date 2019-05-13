% Note: This script is very specific on the output directory structure from the 
% epi corrections pipeline.

epi_corrections_out_dir = '../../epi_corrections_out_2019_04_25_372114315';

FLAIR_3D_struct_array = dir(strcat(epi_corrections_out_dir, '/FLAIR_3D/*/*/*/*.nii'));

EPI_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_raw_DSC/*/*/*/*.nii'));

EPI_applytopup_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applytopup/*/*/*/*applytopup_postp.nii'));
EPI_applytopup_orf_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applytopup/*/*/*/*field_postp.nii'));

EPI_applyepic_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/*/*/*/*applyepic.nii'));
EPI_applyepic_df_struct_array = dir(strcat(epi_corrections_out_dir, '/EPI_applyepic/*/*/*/*field_e*.nii'));

%MNI_region_maps_struct_array = dir(strcat(epi_corrections_out_dir, '/MNI_region_maps/*.nii'));

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
 
% Low res -> High res coreg est reslice : out: upsampled first dynamic
% DSC
% Normalize est : out: deformation field
% Normalize write : out: DSC first dynamic + topup/epic field +
% perfusion maps in MNI space

disp("----");
coreg_norm_pipeline(run_everything, EPI_struct_array, [], FLAIR_3D_struct_array, 'EPI_raw_DSC');
disp("----");
coreg_norm_pipeline(run_everything, EPI_applytopup_struct_array, EPI_applytopup_orf_struct_array, FLAIR_3D_struct_array, 'EPI_applytopup');
disp("----");
coreg_norm_pipeline(run_everything, EPI_applyepic_struct_array, EPI_applyepic_df_struct_array, FLAIR_3D_struct_array, 'EPI_applyepic');
disp("----");

% Todo:
% Log rank of roi histograms

% watershed plot