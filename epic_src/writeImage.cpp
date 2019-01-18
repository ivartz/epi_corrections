#include <string.h>
#include <iostream>
#include <stdexcept>      // for runtime_error
#include "cstring_copy.h"
#include "imgvol.h"       // For CTS stuff.

using std::string;
using std::clog;
using std::endl;


void
writeImage(const string& imageFile, fvol* mri) {
  
  // .c_str() gives a const char*, but MRIwrite() needs a char*
  char* imageFileNonConst = cstring_copy(const_cast<char*>(imageFile.c_str()));
  clog << __FILE__ << ":\nWriting " << imageFileNonConst << endl;
  
  if( fVol2MGH(mri, imageFileNonConst, FLOAT) )  {
    clog << __FILE__ << ":\n";
    clog << "could not write imageFile file " << imageFile << endl;
    delete imageFileNonConst;  // avoid a memory leak
    fVolDelete(mri);
    throw std::runtime_error("Could not write mri file");
  }
  
  clog << "Writing done.\n" << endl;
  
  delete imageFileNonConst;    // avoid a memory leak
}
