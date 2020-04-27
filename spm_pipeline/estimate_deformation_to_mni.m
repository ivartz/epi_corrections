function estimate_deformation_to_mni(img)

    %estimate_deformation_to_nmi('dsc.nii')

    matlabbatch{1}.spm.spatial.normalise.est.subj.vol = {strcat(img, ',1')};
    matlabbatch{1}.spm.spatial.normalise.est.eoptions.biasreg = 0.0001;
    matlabbatch{1}.spm.spatial.normalise.est.eoptions.biasfwhm = 60;
    matlabbatch{1}.spm.spatial.normalise.est.eoptions.tpm = {'/media/loek/HDD3TB1/apps/spm12/tpm/TPM.nii'}; % Note, system specific.
    matlabbatch{1}.spm.spatial.normalise.est.eoptions.affreg = 'mni';
    matlabbatch{1}.spm.spatial.normalise.est.eoptions.reg = [0 0.001 0.5 0.05 0.2];
    matlabbatch{1}.spm.spatial.normalise.est.eoptions.fwhm = 0;
    matlabbatch{1}.spm.spatial.normalise.est.eoptions.samp = 3;
    
	spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);
end