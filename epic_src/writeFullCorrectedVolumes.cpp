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

#include <iostream>
#include <string.h>
#include "inputParams.h"
#include "interpolation.h"          // CTX stuff. fvol
#include "createRescaledMri.h"
#include <cmath>                    // for fabs().
#include "writeImage.h"

using std::string;
using std::clog;
using std::cerr;
using std::endl;


void
writeFullCorrectedVolumes(const InputParams& p, fvol* forwardMri, fvol* reverseMri,
			  float* dispy, const bool trimZbdrys) {

  // These three quantities need to be set as input parameters.
  const INTERPMETHOD interpMethod ( CUBIC );  // NEAREST  LINEAR   CUBIC
  const INTERPEDGE   interpEdge   ( ZEROPAD ); // MIRROR   ZEROPAD  THROWAWAY: Want MIRROR for wraparound.
  
  const int bPositiveYES ( 1 );
  const int bPositiveNO  ( 0 );
  const int bcopydataNO  ( 0 );
  const int bcopydataYES ( 1 );
  
  if(interpMethod == CUBIC)
    clog << __FILE__ << ":\n Using cubic interpolation...\n" << '\n';
  
  int nvoxNewZbdry ( 0 );
  
  int width  ( forwardMri->info.dim[1] );
  int height ( forwardMri->info.dim[0] );
  int depth  ( forwardMri->info.dim[2] );
  
  int numVox ( width*height*depth );
  
  int depthOrig ( depth );
  if( trimZbdrys ) {
    nvoxNewZbdry = p.getNvoxNewZbdry();  // Or whatever was used in mriClass.cpp and solveHessian.cpp
    depthOrig = depth - 2*nvoxNewZbdry;
  }
  
  const bool fillDataNO ( false );
  const float xsize ( forwardMri->info.vxlsize[1] );
  const float ysize ( forwardMri->info.vxlsize[0] );
  const float zsize ( forwardMri->info.vxlsize[2] );
  
  fvol* forwardMriC ( createRescaledMri(width, height, depthOrig, xsize, ysize, zsize, forwardMri, fillDataNO) );
  fvol* reverseMriC ( createRescaledMri(width, height, depthOrig, xsize, ysize, zsize, reverseMri, fillDataNO) );
  fvol* avgMriC     ( createRescaledMri(width, height, depthOrig, xsize, ysize, zsize, forwardMri, fillDataNO) );
  fvol* difMriC     ( createRescaledMri(width, height, depthOrig, xsize, ysize, zsize, forwardMri, fillDataNO) );
  fvol* dispyMri    ( createRescaledMri(width, height, depthOrig, xsize, ysize, zsize, forwardMri, fillDataNO) );
  
  float dispyMin (0.0);
  for(int i=0; i<numVox;++i)
    if(dispy[i] < dispyMin) dispyMin = dispy[i];
  clog << __FILE__ << ":\n"
       << "dispyMin = " << dispyMin << '\n';
  
  const int sincVoxWidth ( 5 );
  
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y)
      for(int z = nvoxNewZbdry, za=0; z < depth-nvoxNewZbdry; ++z, ++za) {
	
	int   voxel   ( x*(height * depth) + y*depth + z );	
	float dy      ( dispy[voxel] );
	
	int   ym      ( (y == 0 ? 0 : y-1) );
	int   voxelym ( x*(height * depth) + ym*depth + z );
	float dym     ( dispy[voxelym] );
	
	int   yp      ( (y == height-1 ? height-1 : y+1) );
	int   voxelyp ( x*(height * depth) + yp*depth + z );
	float dyp     ( dispy[voxelyp] );
	
	const float widtha ( 2.0 );                 // Original width around current voxel, ya.
	//float widthb ( widtha+(-dyp+dym)*voxStepInv ); // New width around current voxel.
	float widthb1 ( widtha+dyp-dym ); // New width around current voxel in forward.
	float widthb2 ( widtha-dyp+dym ); // New width around current voxel in reverse.
	
	if(widthb1 <= 0.0) 
	  cerr << __FILE__ << ":  " << __LINE__ << " widthb1 = " << widthb1
	       << "  (" << x << ", " << y << " ," << z << ')' << '\n';
	if(widthb2 <= 0.0) 
	  cerr << __FILE__ << ":  " << __LINE__ << " widthb2 = " << widthb2
	       << "  (" << x << ", " << y << " ," << z << ')' << '\n';
	
	float fval ( 0.0 );
	float rval ( 0.0 );
	
	hvec voxp;
	hVecInit(&voxp, y+dy, x, z, 1.0);
	
	hvec voxm;
	hVecInit(&voxm, y-dy, x, z, 1.0);
	
	GetVxlVal(&voxp, &fval, forwardMri, interpMethod, interpEdge, bPositiveYES);
	if(fval < 0.0)
	  fval = 0.0;
	
	GetVxlVal(&voxm, &rval, reverseMri, interpMethod, interpEdge, bPositiveYES);
	if(rval < 0.0)
	  rval = 0.0;
	
	// Intensity should increase linearly if there is local squishing, decrease if expansion.
	//double term = SQR( fabs(widthb1/widtha)*fval - fabs(widthb2/widtha)*rval );
	fval *= fabs(widthb1/widtha);
	rval *= fabs(widthb2/widtha);
	
	fVolSetVal(forwardMriC, y, x, za, fval);
	fVolSetVal(reverseMriC, y, x, za, rval);
	fVolSetVal(avgMriC,     y, x, za, 0.5*(fval+rval));
	fVolSetVal(difMriC,     y, x, za, fval-rval);
	fVolSetVal(dispyMri,    y, x, za, dy);
      }
  
  
  string outDir               ( p.getOutDir() + "/" );
  string forwardCorrectedFile ( outDir + p.getForwardImageOutFileName() );
  string reverseCorrectedFile ( outDir + p.getReverseImageOutFileName() );
  string avgCorrectedFile     ( outDir + "avgEIP.mgz" );
  string difCorrectedFile     ( outDir + "difEIP.mgz" );
  string dispyFieldFile       ( outDir + p.getDisplacementFieldOutFileName() );
  
  writeImage(forwardCorrectedFile, forwardMriC);
  writeImage(reverseCorrectedFile, reverseMriC);
  writeImage(avgCorrectedFile,     avgMriC);
  writeImage(difCorrectedFile,     difMriC);
  writeImage(dispyFieldFile,       dispyMri);
  
  fVolDelete(forwardMriC);
  fVolDelete(reverseMriC);
  fVolDelete(avgMriC);
  fVolDelete(difMriC);
  fVolDelete(dispyMri);  
  
}
