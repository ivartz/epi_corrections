#ifndef GUARD_createRescaledMri
#define GUARD_createRescaledMri

#include "imgvol.h" // CTX stuff. fvol

fvol*
createRescaledMri(fvol* atlasMri, fvol* subjectMri, const bool fillData, const bool useCubic = false);

fvol*
createRescaledMri(const int   awidth, const int   aheight, const int   adepth,
		  const float axsize, const float aysize,  const float azsize, fvol* subjectMri, const bool fillData, const bool useCubic = false);

#endif
