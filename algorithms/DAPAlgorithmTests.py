import unittest

import random
from typing import List

from core.Models import Network, Link, Demand, Path
from configuration.Configuration import Configuration
import algorithms.DAPAlgorithm as dap


class TestCase:
  demand: Demand
  expectedResult: List[int]

  def __init__(self, volume, numberOfPaths, result):
    paths = list(map(
      lambda i, x: Path(i, [x]),
      range(numberOfPaths),
      [0] * numberOfPaths
    ))
    self.demand = Demand(0, 0, 0, volume, paths)
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
      result = dap.createGene(case.demand)
      self.assertEqual(result.values, case.expectedResult)
      self.assertEqual(sum(result.values), case.demand.volume)


  def test_getLinkLoad_createsLoadsValuesOnEveryLink(self):
    network = self.__createNetwork()

    self.__interceptSeed()
    chromosome = dap.createChromosome(network)
    linkLoadList = dap.getLinkLoad(network, chromosome)

    self.assertEqual(linkLoadList, [91, 63, 44, 101, 61])

  def test_getMaximumLoad_returnsTheBiggestValueFromTheList(self):
    network = self.__createNetwork()

    self.__interceptSeed()
    chromosome = dap.createChromosome(network)
    linkLoadList = dap.getLinkLoad(network, chromosome)

    maximumLoad = dap.getMaximumLoad(linkLoadList, network.links)

    self.assertEqual(maximumLoad, 37)

  def test_getBestParents_returnsFourChromosomes(self):
    network = self.__createNetwork()
    configuration = self.testConfiguration()

    self.__interceptSeed()
    initialGeneration = dap.createFirstGeneration(network, configuration)
    controllers = dap.createChromControllers(network, initialGeneration)
    controllers.sort(key=lambda c: c.maximumLoad)

    bestParents = dap.getBestParents(controllers)
    highestMaximumLoads = list(map(
      lambda x: x.maximumLoad,
      bestParents
    ))

    self.assertEqual(highestMaximumLoads, [13, 19, 20, 26])


  # MARK: - Helper methods

  def __interceptSeed(self):
    random.seed(2000)


  def __createNetwork(self):
    demands = [
      Demand(id=1, startNode=1, endNode=2, volume=30, paths=[
        Path(id=1, linkId=[1]),
        Path(id=2, linkId=[2, 3]),
        Path(id=3, linkId=[2, 5, 4])
        ]
      ),
      Demand(id=2, startNode=1, endNode=3, volume=40, paths=[
        Path(id=1, linkId=[2]),
        Path(id=2, linkId=[1, 3]),
        Path(id=3, linkId=[1, 4, 5])
        ]
      ),
      Demand(id=3, startNode=1, endNode=4, volume=50, paths=[
        Path(id=1, linkId=[1, 4]),
        Path(id=2, linkId=[2, 5]),
        ]
      ),
      Demand(id=4, startNode=2, endNode=3, volume=20, paths=[
        Path(id=1, linkId=[3]),
        Path(id=2, linkId=[1, 2]),
        Path(id=3, linkId=[4, 5]),
        ]
      ),
      Demand(id=5, startNode=2, endNode=4, volume=30, paths=[
        Path(id=1, linkId=[4]),
        Path(id=2, linkId=[3, 5]),
        Path(id=3, linkId=[1, 2, 5]),
        ]
      ),
      Demand(id=6, startNode=3, endNode=4, volume=40, paths=[
        Path(id=1, linkId=[5]),
        Path(id=2, linkId=[3, 4]),
        Path(id=3, linkId=[2, 1, 4]),
        ]
      ),
    ]
    links = [
      Link(id=1, startNode=1, endNode=2, numberOfModules=32, moduleCost=1, linkModule=2),
      Link(id=2, startNode=1, endNode=3, numberOfModules=32, moduleCost=1, linkModule=2),
      Link(id=3, startNode=2, endNode=3, numberOfModules=32, moduleCost=1, linkModule=2),
      Link(id=4, startNode=2, endNode=4, numberOfModules=32, moduleCost=1, linkModule=2),
      Link(id=5, startNode=3, endNode=4, numberOfModules=32, moduleCost=1, linkModule=2)
    ]
    return Network(links, demands)


  def testConfiguration(self):
    return Configuration()


# MARK: - Launch 

if __name__ == '__main__':
  unittest.main()