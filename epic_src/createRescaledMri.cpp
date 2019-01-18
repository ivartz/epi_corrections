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

#include <string.h>
#include <iostream>
#include "createRescaledMri.h"
#include "interpolation.h"     // CTX stuff. fvol

using std::string;
using std::clog;
using std::endl;


//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
// See rescaleMri.cpp. NOTE: these routines do not change the center LPH
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////


fvol*
createRescaledMri(fvol* volT, fvol* volS, const bool fillData, const bool useCubic) {
  
  if(!volS || !volT)
    return 0; // Nothing to do.
  
  int widthT   ( volT->info.dim[1] );
  int heightT  ( volT->info.dim[0] );
  int depthT   ( volT->info.dim[2] );
  
  float xsizeT ( volT->info.vxlsize[1] );
  float ysizeT ( volT->info.vxlsize[0] );
  float zsizeT ( volT->info.vxlsize[2] );
  
  return ( createRescaledMri(widthT, heightT, depthT, xsizeT, ysizeT, zsizeT, volS, fillData, useCubic) );
}


////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////// O V E R L O A D I N G ///////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////


fvol*
createRescaledMri(const int   widthC, const int   heightC, const int   depthC,
		  const float xsizeC, const float ysizeC,  const float zsizeC, fvol* volS, const bool fillData, const bool useCubic) {
  
  
  const INTERPMETHOD interpMethod ( useCubic ? CUBIC : LINEAR ); // NEAREST  LINEAR   CUBIC
  const INTERPEDGE   interpEdge   ( ZEROPAD );                    // MIRROR   ZEROPAD  THROWAWAY: Want MIRROR for wraparound.
  
  if(!volS)
    return 0; // Nothing to do.
  
  int widthS  ( volS->info.dim[1] );
  int heightS ( volS->info.dim[0] );
  int depthS  ( volS->info.dim[2] );
  
  float xsizeS ( volS->info.vxlsize[1] );
  float ysizeS ( volS->info.vxlsize[0] );
  float zsizeS ( volS->info.vxlsize[2] );
  
  if( widthS  == widthC  &&
      heightS == heightC &&
      depthS  == depthC  &&
      xsizeS  == xsizeC  &&
      ysizeS  == ysizeC  &&
      zsizeS  == zsizeC ) {
    
    int bcopydata  ( fillData ? 1 : 0 );
    
    return ( fVolCopy(volS, bcopydata) );
  }
  
  clog<<__FILE__<<":\n"
      <<"widthS  = "<<widthS <<"\t"<<"widthC  = "<<widthC <<"\n"
      <<"heightS = "<<heightS<<"\t"<<"heightC = "<<heightC<<"\n"
      <<"depthS  = "<<depthS <<"\t"<<"depthC  = "<<depthC <<"\n\n"
      <<"xsizeS  = "<<xsizeS <<"\t"<<"xsizeC  = "<<xsizeC <<"\n"
      <<"ysizeS  = "<<ysizeS <<"\t"<<"ysizeC  = "<<ysizeC <<"\n"
      <<"zsizeS  = "<<zsizeS <<"\t"<<"zsizeC  = "<<zsizeC <<endl;
  
  if(widthC  != widthS)  clog<<"widthC-widthS   = "<<widthC-widthS  <<endl;
  if(heightC != heightS) clog<<"heightC-heightS = "<<heightC-heightS<<endl;
  if(depthC  != depthS)  clog<<"depthC-depthS   = "<<depthC-depthS  <<endl;
  
  if(xsizeC != xsizeS)   clog<<"xsizeC-xsizeS   = "<<xsizeC-xsizeS<<endl;
  if(ysizeC != ysizeS)   clog<<"ysizeC-ysizeS   = "<<ysizeC-ysizeS<<endl;
  if(zsizeC != zsizeS)   clog<<"zsizeC-zsizeS   = "<<zsizeC-zsizeS<<endl;
  
  clog<<__FILE__<<"\nRescaling image...\n"<<endl;
  if(useCubic)
    clog<<__FILE__<<"\nUsing cubic interpolation...\n"<<endl;
  
  ///////////////////////////////////////////////
  // Create a new volA to hold the rescaled volS.
  
  float ysizeA ( ysizeC ); // NEW voxel size
  float xsizeA ( xsizeC );
  float zsizeA ( zsizeC );
  
  float y_lA ( hMatGetVal(&(volS->info.M_vxl2lph), 0, 0)/ysizeS ); // OLD direction cosines
  float y_pA ( hMatGetVal(&(volS->info.M_vxl2lph), 1, 0)/ysizeS );
  float y_hA ( hMatGetVal(&(volS->info.M_vxl2lph), 2, 0)/ysizeS );
  
  float x_lA ( hMatGetVal(&(volS->info.M_vxl2lph), 0, 1)/xsizeS ); // OLD
  float x_pA ( hMatGetVal(&(volS->info.M_vxl2lph), 1, 1)/xsizeS );
  float x_hA ( hMatGetVal(&(volS->info.M_vxl2lph), 2, 1)/xsizeS );
  
  float z_lA ( hMatGetVal(&(volS->info.M_vxl2lph), 0, 2)/zsizeS ); // OLD
  float z_pA ( hMatGetVal(&(volS->info.M_vxl2lph), 1, 2)/zsizeS );
  float z_hA ( hMatGetVal(&(volS->info.M_vxl2lph), 2, 2)/zsizeS );
  
  // Build new vox --> lph matrix, Mvxl2lphA, for volA using the
  // NEW voxel sizes and the OLD direction cosines.
  
  hmat Mvxl2lphA;
  hMatEye(&Mvxl2lphA);
  
  hmat Mpat2grad;
  hMatEye(&Mpat2grad);
  
  hvec rvec, cvec, dvec;
  
  hVecInit(&rvec, ysizeA*y_lA, ysizeA*y_pA, ysizeA*y_hA, 0);
  hMatSetCol(&Mvxl2lphA, &rvec, 0);
  
  hVecInit(&cvec, xsizeA*x_lA, xsizeA*x_pA, xsizeA*x_hA, 0);
  hMatSetCol(&Mvxl2lphA, &cvec, 1);
  
  hVecInit(&dvec, zsizeA*z_lA, zsizeA*z_pA, zsizeA*z_hA, 0);
  hMatSetCol(&Mvxl2lphA, &dvec, 2);
  
  int heightA  ( heightC );  // NEW
  int widthA   ( widthC  );
  int depthA   ( depthC  );
  
  int dimA[3] = {heightA, widthA, depthA};
  
  hvec cent_vxlS; // OLD
  hVecInit(&cent_vxlS, (heightS-1.0)/2.0, (widthS-1.0)/2.0, (depthS-1.0)/2.0, 1.0);
  
  hvec cent_lph;  // OLD; volA will have same c_l, c_p, c_h (or c_r, c_a, c_s) as volS.
  hMatMultiplyhVec(&(volS->info.M_vxl2lph), &cent_vxlS, &cent_lph);
  
  hVecSetVal(&cent_lph, 3, 0.0); // Change 4th component of cent_lph from 1.0 to 0.0
  
  hvec cent_vxlANeg;
  hVecInit(&cent_vxlANeg, -(heightA-1.0)/2.0, -(widthA-1.0)/2.0, -(depthA-1.0)/2.0, 1.0);
  
  hvec T1, T;
  hMatMultiplyhVec(&Mvxl2lphA, &cent_vxlANeg, &T1);
  hVecAdd(&T1, &cent_lph, &T);
  hMatSetCol(&Mvxl2lphA, &T, 3);
  
  fvol* volA( fVolNew(dimA, &Mvxl2lphA, &Mpat2grad, NULL) ); // The new image as a tabla raza.
  
  // Now, load up volA with volS rescaled to fit the sepcified dimensions.
  
  hvec lph, voxS, voxA;
  hmat lph2VoxS;
  hMatInverse(&(volS->info.M_vxl2lph), &lph2VoxS); // volS->info.M_vxl2lph is vox --> lph matrix for volS.
  
  if( fillData )
    for(int i=0; i<heightA; ++i)
      for(int j=0; j<widthA; ++j)
	for(int k=0; k<depthA; ++k) {
	  
	  hVecInit(&voxA, i, j, k, 1.0);
	  hMatMultiplyhVec(&Mvxl2lphA, &voxA, &lph);
	  hMatMultiplyhVec(&lph2VoxS, &lph, &voxS);
	  
	  float valS ( 0.0 );
	  int bPositive ( 1 );
	  
	  GetVxlVal(&voxS, &valS, volS, interpMethod, interpEdge, bPositive); // THROWAWAY or ZEROPAD
	  
	  fVolSetVal(volA, i, j, k, valS);
	}  
  
  return volA;
  
}



/**********************************************************************************************************************
 **********************************************************************************************************************
 **********************************************************************************************************************
#define MRIgetVoxelToRasXform   extract_i_to_r
#define MRIgetRasToVoxelXform   extract_r_to_i

MATRIX *extract_r_to_i(MRI *mri)
{
  MATRIX *m_ras_to_voxel, *m_voxel_to_ras ;

  m_voxel_to_ras = extract_i_to_r(mri) ;
  m_ras_to_voxel = MatrixInverse(m_voxel_to_ras, NULL) ;
  MatrixFree(&m_voxel_to_ras) ;
  return(m_ras_to_voxel) ;
}
  

MATRIX *extract_i_to_r(MRI *mri)
{
  MATRIX *m;
  float m11, m12, m13, m14;
  float m21, m22, m23, m24;
  float m31, m32, m33, m34;
  float ci, cj, ck;

  m = MatrixAlloc(4, 4, MATRIX_REAL);
  if(m == NULL)
  {
    ErrorReturn(NULL, (ERROR_BADPARM, "extract_i_to_r(): error allocating matrix"));
  }

  m11 = mri->info.vxlsize[1] * mri->x_r;  m12 = mri->info.vxlsize[0] * mri->y_r;  m13 = mri->info.vxlsize[2] * mri->z_r;
  m21 = mri->info.vxlsize[1] * mri->x_a;  m22 = mri->info.vxlsize[0] * mri->y_a;  m23 = mri->info.vxlsize[2] * mri->z_a;
  m31 = mri->info.vxlsize[1] * mri->x_s;  m32 = mri->info.vxlsize[0] * mri->y_s;  m33 = mri->info.vxlsize[2] * mri->z_s;

  ci = (mri->info.dim[1]) / 2.0;
  cj = (mri->info.dim[0]) / 2.0;
  ck = (mri->info.dim[2]) / 2.0;
  
  m14 = mri->c_r - (m11 * ci + m12 * cj + m13 * ck);
  m24 = mri->c_a - (m21 * ci + m22 * cj + m23 * ck);
  m34 = mri->c_s - (m31 * ci + m32 * cj + m33 * ck);

  stuff_four_by_four(m, m11, m12, m13, m14, 
		        m21, m22, m23, m24, 
		        m31, m32, m33, m34, 
		        0.0, 0.0, 0.0, 1.0);

  return(m);

}
***********************************************************************************************************************
***********************************************************************************************************************
***********************************************************************************************************************/
