from dataclasses import dataclass
from typing import List, Union


@dataclass
class PathElement:
    id: int
    linkId: Union[List[int], int]


@dataclass
class PurplePath:
    id: int
    linkId: List[int]


@dataclass
class Paths:
    path: Union[List[PathElement], PurplePath]


@dataclass
class Demand:
    id: int
    startNode: int
    endNode: int
    volume: int
    paths: Paths


@dataclass
class Demands:
    demand: List[Demand]


@dataclass
class Link:
    id: int
    startNode: int
    endNode: int
    numberOfModules: int
    moduleCost: int
    linkModule: int


@dataclass
class Links:
    link: List[Link]


@dataclass
class Network:
    links: Links
    demands: Demands


@dataclass
class Data:
    network: Network
    standalone: str
