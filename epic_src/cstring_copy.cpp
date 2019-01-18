#include <cstring>   // for strlen and strcpy
//#include <cstddef>   // size_t defined here....use std::size_t instead

// NOTE: This function imposes on its caller the responsibility of
// freeing the object at an appropriate time.

char*
cstring_copy(char* cstring) {
  const std::size_t len(strlen(cstring) + 1);
  char* copy(new char[len+1]);
  strcpy(copy, cstring);
  return copy;
}
