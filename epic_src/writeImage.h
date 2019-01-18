#ifndef GUARD_writeImage
#define GUARD_writeImage

#include <string.h>
#include <vector>
#include "inputParams.h"

#include "imgvol.h"       // For CTS stuff.
extern "C" {
  //#include "fsStuff.h"  // for MRI struct
}

void
writeImage(const std::string& imageFile,  fvol* mri);

/*
void
writeImage(const InputParams& p,
	   const MRI* mri, const MRI* targMri, const std::string& subject,
	   const float* rigidRegMatrix, const std::string direction = "");

void
writeImage(const std::string& imagepFile,  const MRI* mri, const MRI* targMri,
	   const float* affineRegMatrix, const std::string direction = "");

void
writeImage(const std::string& imagepFile, MRI* mri, const MRI* targMri);

void
writeImage(const std::string& imagepFile, const MRI* mri, const float* affineRegMatrix);

void
writeImage(const std::string& imageFile,  MRI* subjectMri, const std::vector<int>& targetShiftValues, const float scaleFac, const bool useSinc = false);
*/

#endif
