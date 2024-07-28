from abc import ABC, abstractmethod
import math

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
    @abstractmethod
    def __call__(self, vec):
        pass

class Griewank(Equation):
    def __call__(self, vec):
        summation = 0
        product = 1
        # because summation for the equation starts at 1.
        for i, n in enumerate(vec, start=1):
            assert -512 <= n and n < 512
            summation += n ** 2
            product *= math.cos(n / math.sqrt(i))
        return 1 + summation / 4000 + product
    
class Rastrigin(Equation):
    def __call__(self, vec):
        result = len(vec) * 10
        for n in vec:
            assert -5.12 <= n and n < 5.12
            result += n ** 2
            result -= 10 * math.cos(2 * math.pi * n)
        return result

class Schwefel(Equation):
    def __call__(self, vec):
        result = 0
        for n in vec:
            assert -512 <= n and n < 512
            result -= n * math.sin(math.sqrt(n))
        return result
