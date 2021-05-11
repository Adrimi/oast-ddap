## TO BE DELETED!
'''
OAST - algorytm ewolucyjny dla problemu DAP

# linkList
startNode - wezel poczatkowy
endNode - wezel koncowy
numberOfModules - ilosc wlokien optycznych w kablu
moduleCost - koszt wlokna
linkModule - ilosc lambda w wloknie

# demandList
startNode - wezel poczatkowy
endNode - wezel koncowy
volume - ilosc zapotrzebowania
paths - sciezki do zapotrzebowaniu
linkId - identyfikator łącza w zapotrzebowaniu
'''
## TO BE DELETED!

import random
from dataclasses import dataclass
from typing import List


# MARK: - Models namespace, algorithm specific objects


@dataclass
class Gene:
  values: List[int]

@dataclass
class Chromosome:
  genes: List[Gene]


class ChromosomeController:
  chromosome: Chromosome
  linkLoad: List[int]
  maximumLoad: int

  def __init__(self, chromosome, linkLoad, maximumLoad):
    self.chromosome = chromosome
    self.linkLoad = linkLoad
    self.maximumLoad = maximumLoad


@dataclass
class Configuration:
  populationSize = 40 # is that should be % 4 == 0 ?
  crossoverProbability = 0.5
  mutationProbability = 0.1

  # Stop criteria parameters
  maxTimeInSeconds = 10
  maxGenerationNumber = 50
  maxMutationEvents = 800
  maxImprovementsNumber = 15

  def stopCrtiteriaHit(self, currentGeneration, mutationCount, currentTimeInSeconds):
    return currentGeneration > self.maxGenerationNumber or mutationCount > self.maxMutationEvents or currentTimeInSeconds > self.maxTimeInSeconds


# MARK: - Main API

def solve(network, configuration): 
  initialGeneration = createFirstGeneration(network, configuration)
  chromControllers = createChromControllers(network, initialGeneration)
  chromControllers.sort(key=lambda c: c.maximumLoad)

  currentGeneration = 0
  mutationCount = 0
  currentTimeInSeconds = 0

  while configuration.stopCrtiteriaHit(currentGeneration, mutationCount, currentTimeInSeconds) == False:
    parents = chromControllers[:len(chromControllers)/2]
    
    currentGenerationIteration = 0
    offSprings = []

    for index in range(len(parents)):
      if uniformProbability(configuration.crossoverProbability):
        firstParent = parents[index].chromosome.genes
        secondParent = parents[index + 1].chromosome.genes

        firstChild, secondChild = rollGenesWithUniformRandomizer(firstParent, secondParent, lambda: uniformProbability(configuration.crossoverProbability))
      
        offSprings += [Chromosome(firstChild), Chromosome(secondChild)]




# MARK: - Helper methods

def setSeed(seed):
  random.seed(seed)


# MARK: - Operation on Chromosomes and Genes

def getBestParents(controllers):
  return controllers[:4]

def uniformProbability(p: float):
  def inner():
    return random.uniform(0, 1) < p
  return inner


def rollGenesWithUniformRandomizer(firstGenes: List[Gene], secondGenes: List[Gene], calculateProbability):
  newFirstGenes = []
  newSecondGenes = []
  for index, gene in enumerate(firstGenes):  
    if calculateProbability():
      newFirstGenes.append(secondGenes[index])
      newSecondGenes.append(gene)
    else:
      newFirstGenes.append(gene)
      newSecondGenes.append(secondGenes[index])
  return newFirstGenes, newSecondGenes




# MARK: - Chromosome controllers

def createChromControllers(network, generation):
  chromControllers = []
  for chrom in generation:
    linkLoad = getLinkLoad(network, chrom)
    maximumLoad = getMaximumLoad(linkLoad, network.links)
    chromControllers.append(ChromosomeController(chrom, linkLoad, maximumLoad))
  return chromControllers

def getLinkLoad(network, chromosome):
  linkLoad = [0] * len(network.links)

  for demandId, demand in enumerate(network.demands):
    gene = chromosome.genes[demandId]
    for pathId, path in enumerate(demand.paths):
      value = gene.values[pathId]
      for linkId in path.linkId:
        linkLoad[linkId - 1] += gene.values[pathId]
  
  return linkLoad

def getMaximumLoad(linkLoad, links):
  maximumLoad = 0
  for link in links:
    maximumLoad = max(linkLoad[link.id - 1] - link.numberOfModules * link.linkModule, maximumLoad)
  return maximumLoad

# MARK: - Chromosome generation

def createFirstGeneration(network, configuration) -> List[Chromosome]:
  generation = []
  for i in range(configuration.populationSize):
    generation.append(createChromosome(network))
  return generation


def createChromosome(network) -> Chromosome:
  genes = list(map(
    createGene,
    network.demands
  ))
  return Chromosome(genes)


def createGene(demand) -> Gene:
  values = []
  numberOfPaths = len(demand.paths)

  while sum(values) != demand.volume:
    for index in range(numberOfPaths):
      values.append(random.randint(0, demand.volume - sum(values)))

      # if this is last iteration of for loop AND sum is still mismatched, then add the missing value 
      if index == numberOfPaths - 1 and sum(values) != demand.volume:
        values = values[:-1] + [values[-1] + demand.volume - sum(values)]

  return Gene(values)


