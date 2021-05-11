from dataclasses import dataclass

@dataclass
class Configuration:
  populationSize = 40 # is that should be % 4 == 0 ?
  crossoverProbability = 0.1
  mutationProbability = 0.1

  # Stop criteria parameters
  maxTimeInSeconds = 10
  maxGenerationNumber = 50
  maxMutationEvents = 800
  maxImprovementsNumber = 15

  def stopCrtiteriaHit(self, currentGeneration, mutationCount, currentTimeInSeconds):
    return currentGeneration > self.maxGenerationNumber or mutationCount > self.maxMutationEvents or currentTimeInSeconds > self.maxTimeInSeconds