#ifndef GUARD_BiCGSTABF
#define GUARD_BiCGSTABF

void
bicgstabf_(int* n, double* b, double* x, double* work, int* ldw, int* iter, double* resid,
	   void (*matvec)(double*, double*, double*, double*), void (*psolve)(double*, double*),
	   int* info);

#endif
