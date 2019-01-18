#ifndef GUARD_setupHessian
#define GUARD_setupHessian

#include "hessian.h"
#include "imgvol.h" // CTX stuff. fvol

void
setupHessian(Hessian&       hessian,
	     double*        dispy,
	     const int&     voxStep,
	     fvol*          vol1Mri,
	     fvol*          vol2Mri,
	     const int&     zaMin,
	     const int&     zaMax,
	     const double&  lambda1,
	     const double&  lambda2,
	     const double&  lambda2P,
	     const float&   h,
	     const bool cubicInterp = false);

#endif
