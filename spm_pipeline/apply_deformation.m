function apply_deformation(def, fname, saveusr, prefix)

    %apply_deformation('y_inv_y_flair.nii', 'labels_Neuromorphometrics_lrmerged.nii','.')
    
    matlabbatch{1}.spm.util.defs.comp{1}.def = {def};
    matlabbatch{1}.spm.util.defs.out{1}.pull.fnames = {fname};
    matlabbatch{1}.spm.util.defs.out{1}.pull.savedir.saveusr = {saveusr};
    matlabbatch{1}.spm.util.defs.out{1}.pull.interp = 0; % Nearest neighbor interpolation
    matlabbatch{1}.spm.util.defs.out{1}.pull.mask = 1;
    matlabbatch{1}.spm.util.defs.out{1}.pull.fwhm = [0 0 0];
    matlabbatch{1}.spm.util.defs.out{1}.pull.prefix = prefix;
    
	spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);
end

