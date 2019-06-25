%-----------------------------------------------------------------------
% Job saved on 28-Mar-2019 10:32:46 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7487)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
matlabbatch{1}.spm.spatial.normalise.write.subj.def = {};
%%
matlabbatch{1}.spm.spatial.normalise.write.subj.resample = {};
%%
matlabbatch{1}.spm.spatial.normalise.write.woptions.bb = [-78 -112 -70
                                                          78 76 85];
matlabbatch{1}.spm.spatial.normalise.write.woptions.vox = [2 2 2];
%matlabbatch{1}.spm.spatial.normalise.write.woptions.interp = 4; % 4. order b-spline
matlabbatch{1}.spm.spatial.normalise.write.woptions.interp = 1; % Trilinear (was found to perform most stable in intensity values)
%matlabbatch{1}.spm.spatial.normalise.write.woptions.interp = 0; % Nearest
matlabbatch{1}.spm.spatial.normalise.write.woptions.prefix = 'w';
