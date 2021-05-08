import unittest

from typing import List

import TestHelpers
import xml.dom.minidom as xml
from NetworkParser import createNetworkFrom
from NetworkModels import Network, Link, Demand, Path


class NetworkParserIntegrationTests(unittest.TestCase):

  def test_createNetwork_parseDataFromXMLFile(self):
    XMLString = TestHelpers.XML_STRING
    expectedNetwork = self.__testNetwork()
    doc = xml.parseString(XMLString)
    self.maxDiff = None

    network = createNetworkFrom(doc)
    self.assertEqual(network, expectedNetwork)


  def __testNetwork(self):
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

# MARK: - Launch 

if __name__ == '__main__':
  unittest.main()