/////////////////////////////////////////////////////////////////
//
// Check that input directories already exist. Report if not, and
// exit. Check that output directories exist, and if not, attempt
// to make them, and report any error.
//
/////////////////////////////////////////////////////////////////

#include <sys/types.h> // for the system call stat()
#include <sys/stat.h>  // for the system call stat()
#include <cstdlib>     // for exit()...use std::exit instead

#include <iostream>
#include "inputParams.h"
#include "makeDirectory.h"

using std::clog;
using std::cerr;
using std::endl;
using std::exit;


void
checkInOutDirs(const InputParams& p) {

  struct stat  statbuf;                         // to see status of input files
  int          status;                          // for stat()

  // Check that outDir exists, make if not
  status = stat(p.getOutDir().c_str(), &statbuf);
  if(status != 0 || !(statbuf.st_mode & S_IFDIR) )  {
    clog << __FILE__ << ": " << p.getOutDir() << " does not exist" << endl;
    clog << __FILE__ << ": attempting to mkdir " << p.getOutDir() << '\n' << endl;
    
    int err = makeDirectory("/", p.getOutDir().c_str());
    if(err) {
      cerr << __FILE__ << ": err = " << err << endl;
      exit(EXIT_FAILURE);
    }
  }
  
}

//extern "C" {
//#include "makeDirectory.c"
//}
