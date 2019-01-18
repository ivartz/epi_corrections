#include <iostream>
#include <vector>
#include <string.h>
#include <algorithm>   // for find()

using std::vector;
using std::string;
using std::clog;
using std::endl;
using std::find;


bool
checkCommandLine(char** argv, const vector<string>& commandLine) {
  
  bool errorFlag ( false );
  vector<string>::const_iterator pos;
  
  bool defaults (false); // print defaults
  pos = find(commandLine.begin(), commandLine.end(), "-defaults");
  if(pos != commandLine.end())
    return errorFlag;
  
  bool f (false); // forward image
  pos = find(commandLine.begin(), commandLine.end(), "-f");
  if(pos != commandLine.end())
    f = true;
  
  bool r (false); // reverse image
  pos = find(commandLine.begin(), commandLine.end(), "-r");
  if(pos != commandLine.end())
    r = true;
  
  bool ip (false); // input parameters file
  pos = find(commandLine.begin(), commandLine.end(), "-ip");
  if(pos != commandLine.end())
    ip = true;
  
  if( (!f && !r && !ip) || (r && !f && !ip) || (f && !r && !ip) )
    errorFlag = true;
  
  return errorFlag;
}
