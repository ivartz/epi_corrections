#ifndef GUARD_mriClass
#define GUARD_mriClass

#include <string.h>
#include "imgvol.h"  // CTX stuff. fvol

class MriClass {
  
 public:
  MriClass() : mri(0) {};
  MriClass(const std::string& fileName, const int nvoxNewZbdry=0);
  MriClass& operator=(const std::string& mriFile);
  ~MriClass();
  
  const fvol* getMri() const { return mri; }
  
 private:
  fvol* mri;
};

#endif
