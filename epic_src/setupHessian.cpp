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

//////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// 	 NEED TO ADD GRADIENT TERM HERE!!!
// 
// 
// Cost function  f == f(dispy),  dispy == (dispy1,...,dispyN).
// 
// Calculate dfddispyi == partialDf/partialDdispyi,  0 <= i < numVox == N.
// 
// Point Pj == (xj,yj,zj), i.e., voxel coordinate. Let this have voxel index j:  Pj <==> j.
// 
// Consider point  Pjp  == (xj,yjp,zj)  ==  Pj + (0, dispy(Pj), 0)  ==  (xj, yj+dispy(Pj), zj)
//     and  point  Pjm  == (xj,yjp,zj)  ==  Pj - (0, dispy(Pj), 0)  ==  (xj, yj-dispy(Pj), zj)
// 
// i.e., yjp = yj + dispy(Pj),
// i.e., yjm = yj - dispy(Pj),
// 
// I1(Pjp) is intensity at point Pjp in volume1,
// I2(Pjm) is intensity at point Pjm in volume2.
// 
// f(dispy)  ==  SUM_(xj,yj,zj) { SQR( I1(Pjp) - I2(Pjm) ) },  suitably avoiding the boundary values of (xj,yj,zj).
// 
// This is the cost function, where  SUM_(xj,yj,zj) == SUM_Pj == SUM_j,
// voxel coords (xj,yj,zj) correspond to index j:  Pj <==> (xj,yj,zj) <==> j; dispy(Pj) == dispy[j].
// 
// Pjp = Pj + dispy[j] y^;   yjp = yj + dispy[j];
// Pjm = Pj - dispy[j] y^;   yjm = yj - dispy[j];
// 
// Let index i corespond to any voxel.
// dispyi == dispy[i], 0 <= i < numVox.
// 
// dfddispyi  ==  SUM_Pj{ 2*(I1(Pjp) - I2(Pjm) ) * ( (dI1(Pjp)/dyjp)*(dyjp/ddispyi) - (dI2(Pjm)/dyjm)*(dyjm/ddispyi) ) }.
// 
// But
// 
// dyjp/ddispyi  =   KroneckerDelta_ij,
// dyjm/ddispyi  =  -KroneckerDelta_ij,
// 
// dI1(Pjp)     I1(xj, yj+dispy(Pj)+h, zj) - I1(xj, yj+dispy(Pj)-h, zj)
// --------  =  -------------------------------------------------------,
// dyjp                                   2h
// 
// dI2(Pjm)     I2(xj, yj-dispy(Pj)+h, zj) - I2(xj, yj-dispy(Pj)-h, zj)
// --------  =  -------------------------------------------------------,
// dyjm                                   2h
// 
// where, e.g., h = 1.0 (1.0 ==> length of side of a voxel, or some fraction or multiple of this).
// 
// So,
// 
// dfddispyi  ==   2*(I1(Pip) - I2(Pim) ) * ( (dI1(Pip)/dyip) + (dI2(Pim)/dyim) ).
// 
// 
//////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <iostream>
#include <cmath>           // for fabs().
#include <cstring>         // for memset()
#include "hessian.h"
#include "interpolation.h" // CTX stuff. fvol

#ifndef SQR
#define SQR(a)   ((a)*(a))
#endif


void
setupHessian(Hessian&       hessian,
	     double*        dispy,
	     const int&     voxStep,
	     fvol*          vol1Mri,
	     fvol*          vol2Mri,
	     const int&     zaMin,
	     const int&     zaMax,
	     const double&  lambda1,
	     const double&  lambda2,
	     const double&  lambda2P,
	     const float&   h,
	     const bool     cubicInterp) {
  
  //  std::clog << "\nIn " << __FILE__ << std::endl;
  
  // These three quantities need to be set as input parameters.
  const INTERPMETHOD interpMethod ( cubicInterp ? CUBIC : LINEAR ); // NEAREST  LINEAR   CUBIC
  const INTERPEDGE   interpEdge   ( ZEROPAD );                       // MIRROR   ZEROPAD  THROWAWAY: Want MIRROR for wraparound.
  const int bPositive ( 1 );
  
  if(interpMethod == CUBIC)
    std::clog << __FILE__ << ":\n Using cubic interpolation...\n" << std::endl;
  
  double* dcostddispy (hessian.dcostddispy);   // Will be deleted in solveHessian.cpp.
  double* Hjj         (hessian.Hjj);           // Will be deleted in solveHessian.cpp.
  double* Hjjp        (hessian.Hjjp);          // Will be deleted in solveHessian.cpp.
  double* Hjjpp       (hessian.Hjjpp);         // Will be deleted in solveHessian.cpp.
  
  const int width  (vol1Mri->info.dim[1]);
  const int height (vol1Mri->info.dim[0]);
  const int depth  (vol1Mri->info.dim[2]);
  
  const int numVoxX ( width  / voxStep + (width  % voxStep ? 1 : 0) );
  const int numVoxY ( height / voxStep + (height % voxStep ? 1 : 0) );
  const int numVoxZ ( depth  / voxStep + (depth  % voxStep ? 1 : 0) );
  const int numVoxZb( zaMax - zaMin );
  
  const int numVox  ( numVoxX*numVoxY*numVoxZ );
  const int numVoxb ( numVoxX*numVoxY*numVoxZb );
  
  const double numVoxInv (1.0/numVox);
  
  const float voxStepInv ( 1.0/voxStep );
  const float dgwdw      ( 1.0/(2.0*voxStep) );
  
  memset(dcostddispy, 0, numVoxb*sizeof(double));
  memset(Hjj,         0, numVoxb*sizeof(double));
  memset(Hjjp,        0, numVoxb*sizeof(double));
  memset(Hjjpp,       0, numVoxb*sizeof(double));
  
  //int zb ( 0 );
  
  for(int xa = 0; xa < numVoxX; ++xa)
    for(int ya = 0; ya < numVoxY; ++ya)
      for(int za = zaMin, zb = 0; za < zaMax; ++za, ++zb) {
	//      for(int za = 0; za < numVoxZ; ++za) {
	
	hvec vox; // To be set repeatedly below.
	
	int voxel ( xa*(numVoxY * numVoxZ)  + ya*numVoxZ  + za );
	int voxelb( xa*(numVoxY * numVoxZb) + ya*numVoxZb + zb );
	
	float x   ( xa*voxStep );
	float y   ( ya*voxStep );
	float z   ( za*voxStep );
	float dy  ( dispy[voxel] );
	
	int   yam     ( (ya == 0 ? 0 : ya-1) );
	//int   yam     ( (ya == 0 ? numVoxY-1 : ya-1) );   // periodic in y  !!ONLY GUARANTEED TO WORK IF voxStep == 1 !!
	int   voxelym ( xa*(numVoxY * numVoxZ)  + yam*numVoxZ  + za );
	int   voxelbym( xa*(numVoxY * numVoxZb) + yam*numVoxZb + zb );
	float dym     ( dispy[voxelym] );
	float ym      ( yam*voxStep );
	
	int   yap     ( (ya == numVoxY-1 ? numVoxY-1 : ya+1) );
	//int   yap     ( (ya == numVoxY-1 ? 0 : ya+1) );   // periodic in y
	int   voxelyp ( xa*(numVoxY * numVoxZ)  + yap*numVoxZ  + za );
	int   voxelbyp( xa*(numVoxY * numVoxZb) + yap*numVoxZb + zb );
	float dyp     ( dispy[voxelyp] );
	float yp      ( yap*voxStep );
	
	float gy      ( (dyp - dym)/(2.0*voxStep) ); // Use this, and/or the following pair:
	float gyp     ( (dyp - dy )/(2.0*voxStep) ); // Could use just voxStep in denom, but using H.lamSmooth in mult() in solveHessian().
	float gym     ( (dy  - dym)/(2.0*voxStep) ); // ...or the following pair:
	//float ggyp    ( gyp*gyp );
	//float ggym    ( gym*gym );
	

	int   yamm    ( (yam == 0 ? 0 : yam-1) );
	//int   yamm    ( (yam == 0 ? numVoxY-1 : yam-1) ); // periodic in y
	int   voxelymm( xa*(numVoxY * numVoxZ) + yamm*numVoxZ + za );
	float dymm    ( dispy[voxelymm] );
	//float ymm     ( yamm*voxStep );
	
	int   yapp    ( (yap == numVoxY-1 ? numVoxY-1 : yap+1) );
	//int   yapp    ( (yap == numVoxY-1 ? 0 : yap+1) ); // periodic in y
	int   voxelypp( xa*(numVoxY * numVoxZ) + yapp*numVoxZ + za );
	float dypp    ( dispy[voxelypp] );
	//float ypp     ( yapp*voxStep );
	
	//float gyp     ( (dypp - dy  )/(2.0*voxStep) );
	//float gym     ( (dy   - dymm)/(2.0*voxStep) );
		
	int   xam     ( (xa == 0 ? 0 : xa-1) );
	//int   xam     ( (xa == 0 ? numVoxX-1 : xa-1) );   // periodic in x
	int   voxelxm ( xam*(numVoxY * numVoxZ)  + ya*numVoxZ  + za );
	int   voxelbxm( xam*(numVoxY * numVoxZb) + ya*numVoxZb + zb );
	float dxm     ( dispy[voxelxm] );
	//float xm      ( xam*voxStep );
	
	int   xap     ( (xa == numVoxX-1 ? numVoxX-1 : xa+1) );
	//int   xap     ( (xa == numVoxX-1 ? 0 : xa+1) );   // periodic in x
	int   voxelxp ( xap*(numVoxY * numVoxZ)  + ya*numVoxZ  + za );
	int   voxelbxp( xap*(numVoxY * numVoxZb) + ya*numVoxZb + zb );
	float dxp     ( dispy[voxelxp] );
	//float xp      ( xap*voxStep );
	
	float gx      ( (dxp - dxm)/(2.0*voxStep) );        // Use this, and/or the following pair:
	float gxp     ( (dxp - dy )/(2.0*voxStep) );
	float gxm     ( (dy  - dxm)/(2.0*voxStep) );        // ...or the following pair:
	//float ggxp    ( gxp*gxp );
	//float ggxm    ( gxm*gxm );
	
	int   zam     ( (za == 0 ? 0 : za-1) );
	//int   zam     ( (za == 0 ? numVoxZ-1 : za-1) );   // periodic in z
	int   zbm     ( (zb == 0 ? 0 : zb-1) );
	int   voxelzm ( xa*(numVoxY * numVoxZ)  + ya*numVoxZ  + zam );
	int   voxelbzm( xa*(numVoxY * numVoxZb) + ya*numVoxZb + zbm );
	float dzm     ( dispy[voxelzm] );
	//float zm      ( zam*voxStep );
	
	int   zap     ( (za == numVoxZ -1 ? numVoxZ -1 : za+1) );
	//int   zap     ( (za == numVoxZ -1 ? 0 : za+1) );  // periodic in z
	int   zbp     ( (zb == numVoxZb-1 ? numVoxZb-1 : zb+1) );
	int   voxelzp ( xa*(numVoxY * numVoxZ)  + ya*numVoxZ  + zap );
	int   voxelbzp( xa*(numVoxY * numVoxZb) + ya*numVoxZb + zbp );
	float dzp     ( dispy[voxelzp] );
	//float zp      ( zap*voxStep );
	
	//std::clog << __FILE__ << "\n:za = " << za << ";  zap = " << zap << std::endl;
	
	float gz      ( (dzp - dzm)/(2.0*voxStep) );        // Use this, and/or the following pair:
	float gzp     ( (dzp - dy )/(2.0*voxStep) );
	float gzm     ( (dy  - dzm)/(2.0*voxStep) );        // ...or the following pair:
	//float ggzp    ( gzp*gzp );
	//float ggzm    ( gzm*gzm );
	
	
#if 1	// double gradTerm ( lambda2 * (gx*gx + gy*gy + gz*gz) ); This is the standard one.
	dcostddispy[voxelbxm]  +=  numVoxInv * 2.0 * lambda2 * gx * (-dgwdw); // == dGradTerm/d(dxm)
	dcostddispy[voxelbxp]  +=  numVoxInv * 2.0 * lambda2 * gx * ( dgwdw); // == dGradTerm/d(dxp)
	
	dcostddispy[voxelbym]  +=  numVoxInv * 2.0 * lambda2 * gy * (-dgwdw); // Etc.
	dcostddispy[voxelbyp]  +=  numVoxInv * 2.0 * lambda2 * gy * ( dgwdw);
	
	dcostddispy[voxelbzm]  +=  numVoxInv * 2.0 * lambda2 * gz * (-dgwdw);
	dcostddispy[voxelbzp]  +=  numVoxInv * 2.0 * lambda2 * gz * ( dgwdw);	
#endif
	
	// CAN COMBIE THE ABOVE WITH THE FOLLOWING.
	// OR USE EITHER THE ABOVE OR THE FOLLOWING.
	// See aslo mult() in solveHessian().
	
#if 1	//double gradTerm = lambda2P * ((gxp*gxp+gxm*gxm) + (gyp*gyp+gym*gym) + (gzp*gzp+gzm*gzm));
	dcostddispy[voxelb]   = numVoxInv * 2.0*lambda2P*( 1.0/(2.0*voxStep) )*( 2.0*gxm - 2.0*gxp +
										 2.0*gym - 2.0*gyp +
										 2.0*gzm - 2.0*gzp  ); // == d(GradTerm)/d(dy)	
#endif



#if 0	// NOT TESTED!!! double gradTerm = lambda * (SQR(ggxp+ggxm) + SQR(ggyp+ggym) + SQR(ggzp+ggzm));
	dcostddispy[voxelb]   += 2.0*lambda2*( (ggxp+ggxm) * 2.0 * ( gxp*(-voxStepInv) + gxm*voxStepInv ) +
					       (ggyp+ggym) * 2.0 * ( gyp*(-voxStepInv) + gym*voxStepInv ) +
					       (ggzp+ggzm) * 2.0 * ( gzp*(-voxStepInv) + gzm*voxStepInv ) ); // == d(GradTerm)/d(dy)	
#endif


	// Gradient, wrt minimization parameters, of main merit term
	// in cost function.
	
	float val1y (0.0);
	//float ypdy ( y+dy < -0.5 ? ((height-1.0)+0.5 - (-0.5-(y+dy))) : ( y+dy >= (height-1.0)+0.5 ? -0.5 + ((y+dy)-((height-1.0)+0.5)) : y+dy ) );
	//float ypdy ( y+dy < -0.5 ? (height+(y+dy)) : ( y+dy >= height-0.5 ? ((y+dy)-height) : y+dy ) );
	hVecInit(&vox, y+dy, x, z, 1.0);
	GetVxlVal(&vox, &val1y, vol1Mri, interpMethod, interpEdge, bPositive);
	
	float val2y (0.0);
	hVecInit(&vox, y-dy, x, z, 1.0);
	GetVxlVal(&vox, &val2y, vol2Mri, interpMethod, interpEdge, bPositive);
	
	float val1y_hp (0.0);
	hVecInit(&vox, y+dy+h, x, z, 1.0);
	GetVxlVal(&vox, &val1y_hp, vol1Mri, interpMethod, interpEdge, bPositive);
	float val1y_hm (0.0);
	hVecInit(&vox, y+dy-h, x, z, 1.0);
	GetVxlVal(&vox, &val1y_hm, vol1Mri, interpMethod, interpEdge, bPositive);
	float dI1ydpy ( (val1y_hp - val1y_hm)/(2.0*h) );

	float val2y_hp (0.0);
	hVecInit(&vox, y-dy+h, x, z, 1.0);
	GetVxlVal(&vox, &val2y_hp, vol2Mri, interpMethod, interpEdge, bPositive);
	float val2y_hm (0.0);
	hVecInit(&vox, y-dy-h, x, z, 1.0);
	GetVxlVal(&vox, &val2y_hm, vol2Mri, interpMethod, interpEdge, bPositive);
	float dI2ydmy ( (val2y_hp - val2y_hm)/(2.0*h) );
	
	//Calculate gradient of I1 wrt dy at y+dy+h (dI1yhpdpy), and at y+dy-h (dI1yhmdpy)
	//so as to calculate the 2nd derivative if I1 at y+dy, i.e.,
	//ddI1ydpydpy = (dI1yhpdpy - dI1yhmdpy)/(2.0*h).
	float val1yhp_hp (0.0);
	hVecInit(&vox, y+dy+2.0*h, x, z, 1.0);
	GetVxlVal(&vox, &val1yhp_hp, vol1Mri, interpMethod, interpEdge, bPositive);
	float val1yhp_hm (val1y);
	float dI1yhpdpy ( (val1yhp_hp - val1yhp_hm)/(2.0*h) );
	
	float val1yhm_hp (val1y);
	float val1yhm_hm (0.0);
	hVecInit(&vox, y+dy-2.0*h, x, z, 1.0);
	GetVxlVal(&vox, &val1yhm_hm, vol1Mri, interpMethod, interpEdge, bPositive);
	float dI1yhmdpy ( (val1yhm_hp - val1yhm_hm)/(2.0*h) );
	
	float ddI1ydpydpy ( (dI1yhpdpy - dI1yhmdpy)/(2.0*h) );
	
	//Calculate gradient of I2 wrt dy at y-dy+h (dI2yhpdmy), and at y-dy-h (dI2yhmdmy)
	//so as to calculate the 2nd derivative if I2 at y-dy, i.e.,
	//ddI2ydmydmy = (dI2yhpdmy - dI2yhmdmy)/(2.0*h).
	float val2yhp_hp (0.0);
	hVecInit(&vox, y-dy+2.0*h, x, z, 1.0);
	GetVxlVal(&vox, &val2yhp_hp, vol2Mri, interpMethod, interpEdge, bPositive);
	float val2yhp_hm (val2y);
	float dI2yhpdmy ( (val2yhp_hp - val2yhp_hm)/(2.0*h) );
	
	float val2yhm_hp (val2y);
	float val2yhm_hm (0.0);
	hVecInit(&vox, y-dy-2.0*h, x, z, 1.0);
	GetVxlVal(&vox, &val2yhm_hm, vol2Mri, interpMethod, interpEdge, bPositive);
	float dI2yhmdmy ( (val2yhm_hp - val2yhm_hm)/(2.0*h) );
	
	float ddI2ydmydmy ( (dI2yhpdmy - dI2yhmdmy)/(2.0*h) );
	
	
	float val1yp (0.0);
	hVecInit(&vox, yp+dyp, x, z, 1.0);
	GetVxlVal(&vox, &val1yp, vol1Mri, interpMethod, interpEdge, bPositive);
	
	float val2yp (0.0);
	hVecInit(&vox, yp-dyp, x, z, 1.0);
	GetVxlVal(&vox, &val2yp, vol2Mri, interpMethod, interpEdge, bPositive);
	
	float val1yp_hp (0.0);
	hVecInit(&vox, yp+dyp+h, x, z, 1.0);
	GetVxlVal(&vox, &val1yp_hp, vol1Mri, interpMethod, interpEdge, bPositive);
	float val1yp_hm (0.0);
	hVecInit(&vox, yp+dyp-h, x, z, 1.0);
	GetVxlVal(&vox, &val1yp_hm, vol1Mri, interpMethod, interpEdge, bPositive);
	float dI1ypdpyp ( (val1yp_hp - val1yp_hm)/(2.0*h) );
	
	float val2yp_hp (0.0);
	hVecInit(&vox, yp-dyp+h, x, z, 1.0);
	GetVxlVal(&vox, &val2yp_hp, vol2Mri, interpMethod, interpEdge, bPositive);
	float val2yp_hm (0.0);
	hVecInit(&vox, yp-dyp-h, x, z, 1.0);
	GetVxlVal(&vox, &val2yp_hm, vol2Mri, interpMethod, interpEdge, bPositive);
	float dI2ypdmyp ( (val2yp_hp - val2yp_hm)/(2.0*h) );
	
	
	float val1ym (0.0);
	hVecInit(&vox, ym+dym, x, z, 1.0);
	GetVxlVal(&vox, &val1ym, vol1Mri, interpMethod, interpEdge, bPositive);
	
	float val2ym (0.0);
	hVecInit(&vox, ym-dym, x, z, 1.0);
	GetVxlVal(&vox, &val2ym, vol2Mri, interpMethod, interpEdge, bPositive);
#if 0
	float val1ym_hp (0.0);
	hVecInit(&vox, ym+dym+h, x, z, 1.0);
	GetVxlVal(&vox, &val1ym_hp, vol1Mri, interpMethod, interpEdge, bPositive);
	float val1ym_hm (0.0);
	hVecInit(&vox, ym+dym-h, x, z, 1.0);
	GetVxlVal(&vox, &val1ym_hm, vol1Mri, interpMethod, interpEdge, bPositive);
	float dI1ymdpym ( (val1ym_hp - val1ym_hm)/(2.0*h) );
	
	float val2ym_hp (0.0);
	hVecInit(&vox, ym-dym+h, x, z, 1.0);
	GetVxlVal(&vox, &val2ym_hp, vol2Mri, interpMethod, interpEdge, bPositive);
	float val2ym_hm (0.0);
	hVecInit(&vox, ym-dym-h, x, z, 1.0);
	GetVxlVal(&vox, &val2ym_hm, vol2Mri, interpMethod, interpEdge, bPositive);
	float dI2ymdmym ( (val2ym_hp - val2ym_hm)/(2.0*h) );
#endif
	
	
	/* 
	   COULD HAVE:
	   
	   (1)
	   const float widtha ( voxStep );                           // Original width of all voxels.
	   WITH
	   float widthb1y   ( widtha+( dyp-dym)*voxStepInv/2.0 );    // New width of current voxel, y, in vol1.
	   float widthb2y   ( widtha+(-dyp+dym)*voxStepInv/2.0 );    // New width of current voxel, y, in vol2.
	   ETC
	   
	   INSTEAD OF:
	   
	   (2)
	   const float widtha ( 2*voxStep );                         // Original width around all voxels.
	   WITH
	   float widthb1y   ( widtha+2*( dyp-dym)*voxStepInv/2.0 );  // New width around current voxel, y, in vol1.
	   float widthb2y   ( widtha+2*(-dyp+dym)*voxStepInv/2.0 );  // New width around current voxel, y, in vol2.
	   ETC
	   
	   TO USE (1), SHOULD HAVE
	   dwidthb1yddyp   (  voxStepInv/2.0 );
	   ETC.
	   
	   TO USE (2), SHOULD HAVE
	   dwidthb1yddyp   (  voxStepInv );
	   ETC.
	   
	   CURRENTLY, (2) FUNCTIONES CORRECTLY IN THIS CODE. TO
	   IMPLEMENT (1), NEED TO HALVE THE DERIVATIVES dwidthb1yddyp,
	   ETC.
	*/
	
	
	
	
	//float voxStepInv ( 1.0/voxStep );                     // == dwidthbdym = -dwidthbdyp.
	//const float widtha ( 1.0 );                           // Original width of all voxels.
	const float widtha ( 2*voxStep );                         // Original width of all voxels.
	float widthb1y   ( widtha+2*( dyp-dym)*voxStepInv/2.0 );  // New width of current voxel, y, in vol1.
	float widthb2y   ( widtha+2*(-dyp+dym)*voxStepInv/2.0 );  // New width of current voxel, y, in vol2.
				  		      
	float widthb1yp  ( widtha+2*( dypp-dy)*voxStepInv/2.0 );  // New width of voxel yp in vol1.
	float widthb2yp  ( widtha+2*(-dypp+dy)*voxStepInv/2.0 );  // New width of voxel yp in vol2.	
				  		      
	float widthb1ym  ( widtha+2*( dy-dymm)*voxStepInv/2.0 );  // New width of voxel ym in vol1.
	float widthb2ym  ( widtha+2*(-dy+dymm)*voxStepInv/2.0 );  // New width of voxel ym in vol2.	
	
	
	// Can represent fabs(y(x)) as sqrt(SQR(y(x))) to see the role
	// of the sign of y in the derivative of fabs(y(x)).
	float signWidthb1y    ( (widthb1y >= 0.0) ? 1.0 : -1.0 );
	float signWidthb2y    ( (widthb2y >= 0.0) ? 1.0 : -1.0 );
	
	float signWidthb1yp   ( (widthb1yp >= 0.0) ? 1.0 : -1.0 );
	float signWidthb2yp   ( (widthb2yp >= 0.0) ? 1.0 : -1.0 );
	
	float signWidthb1ym   ( (widthb1ym >= 0.0) ? 1.0 : -1.0 );
	float signWidthb2ym   ( (widthb2ym >= 0.0) ? 1.0 : -1.0 );
	
	//float dwidthb1yddym   ( -voxStepInv );
	float dwidthb1yddyp   (  voxStepInv );
	
	//float dwidthb2yddym   (  voxStepInv );
	float dwidthb2yddyp   ( -voxStepInv );
	
	float dwidthb1ypddy   ( -voxStepInv );
	float dwidthb1ypddypp (  voxStepInv );

	float dwidthb2ypddy   (  voxStepInv );
	float dwidthb2ypddypp ( -voxStepInv );
	
	//float dwidthb1ymddymm ( -voxStepInv );
	float dwidthb1ymddy   (  voxStepInv );
	
	//float dwidthb2ymddymm (  voxStepInv );
	float dwidthb2ymddy   ( -voxStepInv );
	
	// fabs(widthb1y/widtha) gives the relative change in intensity due to local squishing or expansion.
	float intensityCosty           ( fabs(widthb1y /widtha)*val1y                   - fabs(widthb2y /widtha)*val2y  );
	float intensityCostym          ( fabs(widthb1ym/widtha)*val1ym                  - fabs(widthb2ym/widtha)*val2ym );
	float intensityCostyp          ( fabs(widthb1yp/widtha)*val1yp                  - fabs(widthb2yp/widtha)*val2yp );
	
	float  dIntensityCostyddy      ( fabs(widthb1y/widtha)*dI1ydpy                  + fabs(widthb2y/widtha)*dI2ydmy );
	//float  dIntensityCostyddym     ( signWidthb1y*(dwidthb1yddym/widtha)*val1y      - signWidthb2y*(dwidthb2yddym/widtha)*val2y );
	float  dIntensityCostyddyp     ( signWidthb1y*(dwidthb1yddyp/widtha)*val1y      - signWidthb2y*(dwidthb2yddyp/widtha)*val2y );
	
	// 2nd deriv of of intensityCosty wrt dy, involving 2nd deriv of I1 (ddI1ydpydpy) and of I2 (ddI2ydmydmy).
	float ddIntensityCostyddyddy   ( fabs(widthb1y/widtha)*ddI1ydpydpy              + fabs(widthb2y/widtha)*ddI2ydmydmy );
	
	//float ddIntensityCostyddyddym  ( signWidthb1y*(dwidthb1yddym/widtha)*dI1ydpy    + signWidthb2y*(dwidthb2yddym/widtha)*dI2ydmy );
	float ddIntensityCostyddyddyp  ( signWidthb1y*(dwidthb1yddyp/widtha)*dI1ydpy    + signWidthb2y*(dwidthb2yddyp/widtha)*dI2ydmy );
	
	float  dIntensityCostypddy     ( signWidthb1yp*(dwidthb1ypddy/widtha)*val1yp    - signWidthb2yp*(dwidthb2ypddy/widtha)*val2yp );
	float  dIntensityCostypddyp    ( fabs(widthb1yp/widtha)*dI1ypdpyp               + fabs(widthb2yp/widtha)*dI2ypdmyp );
	float  dIntensityCostypddypp   ( signWidthb1yp*(dwidthb1ypddypp/widtha)*val1yp  - signWidthb2yp*(dwidthb2ypddypp/widtha)*val2yp );
	float ddIntensityCostypddyddyp ( signWidthb1yp*(dwidthb1ypddy/widtha)*dI1ypdpyp + signWidthb2yp*(dwidthb2ypddy/widtha)*dI2ypdmyp );
	
	float  dIntensityCostymddy     ( signWidthb1ym*(dwidthb1ymddy/widtha)*val1ym    - signWidthb2ym*(dwidthb2ymddy/widtha)*val2ym );
	//float  dIntensityCostymddym    ( fabs(widthb1ym/widtha)*dI1ymdpym               + fabs(widthb2ym/widtha)*dI2ymdmym );
	//float  dIntensityCostymddymm   ( signWidthb1ym*(dwidthb1ymddymm/widtha)*val1ym  - signWidthb2ym*(dwidthb2ymddymm/widtha)*val2ym );
	//float ddIntensityCostymddyddym ( signWidthb1yp*(dwidthb1ymddy/widtha)*dI1ymdpym + signWidthb2ym*(dwidthb2ymddy/widtha)*dI2ymdmym );
	
	// y-term in merit function (ignoring smoothing part):
	//float termy ( numVoxInv * intensityCosty * intensityCosty );
	
	// 1st derivatve wrt dy of y-term in merit function (ignoring smoothing part):
	float dtermyddy ( numVoxInv * 2.0 * intensityCosty * dIntensityCostyddy );
	
	// derivative of (1st derivatve wrt dy of y-term in merit function (ignoring smoothing part)), i.e., relevant...
	// 2nd derivatves of y-term in merit function (ignoring smoothing part):
	float ddtermyddyddy   ( numVoxInv * 2.0 * ( dIntensityCostyddy  *  dIntensityCostyddy     +
						    intensityCosty * ddIntensityCostyddyddy         ) );
	//float ddtermyddyddym  ( numVoxInv * 2.0 * (  intensityCosty     * ddIntensityCostyddyddym +
	//				 	    dIntensityCostyddym *  dIntensityCostyddy       ) );
	float ddtermyddyddyp  ( numVoxInv * 2.0 * (  intensityCosty     * ddIntensityCostyddyddyp +
						    dIntensityCostyddyp *  dIntensityCostyddy       ) );
	
	// ym-term in merit function (ignoring smoothing part):
	//float termym ( numVoxInv * intensityCostym * intensityCostym );
	
	// 1st derivatve wrt dy of ym-term in merit function (ignoring smoothing part):
	float dtermymddy ( numVoxInv * 2.0 * intensityCostym * dIntensityCostymddy );
	
	// derivative of (1st derivatve wrt dy of ym-term in merit function (ignoring smoothing part)), i.e., relevant...
	// 2nd derivatves of ym-term in merit function (ignoring smoothing part):
	float ddtermymddyddy   ( numVoxInv * 2.0 *   dIntensityCostymddy  *  dIntensityCostymddy         );
	//float ddtermymddyddym  ( numVoxInv * 2.0 * (  intensityCostym     * ddIntensityCostymddyddym +
	//					     dIntensityCostymddym *  dIntensityCostymddy       ) );
	//float ddtermymddyddymm ( numVoxInv * 2.0 *   dIntensityCostymddymm *  dIntensityCostymddy       );
	
	
	// yp-term in merit function (ignoring smoothing part):
	//float termyp ( numVoxInv * intensityCostyp * intensityCostyp );
	
	// 1st derivatve wrt dy of yp-term in merit function (ignoring smoothing part):
	float dtermypddy ( numVoxInv * 2.0 * intensityCostyp * dIntensityCostypddy );
	
	// derivative of (1st derivatve wrt dy of yp-term in merit function (ignoring smoothing part)), i.e., relevant...
	// 2nd derivatves of yp-term in merit function (ignoring smoothing part):
	float ddtermypddyddy   ( numVoxInv * 2.0 *   dIntensityCostypddy   *  dIntensityCostypddy         );
	float ddtermypddyddyp  ( numVoxInv * 2.0 * (  intensityCostyp      * ddIntensityCostypddyddyp +
						     dIntensityCostypddyp  *  dIntensityCostypddy       ) );
	float ddtermypddyddypp ( numVoxInv * 2.0 *   dIntensityCostypddypp *  dIntensityCostypddy         );
	
	float dLambda1Termdy   ( numVoxInv * 2.0 * lambda1 * dy );
	
	// Load 1st derivative of merit function. Include 1st derivative wrt dy of "double scaleTerm( lambda1 * dy * dy );"
	// Note: The lambda2 (and lambda2P) terms were already calculated and added above.
	dcostddispy[voxelb] += dtermyddy + dtermymddy + dtermypddy + dLambda1Termdy;
	
	
	// Load the second derivatives into arrays...note that the Hessian is symmetric.
	Hjj  [voxelb] = ddtermyddyddy  + ddtermymddyddy + ddtermypddyddy; // == H[voxel][voxel]    = d2M/dydy
	Hjjp [voxelb] = ddtermyddyddyp + ddtermypddyddyp;                 // == H[voxel][voxelyp]  = d2M/dydyp  = d2M/dypdy
	Hjjpp[voxelb] = ddtermypddyddypp;                                 // == H[voxel][voxelypp] = d2M/dydypp = d2M/dyppdy
      //Hjjm [voxel] = ddtermyddyddym + ddtermymddyddym;                 // == H[voxel][voxelym]  = d2M/dydym   NO NEED TO STORE THESE
      //Hjjmm[voxel] = ddtermymddyddymm;                                 // == H[voxel][voxelymm] = d2M/dydymm  NO NEED TO STORE THESE
	
	// Note: the 2nd derivatives (a bunch of Kronecker deltas) of
	// the smoothing term(s) in the cost function have yet to be
	// included in the Hessian. Defer this little exercise to the
	// maxtrix-vector multiplication routine (mult() in
	// solveHessian.cpp). Also defer to mult() in solveHessian.cpp
	// the inclusion of the 2nd derivative (another Kronecker
	// delta) of the scale (i.e., lambda1) term in the Hessian.
	
      }
}

#undef SQR
