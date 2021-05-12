import xml.dom.minidom as xml

from parsers.NetworkModels import Network, Link, Demand, Path

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
  return f"<link id=\"{link.id}\"><startNode>{link.startNode}</startNode><endNode>{link.endNode}</endNode><numberOfModules>{link.numberOfModules}</numberOfModules><moduleCost>{link.moduleCost}</moduleCost><linkModule>{link.linkModule}</linkModule></link>"

def encodeDemandToXMLString(demand: Demand):
  paths = ""
  for path in demand.paths:
    paths += encodePathToXMLString(path)
  return f"<demand id=\"{demand.id}\"><startNode>{demand.startNode}</startNode><endNode>{demand.endNode}</endNode><volume>{demand.volume}</volume><paths>{paths}</paths></demand>"

def encodePathToXMLString(path: Path):
  links = ""
  for link in path.linkId:
    links += f"<linkId>{link}</linkId>"
  return f"<path id=\"{path.id}\">{links}</path>"