function compute_inverse(def, space, ofname, saveusr)
    %matlabbatch{1}.spm.util.defs.comp{1}.inv.comp{1}.inv.comp{1}.def = {'/media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections_out_2019_07_02_native/temp/y_e1_135702_WIP_FLAIR_3D_SENSE_401.nii'};
    %matlabbatch{1}.spm.util.defs.comp{1}.inv.space = {'/media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections_out_2019_07_02_native/temp/e1_135702_WIP_FLAIR_3D_SENSE_401.nii'};
    %matlabbatch{1}.spm.util.defs.out{1}.savedef.ofname = 'inv';
    %matlabbatch{1}.spm.util.defs.out{1}.savedef.savedir.saveusr = {'/media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections_out_2019_07_02_native/temp'};

    matlabbatch{1}.spm.util.defs.comp{1}.inv.comp{1}.def = {def};
    matlabbatch{1}.spm.util.defs.comp{1}.inv.space = {space};
    matlabbatch{1}.spm.util.defs.out{1}.savedef.ofname = ofname;
    matlabbatch{1}.spm.util.defs.out{1}.savedef.savedir.saveusr = {saveusr};
    
	spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);
end