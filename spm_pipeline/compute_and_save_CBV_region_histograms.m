function compute_and_save_CBV_region_histograms(epi_corrections_out_dir)

epi_corrections_out_dir = ...
    '../../epi_corrections_out_2019_06_19_372114315';

[region_values,...
    hist_edges,...
    raw_CBV_region_histograms,...
    topup_CBV_region_histograms,...
    epic_CBV_region_histograms] =...
    get_all_region_histograms(epi_corrections_out_dir);

CBV_out_dir = strcat(epi_corrections_out_dir, '/', 'CBV_histograms');

%mkdir(CBV_out_dir);

%save(strcat(CBV_out_dir, '/', 'region_values.mat'), 'region_values');
%save(strcat(CBV_out_dir, '/', 'hist_edges.mat'), 'hist_edges');
%save(strcat(CBV_out_dir, '/', 'raw_CBV_region_histograms.mat'), 'raw_CBV_region_histograms');
%save(strcat(CBV_out_dir, '/', 'topup_CBV_region_histograms.mat'), 'topup_CBV_region_histograms');
%save(strcat(CBV_out_dir, '/', 'epic_CBV_region_histograms.mat'), 'epic_CBV_region_histograms');

%raw_CBV_region_histograms

end