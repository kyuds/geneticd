from collections import defaultdict
import ray

@ray.remote
class LocalIsland:
    def __init__(self):
        pass

class Topology:
    def __init__(self):
        self.topology = defaultdict(set)

    def connect(self, n1: str, n2: str):
        assert n1 != n2, "island cannot connect to itself"
        self.topology[n1].add(n2)
        self.topology[n2].add(n1)

    @staticmethod
    def squareTopology(nodes: list[str]) -> 'Topology':
        return Topology()
