import xml.dom.minidom as xml

from parsers.NetworkModels import Network, Link, Demand, Path

# MARK: - API

def save(network: Network, filePath: str):
  with open(filePath, "wb") as file:
    saveNetwork(network.links, file)

def saveNetwork(network, file):
  string = encodeNetworkToXMLString(network)
  doc = xml.parseString(string)
  doc.writexml(file)

# MARK: - Enocoders

def encodeNetworkToXMLString(network: Network):
  header = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"

  links = reduce(network.links, encodeLinkToXMLString)
  demands = reduce(network.demands, encodeDemandToXMLString)

  networkString = f"<network><links>{links}</links><demands>{demands}</demands></network>"
  return header + networkString

def encodeLinkToXMLString(link: Link):
  return f"<link id=\"{link.id}\"><startNode>{link.startNode}</startNode><endNode>{link.endNode}</endNode><numberOfModules>{link.numberOfModules}</numberOfModules><moduleCost>{link.moduleCost}</moduleCost><linkModule>{link.linkModule}</linkModule></link>"

def encodeDemandToXMLString(demand: Demand):
  paths = reduce(demand.paths, encodePathToXMLString)

  return f"<demand id=\"{demand.id}\"><startNode>{demand.startNode}</startNode><endNode>{demand.endNode}</endNode><volume>{demand.volume}</volume><paths>{paths}</paths></demand>"

def encodePathToXMLString(path: Path):
  links = reduce(path.linkId, lambda link: f"<linkId>{link}</linkId>")

  return f"<path id=\"{path.id}\">{links}</path>"

# MARK: - Helper methods

def reduce(elements, encoder):
  joinedElements = ""
  for element in elements:
    joinedElements += encoder(element)
  return joinedElements