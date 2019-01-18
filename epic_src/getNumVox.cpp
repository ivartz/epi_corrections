
#include "inputParams.h"
#include "imgvol.h"          // CTX stuff. fvol


int
getNumVox(const int voxStep, fvol* mriVol) {
  
  int width  ( mriVol->info.dim[1] );
  int height ( mriVol->info.dim[0] );
  int depth  ( mriVol->info.dim[2] );
  
  int numVoxX = width  / voxStep + (width  % voxStep ? 1 : 0);
  int numVoxY = height / voxStep + (height % voxStep ? 1 : 0);
  int numVoxZ = depth  / voxStep + (depth  % voxStep ? 1 : 0);
  
  int numVox  = numVoxX*numVoxY*numVoxZ;
  
  return numVox;
}
