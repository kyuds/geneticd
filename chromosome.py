class Chromosome:
    """
    Wrapper class for easy accessing chromosome values and relevant
    metadata, such as epoch and fitness value.
    
    """
    def __init__(self, value, epoch = None, fitness = None):
        self.value = value
        self.epoch = epoch
        self.fitness = fitness

    def __repr__(self):
        rounded = [round(v, 2) for v in self.value]
        return f"({self.epoch}) {self.fitness} -> {rounded}"
