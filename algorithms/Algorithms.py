import random
import math
from typing import List
from configuration.Configuration import Configuration
from core.Models import DAPChromosomeController, DDAPChromosomeController, Chromosome, Gene

# MARK: - Main API

# DAP
def solveDAP(network, configuration) -> DAPChromosomeController: 
  initialGeneration = createFirstGeneration(network, configuration)
  chromControllers = createDAPChromControllers(network, initialGeneration)
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
        
        offSprings += createDAPChromControllers(network, [Chromosome(firstChildGenes), Chromosome(secondChildGenes)])
    
    newPopulation = chromControllers + offSprings
    newPopulation.sort(key=lambda c: c.maximumLoad)
    chromControllers = newPopulation[:configuration.populationSize]

    currentGeneration += 1
    print(f'Best DAP: {chromControllers[0].maximumLoad}')
    
  return chromControllers[0]
  

# DDAP
def solveDDAP(network, configuration) -> DDAPChromosomeController: 
  initialGeneration = createFirstGeneration(network, configuration)
  chromControllers = createDDAPChromControllers(network, initialGeneration)
  chromControllers.sort(key=lambda c: c.totalCost)

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
        
        offSprings += createDDAPChromControllers(network, [Chromosome(firstChildGenes), Chromosome(secondChildGenes)])
    
    newPopulation = chromControllers + offSprings
    newPopulation.sort(key=lambda c: c.totalCost)
    chromControllers = newPopulation[:configuration.populationSize]

    currentGeneration += 1
    print(f'Best DDAP: {chromControllers[0].totalCost}')
    
  return chromControllers[0]

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
  if numberOfPaths == 1: return gene

  pathRandomOne, pathRandomTwo = getTwoRandomIndexes(numberOfPaths)
  
  pathLoadValueOne = gene.values[pathRandomOne]
  pathLoadValueTwo = gene.values[pathRandomTwo]

  gene.values[pathRandomOne] = pathLoadValueTwo
  gene.values[pathRandomTwo] = pathLoadValueOne
  
  return gene

# MARK: - Chromosome controllers

def createDAPChromControllers(network, generation: List[Chromosome]):
  chromControllers = []
  for chrom in generation:
    linkLoad = getLinkLoad(network, chrom)
    maximumLoad = getMaximumLoad(linkLoad, network.links)
    chromControllers.append(DAPChromosomeController(chrom, linkLoad, maximumLoad))
  return chromControllers

def createDDAPChromControllers(network, generation: List[Chromosome]):
  chromControllers = []
  for chrom in generation:
    linkLoad = getLinkLoad(network, chrom)
    totalCost = getTotalCost(linkLoad, network.links)
    chromControllers.append(DDAPChromosomeController(chrom, linkLoad, totalCost))
  return chromControllers

def getLinkLoad(network, chromosome):
  linkLoad = [0] * len(network.links)

  for demandId, demand in enumerate(network.demands):
    gene = chromosome.genes[demandId]
    for pathId, path in enumerate(demand.paths):
      for linkId in path.linkId:
        linkLoad[linkId - 1] += gene.values[pathId]
  
  return linkLoad

def getMaximumLoad(linkLoad, links):
  maximumLoad = 0
  for link in links:
    maximumLoad = linkLoad[link.id - 1] - link.numberOfModules * link.linkModule
  return maximumLoad

def getTotalCost(linkLoad, links):
  link_size_matrix = {}
  totalCost = 0
  
  for link in links:
    link_size = math.ceil(linkLoad[link.id - 1] / link.linkModule)
    link_size_matrix[link.id - 1] = link_size
    totalCost += link_size * link.moduleCost
  return totalCost

# MARK: - Chromosome generation

def createFirstGeneration(network, configuration: Configuration) -> List[Chromosome]:
  generation = []
  for _ in range(configuration.populationSize):
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


