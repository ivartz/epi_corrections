///////////////////////////////////////////////////////////////////////
// This source code is Copyright ©2007-2010 Dominic Holland and Anders
// Dale. Permission is granted by Dominic Holland and Anders Dale to
// copy, distribute and modify this source code, provided that it is
// used for research purposes only, and only by not-for-profit
// organizations, and further provided that:
// 
//    * this copyright notice appears in all copies.
//    * you indemnify and hold harmless Dominic Holland and Anders
//      Dale and their successors and associates from any and all
//      liability from any use of the information.
//    * you ensure that these conditions apply to any further
//      redistribution of the source code or derived software
// 
// For commercial entities and for commercial applications, the right
// to copy, distribute or modify this source code is retained by
// Dominic Holland and Anders Dale, and must be obtained through
// completion of a written license agreement with Dominic Holland and
// Anders Dale.
///////////////////////////////////////////////////////////////////////

// ==================================================
// Copyright ©2007-2010 Dominic Holland and Anders Dale
// All rights reserved
// ==================================================


void
initDispyFullRes(float* dispyFullRes,
		 const float* dispy,
		 const int width,
		 const int height,
		 const int depth,
		 const int numVoxFullRes,
		 const int voxStepSample) {
  
  int numVoxXSample ( width  / voxStepSample + (width  % voxStepSample ? 1 : 0) );
  int numVoxYSample ( height / voxStepSample + (height % voxStepSample ? 1 : 0) );
  int numVoxZSample ( depth  / voxStepSample + (depth  % voxStepSample ? 1 : 0) );
  
  double voxStepSampleInv(1.0/voxStepSample);
  
  for(int xc = 0; xc < numVoxXSample-1; ++xc)
    for(int yc = 0; yc < numVoxYSample-1; ++yc)
      for(int zc = 0; zc < numVoxZSample-1; ++zc) {
	
	// Determine coarse-grained boundary voxels of a cube of side
	// voxStepSample voxels. These voxel indices can be used to
	// dereference dispy[].
	
	int cvox000 (     xc*(numVoxYSample * numVoxZSample) +     yc*numVoxZSample +     zc );
	int cvox100 ( (xc+1)*(numVoxYSample * numVoxZSample) +     yc*numVoxZSample +     zc );
	int cvox010 (     xc*(numVoxYSample * numVoxZSample) + (yc+1)*numVoxZSample +     zc );
	int cvox001 (     xc*(numVoxYSample * numVoxZSample) +     yc*numVoxZSample + (zc+1) );
	
	int cvox111 ( (xc+1)*(numVoxYSample * numVoxZSample) + (yc+1)*numVoxZSample + (zc+1) );
	int cvox011 (     xc*(numVoxYSample * numVoxZSample) + (yc+1)*numVoxZSample + (zc+1) );
	int cvox101 ( (xc+1)*(numVoxYSample * numVoxZSample) +     yc*numVoxZSample + (zc+1) );
	int cvox110 ( (xc+1)*(numVoxYSample * numVoxZSample) + (yc+1)*numVoxZSample +     zc );
	
	double d000 ( dispy[cvox000] );
	double d100 ( dispy[cvox100] );
	double d010 ( dispy[cvox010] );
	double d001 ( dispy[cvox001] );
	double d111 ( dispy[cvox111] );
	double d011 ( dispy[cvox011] );
	double d101 ( dispy[cvox101] );
	double d110 ( dispy[cvox110] );
	
	int x0 ( xc*voxStepSample );    int x1 ( (xc+1)*voxStepSample );
	int y0 ( yc*voxStepSample );    int y1 ( (yc+1)*voxStepSample );
	int z0 ( zc*voxStepSample );    int z1 ( (zc+1)*voxStepSample );
	
	for(int xm = 0; xm < voxStepSample; ++xm)
	  for(int ym = 0; ym < voxStepSample; ++ym)
	    for(int zm = 0; zm < voxStepSample; ++zm) {
	      
	      int voxel ( (x0+xm)*(height * depth) + (y0+ym)*depth + (z0+zm) );
	      
	      double xf ( xm*voxStepSampleInv );
	      double yf ( ym*voxStepSampleInv );
	      double zf ( zm*voxStepSampleInv );
	      
	      double dispy_xmymzm = ( d000 * (1.0 - xf) * (1.0 - yf) * (1.0 - zf) +
				      d100 *        xf  * (1.0 - yf) * (1.0 - zf) +
				      d010 * (1.0 - xf) *        yf  * (1.0 - zf) +
				      d001 * (1.0 - xf) * (1.0 - yf) *        zf  +
				      d011 * (1.0 - xf) *        yf  *        zf  +
				      d101 *        xf  * (1.0 - yf) *        zf  +
				      d110 *        xf  *        yf  * (1.0 - zf) +
				      d111 *        xf  *        yf  *        zf  );
	      
	      dispyFullRes[voxel] = dispy_xmymzm;
	    }
      }
  
  // Patch up boundary....errr this could be improved...
  {
    for(int xc = 0; xc < numVoxXSample; ++xc)
      for(int yc = 0; yc < numVoxYSample; ++yc)
	for(int zc = 0; zc < numVoxZSample; ++zc) {
	  
	  if(xc == numVoxXSample-1 || yc == numVoxYSample-1 || zc == numVoxZSample-1) {
	    
	    int cvox ( xc*(numVoxYSample * numVoxZSample) + yc*numVoxZSample + zc );
	    
	    int x0 ( xc*voxStepSample );
	    int y0 ( yc*voxStepSample );
	    int z0 ( zc*voxStepSample );
	    
	    double d ( dispy[cvox] );
	    
	    for(int xm = 0; xm < width-x0; ++xm)
	      for(int ym = 0; ym < height-y0; ++ym)
		for(int zm = 0; zm < depth-z0; ++zm) {
		  
		  int voxel ( (x0+xm)*(height * depth) + (y0+ym)*depth + (z0+zm) );
		  
		  //double xf = xm/(width-x0);
		  //double yf = ym/(height-y0);
		  //double zf = zm/(depth-z0);
		  
		  double dispy_xmymzm ( d );
		  
		  dispyFullRes[voxel] = dispy_xmymzm;
		}
	  }
	}
  }
}
