#ifndef GUARD_writeFullCorrectedVolumes
#define GUARD_writeFullCorrectedVolumes

#include <string.h>
#include "inputParams.h"
#include "imgvol.h"       // CTX stuff. fvol

void
writeFullCorrectedVolumes(const InputParams& p,
			  fvol* forwardMri,
			  fvol* reverseMri,
			  float* disp,
			  const bool trimZbdrys=false);
#endif
