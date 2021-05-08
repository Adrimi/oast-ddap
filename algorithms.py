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


# Models namespace, algorithm specific objects


@dataclass
class Gene:
  values: List[int]

@dataclass
class Chromosome:
  genes: List[Gene]


@dataclass
class Configuration:
  populationSize = 40 # is that should be % 4 == 0 ?
  crossoverProbability = 0.5
  mutationProbability = 0.1
  maxIterationNumber = 50
  maxGenerationNumber = 50
  maxMutationEvents = 800
  maxImprovementsNumber = 15


# Main API

def solve(network, configuration): 
  initialGeneration = createFirstGeneration(network, configuration)
  print(initialGeneration[0])


# Helper methods

def setSeed(seed):
  random.seed(seed)


def createFirstGeneration(network, configuration) -> List[Chromosome]:
  generation = []
  for i in range(configuration.populationSize):
    generation.append(createChromosome(network, configuration))
  return generation


def createChromosome(network, configuration) -> Chromosome:
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

      if index == numberOfPaths - 1 and sum(values) != demand.volume:
        values = values[:-1] + [values[-1] + demand.volume - sum(values)]

  return Gene(values)


