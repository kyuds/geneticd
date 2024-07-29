from abc import ABC, abstractmethod
import math
import random
from chromosome import Chromosome

class Equation(ABC):
    """
    Base class for target-optimization equations. The abstract method __call__
    will take in a vector and output a result of the calculations. Also, 
    we need to provide bounds for these functions as well (these bounds are
    provided by a reference paper linked in the README).

    The equations implemented for this project are considered as minimization 
    problems. The goal is to find the vector of numbers in which the equation 
    results in the smallest value.

    """
    minimum = None
    maximum = None

    def __init__(self, dim: int):
        self.dim = dim

    @abstractmethod
    def calc(self, vec: list[float]) -> float:
        pass

    def generate(self, pop: int) -> list[Chromosome]:
        """
        Generate a list of chromosomes (with precomputed fitness values and 
        epoch) to initialize a population list. This depends on the minimum
        and maximum values of the given function. 
        """
        population = []
        for _ in range(pop):
            vec = [
                random.uniform(self.minimum, self.maximum)
                for _ in range(self.dim)
            ]
            fitness = self.calc(vec)
            population.append(Chromosome(vec, 0, fitness))
        return population

class Griewank(Equation):
    minimum = -512
    maximum = 512

    def __init__(self, dim):
        super().__init__(dim)

    def calc(self, vec: list[float]) -> float:
        summation = 0
        product = 1
        # because summation for the equation starts at 1.
        for i, n in enumerate(vec, start=1):
            assert self.minimum <= n and n <= self.maximum
            summation += n ** 2
            product *= math.cos(n / math.sqrt(i))
        return 1 + summation / 4000 + product
    
class Rastrigin(Equation):
    minimum = -5.12
    maximum = 5.12

    def __init__(self, dim):
        super().__init__(dim)

    def calc(self, vec: list[float]) -> float:
        result = len(vec) * 10
        for n in vec:
            assert self.minimum <= n and n <= self.maximum
            result += n ** 2
            result -= 10 * math.cos(2 * math.pi * n)
        return result

class Schwefel(Equation):
    minimum = -512
    maximum = 512

    def __init__(self, dim):
        super().__init__(dim)

    def calc(self, vec: list[float]) -> float:
        result = 0
        for n in vec:
            assert self.minimum <= n and n <= self.maximum
            result -= n * math.sin(math.sqrt(abs(n)))
        return result
