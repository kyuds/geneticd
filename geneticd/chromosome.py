from abc import ABC, abstractmethod

class Chromosome(ABC):
    """
    Abstract Base Class for Chromosome Instances
    Used mainly for type checking purposes.
    """

    def __init__(self):
        pass

class ChromosomeFactory(ABC):
    """
    Abstract Base Class for Creating Chromosomes

    Constructor:
    ---------------
    population: initial population size (# of chromosomes to be generated).
    
    Methods:
    ---------------
    generate  : creates *pop* number of chromosomes to set the initial 
                population.
    """

    def __init__(self, population: int):
        self.population = population
    
    @abstractmethod
    def generate(self) -> list[Chromosome]:
        pass
