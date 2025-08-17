#ifndef EFFICIENT_TRUCKLOADS_H
#define EFFICIENT_TRUCKLOADS_H

#include <map>

class EfficientTruckloads {
 private:
  std::map<std::pair<int, int>, int> memo;

 public:
  int numTrucks(int numCrates, int loadSize);
};

#endif
