import os
from loaders.XMLFileLoader import loadFileFrom
from parsers.NetworkParser import createNetworkFrom
from algorithms.algorithms import setSeed, solve, Configuration

inputDirectory = "input/"
filename = "net4.xml"

seed = "abc"

environmentConfiguration = Configuration()

def main():
  path = os.path.join(os.getcwd(), inputDirectory + filename)
  doc = loadFileFrom(path)
  network = createNetworkFrom(doc)
  
  setSeed(seed)

  solvedNetwork = solve(network, environmentConfiguration)

if __name__ == '__main__':
  main()