import os
from models import Network, Link, Demand, Path


def createNetworkFrom(doc):
  links = list(map(LinkInit, element("link", doc)))
  demands = list(map(DemandInit, element("demand", doc)))
  return Network(links, demands)


# Convenience initializers for XML DOM

def LinkInit(data):
  return Link(
    id=data.getAttribute("id"), 
    startNode=firstValue("startNode", data),
    endNode=firstValue("endNode", data),
    numberOfModules=firstValue("numberOfModules", data),
    moduleCost=firstValue("moduleCost", data),
    linkModule=firstValue("linkModule", data)
  )

def DemandInit(data):
  return Demand(
    id=data.getAttribute("id"),
    startNode=firstValue("startNode", data),
    endNode=firstValue("endNode", data),
    volume=firstValue("volume", data),
    paths=list(
      map(
        PathInit, 
        element("path", data)
      )
    )
  )

def PathInit(data):
  return Path(
    id=data.getAttribute("id"),
    linkId=list(
      map(
        lambda x: x.firstChild.data, 
        element("linkId", data)
      )
    )
  )
  


# Helpers

def element(name, source):
  return source.getElementsByTagName(name)

def firstValue(name, source):
  return element(name, source)[0].firstChild.data