function compute_inverse(def, space, ofname, saveusr)

    %compute_inverse('y_flair.nii', 'flair.nii', 'inv_y_flair', '.')
    
    matlabbatch{1}.spm.util.defs.comp{1}.inv.comp{1}.def = {def};
    matlabbatch{1}.spm.util.defs.comp{1}.inv.space = {space};
    matlabbatch{1}.spm.util.defs.out{1}.savedef.ofname = ofname;
    matlabbatch{1}.spm.util.defs.out{1}.savedef.savedir.saveusr = {saveusr};
    
	spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);
end