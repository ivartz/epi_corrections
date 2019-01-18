// ==================================================
// Copyright (c) 2010 Dominic Holland and Anders Dale
// All rights reserved
// ==================================================

#include <fstream>           // to open files for reading & writing
#include <cmath>
#include <ctime>             // for clock()
#include "inputParams.h"
#include "mriClass.h"
#include "intensityScaleImages.h"
#include "mriToFloatArray.h" // FOR TESTING LIBRARY ONLY!!!!!!!
#include "imageInfo.h"       // FOR TESTING LIBRARY ONLY!!!!!!!
#include "computeDeformationField.h"
#include "writeOutput.h"
#include "imgvol.h"          // CTX stuff. fvol

#include "writeImage.h"


using std::clog;
using std::endl;


void
processSubject(const InputParams& p) {
  
  MriClass forwardMriC ( p.getForwardImageInFileName(), p.getNvoxNewZbdry() );
  fvol*    forwardMri  ( const_cast<fvol*>(forwardMriC.getMri()) );
  
  MriClass reverseMriC ( p.getReverseImageInFileName(), p.getNvoxNewZbdry() );
  fvol*    reverseMri  ( const_cast<fvol*>(reverseMriC.getMri()) );
  
  if(p.getScaleImages())
    intensityScaleImages(forwardMri, reverseMri, p.getImageMax());
  
#if 0 // TEST LIBRARY  PROBLEM: USES DEFAULT PARAMS ONLY???
  
  int width  ( forwardMri->info.dim[1] );
  int height ( forwardMri->info.dim[0] );
  int depth  ( forwardMri->info.dim[2] );
  int numVox ( width*height*depth );
  
  float* images (new float[2*numVox]); // delete at end of this routine
  
  mriToFloatArray(forwardMri, images);
  mriToFloatArray(reverseMri, images+numVox);
  
  IMAGEINFO info;
  
  info.firstImageDirection = 1;
  info.numVox[0]  = width;
  info.numVox[1]  = height;
  info.numVox[2]  = depth;
  info.voxSize[0] = forwardMri->info.vxlsize[1];
  info.voxSize[1] = forwardMri->info.vxlsize[0];
  info.voxSize[2] = forwardMri->info.vxlsize[2];
  info.numFrames  = 1;
  
  float* d ( computeDeformationField(images, info) ); // Use a default InputParams p.
  delete[] images;
  
#else  
  
  // This will have to call "InputParams p;" default initialization.
  //float* d ( computeDeformationField(forwardMri, reverseMri) );
  
  // Use the p that was already built.
  clock_t start ( clock() );
  std::clog << "p.getKernelWidthMax() = " << p.getKernelWidthMax() <<std::endl;
  
  float* d ( computeDeformationField(forwardMri, reverseMri, p) );
  
  clock_t secondsUsed ( (clock() - start)/(CLOCKS_PER_SEC) );
  
  std::clog << __FILE__ << ": Duration: " << secondsUsed << " seconds" << std::endl;
  
#endif // TEST LIBRARY
  
  writeOutput(forwardMri, reverseMri, d, p);
  
  delete[] d;
}
