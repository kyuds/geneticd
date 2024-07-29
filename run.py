import ray
from equations import Griewank, Rastrigin, Schwefel
from ga import GAEngine, RandomParamGenerator
from islands import Island, Archipelago
from topology import Topology

DIMENSIONS = 10
MIN_POPULATION = 10
MAX_POPULATION = 30
MIN_MUTATION = 0.1
MAX_MUTATION = 0.2
MIN_CROSSOVER = 0.6
MAX_CROSSOVER = 0.9
ISLAND_GRID_ROW = 3
ISLAND_GRID_COL = 2
EPOCH = 10
CYCLE = 10

if __name__ == "__main__":
    generator = RandomParamGenerator(MIN_POPULATION, 
                                     MAX_POPULATION, 
                                     MIN_MUTATION, 
                                     MAX_MUTATION, 
                                     MIN_CROSSOVER, 
                                     MAX_CROSSOVER)
    ## setup
    islands = []
    for i in range(ISLAND_GRID_COL * ISLAND_GRID_ROW):
        name = f"island_{i}"
        ga = GAEngine(generator.generate(), Griewank(DIMENSIONS))
        islands.append((name, Island.remote(name, ga, CYCLE)))

    t = Topology.gridTopology([i[0] for i in islands], 
                              ISLAND_GRID_ROW, 
                              ISLAND_GRID_COL)
    waiter = []
    for name, island in islands:
        names, handles = t.get_connections(name), []
        for n, i in islands:
            if n in names:
                handles.append(i)
        waiter.append(island.connect.remote(handles))
    # wait for handles to be sent to all remote Islands.
    ray.get(waiter)
    print("Connected islands based on topology")

    ## distributed island genetic algorithm
    archipelago = Archipelago([h for _, h in islands], EPOCH)
    results = archipelago.execute()
    for c in results:
        print(c)

    best = sorted(results, key=lambda c: c.fitness)[0]
    print(f"Best fitness: {best.fitness}")
    print("Finished")
