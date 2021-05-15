from dataclasses import dataclass

@dataclass
class Configuration:
  populationSize = 1000
  crossoverProbability = 0.2
  mutationProbability = 0.1

  # Stop criteria parameters
  maxTimeInSeconds = 10
  maxGenerationNumber = 100
  maxMutationEvents = 600
  maxImprovementsNumber = 15

  def stopCrtiteriaHit(self, currentGeneration, mutationCount, currentTimeInSeconds):
    return currentGeneration > self.maxGenerationNumber or mutationCount > self.maxMutationEvents or currentTimeInSeconds > self.maxTimeInSeconds