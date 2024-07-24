from abc import ABC, abstractmethod
from geneticd.chromosome import Chromosome

class GATemplate(ABC):
    """
    This class is not actually used, but the class exists to be a template for
    easy implementation of a genetic algorithm based on this framework. Refer
    to the function signatures below to see what we expect from registered
    functions/handlers. 
    
    """
    
    @abstractmethod
    @staticmethod
    def fitnessFunc(p: Chromosome):
        """
        Returns the fitness value of a given chromosome.

        """
        pass

    @abstractmethod
    @staticmethod
    def fitnessOrder(f1, f2) -> int:
        """
        Returns the fitness order of fitness values f1 and f2. If f1 is 
        more fit, the return value is greater than 0. If equal, 0. If 
        less fit, then the return value is smaller than 0.

        """
        pass

    @abstractmethod
    @staticmethod
    def crossover(p1: Chromosome, p2: Chromosome) -> Chromosome:
        """
        Returns two new chromosomes that are the resulting children of
        p1 and p2's crossover. Parents can be mutated. 

        """
        pass

    @abstractmethod
    @staticmethod
    def mutation(p: Chromosome) -> Chromosome:
        """
        Creates a new chromosome that is the mutated version of the input.
        Return value can be a modified version of the input.

        """
        pass

    @abstractmethod
    @staticmethod
    def select(population: list[Chromosome], size: int) -> list[Chromosome]:
        """
        Given a list of Chromosomes, select *size* number of chromosomes as
        crossover candidates. As with the <retain> function (shown below), 
        the population list is sorted in order with best fitness at lower
        indicies. There is no reason to resort. 

        """
        pass

    @abstractmethod
    @staticmethod
    def retain(population: list[Chromosome], size: int) -> list[Chromosome]:
        """
        Given a list of Chromosomes, select *size* number of chromosomes to
        live through the current generation. This can be used to implement
        elitist strategies, etc. 

        """
        pass
    