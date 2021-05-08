import unittest

import random
from dataclasses import dataclass
from typing import List

from models import Demand, Path
from algorithms import createGene, Gene


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
      TestCase(volume=4, numberOfPaths=3, result=[3, 0, 1]),
      TestCase(volume=2, numberOfPaths=3, result=[1, 0, 1]),
      TestCase(volume=1, numberOfPaths=3, result=[1, 0, 0])
    ]

    for case in testCases:
      self.__interceptSeed()
      result = createGene(case.demand)
      self.assertEqual(result.values, case.expectedResult)


  # MARK: - Helper methods

  def __interceptSeed(self):
    random.seed(2000)


# MARK: - Launch 

if __name__ == '__main__':
  unittest.main()