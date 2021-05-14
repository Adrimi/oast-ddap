from math import ceil
from os import path
from unittest import signals

from core.Models import DAPChromosomeController, DDAPChromosomeController, Gene, Network

def encodeDAP(bestSolution: DAPChromosomeController, network: Network) -> str:
  return __encode(bestSolution.linkLoad, bestSolution.chromosome, network)

def encodeDDAP(bestSolution: DDAPChromosomeController, network: Network) -> str:
  return __encode(bestSolution.linkLoad, bestSolution.chromosome, network)

def __encode(linkLoad, chromosome, network) -> str:
  header = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"

  linkPart = ""
  for index, value in enumerate(linkLoad):
    linkPart += encodeLinkLoad(
      index + 1, 
      ceil(value),
      ceil(value / network.links[index].linkModule)
      )

  demandPart = ""
  for index, gene in enumerate(chromosome.genes):
    pathFlow = PathFlow(index, gene)
    demandPart += encodeDemandPart(
      index + 1,
      pathFlow
    )

  return f"{header}<solution><links>{linkPart}</links><demands>{demandPart}</demands></solution>"

def encodeLinkLoad(id, numberOfSignals, numberOfFibers):
  return f"<link id=\"{id}\"><numberOfSignals>{numberOfSignals}</numberOfSignals><numberOfFibers>{numberOfFibers}</numberOfFibers></link>"

def encodeDemandPart(id, pathFlow):
  return f"<demand id=\"{id}\"><pathFlows>{encodePathFlow(pathFlow)}</pathFlows></demand>"

def encodePathFlow(pathFlow):
  return f"<pathFlow id=\"{pathFlow.id}\"><signalsCount>{pathFlow.signalsCount}</signalsCount></pathFlow>"


class PathFlow:
  id: int
  signalsCount: int

  def __init__(self, id: int, gene: Gene):
    self.id = id
    self.signalsCount = sum(gene.values)