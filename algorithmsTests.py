import unittest

import random
from dataclasses import dataclass
from typing import List

from models import Network, Link, Demand, Path
from algorithms import createGene, createChromosome, Gene


class TestCase:
  demand: Demand
  expectedResult: List[int]

  def __init__(self, volume, numberOfPaths, result):
    paths = [Path([0])] * numberOfPaths
    self.demand = Demand(0, 0, volume, paths)
    self.expectedResult = result


class DAPAlgorithmTests(unittest.TestCase):

  def test_createGene_withValuesGeneratedSumToDemandVolume(self):
    testCases = [
      TestCase(volume=3, numberOfPaths=1, result=[3]),
      TestCase(volume=2, numberOfPaths=2, result=[1, 1]),
      TestCase(volume=4, numberOfPaths=3, result=[3, 0, 1]),
      TestCase(volume=8, numberOfPaths=4, result=[7, 0, 1, 0]),
      TestCase(volume=2, numberOfPaths=5, result=[1, 0, 1, 0, 0]),
      TestCase(volume=453234, numberOfPaths=5, result=[235120, 13004, 201468, 1943, 1699]),
    ]

    for case in testCases:
      self.__interceptSeed()
      result = createGene(case.demand)
      self.assertEqual(result.values, case.expectedResult)
      self.assertEqual(sum(result.values), case.demand.volume)


  def test_createChromosome_returnsCorrectChromosome(self):
    network = self.__loadNetwork()

    chromosome = createChromosome(network)

    self.assertEqual(chromosome.genes, [])

  # MARK: - Helper methods

  def __interceptSeed(self):
    random.seed(2000)

  def __loadNetwork(self):
    return Network([], [])

# MARK: - Launch 

if __name__ == '__main__':
  unittest.main()