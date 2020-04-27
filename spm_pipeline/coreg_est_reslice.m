function coreg_est_reslice(ref, source, other_files, interp_index)

    %coreg_est_reslice_function(ref, src, other, 0);

    matlabbatch{1}.spm.spatial.coreg.estwrite.ref = {strcat(ref, ',1')};
    matlabbatch{1}.spm.spatial.coreg.estwrite.source = {strcat(source, ',1')};
    matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
    matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
    matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
    matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
    matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.interp = interp_index;
    matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
    matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.mask = 0;
    matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.prefix = 'r';
    matlabbatch{1}.spm.spatial.coreg.estwrite.other = other_files;

    spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);

end