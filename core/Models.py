from dataclasses import dataclass
from typing import List

# MARK: - Core models

@dataclass
class Path:
  id: int
  linkId: List[int]


@dataclass
class Demand:
  id: int
  startNode: int
  endNode: int
  volume: int
  paths: List[Path]


@dataclass
class Link:
  id: int
  startNode: int
  endNode: int
  numberOfModules: int
  moduleCost: int
  linkModule: int


@dataclass
class Network:
  links: List[Link]
  demands: List[Demand]


# MARK: - Algorithm specific models

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
