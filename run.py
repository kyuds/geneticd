from equations import Griewank, Rastrigin
from ga import GAEngine, RandomParamGenerator

DIMENSIONS = 5
MIN_POPULATION = 10
MAX_POPULATION = 30
MIN_MUTATION = 0.05
MAX_MUTATION = 0.15
MIN_CROSSOVER = 0.6
MAX_CROSSOVER = 0.9

if __name__ == "__main__":
    generator = RandomParamGenerator(MIN_POPULATION, 
                                     MAX_POPULATION, 
                                     MIN_MUTATION, 
                                     MAX_MUTATION, 
                                     MIN_CROSSOVER, 
                                     MAX_CROSSOVER)
    ga = GAEngine(generator.generate(), Griewank(), DIMENSIONS)
    ga.start()
    for p in ga.population:
        print(p)
