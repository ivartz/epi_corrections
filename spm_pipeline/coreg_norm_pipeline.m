function coreg_norm_pipeline(run_everything, EPI_struct_array, EPI_field_struct_array, FLAIR_3D_struct_array, EPI_folder_name)

    % Low res -> High res coreg est reslice : out: upsampled first dynamic
    % DSC
    % Normalize est : out: deformation field
    % Normalize write : out: DSC first dynamic + topup/epic field +
    % perfusion maps in MNI space

    EPI_corrected = false;
    if strcmp(EPI_folder_name, 'EPI_applytopup') || strcmp(EPI_folder_name, 'EPI_applyepic')
        EPI_corrected = true;        
    end
    
    %for i = 1:length(EPI_struct_array)-1
    for i = 1:length(EPI_struct_array)
        
        % --------------------------------
        % 1. Get the files
        DSC_struct_array = EPI_struct_array(i);
        DSC_file = strcat(DSC_struct_array.folder, '/', DSC_struct_array.name);

        [FLAIR_3D_folder, FLAIR_3D_file_name, FLAIR_3D_file] = find_corresponding_flair_3d_file_for_dsc(DSC_struct_array, FLAIR_3D_struct_array, EPI_folder_name, 'FLAIR_3D');

        if EPI_corrected
            field_struct_array = EPI_field_struct_array(i);
            field = strcat(field_struct_array.folder, '/', field_struct_array.name);
        end

        DSC_header = spm_vol(DSC_file);
        num_dyn = length(DSC_header);

        disp(DSC_file);
        if EPI_corrected
            disp(field);
        end
        %disp(FLAIR_3D_folder);
        %disp(FLAIR_3D_file_name);
        disp(FLAIR_3D_file);

        % --------------------------------
        
        % --------------------------------

        % 2. Low res. (DSC first dynamic volume, src) -> low res. (FLAIR 3D, ref)
        % coregistration; estimate and reslice.

        % Flair 3D as ref file
        ref_file = FLAIR_3D_file;
        ref = strcat(ref_file, ',1');
        
        % First dynamic volume as src file
        % Make a copy of the file to work on        
        src_file = strcat(DSC_file);
        src_file_copied = strcat(DSC_struct_array.folder, '/_coregest_', DSC_struct_array.name);
        if run_everything
            copyfile(src_file, src_file_copied);
        end
        src = strcat(src_file_copied, ',1');
        
        to_reslice = {};
        
        % Fill in the perfusion maps
        DSC_file_name = DSC_struct_array.name;
        perfusion_dir_string = strcat(DSC_struct_array.folder, '/', DSC_file_name(1:length(DSC_file_name)-length('.nii')), '_perf');
        perfusion_struct_array = dir(strcat(perfusion_dir_string, '/*.nii'));
        for j = 1:length(perfusion_struct_array)
            perfusion_maps_struct_array = perfusion_struct_array(j);
            perfusion_file = strcat(perfusion_maps_struct_array.folder, '/', perfusion_maps_struct_array.name);
            perfusion_file_copied = strcat(perfusion_maps_struct_array.folder, '/_coregest_', perfusion_maps_struct_array.name);
            if run_everything
                copyfile(perfusion_file, perfusion_file_copied);
            end
            to_reslice{end+1} = strcat(perfusion_file_copied, ',1');
        end
        
        if EPI_corrected
            % The off-resonance field (topup) or deformation field (epic)
            %src_file = strcat(DSC_file);
            field_copied = strcat(field_struct_array.folder, '/_coregest_', field_struct_array.name);
            if run_everything
                copyfile(field, field_copied);
            end
            to_reslice{end+1} = strcat(field_copied, ',1');
        end
        
        % transpose
        to_reslice = to_reslice';
        
        % other
        other = to_reslice;
        
        if run_everything
            coreg_est_reslice_function(ref, src, other, 4); % 4.order b-spline interpolation
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
        vol = strcat(FLAIR_3D_folder, '/', FLAIR_3D_file_name, ',1');
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
        def = strcat(FLAIR_3D_folder, '/y_', FLAIR_3D_file_name);
        inputs{1, 1} = cellstr(def);
        
        to_resample = {};

        to_resample{end+1} = strcat(DSC_struct_array.folder, '/r_coregest_', DSC_struct_array.name, ',1');
        
        % Fill in the coregistered perfusion maps
        for j = 1:length(perfusion_struct_array)
            perfusion_maps_struct_array = perfusion_struct_array(j);
            pefusion_file_copied_coregistered = strcat(perfusion_maps_struct_array.folder, '/r_coregest_', perfusion_maps_struct_array.name);
            to_resample{end+1} = strcat(pefusion_file_copied_coregistered, ',1');
        end
        
        if EPI_corrected
            % The coregistered off-resonance field (topup) or deformation field (epic)
            to_resample{end+1} = strcat(field_struct_array.folder, '/r_coregest_', field_struct_array.name, ',1');
        end
        
        % transpose
        to_resample = to_resample';
        
        % images to write
        inputs{2, 1} = cellstr(to_resample);
        
        if run_everything
            spm('defaults', 'FMRI');
            spm_jobman('run', jobs, inputs{:});
            
            % Copy over useful flair files to epi directories to save them
            % (they will be overwritten in the next for loop)
            type = determine_e1_or_e2_DSC(DSC_struct_array.name);
            
            FLAIR_3D_deformation_file = strcat(FLAIR_3D_folder, '/y_', FLAIR_3D_file_name);
            FLAIR_3D_deformation_file_copied = strcat(DSC_struct_array.folder, '/y_', type, '_', FLAIR_3D_file_name);
            copyfile(FLAIR_3D_deformation_file, FLAIR_3D_deformation_file_copied);
        end

        % --------------------------------
    end
end