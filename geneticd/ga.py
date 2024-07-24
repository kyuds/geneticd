import random
import math
import copy
from abc import ABC, abstractmethod
from functools import cmp_to_key
from geneticd.chromosome import ChromosomeFactory, Chromosome

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
    factory : ChromosomeFactory to initialize population.

    Note: individual GA Engines have stable populations. Variadic GA are known
    to be effective, so to achieve this, vary population size on Island
    granularity by randomizing parameters.

    """
    def __init__(self, 
                 p: 'GAParameter', # refer below
                 factory: ChromosomeFactory):
        self.p = p
        self.factory = factory

        self.population = None
        self.fitnessFunc = None
        # function to compare fitness values (maximum, minimum, etc). 
        # If better fitness => 1. Equal => 0, Worse => -1.
        self.fitnessOrder = None
        # crossover and mutation functions are stored in a list of tuples, 
        # where the first element is the function and the second element 
        # is the weight. Use the __co, __mu selector functions. 
        self.crossoverFuncs = []
        self.mutationFuncs = []
        self.selectionFunc = None
        self.retainFunc = None

        # stored to return result of GA.
        self.bestChromosome = None

    def start(self, epoch: int = 20):
        """
        Setup GA engine.
        """
        assert self.fitnessFunc is not None
        assert self.fitnessOrder is not None
        assert self.selectionFunc is not None
        assert self.retainFunc is not None
        assert len(self.crossoverFuncs) > 0
        assert len(self.mutationFuncs) > 0
        assert self.bestChromosome is None

        self.population = self.factory.generate(self.p.population)
        for p in self.population:
            p.fitness, p.epoch = self.fitnessFunc(p), 0
            if self.bestChromosome is None or \
                self.fitnessOrder(p.fitness, self.bestChromosome.fitness) > 0:
                self.bestChromosome = p

        self.proceed(epoch)

    def proceed(self, epoch: int = 20):
        """
        Runs actual GA. Can be called as a continuation after a previous round
        of "proceed"ing. When called for the first time, <start> has to be
        called.
        """
        assert self.population is not None, "call <start> to start GA."
        # 0 epoch = initialization.
        for ep in range(1, epoch + 1):
            assert len(self.population) == self.p.population, \
                   "population needs to be stable."
            
            self.population.sort(
                key=lambda p: cmp_to_key(self.fitnessOrder)(p.fitness), 
                reverse=True)
            
            numSelect = (math.floor(
                self.p.population * self.p.crossoverRate) + 1) // 2 * 2
            numRetain = self.p.population - numSelect

            parents = self.selectionFunc(self.population, numSelect)
            retained = self.retainFunc(self.population, numRetain)

            newGen = retained
            for i in range(0, numSelect, 2):
                c1, c2 = self.__co()(parents[i], parents[i + 1])
                c1.epoch, c2.epoch = ep, ep
                newGen.extend([c1, c2])

            for i in range(len(newGen)):
                mutated = random.random() < self.p.mutationRate
                if mutated:
                    newGen[i] = self.__mu()(newGen[i])
                if newGen[i].epoch == ep or mutated:
                    f = self.fitnessFunc(newGen[i])
                    if self.fitnessOrder(f, self.bestChromosome.fitness) > 0:
                        # we use deep copy to prevent object from being 
                        # modified in subsequent generations.
                        self.bestChromosome = copy.deepcopy(newGen[i])
                    newGen[i].fitness = f
            
            self.population = newGen

            # check if GA has converged over a specific number of epochs.
            # we don't check for convergence if convergence epoch is -1.
            ce, be = self.p.convergeEpoch, self.bestChromosome.epoch
            if ce != -1 and ep - be > ce:
                return

    def __select(self, funcs: list):
        assert len(funcs) > 0
        if len(funcs) == 1:
            return funcs[0][0]
        f, w = zip(*funcs)
        return random.choices(f, weights=w, k=1)[0]

    def __co(self):
        return self.__select(self.crossoverFuncs)

    def __mu(self):
        return self.__select(self.mutationFuncs)

    def addCrossover(self, func, weight: int = 1) -> 'GAEngine':
        assert weight > 0
        self.crossoverFuncs.append((func, weight))
        return self

    def addMutation(self, func, weight: int = 1) -> 'GAEngine':
        assert weight > 0
        self.mutationFuncs.append((func, weight))
        return self
    
    def setSelection(self, func) -> 'GAEngine':
        assert self.selectionFunc is None
        self.selectionFunc = func
        return self
    
    def setRetain(self, func) -> 'GAEngine':
        assert self.retainFunc is None
        self.retainFunc = func
        return self
    
    def setFitness(self, fitness, order) -> 'GAEngine':
        assert self.fitnessFunc is None
        assert self.fitnessOrder is None
        self.fitnessFunc = fitness
        self.fitnessOrder = order
        return self
    
    def best(self) -> Chromosome:
        return self.bestChromosome

class GAParameter:
    """
    Parameters for Genetic Algorithm 

    Constructor:
    ---------------
    population    : initial population number.
    mutationRate  : mutation rate
    crossoverRate : crossover rate
    convergeEpoch : number of epochs after which GA will terminate early,
                    provided that the best chromosome remains the same.
                    defaulted to -1 (no early termination)
                    
    """
    def __init__(self,
                 population: int,
                 mutationRate: float,
                 crossoverRate: float,
                 convergeEpoch: int = -1):
        assert population > 0, "population must be positive"
        self.population = population
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.convergeEpoch = convergeEpoch
    
    def setConvergence(self, epoch: int):
        """
        Refer to class description.
        """
        self.convergeEpoch = epoch
    
    @staticmethod
    def random(min_p: int, max_p: int) -> 'GAParameter':
        """
        As shown in literature, a random, heterogenous parameter formulation
        for distributed island genetic algorithms are very advantageous. This
        helper function creates randomized parameters easily.
        https://ieeexplore.ieee.org/document/5949703
        """
        assert min_p < max_p and min_p > 0
        return GAParameter(
            random.randint(min_p, max_p),
            random.uniform(0.05, 0.2),
            random.uniform(0.65, 1.0))
    
    @staticmethod
    def default() -> 'GAParameter':
        return GAParameter(20, 0.1, 0.7)
