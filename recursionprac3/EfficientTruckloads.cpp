#include "EfficientTruckloads.h"

int EfficientTruckloads::numTrucks(int numCrates, int loadSize) {
  if (numCrates <= 0 || loadSize <= 0) return -1;
  if (numCrates <= loadSize) return 1;

  auto key = std::make_pair(numCrates, loadSize);
  if (memo.find(key) != memo.end()) return memo[key];

  int left = numCrates / 2;
  int right = numCrates - left;

  memo[key] = numTrucks(left, loadSize) + numTrucks(right, loadSize);
  return memo[key];
}
