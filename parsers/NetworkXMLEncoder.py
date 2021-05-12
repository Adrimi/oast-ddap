from core.Models import Network, Link, Demand, Path

# MARK: - Enocoders

def encodeNetworkToXMLString(network: Network):
  links = reduce(network.links, encodeLinkToXMLString)
  demands = reduce(network.demands, encodeDemandToXMLString)

  return f"<network><links>{links}</links><demands>{demands}</demands></network>"

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