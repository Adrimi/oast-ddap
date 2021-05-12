def save(string: str, filePath: str):
  with open(filePath, "w") as file:
    file.write(string)