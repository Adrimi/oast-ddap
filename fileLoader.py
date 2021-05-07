import xml.dom.minidom
import os

def loadFileFrom(path):
  doc = xml.dom.minidom.parse(path)
  return doc