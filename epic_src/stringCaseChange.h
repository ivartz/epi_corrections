#ifndef GUARD_stringCaseChange
#define GUARD_stringCaseChange

#include <iostream>
#include <string.h>
#include <cctype>
#include <cwctype>
#include <stdexcept>

void toUpper(std::basic_string<char>& s);
void toUpper(std::basic_string<wchar_t>& s);
void toLower(std::basic_string<char>& s);
void toLower(std::basic_string<wchar_t>& s);

#endif
