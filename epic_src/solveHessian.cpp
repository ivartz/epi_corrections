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
#include <cstdlib>
#include <cmath>
#include <ctime>          // for clock()
#include <cstring>        // for memset()
#include <vector>
#include <algorithm>

extern "C" {
#include "bicgstabc.h"
#include "BiCGSTABF.h"
}

#include "lsolver/cghs.h"
#include "lsolver/bicgsq.h"
#include "lsolver/bicgstab.h"
#include "lsolver/gmres.h"

#include "hessian.h"
#include "setupHessian.h"

#ifndef SQR
#define SQR(a)   ((a)*(a))
#endif

using std::cerr;
using std::cout;
using std::endl;
using std::vector;
using std::count;

int numVoxExtern;
Hessian HExtern;


void mult( const Hessian& H, const double *v, double *w ) { // H * v = w
  
  int numVoxX ( H.numVoxX );
  int numVoxY ( H.numVoxY );
  int numVoxZ ( H.numVoxZ );
  
  for(int xa = 0; xa < numVoxX; ++xa)
    for(int ya = 0; ya < numVoxY; ++ya)
      for(int za = 0; za < numVoxZ; ++za) {

	int voxel( xa*(numVoxY * numVoxZ) + ya*numVoxZ + za );
	
	int   yam     ( (ya == 0 ? 0 : ya-1) );
	int   voxelym ( xa*(numVoxY * numVoxZ) + yam*numVoxZ + za );
	
	int   yamm    ( (yam == 0 ? 0 : yam-1) );
	int   voxelymm( xa*(numVoxY * numVoxZ) + yamm*numVoxZ + za );
	
	int   yap     ( (ya == numVoxY-1 ? numVoxY-1 : ya+1) );
	int   voxelyp ( xa*(numVoxY * numVoxZ) + yap*numVoxZ + za );
	
	int   yapp    ( (yap == numVoxY-1 ? numVoxY-1 : yap+1) );
	int   voxelypp( xa*(numVoxY * numVoxZ) + yapp*numVoxZ + za );
	
	int   xam     ( (xa == 0 ? 0 : xa-1) );
	int   voxelxm ( xam*(numVoxY * numVoxZ) + ya*numVoxZ + za );
	
	int   xamm    ( (xam == 0 ? 0 : xam-1) );
	int   voxelxmm( xamm*(numVoxY * numVoxZ) + ya*numVoxZ + za );
	
	int   xap     ( (xa == numVoxX-1 ? numVoxX-1 : xa+1) );
	int   voxelxp ( xap*(numVoxY * numVoxZ) + ya*numVoxZ + za );
	
	int   xapp    ( (xap == numVoxX-1 ? numVoxX-1 : xap+1) );
	int   voxelxpp( xapp*(numVoxY * numVoxZ) + ya*numVoxZ + za );
	
	int   zam     ( (za == 0 ? 0 : za-1) );
	int   voxelzm ( xa*(numVoxY * numVoxZ) + ya*numVoxZ + zam );
	
	int   zamm    ( (zam == 0 ? 0 : zam-1) );
	int   voxelzmm( xa*(numVoxY * numVoxZ) + ya*numVoxZ + zamm );
	
	int   zap     ( (za == numVoxZ-1 ? numVoxZ-1 : za+1) );
	int   voxelzp ( xa*(numVoxY * numVoxZ) + ya*numVoxZ + zap );
	
	int   zapp    ( (zap == numVoxZ-1 ? numVoxZ-1 : zap+1) );
	int   voxelzpp( xa*(numVoxY * numVoxZ) + ya*numVoxZ + zapp );
	
	w[voxel] = ( H.Hjjpp[voxelymm] * v[voxelymm] +
		     H.Hjjp [voxelym ] * v[voxelym ] +
		     H.Hjj  [voxel   ] * v[voxel   ] +
		     H.Hjjp [voxel   ] * v[voxelyp ] +
		     H.Hjjpp[voxel   ] * v[voxelypp] +
		     
      // CHOOSE ONE OF THE FOLLOWING (see also setupHessian.cpp):
#if 0 // double gradTerm ( lambda2 * (gx*gx + gy*gy + gz*gz) ); This is the standard one.
		     H.lamSize   * v[voxel] +
		     H.lamSmooth * ( v[voxel   ] * 6.0 -
				     v[voxelxmm] -
				     v[voxelymm] -
				     v[voxelzmm] -
				     v[voxelxpp] -
				     v[voxelypp] -
				     v[voxelzpp]        ) );
	
      //double gradTerm = lambda2P * ((gxp*gxp+gxm*gxm) + (gyp*gyp+gym*gym) + (gzp*gzp+gzm*gzm));
#elif 0
		     H.lamSize   * v[voxel] +
		     H.lamSmoothP* ( v[voxel  ] * 12.0 -
				     v[voxelxm] * 2.0 -
				     v[voxelym] * 2.0 -
				     v[voxelzm] * 2.0 -
				     v[voxelxp] * 2.0 -
				     v[voxelyp] * 2.0 -
				     v[voxelzp] * 2.0   ) );
  
#else // Combination of the above two.
		     H.lamSize   * v[voxel] +
		     H.lamSmooth * ( v[voxel   ] * 6.0 -
				     v[voxelxmm] -
				     v[voxelymm] -
				     v[voxelzmm] -
				     v[voxelxpp] -
				     v[voxelypp] -
				     v[voxelzpp]        ) +
		       
		     H.lamSmoothP* ( v[voxel  ] * 12.0 -
				     v[voxelxm] * 2.0 -
				     v[voxelym] * 2.0 -
				     v[voxelzm] * 2.0 -
				     v[voxelxp] * 2.0 -
				     v[voxelyp] * 2.0 -
				     v[voxelzp] * 2.0   ) );
#endif
      }
}


double
normHessian(const Hessian& H) {
  
  int numVoxX ( H.numVoxX );
  int numVoxY ( H.numVoxY );
  int numVoxZ ( H.numVoxZ );
  
  int numVox ( numVoxX * numVoxY * numVoxZ );
  
  double norm (0.0);

  for(int i=0; i<numVox; ++i)
    norm += SQR(H.Hjj[i]) + SQR(H.Hjjp[i]) + SQR(H.Hjjpp[i]);

  return sqrt(norm);
}


/*
  This PSOLVE is for the unpreconditioned version, i.e. just does
  a vector copy ( B to X ) then returns.

  Arguments
  =========

  B       (input) DOUBLE PRECISION array, dimension N.
          On entry, right hand side vector B.
          Unchanged on exit.

  X       (output) DOUBLE PRECISION array, dimension N.
          Set to solution on output.
  BLAS:  DCOPY
  ============================================================

     .. Executable Statements ..

    Parameter adjustments
    --b;
    --x;

    Function Body
    dcopy_(&matdim_1.n, &b[1], &c__1, &x[1], &c__1);

    return 0;
*/


int
psolve(double* x, double* b) {
  memcpy(x, b, numVoxExtern*sizeof(double));
  return 0;
}


void
psolve_(double* x, double* b) {
  memcpy(x, b, numVoxExtern*sizeof(double));
}


int
matvec( double* done, double *v, double* dzero, double *w ) {
  mult( HExtern, v, w );
  return 0;
};  // H * v = w


void
matvec_( double* done, double *v, double* dzero, double *w ) {
  mult( HExtern, v, w );
};  // H * v = w




int
solveHessian(double* dispy, fvol* mri1, fvol* mri2,
	     const int& voxStep, const int& numVox, const int& nChunkZ,
	     const double& tol, const int& maxIter, const double& hessianErrorMax,
             const int nvoxNewZbdry,
	     const float& lambda1, const float& lambda2, const float& lambda2P, const float& h, const bool cubicInterp) {
  
  
  const int width    ( mri1->info.dim[1] );
  const int height   ( mri1->info.dim[0] );
  const int depth    ( mri1->info.dim[2] );
  const int numVoxX  ( width  / voxStep + (width  % voxStep ? 1 : 0) );
  const int numVoxY  ( height / voxStep + (height % voxStep ? 1 : 0) );
  const int numVoxZ  ( depth  / voxStep + (depth  % voxStep ? 1 : 0) );
  //const int numVox   ( numVoxX * numVoxY * numVoxZ );
  const double numVoxInv (1.0/numVox);
  
  const int overlapVox ( 4 ); // 4 or 3 is good. 2 would even do.
  int nzChunkVox ( numVoxZ/nChunkZ + ((numVoxZ % nChunkZ) ? 1 : 0) );      // This may be adjusted for the LAST chunk.
  
  Hessian hessian;
  hessian.numVoxX = numVoxX;                                               // Need these in mult().
  hessian.numVoxY = numVoxY;
  
  //bool bicgstabSuccess (true);
  
  vector<bool> chunkHessianError;
  
  for(int chunk = 0; chunk < nChunkZ; ++chunk) {
    
    int zaMin ( 0 );
    int zaMax ( numVoxZ );
    if(chunk > 0)
      zaMin =  chunk   *nzChunkVox-overlapVox < 0       ? 0       :  chunk    * nzChunkVox - overlapVox;
    if(chunk < nChunkZ-1)
      zaMax = (chunk+1)*nzChunkVox+overlapVox > numVoxZ ? numVoxZ : (chunk+1) * nzChunkVox + overlapVox;
    
#if 0
    int zaMax ( depth );
    if(chunk > 0)
      zaMin =  chunk   *nzChunkVox-overlapVox < 0     ? 0     :  chunk    * nzChunkVox - overlapVox;
    if(chunk < nChunkZ-1)
      zaMax = (chunk+1)*nzChunkVox+overlapVox > depth ? depth : (chunk+1) * nzChunkVox + overlapVox;
#endif
    int numVoxZb ( zaMax - zaMin );
    int numVoxb  ( numVoxX*numVoxY*numVoxZb );
    
    // redo this with a class, where constructor automatically takes care of allocating.
    hessian.Hjj         = new double[numVoxb];
    hessian.Hjjp        = new double[numVoxb];
    hessian.Hjjpp       = new double[numVoxb];
    hessian.dcostddispy = new double[numVoxb];
    hessian.numVoxZ     = numVoxZb;                                // NOTE the b!!
    hessian.lamSize     = numVoxInv*2.0*lambda1;                   // The 2.0 prefactor is from the square in the cost term
    hessian.lamSmooth   = numVoxInv*2.0*lambda2/SQR(2.0*voxStep);  // The 2.0 prefactor is from the square in the cost term
    hessian.lamSmoothP  = numVoxInv*2.0*lambda2P/SQR(2.0*voxStep); // The 2.0 prefactor is from the square in the cost term
    
    clock_t start1 ( clock() );
    
    setupHessian(hessian, dispy, voxStep, mri1, mri2, zaMin, zaMax, lambda1, lambda2, lambda2P, h, cubicInterp);
    
    clock_t secondsUsed1 ( (clock() - start1)/(CLOCKS_PER_SEC) );
//cout << "compute time SETUPHESSIAN (seconds): " << secondsUsed1 << endl;
    
    double normH = normHessian(hessian);
//    std::clog<<"normH = "<<normH<<std::endl;
    
    double* b ( hessian.dcostddispy );
    double* u ( new double[numVoxb] );           // For the new estimate of the negative increment to dispy[].
    memset(u, 0, numVoxb*sizeof(double));
    
    clock_t start ( clock() );
    
#if 1
    
    numVoxExtern = numVoxb;                      // Needed in psolve(), needed in bicgstabc().
    
    HExtern.numVoxX     = hessian.numVoxX;
    HExtern.numVoxY     = hessian.numVoxY;
    HExtern.numVoxZ     = hessian.numVoxZ;
    HExtern.Hjj         = hessian.Hjj;
    HExtern.Hjjp        = hessian.Hjjp;
    HExtern.Hjjpp       = hessian.Hjjpp;
    HExtern.dcostddispy = hessian.dcostddispy;
    HExtern.lamSize     = hessian.lamSize;
    HExtern.lamSmooth   = hessian.lamSmooth;
    HExtern.lamSmoothP  = hessian.lamSmoothP;
    
    int     iters       (maxIter);               // Iterate until residue < tol.
    double  resid       (tol);                   // resid will be recalculated in bicgstabTemplates().
    int     info        (0);
    double* work        (new double[numVoxb*7]); // For the '7', see header comment in bicgstabc.c.
    int     bicgstabErr (0);
    int     n           (numVoxb);
    
    // NOTE: bicgstabc() will return early if resid starts increasing.
    // See "if (*resid > residPrev)" in bicgstabc.c.
    
    short  enforceDecrease_short   ( 1 );    // ( enforceDecrease ? 1 : 0 );
    double bicgstabErrFac_nonConst ( 1.0 );  // 1.0 ( bicgstabErrFac );
    
    //bicgstabf_(&n, b, u, work, &n, &iters, &resid, matvec_, psolve_, &info);
    //bicgstabErr = bicgstabc(&n, b, u, work, &n, &iters, &resid, matvec, psolve, &info);
    bicgstabErr = bicgstabc(&n, b, u, work, &n, &iters, &resid, matvec, psolve, &info, enforceDecrease_short, bicgstabErrFac_nonConst);
//    std::clog<<"bicgstabErr = "<<bicgstabErr<<"\tresid = "<<resid<<"\titers = "<<iters<<"\tinfo = "<<info<<std::endl;
/*    
    if(info == -12)
      std::clog<<"bicgstabc() returned because the residue started increasing."<<std::endl;
*/
    delete[] work;
    
#else
    
    int iters = -1;
    iters = bicgstab(numVoxb, hessian, b, u, tol, true);   // hessian * u = b. Solve for u.
    // iters = cghs(numVoxb, hessian, b, u, tol, true);    // only defined for symmetric matrices.
    // iters = bicgsq(numVoxb, hessian, b, u, tol, true);
    // iters = gmres(M, numVoxb, hessian, b, u, tol, true);
    
#endif
    
    clock_t secondsUsed ( (clock() - start)/(CLOCKS_PER_SEC) );
    
    // Residue...
    double* v ( new double[numVoxb] );
    double* w ( new double[numVoxb] );

    mult(hessian, u, v);          // hessian * u = v
    
    for ( int i=0; i<numVoxb; ++i )
      w[i] = v[i]-b[i];           // NOTE: v[] should approx equal -b[].
    
    double c(0.0), d(0.0), e(0.0);
    for ( int i=0; i<numVoxb; ++i )
      c += w[i]*w[i];
    
    for ( int j=0; j<numVoxb; ++j )
      d += b[j]*b[j];
    
    for ( int j=0; j<numVoxb; ++j )
      e += v[j]*v[j];
    
    // redo this with a class, where destructor automatically takes care of deleting.    
    delete[] v;
    delete[] w;
    delete[] hessian.Hjj;         // Was allocated in setupHessian.cpp.
    delete[] hessian.Hjjp;        // Was allocated in setupHessian.cpp.
    delete[] hessian.Hjjpp;       // Was allocated in setupHessian.cpp.
    delete[] hessian.dcostddispy; // Was allocated in setupHessian.cpp.
    
    double error (sqrt(c));
/*
    cout << "iterations = " << iters
	 << "\nerror    = " << sqrt(c)
	 << "\nnorm(b)  = " << sqrt(d)
	 << "\nnorm(v)  = " << sqrt(e) << endl;
    
    cout << "compute time (seconds): " << secondsUsed << endl;
*/
    
    // Update dispy[] with u[], and handle error codes systematically....
    
    bool hessianSuccess ( (error < hessianErrorMax) ? true : false );
//    std::clog<<__FILE__<<__LINE__<<": hessianSuccess = "<<hessianSuccess<<std::endl;
    
    chunkHessianError.push_back(hessianSuccess);
    
//    if(bicgstabSuccess && hessianSuccess) {
      for(int xa = 0; xa < numVoxX; ++xa)
        for(int ya = 0; ya < numVoxY; ++ya)
	  for(int za = zaMin, zb = 0; za < zaMax; ++za, ++zb) {
	    
	    if(zaMin > 0 && (za-zaMin) < overlapVox)
	      continue;
	    if(zaMax < depth && za >= zaMax-overlapVox)
	      continue;
	    
	    int voxel ( xa*(numVoxY * numVoxZ)  + ya*numVoxZ  + za );
	    int voxelb( xa*(numVoxY * numVoxZb) + ya*numVoxZb + zb );
	    
	    dispy[voxel] -= u[voxelb];
	  }
//    }
    
    delete[] u;
    
  }
  
  
  // Fix up z-boundaries. (Recall, nvoxNewZbdry repeat layers were added in subjectMri.cpp)
  // Make the outer nvoxNewZbdry-layers identical to the (nvoxNewZbdry+1)th inner layer, at both z-boundaries.
  // This works only if voxStep==1. See also writeFullCorrectedVolumes.cpp.
  
  //const int nvoxNewZbdry ( 2 );
  
  // Lower z-bdry:  
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y) {
      
      int voxel ( x*(numVoxY * numVoxZ)  + y*numVoxZ  + nvoxNewZbdry );
      float dy ( dispy[voxel] );
      
      for(int z=0; z<nvoxNewZbdry; ++z) {
	int voxelZ ( x*(numVoxY * numVoxZ)  + y*numVoxZ  + z );
	dispy[voxelZ] = dy;
      }
    }
  
  
  // Upper z-bdry:
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y) {
      
      int voxel ( x*(numVoxY * numVoxZ)  + y*numVoxZ  + depth-1-nvoxNewZbdry );
      float dy ( dispy[voxel] );
      
      for(int z=depth-nvoxNewZbdry; z<depth; ++z) {
	int voxelZ ( x*(numVoxY * numVoxZ)  + y*numVoxZ  + z );
	dispy[voxelZ] = dy;
      }
    }
  
  
  int numFailed ( count(chunkHessianError.begin(), chunkHessianError.end(), false) );
  if( numFailed )
    std::clog<<__FILE__<<":\n"
	     <<numFailed<<" chunks had error in excess of hessianErrorMax ("
	     <<hessianErrorMax<<")"<<std::endl;
  
  return numFailed;
}

#undef SQR
