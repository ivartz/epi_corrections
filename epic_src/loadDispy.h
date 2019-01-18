#ifndef GUARD_loadDispy
#define GUARD_loadDispy

#include <string.h>

void
loadDispy(const std::string& dyFile,
	  const int& numVox,
	  const int& voxStep,
	  const int nvoxNewZbdry,
	  double* dispy);

#endif
