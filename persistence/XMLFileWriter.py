import xml.dom.minidom as xml

from parsers.NetworkModels import Network, Link

def save(network: Network, filePath: str):
  with open(filePath, "wb") as file:
    saveNetwork(network.links, file)


def saveNetwork(network, file):
  string = encodeNetworkToXMLString(network)
  doc = xml.parseString(string)
  doc.writexml(file)


def encodeNetworkToXMLString(network: Network):
  header = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"
  networkString = "<network><links></links></network>"
  return header + networkString


def encodeLinkToXMLString(link: Link):
  return f"<link id=\"{link.id}\">" + f"<startNode>{link.startNode}</startNode>" + f"<endNode>{link.endNode}</endNode>" + f"<numberOfModules>{link.numberOfModules}</numberOfModules>" + f"<moduleCost>{link.moduleCost}</moduleCost>" + f"<linkModule>{link.linkModule}</linkModule>" + "</link>"