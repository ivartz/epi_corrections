#include <iostream>
#include <cstring>           // for memset()
#include "inputParams.h"
#include "imgvol.h"          // CTX stuff. fvol
#include "getNumVox.h"
#include "initDispyFullRes.h"
#include "writeFullCorrectedVolumes.h"


void
writeOutput(fvol* forwardMri, fvol* reverseMri, float* d, const InputParams& p) {
  
  // If voxStep > 1, calculate the full resolution displacements,
  // i.e., for every voxel in the input image. Else, simply write
  // out the already full resolution dispy[] and the corrected
  // volues.
  
  if(p.getVoxStep() == 1) {
    std::clog<<__FILE__<<":\t"<<__LINE__<<std::endl;
    bool trimZbdrys ( true );
    writeFullCorrectedVolumes(p, forwardMri, reverseMri, d, trimZbdrys);
  }
  else {
    int     voxStepSample ( p.getVoxStep() );
    int     numVoxFullRes ( getNumVox(1, forwardMri) );
    
    float* dFullRes  ( new float[numVoxFullRes] );
    memset(dFullRes, 0, numVoxFullRes*sizeof(float));
    
    int width  ( forwardMri->info.dim[1] );
    int height ( forwardMri->info.dim[0] );
    int depth  ( forwardMri->info.dim[2] );
    
    initDispyFullRes(dFullRes, d, width, height, depth, numVoxFullRes, voxStepSample);	
    
    writeFullCorrectedVolumes(p, forwardMri, reverseMri, dFullRes);
    delete[] dFullRes;
  }
  
}
