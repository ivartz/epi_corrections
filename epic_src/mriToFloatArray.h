#ifndef GUARD_mriToFloatArray
#define GUARD_mriToFloatArray

#include "imgvol.h"       // CTX stuff. fvol

int
mriToFloatArray(const fvol* mri,
		float*     farray,
		const int& voxStep = 1);

#endif
