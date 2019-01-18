#ifndef GUARD_hessian
#define GUARD_hessian

struct Hessian {
  
  int numVoxX;
  int numVoxY;
  int numVoxZ;
  
  double* Hjj;
  double* Hjjp;
  double* Hjjpp;
  double* dcostddispy;
  double  lamSize;
  double  lamSmooth;
  double  lamSmoothP;
};

#endif
