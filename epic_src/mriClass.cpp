#include <iostream>
#include <stdexcept>             // for runtime_error
#include <sys/types.h>           // for the system call stat()
#include <sys/stat.h>            // for the system call stat()
#include "mriClass.h"
#include "stringCaseChange.h"
#include "cstring_copy.h"
#include "createRescaledMri.h"
#include <cstdlib>     // for exit()...use std::exit instead

using std::string;
using std::exit;
using std::clog;
using std::endl;


MriClass::MriClass(const string& mriFile, const int nvoxNewZbdry) {
  
  struct stat  statbuf;          // to see status of input files
  int          status;           // for stat()
  
  // Check that mriFile exists, exit if not
  status = stat(mriFile.c_str(), &statbuf);
  if(status != 0 || !(statbuf.st_mode & S_IFREG) )  {
    clog << __FILE__ << ": " << mriFile << " does not exist. Exiting...\n" << endl;
    exit(0);
  }
  
  // .c_str() gives a const char*, but fVolFromMGH() needs a char*
  char* mriFileNonConst = cstring_copy(const_cast<char*>(mriFile.c_str()));
  
  clog << __FILE__ << ":\nReading " << mriFile << endl;
  int bLoadData ( 1 );
  fvol* mriAux = fVolFromMGH(mriFileNonConst, bLoadData);
  delete mriFileNonConst;        // ...avoid a memory leak
  
  if(!mriAux) {
    clog << __FILE__ << ":\n";
    clog << "could not open mri file " << mriFile << endl;
    throw std::runtime_error("Could not open mri file"); // see p. 28 Exceptional C++/Sutter
  }
  clog << "Reading done.\n";
  
  VolInfoPrint(&(mriAux->info));
  
  //const int nvoxNewZbdry ( 0 );  // See also solveHessian.cpp and writeFullCorrectedVolumes.cpp
  
  clog << __FILE__
	    << ":\nExpanding z-boundaries by " << nvoxNewZbdry
	    << " voxels, i.e., adding "        << nvoxNewZbdry 
	    << " new xy-planes at top and bottom..." << endl;
  
  int width   ( mriAux->info.dim[1] );
  int height  ( mriAux->info.dim[0] );
  int depth   ( mriAux->info.dim[2] );
  int depthNew( depth + 2*nvoxNewZbdry );
  
  const bool fillDataNO ( false );
  const float xsize ( mriAux->info.vxlsize[1] );
  const float ysize ( mriAux->info.vxlsize[0] );
  const float zsize ( mriAux->info.vxlsize[2] );
  
  mri = createRescaledMri(width, height, depthNew, xsize, ysize, zsize, mriAux, fillDataNO);
  
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y)
      for(int z = 0; z < depth; ++z) {
	
	float val ( fVolGetVal(mriAux, y, x, z) );
	fVolSetVal(mri, y, x, z+nvoxNewZbdry, val);
      }
  
  // Let the new layers be duplicates of the current top and bottom end layers
  // Lower bdry:
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y) {
      
      float val ( fVolGetVal(mriAux, y, x, 0) );
      
      for(int z = 0; z < nvoxNewZbdry; ++z)
	fVolSetVal(mri, y, x, z, val);
    }
  
  // Upper bdry:
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y) {
      
      float val ( fVolGetVal(mriAux, y, x, depth-1) );
      
      for(int z = depthNew-nvoxNewZbdry; z < depthNew; ++z)
	fVolSetVal(mri, y, x, z, val);
    }
  
  VolInfoPrint(&(mri->info));
  
  fVolDelete(mriAux);
};


MriClass::~MriClass() {
  clog<<__FILE__<<__LINE__<<":\n"<<mri<<endl;
  //if(mri)
  //  MRIfree(&mri);
}


MriClass& MriClass::operator=(const string& mriFile) {
  
  struct stat  statbuf;          // to see status of input files
  int          status;           // for stat()
  
  // Check that mriFile exists, exit if not
  status = stat(mriFile.c_str(), &statbuf);
  if(status != 0 || !(statbuf.st_mode & S_IFREG) )  {
    clog << __FILE__ << ": " << mriFile << " does not exist. Exiting...\n" << endl;
    exit(0);
  }
    
  // .c_str() gives a const char*, but fVolFromMGH() needs a char*
  char* mriFileNonConst = cstring_copy(const_cast<char*>(mriFile.c_str()));
  
  clog << __FILE__ << ":\nReading " << mriFile << endl;
  int bLoadData ( 1 );
  fvol* mriAux = fVolFromMGH(mriFileNonConst, bLoadData);
  delete mriFileNonConst;        // ...avoid a memory leak
  
  if(!mriAux) {
    clog << __FILE__ << ":\n";
    clog << "could not open mri file " << mriFile << endl;
    throw std::runtime_error("Could not open mri file"); // see p. 28 Exceptional C++/Sutter
  }
  clog << "Reading done.\n";
  
  VolInfoPrint(&(mriAux->info));
  
  const int nvoxNewZbdry ( 2 );  // See also solveHessian.cpp and writeFullCorrectedVolumes.cpp
  
  clog << __FILE__
	    << ":\nExpanding z-boundaries by " << nvoxNewZbdry
	    << " voxels, i.e., adding "        << nvoxNewZbdry 
	    << " new xy-planes at top and bottom..." << endl;

  int width   ( mriAux->info.dim[1] );
  int height  ( mriAux->info.dim[0] );
  int depth   ( mriAux->info.dim[2] );
  int depthNew( depth + 2*nvoxNewZbdry );
  
  const bool fillDataNO ( false );
  const float xsize ( mriAux->info.vxlsize[1] );
  const float ysize ( mriAux->info.vxlsize[0] );
  const float zsize ( mriAux->info.vxlsize[2] );
  
  mri = createRescaledMri(width, height, depthNew, xsize, ysize, zsize, mriAux, fillDataNO);
  
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y)
      for(int z = 0; z < depth; ++z) {
	
	float val ( fVolGetVal(mriAux, y, x, z) );
	fVolSetVal(mri, y, x, z+nvoxNewZbdry, val);
      }
  
  // Let the new layers be duplicates of the current top and bottom end layers
  // Lower bdry:
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y) {
      
      float val ( fVolGetVal(mriAux, y, x, 0) );
      
      for(int z = 0; z < nvoxNewZbdry; ++z)
	fVolSetVal(mri, y, x, z, val);
    }
  
  // Upper bdry:
  for(int x = 0; x < width; ++x)
    for(int y = 0; y < height; ++y) {
      
      float val ( fVolGetVal(mriAux, y, x, depth-1) );
      
      for(int z = depthNew-nvoxNewZbdry; z < depthNew; ++z)
	fVolSetVal(mri, y, x, z, val);
    }
  
  VolInfoPrint(&(mriAux->info));
  
  fVolDelete(mriAux);
  
  return *this;
};
