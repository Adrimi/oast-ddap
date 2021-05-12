import unittest

from typing import List
from unittest.case import expectedFailure
import xml.dom.minidom as xml

import persistence.TestHelpers as Helpers
from parsers.NetworkModels import Network, Link, Demand, Path
import persistence.XMLFileWriter as writer

class XMLFileWriterIntegrationTests(unittest.TestCase):

  def test_encoding_convertLinkObjectToXMLString(self):
    expectedXMLString = Helpers.LINK_XML_STRING
    testLink = self.__testNetwork().links[0]
    
    receivedXMLString = writer.encodeLinkToXMLString(testLink)

    self.assertEqual(expectedXMLString, receivedXMLString)

  def test_encoding_convertDemandObjectToXMLString(self):
    expectedXMLString = Helpers.DEMAND_XML_STRING
    testDemand = self.__testNetwork().demands[0]
    
    receivedXMLString = writer.encodeDemandToXMLString(testDemand)

    self.assertEqual(expectedXMLString, receivedXMLString)

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