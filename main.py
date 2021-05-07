import os
import fileLoader

def main():
  path = os.path.join(os.getcwd(), "input/net12_1.xml")
  doc = fileLoader.loadFileFrom(path)
  network = parse(doc)

if __name__ == '__main__':
  main()