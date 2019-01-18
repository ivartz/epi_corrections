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

#ifndef SURFACE_H_
#define SURFACE_H_
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

/*
 * Surface Struct
 */
typedef struct {
    
    int ballocV;
    int ballocT;
    //Number of vertices
    unsigned int numV;
    //Number of Triangles
    unsigned int numT;
    // 3 X numV in lph coordinates
    double * vertices;
    // 3 X numT 
    unsigned int *triangles;
    
} mesh;

/*
 * Mask indx.
 */
typedef struct {
    int balloc;
    unsigned int numi;
    unsigned int *indx;
} maskindx;

// New and delete
 int mesh2CXS(char * filename, mesh *pmesh);
 mesh* meshFromCXS(char * filename);
 mesh* meshNew(unsigned int numv, unsigned int numt, double * pvert, unsigned int * ptri);
 void meshDelete(mesh* surf);
 maskindx* maskindxNew(unsigned int numi,  unsigned int * pind);
 void maskindDelete(maskindx* maski);

//Access
 void meshGetVert(mesh *pmesh, int i, hvec* vec);
 void meshSetVert(mesh *pmesh, int i, hvec* vec);

//index from volume threshold
 maskindx* maskindxFromfVolTh(fvol *vol, float Il, float Ih);
 maskindx* maskindxFromucVolTh(ucvol *vol, int Il, int Ih);


//Mesh to vol
 double getmin(int isize,  float *pval);
 double getmax(int isize,  float *pval);
 maskindx * meshGetMaskVol(fvol *vol, mesh *pmesh, hmat *Mreg,  int brind, fvol* maskvol, ucvol *mask);
 double meshGetVolSize(mesh *pmesh);

// mesh Properties
 void meshComputeNormals(mesh *pmesh, double *pnormal);
 double meshTriArea(mesh *pmesh, double *parea);
 void meshGetCOM(mesh *pmesh, double* pcom);
 void meshInflateQ(mesh* pmesh, mesh *pmeshif, int numIts, double stepSize, int Normalize);
 void meshGetMeanEdgeVec(mesh *pmesh, double *pmev);
 void meshSmoothVertexValue(mesh *pmesh, int numIts, double * pval, double * pvals);

#ifdef __cplusplus
} /* closing brace for extern "C" */
#endif


#endif /*SURFACE_H_*/
