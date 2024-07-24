from abc import ABC, abstractmethod

class Chromosome(ABC):
    """
    Abstract Base Class for Chromosome Instances
    The fitness/epoch member variables are used internally. These variables
    can/should be used to implement selection functions, but please don't
    mutate them.

    Members:
    ---------------
    fitness : fitness values of the chromosome
    epoch   : epoch in which chromosome was crafted. (0 for initialization)

    As a side note, the framework does deepcopy chromosomes (sometimes, mainly
    for keeping track of the best chromosome). So, if necessary, implement the
    __deepcopy__ function. 
    
    """
    def __init__(self):
        self.fitness = None
        self.epoch = None
    
    @abstractmethod
    def hash(self):
        """
        For deduplication purposes. TBD.
        """
        pass

class ChromosomeFactory(ABC):
    """
    Abstract Base Class for Creating Chromosomes

    """
    def __init__(self):
        pass
    
    @abstractmethod
    def generate(self, population) -> list[Chromosome]:
        """
        Creates *population* number of chromosomes to set the initial 
        population. Considering using variadic arguments for explicit 
        initialization of the population. This function is called internally
        from the framework.
        """
        pass
