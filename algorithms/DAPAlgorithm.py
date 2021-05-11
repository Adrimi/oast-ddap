import random
from dataclasses import dataclass
from typing import List
from configuration.Configuration import Configuration

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


# MARK: - Main API

def solve(network, configuration): 
  initialGeneration = createFirstGeneration(network, configuration)
  chromControllers = createChromControllers(network, initialGeneration)
  chromControllers.sort(key=lambda c: c.maximumLoad)

  currentGeneration = 0
  mutationCount = 0
  currentTimeInSeconds = 0

  while configuration.stopCrtiteriaHit(currentGeneration, mutationCount, currentTimeInSeconds) == False:
    # get half of the best chromosomes to be the candidates for parent crossing
    parents = chromControllers[0:int(len(chromControllers)/2)]
    offSprings = []
    
    for index in range(len(parents) - 1):
      # crossing
      if uniformProbability(configuration.crossoverProbability):
        firstParentGenes = parents[index].chromosome.genes
        secondParentGenes = parents[index + 1].chromosome.genes

        firstChildGenes, secondChildGenes = crossGenes(
          firstParentGenes, 
          secondParentGenes, 
          lambda: uniformProbability(configuration.crossoverProbability)
        )
      
        # mutate first offspring 
        if uniformProbability(configuration.mutationProbability):
          mutationCount += 1
          randomDemandId = getRandomIndex(len(network.demands) - 1)
          firstChildGenes[randomDemandId] = mutate(firstChildGenes[randomDemandId])
          
        # mutate second offspring 
        if uniformProbability(configuration.mutationProbability):
          mutationCount += 1
          randomDemandId = getRandomIndex(len(network.demands) - 1)
          secondChildGenes[randomDemandId] = mutate(secondChildGenes[randomDemandId])
        
        offSprings += createChromControllers(network, [Chromosome(firstChildGenes), Chromosome(secondChildGenes)])
    
    newPopulation = chromControllers + offSprings
    newPopulation.sort(key=lambda c: c.maximumLoad)
    chromControllers = newPopulation[:configuration.populationSize]
    currentGeneration += 1
    
    print(chromControllers[0].maximumLoad)
  

# MARK: - Helper methods

def setSeed(seed):
  random.seed(seed)

def getRandomIndex(max: int) -> int:
  return random.randint(0, max)

def getTwoRandomIndexes(max: int):
  return random.sample(range(0, max), 2)

# MARK: - Operation on Chromosomes and Genes

def getBestParents(controllers):
  return controllers[:4]

def uniformProbability(p: float):
  return random.uniform(0, 1) < p

def crossGenes(firstGenes: List[Gene], secondGenes: List[Gene], crossingIsPossible):
  newFirstGenes = []
  newSecondGenes = []
  for index, gene in enumerate(firstGenes):  
    if crossingIsPossible():
      newFirstGenes.append(secondGenes[index])
      newSecondGenes.append(gene)
    else:
      newFirstGenes.append(gene)
      newSecondGenes.append(secondGenes[index])
  return newFirstGenes, newSecondGenes


def mutate(gene: Gene) -> Gene:
  numberOfPaths = len(gene.values)
  pathRandomOne, pathRandomTwo = getTwoRandomIndexes(numberOfPaths)

  if numberOfPaths == 1: return gene
  
  pathLoadValueOne = gene.values[pathRandomOne]
  pathLoadValueTwo = gene.values[pathRandomTwo]

  gene.values[pathRandomOne] = pathLoadValueTwo
  gene.values[pathRandomTwo] = pathLoadValueOne
  
  return gene

# MARK: - Chromosome controllers

def createChromControllers(network, generation: List[Chromosome]):
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

def createFirstGeneration(network, configuration: Configuration) -> List[Chromosome]:
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


