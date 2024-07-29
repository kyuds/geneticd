import random
import copy
import math
from equations import Equation
from chromosome import Chromosome

class GAEngine:
    """
    Genetic Algorithm Engine class that will actually run the genetic
    algorithm. The GAEngine lives inside the Island (defined in island.py)
    and executes on the population there. Alternatively, the GAEngine can be
    used separately to invoke a single process GA. 

    Constructor:
    ---------------
    p       : parameters for the genetic algorithm. 
              See GAParameter class below.
    eq      : target equation to optimize
    dim     : dimension of the equation.
    
    """
    def __init__(self, p: 'GAParameter', eq: Equation):
        self.p = p
        self.equation = eq

        self.population = None
        self.best = None
        self.updated = False
        self.epoch = 0
    
    def start(self, epoch: int = 20):
        """
        Start genetic algorithm process. Initialize our population.
        """
        assert self.population is None
        assert self.best is None
        self.population = self.equation.generate(self.p.population)
        self.proceed(epoch)
    
    def proceed(self, epoch: int = 20):
        """
        Runs actual GA. Can be called as a continuation after a previous round
        of "proceed"ing. When called for the first time, <start> has to be
        called.
        """
        assert self.population is not None
        self.updated = False

        for _ in range(1, epoch + 1):
            self.epoch += 1
            assert len(self.population) == self.p.population, \
                   "population needs to be stable."
            
            # no reversing because this is a minimization problem
            self.population.sort(key=lambda c: c.fitness)
            if self.best is None:
                self.best = copy.deepcopy(self.population[0])
                self.updated = True
            
            num_select = (math.floor(
                self.p.population * self.p.crossover_rate) + 1) // 2 * 2
            num_retain = self.p.population - num_select

            parents = self.__select(num_select)
            generation = self.__retain(num_retain)

            for i in range(0, num_select, 2):
                c1, c2 = self.__crossover(parents[i], parents[i + 1])
                c1.epoch, c2.epoch = self.epoch, self.epoch
                generation.extend([c1, c2])
            
            for c in generation:
                if random.random() < self.p.mutation_rate:
                    self.__mutate(c)
                if c.fitness is None:
                    c.fitness = self.equation.calc(c.value)
                    if c.fitness < self.best.fitness:
                        # we use deep copy to prevent object from being 
                        # modified in subsequent generations.
                        self.best = copy.deepcopy(c)
                        # indicate to island that we have a newly found
                        # local minimum
                        self.updated = True
            
            self.population = generation
    
    def __select(self, num: int) -> list[Chromosome]:
        # Roulette Wheel Selection
        assert num < self.p.population
        # because smaller fitness values = higher weights
        return random.choices(
            self.population, 
            weights=[1 / c.fitness for c in self.population], 
            k=num)

    def __retain(self, num: int) -> list[Chromosome]:
        assert num < self.p.population
        return self.population[:num]

    def __crossover(self, c1: Chromosome, c2: Chromosome) -> tuple[Chromosome]:
        # no in-place modification (will conflict with retained Chromosomes
        # and other crossover operations)
        # one-point crossover
        point = random.randint(0, self.equation.dim - 1)
        g1 = c1.value[:point] + c2.value[point:]
        g2 = c2.value[:point] + c1.value[point:]
        return (Chromosome(g1, None, None), Chromosome(g2, None, None))

    def __mutate(self, c: Chromosome, intensity: int = 0.05):
        # in-place modification
        assert intensity < 1 and intensity > 0
        for i in range(len(c.value)):
            factor = random.uniform(1 - intensity, 1 + intensity)
            m = c.value[i] * factor
            if m < self.equation.minimum or m > self.equation.maximum:
                # reverse to prevent values from clustering to maximum or
                # minimum values.
                m = (2 - factor) * c.value[i]
            c.value[i] = m
        # clear fitness for recalculation
        c.fitness = None

    def add_population(self, chromosomes: list[Chromosome]):
        self.population.extend(chromosomes)
        self.population.sort(key=lambda c: c.fitness)
        self.population = self.population[:self.p.population]

    def result(self):
        return self.best

    def updated_result(self):
        if self.updated:
            return self.best
        return None

class GAParameter:
    """
    Parameters for Genetic Algorithm 

    Constructor:
    ---------------
    population    : initial population number.
    mutationRate  : mutation rate
    crossoverRate : crossover rate
                    
    """
    def __init__(self,
                 population: int,
                 mutation_rate: float,
                 crossover_rate: float):
        assert population > 0
        assert mutation_rate > 0
        assert crossover_rate > 0
        self.population = population
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
    
    def __str__(self):
        m, c = round(self.mutation_rate, 2), round(self.crossover_rate, 2)
        return f"p: {self.population}, m: {m}, c: {c}"

class RandomParamGenerator:
    """
    As shown in the paper, setting random parameters for each GA instance
    is sufficient to run an effective GA. Setting random parameters as
    opposed to fine tuning parameters has the added advantage of being
    simple.

    This class serves to generate heterogenous parameters for individual
    islands in a compact manner.
    
    """
    def __init__(self, 
                 min_population: int,
                 max_population: int,
                 min_mutation: float,
                 max_mutation: float,
                 min_crossover: float,
                 max_crossover: float):
        assert min_population > 0 and max_population > min_population
        assert min_mutation > 0 and max_mutation > min_mutation
        assert min_crossover > 0 and max_crossover > min_crossover
        self.min_population = min_population
        self.max_population = max_population
        self.min_mutation = min_mutation
        self.max_mutation = max_mutation
        self.min_crossover = min_crossover
        self.max_crossover = max_crossover
    
    def generate(self) -> GAParameter:
        return GAParameter(
            random.randint(self.min_population, self.max_population),
            random.uniform(self.min_mutation, self.max_mutation),
            random.uniform(self.min_crossover, self.max_crossover))
