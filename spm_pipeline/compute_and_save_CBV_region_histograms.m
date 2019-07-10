function compute_and_save_CBV_region_histograms(epi_corrections_out_dir, ...
    hist_num_cells, hist_min_value, hist_max_value, region_req_covered_perc)

% epi_corrections_out_dir = ...
%     '../../epi_corrections_out_2019_07_02';
% hist_num_cells = 64;
% hist_min_value = 0;
% hist_max_value = 12;
% region_req_covered_perc = 70;

region_req_covered_frac = region_req_covered_perc/100;

[region_values,...
    hist_edges,...
    raw_e1_CBV_region_histograms,...
    raw_e1_CBV_dirs,...
    raw_e2_CBV_region_histograms,...
    raw_e2_CBV_dirs,...
    topup_e1_CBV_region_histograms,...
    topup_e1_CBV_dirs,...
    topup_e2_CBV_region_histograms,...
    topup_e2_CBV_dirs,...
    epic_e1_CBV_region_histograms,...
    epic_e1_CBV_dirs,...
    epic_e2_CBV_region_histograms,...
    epic_e2_CBV_dirs] =...
    get_all_region_histograms(epi_corrections_out_dir, hist_num_cells, hist_min_value, hist_max_value, region_req_covered_frac);

CBV_out_dir = ...
    strcat(epi_corrections_out_dir, '/', 'CBV_histograms_bins_', ...
    int2str(hist_num_cells), '_min_', int2str(hist_min_value), ...
    '_max_', int2str(hist_max_value), '_region_rec_c_frac_', num2str(region_req_covered_frac));

mkdir(CBV_out_dir);

save(strcat(CBV_out_dir, '/', 'region_values.mat'), 'region_values');
save(strcat(CBV_out_dir, '/', 'hist_edges.mat'), 'hist_edges');

save(strcat(CBV_out_dir, '/', 'raw_e1_CBV_region_histograms.mat'), 'raw_e1_CBV_region_histograms');
save(strcat(CBV_out_dir, '/', 'raw_e1_CBV_dirs.mat'), 'raw_e1_CBV_dirs');
save(strcat(CBV_out_dir, '/', 'raw_e2_CBV_region_histograms.mat'), 'raw_e2_CBV_region_histograms');
save(strcat(CBV_out_dir, '/', 'raw_e2_CBV_dirs.mat'), 'raw_e2_CBV_dirs');
save(strcat(CBV_out_dir, '/', 'topup_e1_CBV_region_histograms.mat'), 'topup_e1_CBV_region_histograms');
save(strcat(CBV_out_dir, '/', 'topup_e1_CBV_dirs.mat'), 'topup_e1_CBV_dirs');
save(strcat(CBV_out_dir, '/', 'topup_e2_CBV_region_histograms.mat'), 'topup_e2_CBV_region_histograms');
save(strcat(CBV_out_dir, '/', 'topup_e2_CBV_dirs.mat'), 'topup_e2_CBV_dirs');
save(strcat(CBV_out_dir, '/', 'epic_e1_CBV_region_histograms.mat'), 'epic_e1_CBV_region_histograms');
save(strcat(CBV_out_dir, '/', 'epic_e1_CBV_dirs.mat'), 'epic_e1_CBV_dirs');
save(strcat(CBV_out_dir, '/', 'epic_e2_CBV_region_histograms.mat'), 'epic_e2_CBV_region_histograms');
save(strcat(CBV_out_dir, '/', 'epic_e2_CBV_dirs.mat'), 'epic_e2_CBV_dirs');

end