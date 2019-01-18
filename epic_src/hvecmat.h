///////////////////////////////////////////////////////////////////////
// This source code is Copyright ©2007-2010 CorTechs Labs
// Inc. Permission is granted by CorTechs Labs to copy, distribute and
// modify this source code, provided that it is used for research
// purposes only, and only by not-for-profit organizations, and
// further provided that:
// 
//    * this copyright notice appears in all copies.
//    * you indemnify and hold harmless CorTechs Labs and its
//      successors and associates from any and all liability from any
//      use of the information.
//    * you ensure that these conditions apply to any further
//      redistribution of the source code or derived software
// 
// For commercial entities and for commercial applications, the right
// to copy, distribute or modify this source code is retained by
// CorTechs Labs, and must be obtained through completion of a written
// license agreement with CorTechs Labs Inc.
///////////////////////////////////////////////////////////////////////

/****************************************************
 *  hvecmat.h                                         
 *  Created on: 13-Dec-2006 08:32:08                      
 *  Implementation of the Class hvecmat       
 *  Original author: Gennan Chen                     
 ****************************************************/

#ifndef HVECMAT_H_
#define HVECMAT_H_
#include <xmmintrin.h>

#ifdef __cplusplus
extern "C" {
#endif


/* Deal with Windows*/
//#ifdef _WIN32
//#ifndef DLLTYPE
//#define DLLTYPE  __declspec(dllimport)
//#endif
//#else
//#define DLLTYPE
//#endif





/**
 * Vector and Matrix for Homogeneous coodinates by using SIMD instructions
 */

/**
 * 4 x 1 vector
 */
typedef struct 
{
	__m128 fVect4;
} hvec;

/**
 * 4 X 4 matrix 
 */
typedef struct 
{
	__m128 rows[4];
} hmat;



/* hVec functions*/
 void hVecInit(hvec *v1,float val1, float val2, float val3, float val4); 
 void hVec2fPtr(hvec *v1,float * fptr);
 void hVecSetVal(hvec *v1, int i, float val);
 float hVecGetVal(hvec *v1, int i);
 void hVecFromfPtr(float * fptr, hvec* v1);
 float hVecDot(hvec *v1, hvec *v2);
 float hVecDot3(hvec *v1, hvec *v2);
 void hVecCrossProduct3(hvec *v1, hvec *v2, hvec *vout);
 double hVecComputeAngle(hvec *v1, hvec *v2);
 void hVecPrint(hvec *v);
 float hVecNorm(hvec *v);
 float* hVecGetfPtr(hvec *v);
 void hVecMultiplyfVal(hvec *v, float val, hvec* vo);
 void hVecMultiplyhVec(hvec *v1, hvec *v2, hvec* vo);
 float hVecSum(hvec *v);
 void hVecAdd(hvec *v1, hvec *v2, hvec* vo);
 void hVecSubtracts(hvec *v1, hvec *v2, hvec* vo);

/* hMat functions*/
 void hMat2fPtr(hmat *mat,float * fptr);
 void hMatFromfPtr(float * fptr, hmat *mat);
 void hMatEye(hmat *mat);
 void hMatSetVal(hmat *mat, int i, int j, float val);
 float hMatGetVal(hmat *mat, int i, int j);
 void hMatMultiplyhVec(hmat *mat, hvec *vin, hvec *vout);
 void hMatMultiplyhMat(hmat *matL, hmat *matR, hmat *matout);
 void hMatInverse(hmat *matin, hmat *matout);
 void hMatTranspose(hmat *matin, hmat *matout);
 void hMatRotI(hmat *mat, double radian);
 void hMatRotJ(hmat *mat, double radian);
 void hMatRotK(hmat *mat, double radian);
 void hMatTranslate(hmat *mat, double ti, double tj, double tk);
 void hMatPrint(hmat *mat);
 void hMatSetRow(hmat *mat, hvec *v, int i);
 void hMatSetCol(hmat *mat, hvec *v, int j);
 void hMatGetRow(hmat *mat, hvec *v, int i);
 void hMatGetCol(hmat *mat, hvec *v, int j);
 void hMatGetNormCol(hmat *mat, hvec *v, int j);
 float * hMatGetRowfPtr(hmat *mat, int i);
 int hMat2File(hmat *mat, char * fn);
 int hMatFromFile(char *fn, hmat *mat);
 void hMatCopy(hmat *mi, hmat *mc);

#ifdef __cplusplus
} /* closing brace for extern "C" */
#endif

#endif 
