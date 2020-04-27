function rigid_register(ref, src, other_1, other_2, other_1_out, other_2_out, interp_index)

    %rigid_register('/media/loek/HDD3TB1/data/roi-example-topup-372114315/epicd/dsc.nii', '/media/loek/HDD3TB1/data/roi-example-topup-372114315/dsc.nii', '/media/loek/HDD3TB1/data/roi-example-topup-372114315/gtrois_e1.nii', '/media/loek/HDD3TB1/data/roi-example-topup-372114315/gttumorrois_e1.nii', '/media/loek/HDD3TB1/data/roi-example-topup-372114315/epicd/gtrois_e1.nii', '/media/loek/HDD3TB1/data/roi-example-topup-372114315/epicd/gttumorrois_e1.nii', 0)

    [~, srcfilename, srcfileext] = fileparts(src);
    [~, other_1_filename, other_1_fileext] = fileparts(other_1);
    [~, other_2_filename, other_2_fileext] = fileparts(other_2);
    [other_1_outpath, ~, ~] = fileparts(other_1_out);
    [other_2_outpath, ~, ~] = fileparts(other_2_out);
    
    assert(strcmp(other_1_outpath, other_2_outpath), 'out paths are not equal');
    
    outpath = other_1_outpath;
    
    src_copy = strcat(outpath, '/_', srcfilename, srcfileext);
    other_1_copy = strcat(outpath, '/_', other_1_filename, other_1_fileext);
    other_2_copy = strcat(outpath, '/_', other_2_filename, other_2_fileext);
    
    copyfile(src, src_copy);
    copyfile(other_1, other_1_copy);
    copyfile(other_2, other_2_copy);
    
    other_copy = {
        other_1_copy
        other_2_copy
        };
    
    coreg_est_reslice(ref, ...
                      src_copy, ...
                      other_copy, ...
                      interp_index);

    resliced_src_copy = strcat(outpath, '/r_', srcfilename, srcfileext);
    resliced_other_1_copy = strcat(outpath, '/r_', other_1_filename, other_1_fileext);
    resliced_other_2_copy = strcat(outpath, '/r_', other_2_filename, other_2_fileext);
                  
    movefile(resliced_other_1_copy, other_1_out);
    movefile(resliced_other_2_copy, other_2_out);
    
    % Clean up    
    delete(resliced_src_copy);
    delete(src_copy);
    delete(other_1_copy);
    delete(other_2_copy);
end