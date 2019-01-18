// ==================================================
// Copyright (c) 2010 Dominic Holland and Anders Dale
// All rights reserved
// ==================================================

#include <iostream>
#include <ctime>          // for time(), time_t and tm
#include "inputParams.h"
#include "processSubject.h"
#include "checkInOutDirs.h"

void usage();


int
main(int argc, char* argv[]) {
  
  if(argc < 2) {
    usage();
    return 1;
  }
  
  InputParams p(argc, argv);
  std::clog << p;
  
  if(p.getDefaults())
    return;
  
  checkInOutDirs(p);
  
  clock_t start ( clock() );
  
  processSubject(p);
  
  clock_t secondsUsed ( (clock() - start)/(CLOCKS_PER_SEC) );
  
  std::clog << "Duration: " << secondsUsed << " seconds" << std::endl;
}
