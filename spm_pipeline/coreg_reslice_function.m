function coreg_reslice_function(ref, source, interp_index)

    matlabbatch{1}.spm.spatial.coreg.write.ref = {ref}; % y_flair..
    %matlabbatch{1}.spm.spatial.coreg.write.source = {source}; % labels_neurom*
    matlabbatch{1}.spm.spatial.coreg.write.source = source; % labels_neurom*
    matlabbatch{1}.spm.spatial.coreg.write.roptions.interp = interp_index;
    matlabbatch{1}.spm.spatial.coreg.write.roptions.wrap = [0 0 0];
    matlabbatch{1}.spm.spatial.coreg.write.roptions.mask = 0;
    matlabbatch{1}.spm.spatial.coreg.write.roptions.prefix = 'r';

    spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);

end