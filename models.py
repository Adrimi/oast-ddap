from dataclasses import dataclass
from typing import List

@dataclass
class Path:
  linkId: List[int]


@dataclass
class Demand:
  startNode: int
  endNode: int
  volume: int
  paths: List[Path]


@dataclass
class Link:
  startNode: int
  endNode: int
  numberOfModules: int
  moduleCost: int
  linkModule: int


@dataclass
class Network:
  links: List[Link]
  demands: List[Demand]