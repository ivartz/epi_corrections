#include <iostream>
#include <string.h>
#include <cctype>
#include <cwctype>
#include <stdexcept>

using std::basic_string;

void toUpper(basic_string<char>& s) {
   for (basic_string<char>::iterator p = s.begin( );
        p != s.end( ); ++p) {
      *p = toupper(*p); // toupper is for char
   }
}

void toUpper(basic_string<wchar_t>& s) {
   for (basic_string<wchar_t>::iterator p = s.begin( );
        p != s.end( ); ++p) {
      *p = towupper(*p); // towupper is for wchar_t
   }
}

void toLower(basic_string<char>& s) {
   for (basic_string<char>::iterator p = s.begin( );
        p != s.end( ); ++p) {
      *p = tolower(*p);
   }
}

void toLower(basic_string<wchar_t>& s) {
   for (basic_string<wchar_t>::iterator p = s.begin( );
        p != s.end( ); ++p) {
      *p = towlower(*p);
   }
}
