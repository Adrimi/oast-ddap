import os
from helpers import loadFileFrom, createNetworkFrom

sourceDirectory = "input/"
filename = "net4.xml"

def main():
  path = os.path.join(os.getcwd(), sourceDirectory + filename)
  doc = loadFileFrom(path)
  network = createNetworkFrom(doc)
  print(network.demands[0].paths[1])

if __name__ == '__main__':
  main()