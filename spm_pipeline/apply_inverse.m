function apply_inverse(def, fname, saveusr)
    %matlabbatch{4}.spm.util.defs.comp{1}.def = {'F:\Elastografi\Friske frivillige\FRIV041\Analyse\Skann1\y_deform_MNI2Skann1.nii'};
    %matlabbatch{4}.spm.util.defs.out{1}.pull.fnames = {'C:\Users\Siri\OneDrive\FORCE\SPM\GM-kart\Accumbens.nii'};
    %matlabbatch{4}.spm.util.defs.out{1}.pull.savedir.saveusr = {'F:\Elastografi\Friske frivillige\FRIV041\Analyse\Skann1'};
    %matlabbatch{4}.spm.util.defs.out{1}.pull.interp = 0;
    %matlabbatch{4}.spm.util.defs.out{1}.pull.mask = 1;
    %matlabbatch{4}.spm.util.defs.out{1}.pull.fwhm = [0 0 0];
    %matlabbatch{4}.spm.util.defs.out{1}.pull.prefix = 'yapplied';


    matlabbatch{1}.spm.util.defs.comp{1}.def = {def};
    matlabbatch{1}.spm.util.defs.out{1}.pull.fnames = {fname};
    matlabbatch{1}.spm.util.defs.out{1}.pull.savedir.saveusr = {saveusr};
    matlabbatch{1}.spm.util.defs.out{1}.pull.interp = 0; % Nearest neighbor interpolation
    matlabbatch{1}.spm.util.defs.out{1}.pull.mask = 1;
    matlabbatch{1}.spm.util.defs.out{1}.pull.fwhm = [0 0 0];
    matlabbatch{1}.spm.util.defs.out{1}.pull.prefix = 'yinvapplied';
    
	spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);
end

