from collections import defaultdict
import ray
import networkx as nx
import matplotlib.pyplot as plt

@ray.remote
class Island:
    def __init__(self, name: str):
        self.name = name

class Topology:
    """
    Island are interconnected with each other as graphs. Whether the
    graph is directed or undirected doesn't matter (though for population
    transfers and nature analogy, undirected makes more sense.)

    The Topology class represents a logical graph structure for the GA setup.
    Each node is a single Island that will run its (possibly distributed)
    GA instance. 

    GA populations will only move between Islands that are "connected" to each
    other defined by the Topology.
    """
    def __init__(self):
        self.topology = defaultdict(set)

    def connect(self, n1: str, n2: str):
        """
        Creates an undirected edge between nodes n1 and n2. n1 and n2 cannot be
        the same node. 
        """
        assert n1 != n2, "island cannot connect to itself"
        self.topology[n1].add(n2)
        self.topology[n2].add(n1)
    
    def directed_connect(self, n1: str, n2: str):
        """
        Creates a directed edge from n1 to n2. n1 and n2 cannot be the same 
        node.
        """
        assert n1 != n2, "island cannot connect to itself"
        self.topology[n1].add(n2)
    
    def visualize(self):
        g = nx.DiGraph()
        for node, neighbors in self.topology.items():
            for neighbor in neighbors:
                g.add_edge(node, neighbor)
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(g)
        nx.draw(g, pos, with_labels=True, node_color='skyblue', 
                node_size=2000, edge_color='gray', font_size=20, 
                font_color='black', arrowsize=20)
        plt.title("Topology")
        plt.show()

    @staticmethod
    def gridTopology(nodes: list[str], r: int, c: int) -> 'Topology':
        """
        Creates a grid-shaped topology. for instance, denote the configuration
        for r = 2, c = 3:
        
        n0 - n1 - n2
        |    |    |
        n3 - n4 - n5

        Populations in n0, for instance, can be sent to and received from n3 
        and n1.
        """
        assert len(nodes) == len(set(nodes)), "node names must be unique"
        assert len(nodes) == r * c, "number of nodes must equal grid size"
        t = Topology()
        for row in range(r):
            for col in range(c):
                pos = row * c + col
                if row != r - 1:
                    t.connect(nodes[pos], nodes[pos + c])
                if col != c - 1:
                    t.connect(nodes[pos], nodes[pos + 1])
        return t
    
    @staticmethod
    def completeTopology(nodes: list[str]) -> 'Topology':
        """
        Creates a topology where all nodes are connected to each other, forming
        a complete graph. Note that this approach is highly unrecommended, not 
        only due to its computational inefficiency, but research has found that
        the solutions found from such constructs are not that optimal either. 
        """
        assert len(nodes) == len(set(nodes)), "node names must be unique"
        t = Topology()
        for i in range(len(nodes) - 1):
            for j in range(i + 1, len(nodes)):
                t.connect(nodes[i], nodes[j])
        return t

    @staticmethod
    def ringTopology(nodes: list[str]) -> 'Topology':
        """
        Creates a ring topology, where each node is connected to its two adjacent 
        nodes, forming a circle.
        """
        assert len(nodes) == len(set(nodes)), "node names must be unique"
        t = Topology()
        t.connect(nodes[0], nodes[-1])
        for i in range(len(nodes) - 1):
            t.connect(nodes[i], nodes[i + 1])
        return t
