// ==================================================
// Copyright (c) 2010 Dominic Holland and Anders Dale
// All rights reserved
// ==================================================

#include <iostream>
#include <cmath>


void
setGaussianKernel(float* gaussKernel, const int& kernelWidth) {

  float sigma(kernelWidth/6.0);                       // Gaussian less than 1% of its max for x,y,z > 3*sigma.
  float sum(0.0);
  std::clog << "sigma = " << sigma << ";  kernelWidth/2 = " << kernelWidth/2 << std::endl;
  // kernelWidth/2 voxels on each side of center voxel.
  
  for(int i=-kernelWidth/2; i<kernelWidth/2+1; ++i)   // See Note-1 below.
    for(int j=-kernelWidth/2; j<kernelWidth/2+1; ++j)
      for(int k=-kernelWidth/2; k<kernelWidth/2+1; ++k) {
	float term( exp(-(i*i+j*j+k*k)/(2.0*sigma*sigma)) );
	gaussKernel[(i+kernelWidth/2)*kernelWidth*kernelWidth +
		    (j+kernelWidth/2)*kernelWidth +
		    (k+kernelWidth/2)] = term;
	sum += term;
      }
  
  float sumInv(1.0/sum);
  for(int i=-kernelWidth/2; i<kernelWidth/2+1; ++i)
    for(int j=-kernelWidth/2; j<kernelWidth/2+1; ++j)
      for(int k=-kernelWidth/2; k<kernelWidth/2+1; ++k)
	gaussKernel[(i+kernelWidth/2)*kernelWidth*kernelWidth +
		    (j+kernelWidth/2)*kernelWidth +
		    (k+kernelWidth/2)] *= sumInv;
  
#if 0
  // Write out Gaussian kernel.
  std::clog << "Kernel matrix:\n";
  for(int i=-kernelWidth/2; i<kernelWidth/2+1; ++i) {  //  or just int i(0);
    for(int j=-kernelWidth/2; j<kernelWidth/2+1; ++j) {
      for(int k=-kernelWidth/2; k<kernelWidth/2+1; ++k)
	std::clog << gaussKernel[(i+kernelWidth/2)*kernelWidth*kernelWidth +
				 (j+kernelWidth/2)*kernelWidth +
				 (k+kernelWidth/2)] << "  ";
      std::clog << '\n';
    }
    std::clog << '\n';
  }
  std::clog << "End kernel matrix\n\n";  
#endif
  
}


///////////////////////////////////////////////////////////////////////
// Note-1:
// 
// Yes yes, there is plenty redundancy here with the Gaussian being
// separable and symmetric. Got a problem with that?
// 
