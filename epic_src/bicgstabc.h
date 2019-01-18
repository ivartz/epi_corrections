#ifndef GUARD_bicgstabc
#define GUARD_bicgstabc

int
bicgstabc(int* n, double* b, double* x, double* work, int* ldw, int* iter, double* resid,
	  int (*matvec)(double*, double*, double*, double*), int (*psolve)(double*, double*),
	  int* info, short enforceDecrease, double errFac);

#endif
