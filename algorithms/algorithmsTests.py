import unittest

import random
from dataclasses import dataclass
from typing import List

import xml.dom.minidom as xml
from parsers.NetworkParser import createNetworkFrom
from parsers.NetworkModels import Network, Link, Demand, Path
from algorithms import createGene, createChromosome, getLinkLoad, createFirstGeneration, Gene, Configuration


class TestCase:
  demand: Demand
  expectedResult: List[int]

  def __init__(self, volume, numberOfPaths, result):
    paths = list(map(
      lambda i, x: [Path(i, x)],
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
      result = createGene(case.demand)
      self.assertEqual(result.values, case.expectedResult)
      self.assertEqual(sum(result.values), case.demand.volume)


  def test_setLinkLoad_createsLoadsValuesOnEveryLink(self):
    network = self.__createNetwork()

    self.__interceptSeed()
    chromosome = createChromosome(network)
    linkLoadList = getLinkLoad(network, chromosome)

    self.assertEqual(linkLoadList, [12, 6, 5, 11, 3])


  # MARK: - Helper methods

  def __interceptSeed(self):
    random.seed(2000)


  def __createNetwork(self):
    demands = [
      Demand(id=1, startNode=1, endNode=2, volume=3, paths=[
        Path(id=1, linkId=[1]),
        Path(id=2, linkId=[2, 3]),
        Path(id=3, linkId=[2, 5, 4])
        ]
      ),
      Demand(id=2, startNode=1, endNode=3, volume=4, paths=[
        Path(id=1, linkId=[2]),
        Path(id=2, linkId=[1, 3]),
        Path(id=3, linkId=[1, 4, 5])
        ]
      ),
      Demand(id=3, startNode=1, endNode=4, volume=5, paths=[
        Path(id=1, linkId=[1, 4]),
        Path(id=2, linkId=[2, 5]),
        ]
      ),
      Demand(id=4, startNode=2, endNode=3, volume=2, paths=[
        Path(id=1, linkId=[3]),
        Path(id=2, linkId=[1, 2]),
        Path(id=3, linkId=[4, 5]),
        ]
      ),
      Demand(id=5, startNode=2, endNode=4, volume=3, paths=[
        Path(id=1, linkId=[4]),
        Path(id=2, linkId=[3, 5]),
        Path(id=3, linkId=[1, 2, 5]),
        ]
      ),
      Demand(id=6, startNode=3, endNode=4, volume=4, paths=[
        Path(id=1, linkId=[5]),
        Path(id=2, linkId=[3, 4]),
        Path(id=3, linkId=[2, 1, 4]),
        ]
      ),
    ]
    links = [
      Link(id=1, startNode=1, endNode=2, numberOfModules=72, moduleCost=1, linkModule=2),
      Link(id=2, startNode=1, endNode=3, numberOfModules=72, moduleCost=1, linkModule=2),
      Link(id=3, startNode=2, endNode=3, numberOfModules=72, moduleCost=1, linkModule=2),
      Link(id=4, startNode=2, endNode=4, numberOfModules=72, moduleCost=1, linkModule=2),
      Link(id=5, startNode=3, endNode=4, numberOfModules=72, moduleCost=1, linkModule=2)
    ]
    network = Network(links, demands)
    return network

  # def __testConfiguration(self) -> Configuration:
  #   Configuration()


# MARK: - Launch 

if __name__ == '__main__':
  unittest.main()