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

#include <string.h>            // For memset() and strings.
#include "inputParams.h"
#include "imgvol.h"          // CTX stuff. fvol
#include "getNumVox.h"
#include "loadDispy.h"
#include "blurImages.h"
#include "solveHessian.h"

#include "computeDeformationField.h"

#include "writeImage.h"

using std::clog;
using std::endl;


float*
computeDeformationField(fvol* forwardMri, fvol* reverseMri, const InputParams& p) {
  
  const float h       ( p.getCgVoxDifferential() );
  const int   voxStep ( p.getVoxStep() );
  const int   numVox  ( getNumVox(voxStep, forwardMri) );
  
  double* ddub ( new double[numVox] );          // Need a double array for GSL. Returned to caller.
  
  if( p.getRestart() )
    loadDispy(p.getDisplacementFieldInFileName(), numVox, voxStep, p.getNvoxNewZbdry(), ddub);
  else
    memset(ddub, 0, numVox*sizeof(double));
  
  int kernelWidthMax ( p.getKernelWidthMax() ); // Pixel width of Gaussian kernel. Keep it an odd number, >= 1.
  
  if(kernelWidthMax)
    kernelWidthMax = kernelWidthMax%2 ? kernelWidthMax : kernelWidthMax+1;    // Make sure it is odd, or zero.
  
  int kernelWidthStep( p.getKernelWidthStep() );
  
  kernelWidthStep = kernelWidthStep%2 ? kernelWidthStep+1 : kernelWidthStep;  // Make sure it is even.
  
  float lambda1  ( p.getLambda1() );
  float lambda2  ( p.getLambda2() );
  float lambda2P ( p.getLambda2P() );
  const int   nchunksZ ( p.getNchunksZ() );
  
  const float l1Max  ( lambda1 );
  const float l1Min  ( 0.0 );
  const float l2Max  ( lambda2 );
  const float l2Min  ( 1.0e3 );
  const float l2PMax ( lambda2P );
  const float l2PMin ( 1.0e3 );
  const int   nKsteps ( kernelWidthMax / kernelWidthStep );
  int nKstep ( 0 );
  
  double hessianErrorMax  ( p.getHessianErrorMax() );
  int    hessianErrorCode ( 0 );
  double bicgstabTol      ( p.getBicgstabTol() );
  int    maxIter          ( p.getBicgstabMaxIter() );
  
  int bcopydataNO  ( 0 );
  fvol* forwardMriBlur ( fVolCopy(forwardMri, bcopydataNO) ); // Free in this block.
  fvol* reverseMriBlur ( fVolCopy(reverseMri, bcopydataNO) ); // Free in this block.
  
  bool cubicInterp ( false );
  
  clock_t startClock ( clock() );
  
  //  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  for(int kernelWidth = kernelWidthMax; kernelWidth > -kernelWidthStep; ) {
    
    clog << __FILE__ << ":  " << __LINE__ << endl;
    clog << "\tkernelWidth     = " << kernelWidth     << endl;
    clog << "\tkernelWidthStep = " << kernelWidthStep << endl;
    
    lambda1  = l1Max  - (l1Max - l1Min)*nKstep/nKsteps; clog << "lambda1  = "<<lambda1 <<endl;
    lambda2  = l2Max  - (l2Max - l2Min)*nKstep/nKsteps; clog << "lambda2  = "<<lambda2 <<endl;
    lambda2P = l2PMax - (l2PMax-l2PMin)*nKstep/nKsteps; clog << "lambda2P = "<<lambda2P<<endl;
    nKstep++;
    
    if(kernelWidth >= 3) {
      blurImages(p, forwardMri, reverseMri, forwardMriBlur, reverseMriBlur, kernelWidth);
      std::cout << "kernelWidth >= 3" << "\n";
      if(kernelWidth <= 3) cubicInterp = true;;
      hessianErrorCode = solveHessian(ddub, forwardMriBlur, reverseMriBlur, voxStep, numVox, nchunksZ, bicgstabTol,
				      maxIter, hessianErrorMax, p.getNvoxNewZbdry(), lambda1, lambda2, lambda2P, h, cubicInterp);
    }

    else {
      std::cout << "kernelWidth < 3" << "\n";
      cubicInterp = true;
      hessianErrorCode = solveHessian(ddub, forwardMri, reverseMri, voxStep, numVox, nchunksZ, bicgstabTol,
				      maxIter, hessianErrorMax, p.getNvoxNewZbdry(), lambda1, lambda2, lambda2P, h, cubicInterp);
    }
    
    //    std::clog << __FILE__ << ":  " << __LINE__ << " hessianErrorCode = "<<hessianErrorCode<<std::endl;
    if( hessianErrorCode )
      break;
    
    //    std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
    if(kernelWidth > 3 && kernelWidth-kernelWidthStep < 3) // 3 ==> 1 voxel on each side of center voxel: minimum Gaussian.
      kernelWidth = 3;
    else if(kernelWidth == 3)
      kernelWidth = 0;
    else if(kernelWidth < 3)
      break;
    else kernelWidth -= kernelWidthStep;
    //    std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
    
  } // END for(int kernelWidth = kernelWidthMax; kernelWidth > -kernelWidthStep; ) {
  
  clock_t secondsUsed ( (clock() - startClock)/(CLOCKS_PER_SEC) );
  std::cout << "\ncompute time computeDeformationField() (seconds): " << secondsUsed << std::endl;
  
  fVolDelete(forwardMriBlur);
  fVolDelete(reverseMriBlur);
  
  float* d ( new float[numVox] );
  for(int i=0; i<numVox; ++i)
    d[i] = ddub[i];
  delete[] ddub;
  return d;
  
}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////// O V E R L O A D ////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////


#include "imageInfo.h"
#include "interpolation.h"     // CTX stuff. fvol

#include "writeImage.h"

float*
computeDeformationField(const float* images, const IMAGEINFO& info) {
  
  InputParams p; // Use defaults.
  //std::clog << p;
  
  int width    ( info.numVox[0] );
  int height   ( info.numVox[1] );
  int depth    ( info.numVox[2] );
  int depthAux ( depth + 2*p.getNvoxNewZbdry() ); // Default nvoxNewZbdry == 2.
  
  int dim[3] = {height ,width , depthAux};
  
  float xsize ( info.voxSize[0] );
  float ysize ( info.voxSize[1] );
  float zsize ( info.voxSize[2] );
  
  float voxSize[3] = {ysize, xsize, zsize};
  
  // New fvol: vol. dim: (height,width,depthAux), vox. dim: (ysize,xsize,zsize), and coronal view.
  hmat mpat2grad;
  hMatEye(&mpat2grad);
  
  hvec dv;
  hmat mvxl2lph;
  
  hVecInit(&dv, 0.0, 0.0, -1.0*ysize, 0.0);
  hMatSetCol(&mvxl2lph, &dv, 0); // y
  
  hVecInit(&dv, 1.0*xsize, 0.0, 0.0, 0.0);
  hMatSetCol(&mvxl2lph, &dv, 1); // x
  
  hVecInit(&dv, 0.0, -1.0*zsize, 0.0, 0.0);
  hMatSetCol(&mvxl2lph, &dv, 2); // z
  
  hVecInit(&dv, -(height-1.0)/2.0, -(width-1.0)/2.0, -(depthAux-1.0)/2.0, 1.0);
  hMatSetCol(&mvxl2lph, &dv, 3);
  
  fvol* forwardMri ( fVolNew(dim, &mvxl2lph, &mpat2grad, 0) );
  fvol* reverseMri ( fVolNew(dim, &mvxl2lph, &mpat2grad, 0) );
  
  const float* imageF ( images );
  const float* imageR ( images + width*height*depth );
  
  // Now, load up forwardMri and reverseMri
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y)
      for(int z = 0; z < depth; ++z)  {
	
	int voxel ( x*height*depth + y*depth + z );
	
	float valF ( imageF[voxel] );
	float valR ( imageR[voxel] );
	
	fVolSetVal(forwardMri, y, x, z+p.getNvoxNewZbdry(), valF);
	fVolSetVal(reverseMri, y, x, z+p.getNvoxNewZbdry(), valR);
      }
  
  // Let the new layers be duplicates of the current top and bottom end layers
  // Lower bdry:
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y) {
      
      int voxel ( x*height*depth + y*depth + 0 );
      
      float valF ( imageF[voxel] );
      float valR ( imageR[voxel] );
      
      for(int z = 0; z < p.getNvoxNewZbdry(); ++z) {
	fVolSetVal(forwardMri, y, x, z, valF);
	fVolSetVal(reverseMri, y, x, z, valR);
      }
    }
  
  // Upper bdry:
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y) {
      
      int voxel ( x*height*depth + y*depth + depth-1 );
      
      float valF ( imageF[voxel] );
      float valR ( imageR[voxel] );
      
      for(int z = depthAux-p.getNvoxNewZbdry(); z < depthAux; ++z) {
	fVolSetVal(forwardMri, y, x, z, valF);
	fVolSetVal(reverseMri, y, x, z, valR);
      }
    }
  
  float* dAux ( computeDeformationField(forwardMri, reverseMri, p) );
  
  fVolDelete(forwardMri);
  fVolDelete(reverseMri);  
  
  float* d ( new float[width*height*depth] );
  
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y)
      for(int z = p.getNvoxNewZbdry(), za=0; z < depthAux-p.getNvoxNewZbdry(); ++z, ++za) {
	
	int   voxelAux ( x*(height * depthAux) + y*depthAux + z  );
	int   voxel    ( x*(height * depth   ) + y*depth    + za );
	d[voxel] = dAux[voxelAux];
      }
  
  delete[] dAux;
  
  return d;
  
}
