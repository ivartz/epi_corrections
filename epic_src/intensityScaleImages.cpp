#include <iostream>
#include "imgvol.h"       // CTX stuff. fvol


void
intensityScaleImages(fvol* mri1, fvol* mri2, const float& imax) {
  
  // First make sure that mri1 is the brighter of the two images, by
  // almost 2x. If it is, then scale mri1 so that its max intensity is
  // imax, and scale mri2 by the sam eamount.

  int width  ( mri1->info.dim[1] );
  int height ( mri1->info.dim[0] );
  int depth  ( mri1->info.dim[2] );
  
  float val1max (0.0), val2max (0.0);
  
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y)
      for(int z = 0; z < depth; ++z)  {
	
	float val1 ( fVolGetVal(mri1, y, x, z) );
	float val2 ( fVolGetVal(mri2, y, x, z) );
	
	if(val1 > val1max) val1max = val1;
	if(val2 > val2max) val2max = val2;
	
      }
  
  float valmax  ( val1max > val2max ? val1max : val2max );
  float iscale  ( imax/valmax );  
  
  std::clog<<'\n'<<__FILE__
	   <<":\nval1max = "<<val1max
	   <<"\tval2max  = "<<val2max
	   <<"\nRescaling intensities of both images by "
	   <<"iscale = "<<iscale<<'\n'<<std::endl;
  
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y)
      for(int z = 0; z < depth; ++z)  {

	float val1 ( fVolGetVal(mri1, y, x, z) );
	float val2 ( fVolGetVal(mri2, y, x, z) );
	
	val1 *= iscale;
	val2 *= iscale;
	
	fVolSetVal(mri1, y, x, z, val1);
	fVolSetVal(mri2, y, x, z, val2);
	
      }
  
}
