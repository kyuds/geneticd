import random

from geneticd.chromosome import Chromosome, ChromosomeFactory

"""
Simple example of a Genetic Algorithm designed to guess a string.

Given the length of the target string, the purpose of this GA is to find the
target string. Note that this is just an example, more targeted towards a 
single node GA, not a distributed GA, simply because the example is too
simple.
"""

ALPHABET_GENES = ' abcdefghijklmnopqrstuvwxyz'

class StringChromosome(Chromosome):
    def __init__(self, initial: str):
        super().__init__()
        self.gene = initial

class StringChromosomeFactory(ChromosomeFactory):
    def __init__(self, population: int, length: int):
        super().__init__(population)
        self.length = length
    
    def generate(self) -> list[StringChromosome]:
        chromosomes = []
        for _ in range(self.population):
            tmp = ""
            for _ in range(self.length):
                tmp += random.choice(ALPHABET_GENES)
            chromosomes.append(StringChromosome(tmp))
        return chromosomes
