#ifndef GUARD_computeDeformationField
#define GUARD_computeDeformationField

#include "inputParams.h"
#include "imgvol.h"          // CTX stuff. fvol

float*
computeDeformationField(fvol* forwardMri, fvol* reverseMri, const InputParams& p);

#include "imageInfo.h"

float*
computeDeformationField(const float* images, const IMAGEINFO& info);

#endif
