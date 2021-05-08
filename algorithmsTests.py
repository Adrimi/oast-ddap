import unittest

import random
from models import Demand, Path
from algorithms import createGene, Gene

class DAPAlgorithmTests(unittest.TestCase):

  def test_createGene_withValuesThatEqualsToSumOfDemandVolume(self):
    volume = 4
    paths = self.__getPaths(3)
    demand = Demand(0, 0, volume, paths)
    
    self.__interceptSeed()
    gene = createGene(demand)

    self.assertEqual(gene.values, [3, 0, 1])


  def test_createGene_withValuesThatEqualsToSumOfDemandVolume_SecondCase(self):
    volume = 2
    paths = self.__getPaths(3)
    demand = Demand(0, 0, volume, paths)
    
    self.__interceptSeed()
    gene = createGene(demand)

    self.assertEqual(gene.values, [1, 0, 1])


  def test_createGene_withValuesThatEqualsToSumOfDemandVolume_ThirdCase(self):
    volume = 1
    paths = self.__getPaths(3)
    demand = Demand(0, 0, volume, paths)
    
    self.__interceptSeed()
    gene = createGene(demand)

    self.assertEqual(gene.values, [1, 0, 0])

  # MARK: - Helper methods

  def __interceptSeed(self):
    random.seed(2000)

  def __getPaths(self, numberOfPaths):
    return [Path([0])] * numberOfPaths 

if __name__ == '__main__':
  unittest.main()