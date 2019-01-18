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
 *  interpolation.h                                         
 *  Created on: 14-Dec-2006 14:50:44                      
 *  Implementation of the Class interpolation       
 ****************************************************/

#ifndef INTERP_H_
#define INTERP_H_

#include "basicstructs.h"


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
 * Functions for interpolation
 */

typedef enum 
{
	NEAREST,
	LINEAR,
	CUBIC
} INTERPMETHOD;

typedef enum 
{
	MIRROR,
	ZEROPAD,
    THROWAWAY
} INTERPEDGE;

typedef enum 
{
    ALL,
    THROUGHPLANE,
    INPLANE
} UNWARPTYPE;
/*
 * Interpolation functions
 */

 int round4(double val); 
 void fVolGetMorphVal(int n, float* pos, float* val, int* inbound, fvol* vol, fvols* dfield, INTERPMETHOD method, INTERPEDGE edge, int bPositive, int bJacobian);
 void fVolMorph(fvol* vol, fvol* volr, int bsame, fvols *dfield, ucvol* mask, INTERPMETHOD method, INTERPEDGE edge, int bPositive, int bJacobian);
 void fVolMorphWithVxlMap(fvol* vol, fvol* volr, fvol *rVi, fvol *rVj,  fvol *rVk, INTERPMETHOD method, INTERPEDGE edge, int bPositive);
 void fVolGetVxlVal(int n, float * pos, float* val, int* inbound, fvol* vol, hmat* M_r2o, INTERPMETHOD method, INTERPEDGE edge, int bPositive);
 int GetVxlVal(hvec * vxl, float* val, fvol* vol, INTERPMETHOD method, INTERPEDGE edge, int bPositive);
 int GetVxlVals(hvec * vxl, float* val, fvols *vols, INTERPMETHOD method, INTERPEDGE edge, int bPositive);
 void fVolResample(fvol* vol, fvol* volr, hmat* M_r2o, INTERPMETHOD method, INTERPEDGE edge, int bPositive);
 float fDataGetValPAD(volinfo *info, float* data, int i, int j, int k, INTERPMETHOD method, INTERPEDGE edge);
 void fVolGetValsOnRay(int nv, double *vertice, double *dvec,int np, double *steps, double *vals, int numSmooth, 
  				   			fvol* vol, hmat* M_r2o, INTERPMETHOD method, INTERPEDGE edge, int bPositive);

/*
 * Gradient Unwarping function 
 */
 void fVolGradUnwarp(fvol* vol, fvol* volr, fvols *dfield, UNWARPTYPE uwtype, int bJacobian, INTERPMETHOD method, INTERPEDGE edge, int bPositive); 
 
 
#ifdef __cplusplus
} /* closing brace for extern "C" */
#endif


#endif 
