import os
from persistence.XMLFileLoader import loadFileFrom
from persistence.XMLFileWriter import save
from parsers.NetworkXMLDecoder import decode
from parsers.XMLEncoder import encodeDAP, encodeDDAP
from algorithms.Algorithms import setSeed, solveDAP, solveDDAP
from configuration.Configuration import Configuration

inputDirectory = "input/"
outputDirectory = "output/"
filename = "net12_1.xml" 

seed = "JSG"

environmentConfiguration = Configuration()

def main():
  pathToLoad = os.path.join(os.getcwd(), inputDirectory + filename)
  doc = loadFileFrom(pathToLoad)
  network = decode(doc)
  
  setSeed(seed)
  dapSolution = solveDAP(network, environmentConfiguration)
  ddapSolution = solveDDAP(network, environmentConfiguration)
  
  dapSolutionStringified = encodeDAP(dapSolution, network)
  ddapSolutionStringified = encodeDDAP(ddapSolution, network)

  pathToSaveDAP = os.path.join(os.getcwd(), outputDirectory + filename + "-DAP.xml")
  pathToSaveDDAP = os.path.join(os.getcwd(), outputDirectory + filename + "-DDAP.xml")

  save(dapSolutionStringified, pathToSaveDAP)
  save(ddapSolutionStringified, pathToSaveDDAP)

if __name__ == '__main__':
  main()