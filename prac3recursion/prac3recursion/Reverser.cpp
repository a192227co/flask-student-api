#include "Reverser.h"

#include <string>

int Reverser::reverseDigit(int value) {
  if (value < 0) return -1;
  if (value < 10) return value;

  return (value % 10) * pow(10, (int)log10(value)) + reverseDigit(value / 10);
}

std::string Reverser::reverseString(std::string characters) {
  if (characters.empty()) return "ERROR";
  if (characters.size() == 1) return characters;

  return characters.back() +
         reverseString(characters.substr(0, characters.size() - 1));
}
