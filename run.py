from geneticd.island import Topology

def run():
    t = Topology.gridTopology([str(i) for i in range(6)], 2, 3)
    print(t.visualize())

if __name__ == "__main__":
    run()
