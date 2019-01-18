#include <cstddef>        // for size_t
#include "imgvol.h"       // CTX stuff. fvol


int
mriToFloatArray(const fvol* mri,
		float*     farray,
		const int& voxStep) {
  
  fvol* vol ( const_cast<fvol*>(mri) );
  
  size_t height  = mri->info.dim[0];
  size_t width   = mri->info.dim[1];
  size_t depth   = mri->info.dim[2];
  
  size_t numVoxX =  width/voxStep + ( width%voxStep ? 1 : 0);
  size_t numVoxY = height/voxStep + (height%voxStep ? 1 : 0);
  size_t numVoxZ =  depth/voxStep + ( depth%voxStep ? 1 : 0);
  
  size_t numVox ( numVoxX*numVoxY*numVoxZ );
  
  for(size_t x = 0; x < numVoxX; ++x)
    for(size_t y = 0; y < numVoxY; ++y)
      for(size_t z = 0; z < numVoxZ; ++z)  {
	size_t voxel = x*numVoxY*numVoxZ + y*numVoxZ + z;
	size_t xa = x*voxStep;
	size_t ya = y*voxStep;
	size_t za = z*voxStep;
	
	farray[voxel] = fVolGetVal(vol, ya, xa, za);
      }
  
  return numVox;
}
