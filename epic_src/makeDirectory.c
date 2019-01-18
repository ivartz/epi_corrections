/*
   E.g., when called thus:
      makeDirectory("/tmp", "/tmp/a/b/c/d");
   this routine will attempt to make the full directory path
      /tmp/a/b/c/d

   NOTE:  "/tmp"  NOT  "tmp/"
   The latter will NOT work.
*/


#include <sys/stat.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>  // for strlen() and strcpy()

#define MAX_TOKEN 512


int makeDirectory(const char* startDir, const char* directory) {
  int status;
  int startLen;
  int pathLen, tmpLen;
  char tmpPath[MAX_TOKEN];
  struct stat statbuf;
  
  startLen = strlen(startDir);
  pathLen = strlen(directory);
  
  strcpy(tmpPath, directory);
  
  tmpLen = pathLen;
  
  while(tmpLen > startLen) {
    status = stat(tmpPath, &statbuf);  /* p. 180 K&R */
    if(status == 0) {
      if(statbuf.st_mode & S_IFDIR) {
	break;
      } else {
	fprintf(stderr,
		"%s: a local non-directory %s already exists \n",
		__FILE__, tmpPath);
	return (1);
      }
    }
    
    /* Go backward */    
    while(tmpLen && tmpPath[tmpLen] != '/')
      tmpLen --;
    tmpPath[tmpLen] = '\0';
  }
  
  /* Now go forward and mk the required dir */
  while(tmpLen < pathLen) {

    /* Put back the '/' */
    tmpPath[tmpLen] = '/';
    status = mkdir(tmpPath, 0755);
    
    if(status < 0) {
      fprintf(stderr,
	      "%s: mkdir failed for %s, errno = %d\n",
	      __FILE__, tmpPath, errno);
      return -1;
    }
    while(tmpLen && tmpPath[tmpLen] != '\0')
      tmpLen ++;
  }
  return 0;
}
