// ==================================================
// Copyright (c) 2010 Dominic Holland and Anders Dale
// All rights reserved
// ==================================================

#ifndef GUARD_inputParams
#define GUARD_inputParams

#include <iostream>
#include <string.h>
#include <vector>


class InputParams {
  
 public:
  InputParams():
    defaults(false),            // print defaults and exit
    forwardImageOutFileName ("fB0uw.mgz"),
    reverseImageOutFileName ("rB0uw.mgz"),
    displacementFieldOutFileName ("d.mgz"),
    outDir ("./"),
    restart(false),
    kernelWidthMax(25),
    kernelWidthStep(2),
    voxStep(1),
    nchunksZ(4),
    scaleImages(true),
    imageMax(3400.0),
    bicgstabTol(1.0e-8),
    bicgstabMaxIter(256),
    hessianErrorMax(256.0),
    cgVoxDifferential(1.0),
    cgTol(1.0e-3),
    cgEpsAbs(1.0e-2),
    cgStepSize(0.5),
    cgMaxIterations(512),
    nvoxNewZbdry(2),
    lambda1(0.0),
    lambda2(1.1e3),
    lambda2P(1.1e3) {};
  
  InputParams(int argc, char** argv):
    defaults(false),            // print defaults and exit
    forwardImageOutFileName ("fB0uw.mgz"),
    reverseImageOutFileName ("rB0uw.mgz"),
    displacementFieldOutFileName ("d.mgz"),
    outDir ("./"),
    restart(false),
    kernelWidthMax(25),
    kernelWidthStep(2),
    voxStep(1),
    nchunksZ(4),
    scaleImages(true),
    imageMax(3400.0),
    bicgstabTol(1.0e-8),
    bicgstabMaxIter(256),
    hessianErrorMax(256.0),
    cgVoxDifferential(1.0),
    cgTol(1.0e-3),
    cgEpsAbs(1.0e-2),
    cgStepSize(0.5),
    cgMaxIterations(512),
    nvoxNewZbdry(2),
    lambda1(0.0),
    lambda2(1.1e3),
    lambda2P(1.1e3)  { readParameters(argc, argv); }
  
  void readParameters(int argc, char**);
  std::ostream& print(std::ostream&) const;
  
  const bool&        getDefaults()                     const { return defaults;               }
  
  const std::string& getForwardImageInFileName()       const { return forwardImageInFileName; }
  const std::string& getReverseImageInFileName()       const { return reverseImageInFileName; }
  
  const std::string& getOutDir()                       const { return outDir; }
  const std::string& getForwardImageOutFileName()      const { return forwardImageOutFileName; }
  const std::string& getReverseImageOutFileName()      const { return reverseImageOutFileName; }
  const std::string& getDisplacementFieldOutFileName() const { return displacementFieldOutFileName; }
  
  const bool&        getRestart()                      const { return restart; }
  const std::string& getDisplacementFieldInFileName()  const { return displacementFieldInFileName; }
  
  const int&         getKernelWidthMax()     const { return kernelWidthMax; }
  const int&         getKernelWidthStep()    const { return kernelWidthStep; }
  
  const int&         getVoxStep()            const { return voxStep; }
  const int&         getNchunksZ()           const { return nchunksZ; }  

  const bool&        getScaleImages()        const { return scaleImages; }
  const float&       getImageMax()           const { return imageMax; }
  
  const float&       getBicgstabTol()        const { return bicgstabTol; }
  const int&         getBicgstabMaxIter()    const { return bicgstabMaxIter; }
  const float&       getHessianErrorMax()    const { return hessianErrorMax; }
  
  const float&       getCgVoxDifferential()  const { return cgVoxDifferential; }
  const float&       getCgTol()              const { return cgTol; }
  const float&       getCgEpsAbs()           const { return cgEpsAbs; }
  const float&       getCgStepSize()         const { return cgStepSize; }
  const int&         getCgMaxIterations()    const { return cgMaxIterations; }
  
  const int&         getNvoxNewZbdry()       const { return nvoxNewZbdry; }
  
  const float&       getLambda1()            const { return lambda1; }
  const float&       getLambda2()            const { return lambda2; }
  const float&       getLambda2P()           const { return lambda2P; }
  
  
 private:
  bool             defaults;              // print defaults and exit
  
  std::string      forwardImageInFileName;
  std::string      reverseImageInFileName;
  std::string      displacementFieldInFileName;
  
  std::string      outDir;
  std::string      forwardImageOutFileName;
  std::string      reverseImageOutFileName;
  std::string      displacementFieldOutFileName;
  
  bool  restart;
  
  int   kernelWidthMax;
  int   kernelWidthStep;
  
  int   voxStep;
  int   nchunksZ;
  
  bool  scaleImages;  
  float imageMax;
  
  float bicgstabTol;
  int   bicgstabMaxIter;
  float hessianErrorMax;
  
  float cgVoxDifferential;
  float cgTol;
  float cgEpsAbs;
  float cgStepSize;
  int   cgMaxIterations;
  
  int   nvoxNewZbdry;
  
  float lambda1;
  float lambda2;
  float lambda2P;
  
};

// Need this declaration to handle expressions like "cout << p;" in main().
std::ostream& operator<<(std::ostream& os, const InputParams& p);

void errorReadFile(const char*, const char*);
void errorReadFile(const char*, const std::string);
void errorReadFile(std::ifstream&, const char*, int) throw(std::string);
void errorReadFile(const std::string, const std::string);

#endif
