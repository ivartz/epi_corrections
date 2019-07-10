function gunzip_function(files)

    matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_gunzip_files.files = {files};
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_gunzip_files.outdir = {''};
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_gunzip_files.keep = true;
    
    spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);
    
end