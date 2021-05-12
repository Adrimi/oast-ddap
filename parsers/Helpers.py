def reduce(elements, encoder):
  joinedElements = ""
  for element in elements:
    joinedElements += encoder(element)
  return joinedElements