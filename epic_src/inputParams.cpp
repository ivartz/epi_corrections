// ==================================================
// Copyright (c) 2010 Dominic Holland and Anders Dale
// All rights reserved
// ==================================================

////////////////////////////////////////////////////////////////////
// Load pareameters from an input-parameters file into an
// InputParams class.
//
// One improvement to be made here would be to include checking that
// ALL REQUIRED parameters were actually loaded...
////////////////////////////////////////////////////////////////////

#include <fstream>        // to open files for reading & writing
//#include <iostream>
//#include <string>
#include <sstream>        // for stringstream
#include <vector>
#include <map>
#include <algorithm>      // for copy() and find()
#include <iterator>       // for ostream_iterator
#include <cctype>         // for isspace()
#include "inputParams.h"
#include "split.h"        // split a string of words into a vector of words
#include "checkCommandLine.h"

using std::ifstream;
using std::ostream;
using std::cerr;
using std::endl;
using std::string;
using std::map;
using std::vector;
using std::stringstream;
using std::exit;
using std::find;

void usage();


void
InputParams::readParameters(int argc, char** argv) {
  
  // Some parameters and names optionally can be supplied on the comand line.
  // Command line values override anyother values.
  vector<string> commandLine;
  
  // Load command line into a string.
  for(int i=0; i<argc; ++i) {
    commandLine.push_back(argv[i]);
    std::clog << commandLine[i] << endl;
  }
  
  if( checkCommandLine(argv, commandLine) ) {
    usage();
    exit(0);
  }
  
  vector<string>::iterator pos;
  
  bool defaultsFlag (false);   // print defaults and exit.
  pos = find(commandLine.begin(), commandLine.end(), "-defaults");
  if(pos != commandLine.end()) {
    defaults = true;           // Default set to false
    defaultsFlag = true;
  }
  
  bool fFlag (false);     // If set, commandline value will override value in file, if provided.
  pos = find(commandLine.begin(), commandLine.end(), "-f");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end())
      forwardImageInFileName = *(pos);
    fFlag = true;
  }
  
  bool rFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-r");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end())
      reverseImageInFileName = *(pos);
    rFlag = true;
  }
  
  bool foFlag (false);     // If set, commandline value will override value in file, if provided.
  pos = find(commandLine.begin(), commandLine.end(), "-fo");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end())
      forwardImageOutFileName = *(pos);
    foFlag = true;
  }
  
  bool roFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-ro");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end())
      reverseImageOutFileName = *(pos);
    roFlag = true;
  }
    
  bool diFlag (false);     // If set, commandline value will override value in file, if provided.
  pos = find(commandLine.begin(), commandLine.end(), "-di");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end())
      displacementFieldInFileName = *(pos);
    diFlag = true;
  }

  bool doFlag (false);     // If set, commandline value will override value in file, if provided.
  pos = find(commandLine.begin(), commandLine.end(), "-do");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end())
      displacementFieldOutFileName = *(pos);
    doFlag = true;
  }
  
  bool odFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-od");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end())
      outDir = *(pos);
    odFlag = true;
  }
  
  bool restartFlag (false);// If set, commandline value will override value in file, if provided.
  pos = find(commandLine.begin(), commandLine.end(), "-restart");
  if(pos != commandLine.end()) {
    restart = true;        // Default set to false
    ++pos;                 // don't forget to iterate on...!
    restartFlag = true;
  }
  
  bool voxStepFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-voxStep");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into an int
      ssn >> voxStep;
    }
    voxStepFlag = true;
  }
  
  bool nchunksZFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-nchunksZ");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into an int
      ssn >> nchunksZ;
    }
    nchunksZFlag = true;
  }
  
  bool scaleImagesFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-scaleImages");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into a bool
      ssn >> scaleImages;
    }
    scaleImagesFlag = true;
  }
  
  bool imageMaxFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-imageMax");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into a float
      ssn >> imageMax;
    }
    imageMaxFlag = true;
  }
  
  bool kernelWidthMaxFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-kernelWidthMax");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into an int
      ssn >> kernelWidthMax;
    }
    kernelWidthMaxFlag = true;
  }
  
  bool kernelWidthStepFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-kernelWidthStep");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into an int
      ssn >> kernelWidthStep;
    }
    kernelWidthStepFlag = true;
  }
  
  bool nvoxNewZbdryFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-nvoxNewZbdry");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into an int
      ssn >> nvoxNewZbdry;
    }
    nvoxNewZbdryFlag = true;
  }
  
  bool lambda1Flag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-lambda1");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into a float
      ssn >> lambda1;
    }
    lambda1Flag = true;
  }
  
  bool lambda2Flag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-lambda2");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into a float
      ssn >> lambda2;
    }
    lambda2Flag = true;
  }
  
  bool lambda2PFlag (false);
  pos = find(commandLine.begin(), commandLine.end(), "-lambda2P");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end()) {
      stringstream ssn(*(pos)); // turn the string into a float
      ssn >> lambda2P;
    }
    lambda2PFlag = true;
  }
  
  
  ////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////
  
  // Open the file referred to by argv[1]
  //ifstream fParamsIn(argv[1]);
  //if(!fParamsIn) errorReadFile(" Cannot open input file", argv[1]);
  
  // Access the file referred to by -ip, or return.
  string inputParamsFileName;
  pos = find(commandLine.begin(), commandLine.end(), "-ip");
  if(pos != commandLine.end()) {
    if(++pos != commandLine.end())
      inputParamsFileName = *(pos);
  }
  else
    return; // Use default initializations.
  
  ifstream fParamsIn(inputParamsFileName.c_str());
  if(!fParamsIn) errorReadFile(" Cannot open input file", inputParamsFileName);
  
  map<string, string> strMap;
  string s;
  int count ( 0 );

  while(getline(fParamsIn, s))  {
    
    if( !s.size() ) continue;              // skip empty lines
    
    vector<string> v = split(s);
    if( !v.size() ) continue;              // skip pure white-space lines
    
    if( v.size() < 3 ) continue;           // skip empty variables (nothing after the "=")
                                           // Yes, I know, this could absorb the previous line.
    if(v[0].substr(0,2) == "//") continue; // skip comment lines
    if(v[2] == "//") continue;             // skip lines whose variables are unset (there's only a comment preceded by "//" after the "=")
    
    // Now, start selecting variables...
    if     (!defaultsFlag  && v[0] == "defaults")    {     // v[2] will be "0" or "1". Translate to true or false.
      stringstream ssn(v[2]);                              // stringstream --> bool
      ssn >> defaults;  count++; }                         // Default set to false
    else if(!fFlag  && v[0] == "forwardImageInFileName")       { forwardImageInFileName       = v[2];  count++; }
    else if(!rFlag  && v[0] == "reverseImageInFileName")       { reverseImageInFileName       = v[2];  count++; }
    else if(!foFlag && v[0] == "forwardImageOutFileName")      { forwardImageOutFileName      = v[2];  count++; }
    else if(!roFlag && v[0] == "reverseImageOutFileName")      { reverseImageOutFileName      = v[2];  count++; }
    else if(!diFlag && v[0] == "displacementFieldInFileName")  { displacementFieldInFileName  = v[2];  count++; }
    else if(!doFlag && v[0] == "displacementFieldOutFileName") { displacementFieldOutFileName = v[2];  count++; }
    else if(!odFlag && v[0] == "outDir")                       { outDir                       = v[2];  count++; } // Set default to current dir.
    else if(!restartFlag && v[0] == "restart")  {                // v[2] will be "0" or "1". Translate to true or false.
      stringstream ssn(v[2]);                                    // stringstream --> bool
      ssn >> restart;  count++;                                  // Default set to false
    }
    else if(!voxStepFlag && v[0] == "voxStep")  {
      stringstream ssn(v[2]);              // turn the string into an int
      ssn >> voxStep;
      count++;
    }
    else if(!nchunksZFlag && v[0] == "nchunksZ")  {
      stringstream ssn(v[2]);              // turn the string into an int
      ssn >> nchunksZ;
      count++;
    }
    else if(!scaleImagesFlag && v[0] == "scaleImages")  {
      stringstream ssn(v[2]);              // turn the string into a bool
      ssn >> scaleImages;
      count++;
    }
    else if(!imageMaxFlag && v[0] == "imageMax")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> imageMax;
      count++;
    }
    else if(!kernelWidthMaxFlag && v[0] == "kernelWidthMax")  {
      stringstream ssn(v[2]);              // turn the string into an int
      ssn >> kernelWidthMax;
      count++;
    }
    else if(!kernelWidthStepFlag && v[0] == "kernelWidthStep")  {
      stringstream ssn(v[2]);              // turn the string into an int
      ssn >> kernelWidthStep;
      count++;
    }
    else if(!nvoxNewZbdryFlag && v[0] == "nvoxNewZbdry")  {
      stringstream ssn(v[2]);              // turn the string into an int
      ssn >> nvoxNewZbdry;
      count++;
    }
    else if(!lambda1Flag && v[0] == "lambda1")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> lambda1;
      count++;
    }
    else if(!lambda2Flag && v[0] == "lambda2")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> lambda2;
      count++;
    }
    else if(!lambda2PFlag && v[0] == "lambda2P")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> lambda2P;
      count++;
    }
    
    
    else if(v[0] == "bicgstabTol")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> bicgstabTol;
      count++;
    }
    else if(v[0] == "bicgstabMaxIter")  {
      stringstream ssn(v[2]);              // turn the string into an int
      ssn >> bicgstabMaxIter;
      count++;
    }
    else if(v[0] == "hessianErrorMax")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> hessianErrorMax;
      count++;
    }
    else if(v[0] == "cgVoxDifferential")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> cgVoxDifferential;
      count++;
    }
    else if(v[0] == "cgTol")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> cgTol;
      count++;
    }
    else if(v[0] == "cgEpsAbs")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> cgEpsAbs;
      count++;
    }
    else if(v[0] == "cgStepSize")  {
      stringstream ssn(v[2]);              // turn the string into a float
      ssn >> cgStepSize;
      count++;
    }
    else if(v[0] == "cgMaxIterations")  {
      stringstream ssn(v[2]);              // turn the string into an int
      ssn >> cgMaxIterations;
      count++;
    }
    
    //    else if(v[0] == "")  {
    //      stringstream ssn(v[2]);              // turn the string into a float
    //      ssn >> ;
    //      count++;
    //    }
    
#if 0
    else {
      cerr << __FILE__ << ":  invalid input file  " << argv[1] << endl;
      cerr << "line " << s << endl;
      cerr << "v[0] " << v[0] << endl;
      exit(EXIT_FAILURE);
    }
#endif
  }
  
  //  if(!fParamsIn.good())   // check if input failed
  //    errorReadFile(fParamsIn, argv[1], count);
}


ostream&
InputParams::print(ostream& os) const {
  os << "\nHave parameters:\n\n";
  
  os << "defaults                     =  " << defaults                    << '\n';
  
  os << "forwardImageInFileName       = " << forwardImageInFileName       << '\n';	 
  os << "reverseImageInFileName       = " << reverseImageInFileName       << '\n'; 
  
  os << "forwardImageOutFileName      = " << forwardImageOutFileName      << '\n'; 
  os << "reverseImageOutFileName      = " << reverseImageOutFileName      << '\n';
  
  os << "displacementFieldInFileName  = " << displacementFieldInFileName  << '\n';
  os << "displacementFieldOutFileName = " << displacementFieldOutFileName << '\n';
  
  os << "outDir                       = " << outDir                       << '\n';
  
  os << "restart                      = " << restart                      << '\n';
  
  os << "voxStep                      = " << voxStep                      << '\n';
  os << "nchunksZ                     = " << nchunksZ                     << '\n';
  
  os << "scaleImages                  = " << scaleImages                  << '\n';
  os << "imageMax                     = " << imageMax                     << '\n';
  
  os << "kernelWidthMax               = " << kernelWidthMax               << '\n';
  os << "kernelWidthStep              = " << kernelWidthStep              << '\n';
  
  os << "nvoxNewZbdry                 = " << nvoxNewZbdry                 << '\n';
  
  os << "lambda1                      = " << lambda1                      << '\n';
  os << "lambda2                      = " << lambda2                      << '\n';
  os << "lambda2P                     = " << lambda2P                     << '\n';
  
  os << "bicgstabTol                  = " << bicgstabTol                  << '\n';
  os << "bicgstabMaxIter              = " << bicgstabMaxIter              << '\n';
  os << "hessianErrorMax              = " << hessianErrorMax              << '\n';
  
  os << "cgVoxDifferential            = " << cgVoxDifferential            << '\n';
  os << "cgTol                        = " << cgTol                        << '\n';
  os << "cgEpsAbs                     = " << cgEpsAbs                     << '\n';
  os << "cgStepSize                   = " << cgStepSize                   << '\n';
  os << "cgMaxIterations              = " << cgMaxIterations              << '\n';
  
  os << '\n';
  
  return os;
}


ostream& operator<<(ostream& os, const InputParams& params) {
  return params.print(os);
}


void
errorReadFile(const char* p, const char* p2 = "") {
  std::cerr << __FILE__ << p << ' ' << p2 << std::endl;
  std::exit(EXIT_FAILURE);
}


void
errorReadFile(const char* p, const string s = "") {
  std::cerr << __FILE__ << p << ' ' << s << std::endl;
  std::exit(EXIT_FAILURE);
}

void
errorReadFile(const string p, const string s = "") {
  std::cerr << __FILE__ << ":\n" << p << ' ' << s << std::endl;
  std::exit(EXIT_FAILURE);
}

void
errorReadFile(ifstream& ifs, const char* p, int c) throw(string) {
  ifs.clear();
  cerr << __FILE__ << "\nInputfile " << p << " appears to contain " 
       << c << " elements.\n\n";
  string s = "Bollocks.\n";
  //  throw(s);    // the gratuitous exception
  std::exit(EXIT_FAILURE);
}
