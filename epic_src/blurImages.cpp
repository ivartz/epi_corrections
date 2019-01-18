///////////////////////////////////////////////////////////////////////
// This source code is Copyright ©2007-2010 Dominic Holland and Anders
// Dale. Permission is granted by Dominic Holland and Anders Dale to
// copy, distribute and modify this source code, provided that it is
// used for research purposes only, and only by not-for-profit
// organizations, and further provided that:
// 
//    * this copyright notice appears in all copies.
//    * you indemnify and hold harmless Dominic Holland and Anders
//      Dale and their successors and associates from any and all
//      liability from any use of the information.
//    * you ensure that these conditions apply to any further
//      redistribution of the source code or derived software
// 
// For commercial entities and for commercial applications, the right
// to copy, distribute or modify this source code is retained by
// Dominic Holland and Anders Dale, and must be obtained through
// completion of a written license agreement with Dominic Holland and
// Anders Dale.
///////////////////////////////////////////////////////////////////////

// ==================================================
// Copyright ©2007-2010 Dominic Holland and Anders Dale
// All rights reserved
// ==================================================

#include <string.h>
#include <stdexcept>      // for runtime_error
#include <cstddef>        // for size_t
#include "cstring_copy.h"
#include "setGaussianKernel.h"

#include <iostream>
#include <cstdlib>
#include <fftw3.h>
#include "inputParams.h"

#include "imgvol.h"       // CTX stuff. fvol

using std::clog;


void // NOTE: this is blurImages() with an 's' at the end! Below is an overloaded blurImage() -- NO 's' at the end.
blurImages(const InputParams& p, fvol* mri1, fvol* mri2, fvol* mri1Blur, fvol* mri2Blur, const int& kernelWidth) {
  
  int width  ( mri1->info.dim[1] );
  int height ( mri1->info.dim[0] );
  int depth  ( mri1->info.dim[2] );
  
  float* gaussKernel ( new float[kernelWidth*kernelWidth*kernelWidth] );                        // Delete at end of this routine.
  
  // Will blur entire images. Must zero-pad boundaries -- see, e.g., Numerical Recipes, section 12.4, pp 425-30.
  int nx ( width+kernelWidth/2 );
  int ny ( height+kernelWidth/2 );
  int nz ( depth+kernelWidth/2 );
  
  setGaussianKernel(gaussKernel, kernelWidth);
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Transform kernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  float*         inKernel;
  fftwf_complex* outKernel;
  
  inKernel  = (float*)         fftwf_malloc(sizeof(float)         * nx*ny*nz);                  // Delete at end of this routine.
  outKernel = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) );         // Delete at end of this routine.
  
  // FFTW plan kernel fourier transform.                                                        // Delete at end of this routine.
  fftwf_plan plan = fftwf_plan_dft_r2c_3d(nx, ny, nz, inKernel, outKernel, FFTW_ESTIMATE);      // Or FFTW_MEASURE. See also Note-2 below.
  
  // Set up zero-padded-image-sized periodic Gaussian kernel.
  memset(inKernel, 0, nx*ny*nz*sizeof(float));
  for(int i=-kernelWidth/2; i<kernelWidth/2+1; ++i)
    for(int j=-kernelWidth/2; j<kernelWidth/2+1; ++j)
      for(int k=-kernelWidth/2; k<kernelWidth/2+1; ++k) {
	int ip = i<0? nx+i:i; // For i<0, the corresponding periodic i.
	int jp = j<0? ny+j:j; // For j<0, the corresponding periodic j.
	int kp = k<0? nz+k:k; // For k<0, the corresponding periodic k.
	inKernel[ip*ny*nz + jp*nz + kp] = gaussKernel[(i+kernelWidth/2)*kernelWidth*kernelWidth +
						      (j+kernelWidth/2)*kernelWidth +
						      (k+kernelWidth/2)];
      }
  
  // Fourier transform the kernel.
  fftwf_execute(plan);    // Produces outKernel.
  
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Prepare to transform mri1 and mri2.
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  float*         inImage;
  fftwf_complex* outImage;
  
  inImage   = (float*)         fftwf_malloc(sizeof(float)         * nx*ny*nz);                  // Delete at end of this routine.
  outImage  = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) );         // See FFTW manual for nz/2+1.
  
  // FFTW plan mri1/2 Fourier transform.
  plan = fftwf_plan_dft_r2c_3d(nx, ny, nz, inImage, outImage, FFTW_ESTIMATE);
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Prepare to inverse transform the product of outImage and outKernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  fftwf_complex* productFT   = (fftwf_complex*)fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) ); // Delete at end of this routine.
  float*         convolution = (float*)        fftwf_malloc(sizeof(float)         * nx*ny*nz);          // Delete at end of this routine.
  
  // FFTW plan productFT fourier transform.
  fftwf_plan planInv = fftwf_plan_dft_c2r_3d(nx, ny, nz, productFT, convolution, FFTW_ESTIMATE); // NOT nz/2+1
  
  float scale(1.0/(nx*ny*nz)); // See Note-3 below.
  
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Now, transform mri1 and mri2, and inverse transform the product of outImage and outKernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  for(int imageNumber = 1; imageNumber <= 2; ++imageNumber) {
    
    fvol* mriIn(0);
    fvol* mriOut(0);
    std::string blurMghFile;
    if(imageNumber == 1) {
      mriIn = mri1;
      mriOut = mri1Blur;
      //blurMghFile = p.getOutputDir() + "/blur1.mgh";
    }
    else if(imageNumber == 2) {
      mriIn = mri2;
      mriOut = mri2Blur;
      //blurMghFile = p.getOutputDir() + "/blur2.mgh";
    }
    
    // Load mriIn into inImage:
    memset(inImage,  0, nx*ny*nz*sizeof(float));
    for(int i=0; i<width; ++i)
      for(int j=0; j<height; ++j)
	for(int k=0; k<depth; ++k)
	  inImage[i*ny*nz + j*nz + k] = fVolGetVal(mriIn, j, i, k);
    
    // Fourier transform inImage.
    fftwf_execute(plan);    // Produces outImage.    
    
    // Set up the Fourier transform of the convolution of inImage with the kernel,
    // i.e., the point by point product of their individual transforms.
    memset(productFT, 0, nx*ny*(nz/2+1)*sizeof(fftwf_complex));
    for(int i=0; i<nx; ++i)
      for(int j=0; j<ny; ++j)
	for(int k=0; k<nz/2+1; ++k) {
	  int ijk( i*ny*(nz/2+1) + j*(nz/2+1) + k );
	  productFT[ijk][0] = ( outImage[ijk][0] * outKernel[ijk][0] - 
				outImage[ijk][1] * outKernel[ijk][1] ) * scale; // [.][0] ==> real, [.][1] ==> imaginary.
	  productFT[ijk][1] = ( outImage[ijk][0] * outKernel[ijk][1] + 
				outImage[ijk][1] * outKernel[ijk][0] ) * scale;
	}
    
    // Inverse Fourier transform the product.
    fftwf_execute(planInv); // Produces convolution.
    
    // Load convolution into mriOut.
    for(int i=0; i<width; ++i)
      for(int j=0; j<height; ++j)
	for(int k=0; k<depth; ++k) {
	  float val = convolution[i*ny*nz + j*nz + k];
	  fVolSetVal(mriOut, j, i, k, val);
	}
    
  }  // END   for(int imageNumber = 1; imageNumber <= 2; ++imageNumber)
  
  delete[] gaussKernel; // OK to mix new/delete and malloc/free on _distinct_ arrays in _same_ routine?
  
  fftwf_destroy_plan(plan);
  fftwf_destroy_plan(planInv);
  
  fftwf_free(inKernel);
  fftwf_free(outKernel);
  
  fftwf_free(inImage);
  fftwf_free(outImage);
  
  fftwf_free(productFT);
  fftwf_free(convolution);
  
}



///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////


void // NOTE: this is blurImage() with no 's' at the end! It is overloaded below.
blurImage(const float* image, float* imageBlur,
	  const int& width, const int& height, const int& depth, const int& kernelWidth) {
  
  
  float* gaussKernel(new float[kernelWidth*kernelWidth*kernelWidth]);                           // Delete at end of this routine.
  
  // Will blur entire images. Must zero-pad boundaries -- see, e.g., Numerical Recipes, section 12.4, pp 425-30.
  int nx(width+kernelWidth/2);
  int ny(height+kernelWidth/2);
  int nz(depth+kernelWidth/2);
  
  setGaussianKernel(gaussKernel, kernelWidth);
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Transform kernel.
  /////////////////////////////////////////////////////////////////////////////////////////////

  float*         inKernel;
  fftwf_complex* outKernel;
  
  inKernel  = (float*)         fftwf_malloc(sizeof(float)         * nx*ny*nz);                  // Delete at end of this routine.
  outKernel = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) );         // Delete at end of this routine.
  
  // FFTW plan kernel fourier transform.                                                        // Delete at end of this routine.
  fftwf_plan plan = fftwf_plan_dft_r2c_3d(nx, ny, nz, inKernel, outKernel, FFTW_ESTIMATE);      // Or FFTW_MEASURE. See also Note-2 below.
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;  
  // Set up zero-padded-image-sized periodic Gaussian kernel.
  memset(inKernel, 0, nx*ny*nz*sizeof(float));
  for(int i=-kernelWidth/2; i<kernelWidth/2+1; ++i)
    for(int j=-kernelWidth/2; j<kernelWidth/2+1; ++j)
      for(int k=-kernelWidth/2; k<kernelWidth/2+1; ++k) {
	int ip = i<0? nx+i:i; // For i<0, the corresponding periodic i.
	int jp = j<0? ny+j:j; // For j<0, the corresponding periodic j.
	int kp = k<0? nz+k:k; // For k<0, the corresponding periodic k.
	inKernel[ip*ny*nz + jp*nz + kp] = gaussKernel[(i+kernelWidth/2)*kernelWidth*kernelWidth +
						      (j+kernelWidth/2)*kernelWidth +
						      (k+kernelWidth/2)];
      }
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  // Fourier transform the kernel.
  fftwf_execute(plan);    // Produces outKernel.
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Prepare to transform image
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  float*         inImage;
  fftwf_complex* outImage;
  
  inImage   = (float*)         fftwf_malloc(sizeof(float)         * nx*ny*nz);                  // Delete at end of this routine.
  outImage  = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) );         // See FFTW manual for nz/2+1.
  
  // FFTW plan image Fourier transform.
  plan = fftwf_plan_dft_r2c_3d(nx, ny, nz, inImage, outImage, FFTW_ESTIMATE);
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Prepare to inverse transform the product of outImage and outKernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  fftwf_complex* productFT   = (fftwf_complex*)fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) ); // Delete at end of this routine.
  float*         convolution = (float*)        fftwf_malloc(sizeof(float)         * nx*ny*nz);          // Delete at end of this routine.
  
  // FFTW plan productFT fourier transform.
  fftwf_plan planInv = fftwf_plan_dft_c2r_3d(nx, ny, nz, productFT, convolution, FFTW_ESTIMATE); // NOT nz/2+1
  
  float scale(1.0/(nx*ny*nz)); // See Note-3 below.
  

  /////////////////////////////////////////////////////////////////////////////////////////////
  // Now, transform image, and inverse transform the product of outImage and outKernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  // Load mriIn into inImage:
  memset(inImage,  0, nx*ny*nz*sizeof(float));
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  for(int i=0; i<width; ++i)
    for(int j=0; j<height; ++j)
      for(int k=0; k<depth; ++k)
	inImage[i*ny*nz + j*nz + k] = image[i*height*depth + j*depth + k];
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  // Fourier transform inImage.
  fftwf_execute(plan);    // Produces outImage.
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;  
  // Set up the Fourier transform of the convolution of inImage with the kernel,
  // i.e., the point by point product of their individual transforms.
  memset(productFT, 0, nx*ny*(nz/2+1)*sizeof(fftwf_complex));
  for(int i=0; i<nx; ++i)
    for(int j=0; j<ny; ++j)
      for(int k=0; k<nz/2+1; ++k) {
	int ijk( i*ny*(nz/2+1) + j*(nz/2+1) + k );
	productFT[ijk][0] = ( outImage[ijk][0] * outKernel[ijk][0] - 
			      outImage[ijk][1] * outKernel[ijk][1] ) * scale; // [.][0] ==> real, [.][1] ==> imaginary.
	productFT[ijk][1] = ( outImage[ijk][0] * outKernel[ijk][1] + 
			      outImage[ijk][1] * outKernel[ijk][0] ) * scale;
      }
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  // Inverse Fourier transform the product.
  fftwf_execute(planInv); // Produces convolution.
  
  // Load convolution into mriOut.
  for(int i=0; i<width; ++i)
    for(int j=0; j<height; ++j)
      for(int k=0; k<depth; ++k)
	imageBlur[i*height*depth + j*depth + k] = convolution[i*ny*nz + j*nz + k];
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  delete[] gaussKernel; // OK to mix new/delete and malloc/free on _distinct_ arrays in _same_ routine?
  
  fftwf_destroy_plan(plan);
  fftwf_destroy_plan(planInv);
  
  fftwf_free(inKernel);
  fftwf_free(outKernel);
  
  fftwf_free(inImage);
  fftwf_free(outImage);
  
  fftwf_free(productFT);
  fftwf_free(convolution);
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;  
}


///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
//////////////////////// O V E R L O A D I N G ////////////////////////
/////////////////////////// overwrite input ///////////////////////////
///////////////////////////////////////////////////////////////////////


void // NOTE: this is blurImage() with no 's' at the end! It is overloaded below. Overwrite input.
blurImage(float* image,
	  const int& width, const int& height, const int& depth, const int& kernelWidth) {
  
  
  float* gaussKernel(new float[kernelWidth*kernelWidth*kernelWidth]);                           // Delete at end of this routine.
  
  // Will blur entire images. Must zero-pad boundaries -- see, e.g., Numerical Recipes, section 12.4, pp 425-30.
  int nx(width+kernelWidth/2);
  int ny(height+kernelWidth/2);
  int nz(depth+kernelWidth/2);
  
  setGaussianKernel(gaussKernel, kernelWidth);
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Transform kernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  float*         inKernel;
  fftwf_complex* outKernel;
  
  inKernel  = (float*)         fftwf_malloc(sizeof(float)         * nx*ny*nz);                  // Delete at end of this routine.
  outKernel = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) );         // Delete at end of this routine.
  
  // FFTW plan kernel fourier transform.                                                        // Delete at end of this routine.
  fftwf_plan plan = fftwf_plan_dft_r2c_3d(nx, ny, nz, inKernel, outKernel, FFTW_ESTIMATE);      // Or FFTW_MEASURE. See also Note-2 below.
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;  
  // Set up zero-padded-image-sized periodic Gaussian kernel.
  memset(inKernel, 0, nx*ny*nz*sizeof(float));
  for(int i=-kernelWidth/2; i<kernelWidth/2+1; ++i)
    for(int j=-kernelWidth/2; j<kernelWidth/2+1; ++j)
      for(int k=-kernelWidth/2; k<kernelWidth/2+1; ++k) {
	int ip = i<0? nx+i:i; // For i<0, the corresponding periodic i.
	int jp = j<0? ny+j:j; // For j<0, the corresponding periodic j.
	int kp = k<0? nz+k:k; // For k<0, the corresponding periodic k.
	inKernel[ip*ny*nz + jp*nz + kp] = gaussKernel[(i+kernelWidth/2)*kernelWidth*kernelWidth +
						      (j+kernelWidth/2)*kernelWidth +
						      (k+kernelWidth/2)];
      }
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  // Fourier transform the kernel.
  fftwf_execute(plan);    // Produces outKernel.
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Prepare to transform image
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  float*         inImage;
  fftwf_complex* outImage;
  
  inImage   = (float*)         fftwf_malloc(sizeof(float)         * nx*ny*nz);                  // Delete at end of this routine.
  outImage  = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) );         // See FFTW manual for nz/2+1.
  
  // FFTW plan image Fourier transform.
  plan = fftwf_plan_dft_r2c_3d(nx, ny, nz, inImage, outImage, FFTW_ESTIMATE);
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Prepare to inverse transform the product of outImage and outKernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  fftwf_complex* productFT   = (fftwf_complex*)fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) ); // Delete at end of this routine.
  float*         convolution = (float*)        fftwf_malloc(sizeof(float)         * nx*ny*nz);          // Delete at end of this routine.
  
  // FFTW plan productFT fourier transform.
  fftwf_plan planInv = fftwf_plan_dft_c2r_3d(nx, ny, nz, productFT, convolution, FFTW_ESTIMATE); // NOT nz/2+1
  
  float scale(1.0/(nx*ny*nz)); // See Note-3 below.
  

  /////////////////////////////////////////////////////////////////////////////////////////////
  // Now, transform image, and inverse transform the product of outImage and outKernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  // Load mriIn into inImage:
  memset(inImage,  0, nx*ny*nz*sizeof(float));
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  for(int i=0; i<width; ++i)
    for(int j=0; j<height; ++j)
      for(int k=0; k<depth; ++k)
	inImage[i*ny*nz + j*nz + k] = image[i*height*depth + j*depth + k];
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  // Fourier transform inImage.
  fftwf_execute(plan);    // Produces outImage.
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;  
  // Set up the Fourier transform of the convolution of inImage with the kernel,
  // i.e., the point by point product of their individual transforms.
  memset(productFT, 0, nx*ny*(nz/2+1)*sizeof(fftwf_complex));
  for(int i=0; i<nx; ++i)
    for(int j=0; j<ny; ++j)
      for(int k=0; k<nz/2+1; ++k) {
	int ijk( i*ny*(nz/2+1) + j*(nz/2+1) + k );
	productFT[ijk][0] = ( outImage[ijk][0] * outKernel[ijk][0] - 
			      outImage[ijk][1] * outKernel[ijk][1] ) * scale; // [.][0] ==> real, [.][1] ==> imaginary.
	productFT[ijk][1] = ( outImage[ijk][0] * outKernel[ijk][1] + 
			      outImage[ijk][1] * outKernel[ijk][0] ) * scale;
      }
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  // Inverse Fourier transform the product.
  fftwf_execute(planInv); // Produces convolution.
  
  // Load convolution into mriOut.
  for(int i=0; i<width; ++i)
    for(int j=0; j<height; ++j)
      for(int k=0; k<depth; ++k)
	image[i*height*depth + j*depth + k] = convolution[i*ny*nz + j*nz + k];
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;
  delete[] gaussKernel; // OK to mix new/delete and malloc/free on _distinct_ arrays in _same_ routine?
  
  fftwf_destroy_plan(plan);
  fftwf_destroy_plan(planInv);
  
  fftwf_free(inKernel);
  fftwf_free(outKernel);
  
  fftwf_free(inImage);
  fftwf_free(outImage);
  
  fftwf_free(productFT);
  fftwf_free(convolution);
  std::clog << __FILE__ << ":  " << __LINE__ << std::endl;  
}


///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
//////////////////////// O V E R L O A D I N G ////////////////////////
///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////


void // NOTE: this is blurImage() with no 's' at the end!
blurImage(fvol* mri1, fvol* mri1Blur, const int& kernelWidth) {
  
  int width  ( mri1->info.dim[1] );
  int height ( mri1->info.dim[0] );
  int depth  ( mri1->info.dim[2] );
  
  float* gaussKernel(new float[kernelWidth*kernelWidth*kernelWidth]);                           // Delete at end of this routine.
  
  // Will blur entire images. Must zero-pad boundaries -- see, e.g., Numerical Recipes, section 12.4, pp 425-30.
  int nx(width+kernelWidth/2);
  int ny(height+kernelWidth/2);
  int nz(depth+kernelWidth/2);
  
  setGaussianKernel(gaussKernel, kernelWidth);
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Transform kernel.
  /////////////////////////////////////////////////////////////////////////////////////////////

  float*         inKernel;
  fftwf_complex* outKernel;
  
  inKernel  = (float*)         fftwf_malloc(sizeof(float)         * nx*ny*nz);                  // Delete at end of this routine.
  outKernel = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) );         // Delete at end of this routine.
  
  // FFTW plan kernel fourier transform.                                                        // Delete at end of this routine.
  fftwf_plan plan = fftwf_plan_dft_r2c_3d(nx, ny, nz, inKernel, outKernel, FFTW_ESTIMATE);      // Or FFTW_MEASURE. See also Note-2 below.
  
  // Set up zero-padded-image-sized periodic Gaussian kernel.
  memset(inKernel, 0, nx*ny*nz*sizeof(float));
  for(int i=-kernelWidth/2; i<kernelWidth/2+1; ++i)
    for(int j=-kernelWidth/2; j<kernelWidth/2+1; ++j)
      for(int k=-kernelWidth/2; k<kernelWidth/2+1; ++k) {
	int ip = i<0? nx+i:i; // For i<0, the corresponding periodic i.
	int jp = j<0? ny+j:j; // For j<0, the corresponding periodic j.
	int kp = k<0? nz+k:k; // For k<0, the corresponding periodic k.
	inKernel[ip*ny*nz + jp*nz + kp] = gaussKernel[(i+kernelWidth/2)*kernelWidth*kernelWidth +
						      (j+kernelWidth/2)*kernelWidth +
						      (k+kernelWidth/2)];
      }
  
  // Fourier transform the kernel.
  fftwf_execute(plan);    // Produces outKernel.
  
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Prepare to transform mri1
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  float*         inImage;
  fftwf_complex* outImage;
  
  inImage   = (float*)         fftwf_malloc(sizeof(float)         * nx*ny*nz);                  // Delete at end of this routine.
  outImage  = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) );         // See FFTW manual for nz/2+1.
  
  // FFTW plan mri1 Fourier transform.
  plan = fftwf_plan_dft_r2c_3d(nx, ny, nz, inImage, outImage, FFTW_ESTIMATE);
  
  /////////////////////////////////////////////////////////////////////////////////////////////
  // Prepare to inverse transform the product of outImage and outKernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  fftwf_complex* productFT   = (fftwf_complex*)fftwf_malloc(sizeof(fftwf_complex) * nx*ny*( nz/2+1 ) ); // Delete at end of this routine.
  float*         convolution = (float*)        fftwf_malloc(sizeof(float)         * nx*ny*nz);          // Delete at end of this routine.
  
  // FFTW plan productFT fourier transform.
  fftwf_plan planInv = fftwf_plan_dft_c2r_3d(nx, ny, nz, productFT, convolution, FFTW_ESTIMATE); // NOT nz/2+1
  
  float scale(1.0/(nx*ny*nz)); // See Note-3 below.


  /////////////////////////////////////////////////////////////////////////////////////////////
  // Now, transform mri1, and inverse transform the product of outImage and outKernel.
  /////////////////////////////////////////////////////////////////////////////////////////////
  
  fvol* mriIn(0);
  fvol* mriOut(0);
  std::string blurMghFile;
  mriIn = mri1;
  mriOut = mri1Blur;
  //blurMghFile = p.getOutputDir() + "/blur1.mgh";
  
  // Load mriIn into inImage:
  memset(inImage,  0, nx*ny*nz*sizeof(float));
  for(int i=0; i<width; ++i)
    for(int j=0; j<height; ++j)
      for(int k=0; k<depth; ++k)
	inImage[i*ny*nz + j*nz + k] = fVolGetVal(mriIn, j, i, k);
  
  // Fourier transform inImage.
  fftwf_execute(plan);    // Produces outImage.    
  
  // Set up the Fourier transform of the convolution of inImage with the kernel,
  // i.e., the point by point product of their individual transforms.
  memset(productFT, 0, nx*ny*(nz/2+1)*sizeof(fftwf_complex));
  for(int i=0; i<nx; ++i)
    for(int j=0; j<ny; ++j)
      for(int k=0; k<nz/2+1; ++k) {
	int ijk( i*ny*(nz/2+1) + j*(nz/2+1) + k );
	productFT[ijk][0] = ( outImage[ijk][0] * outKernel[ijk][0] - 
			      outImage[ijk][1] * outKernel[ijk][1] ) * scale; // [.][0] ==> real, [.][1] ==> imaginary.
	productFT[ijk][1] = ( outImage[ijk][0] * outKernel[ijk][1] + 
			      outImage[ijk][1] * outKernel[ijk][0] ) * scale;
      }
  
  // Inverse Fourier transform the product.
  fftwf_execute(planInv); // Produces convolution.
  
  // Load convolution into mriOut.
  for(int i=0; i<width; ++i)
    for(int j=0; j<height; ++j)
      for(int k=0; k<depth; ++k) {
	float val ( convolution[i*ny*nz + j*nz + k] );
	fVolSetVal(mriOut, j, i, k, val);
      }
  
  delete[] gaussKernel; // OK to mix new/delete and malloc/free on _distinct_ arrays in _same_ routine?
  
  fftwf_destroy_plan(plan);
  fftwf_destroy_plan(planInv);
  
  fftwf_free(inKernel);
  fftwf_free(outKernel);

  fftwf_free(inImage);
  fftwf_free(outImage);
  
  fftwf_free(productFT);
  fftwf_free(convolution);
  
}


///////////////////////////////////////////////////////////////////////
// Note-2:
// 
// Out-of-place transforms are generally faster than in-place.
// 
///////////////////////////////////////////////////////////////////////
// Note-3:
// 
// These transforms are unnormalized, so an r2c followed by a c2r
// transform (or vice versa) will result in the original data scaled
// by the number of real data elements (product of dimensions of
// zero-padded real arrays).
// 
///////////////////////////////////////////////////////////////////////
// Note-4:
// 
