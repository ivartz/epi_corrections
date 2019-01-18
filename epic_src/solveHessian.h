#ifndef GUARD_solveHessian
#define GUARD_solveHessian

#include "imgvol.h" // CTX stuff. fvol

int
solveHessian(double* dispy, fvol* mri1, fvol* mri2,
	     const int& voxStep, const int& numVox, const int& nchunksZ,
	     const double& tol, const int& maxIter, const double& hessianErrorMax,
	     const int nvoxNewZbdry,
	     const float& lambda1, const float& lambda2, const float& lambda2P, const float& h, const bool cubicInterp = false);

#endif
