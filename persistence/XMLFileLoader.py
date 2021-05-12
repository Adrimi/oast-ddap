import xml.dom.minidom as xml

def loadFileFrom(path):
  return xml.parse(path)