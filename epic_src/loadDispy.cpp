#include <iostream>
#include <string.h>
#include <cstdlib>        // for exit()
#include "mriClass.h"
#include "imgvol.h"       // CTX stuff. fvol

using std::string;


void
loadDispy(const string& dyFile,
	  const int& numVox,
	  const int& voxStep,
	  const int nvoxNewZbdry,
	  double* dispy) {
  
  MriClass dyMriC ( dyFile, nvoxNewZbdry );
  fvol*    dyMri  ( const_cast<fvol*>(dyMriC.getMri()) );
  
  int width  ( dyMri->info.dim[1] );
  int height ( dyMri->info.dim[0] );
  int depth  ( dyMri->info.dim[2] );
  
  int numVoxX =  width/voxStep + ( width%voxStep ? 1 : 0);
  int numVoxY = height/voxStep + (height%voxStep ? 1 : 0);
  int numVoxZ =  depth/voxStep + ( depth%voxStep ? 1 : 0);
  int numVoxp = numVoxX*numVoxY*numVoxZ;
  
  if( numVoxp != numVox ) {
    std::cerr << "numVoxp = " << numVoxp << ",   numVox = " << numVox << std::endl;
    exit(1);
  }
  
  for(int x = 0; x < numVoxX; ++x)
    for(int y = 0; y < numVoxY; ++y)
      for(int z = 0; z < numVoxZ; ++z)  {
	int voxel = x*numVoxY*numVoxZ + y*numVoxZ + z;
	int xa = x*voxStep;
	int ya = y*voxStep;
	int za = z*voxStep;
	dispy[voxel] = fVolGetVal(dyMri, ya, xa, za);
      }
  
}
