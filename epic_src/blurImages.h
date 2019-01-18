#ifndef GUARD_blurImages
#define GUARD_blurImages

#include "inputParams.h"
#include "imgvol.h"      // CTX stuff. fvol

void
blurImages(const InputParams& p, fvol* mri1, fvol* mri2, fvol* mri1Blur, fvol* mri2Blur, const int& kernelWidth);

void // NOTE: this is blurImage() with no 's' at the end!
blurImage(const float* image, float* imageBlur,
	  const int& width, const int& height, const int& depth, const int& kernelWidth);

void // NOTE: this is blurImage() with no 's' at the end! Overwrite input. Overwrite input.
blurImage(float* image,
	  const int& width, const int& height, const int& depth, const int& kernelWidth);

void // NOTE: this is blurImage() with no 's' at the end!
blurImage(fvol* mri1, fvol* mri1Blur, const int& kernelWidth);

#endif
