#ifndef GUARD_writeOutput
#define GUARD_writeOutput

#include "inputParams.h"
#include "imgvol.h"          // CTX stuff. fvol

void
writeOutput(fvol* forwardMri, fvol* reverseMri, float* d, const InputParams& p);

#endif
