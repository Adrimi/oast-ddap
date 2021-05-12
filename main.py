import os
from persistence.XMLFileLoader import loadFileFrom
from persistence.XMLFileWriter import save
from parsers.NetworkXMLDecoder import decode
from parsers.XMLEncoder import encode
from algorithms.DAPAlgorithm import setSeed, solve
from configuration.Configuration import Configuration

inputDirectory = "input/"
outputDirectory = "output/"
filename = "net12_1.xml" 

seed = "abc"

environmentConfiguration = Configuration()

def main():
  pathToLoad = os.path.join(os.getcwd(), inputDirectory + filename)
  doc = loadFileFrom(pathToLoad)
  network = decode(doc)
  
  setSeed(seed)
  solution = solve(network, environmentConfiguration)

  pathToSave = os.path.join(os.getcwd(), outputDirectory + filename + "-solved.xml")
  
  stringifiedSolution = encode(solution)

if __name__ == '__main__':
  main()