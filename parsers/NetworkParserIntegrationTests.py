import unittest

from typing import List

import TestHelpers
import xml.dom.minidom as xml
from NetworkParser import createNetworkFrom
from NetworkModels import Network, Link, Demand, Path


class NetworkParserIntegrationTests(unittest.TestCase):

  def test_createNetwork_parseDataFromXMLFile(self):
    XMLString = TestHelpers.XML_STRING

    self.maxDiff = None
    doc = xml.parseString(XMLString)
    network = createNetworkFrom(doc)

    self.assertEqual(network.links, [
      Link(startNode=1, endNode=2, numberOfModules=72, moduleCost=1, linkModule=2),
      Link(startNode=1, endNode=3, numberOfModules=72, moduleCost=1, linkModule=2),
      Link(startNode=2, endNode=3, numberOfModules=72, moduleCost=1, linkModule=2),
      Link(startNode=2, endNode=4, numberOfModules=72, moduleCost=1, linkModule=2),
      Link(startNode=3, endNode=4, numberOfModules=72, moduleCost=1, linkModule=2)
    ])
    self.assertEqual(network.demands, [
      Demand(startNode=1, endNode=2, volume=3, paths=[Path(linkId=[1]), Path(linkId=[2, 3]), Path(linkId=[2, 5, 4])]),
      Demand(startNode=1, endNode=3, volume=4, paths=[Path(linkId=[2]), Path(linkId=[1, 3]), Path(linkId=[1, 4, 5])]),
      Demand(startNode=1, endNode=4, volume=5, paths=[Path(linkId=[1, 4]), Path(linkId=[2, 5])]),
      Demand(startNode=2, endNode=3, volume=2, paths=[Path(linkId=[3]), Path(linkId=[1, 2]), Path(linkId=[4, 5])]),
      Demand(startNode=2, endNode=4, volume=3, paths=[Path(linkId=[4]), Path(linkId=[3, 5]), Path(linkId=[1, 2, 5])]),
      Demand(startNode=3, endNode=4, volume=4, paths=[Path(linkId=[5]), Path(linkId=[3, 4]), Path(linkId=[2, 1, 4])])
    ])


# MARK: - Launch 

if __name__ == '__main__':
  unittest.main()