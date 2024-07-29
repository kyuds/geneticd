import asyncio
import ray
from ga import GAEngine
from topology import Topology
from chromosome import Chromosome

@ray.remote
class Island:
    """
    Class definition for a remote island. An island is remote because
    individual populations will evolve separately from other neighboring
    islands. By theory of evolution, it is regarded that the fitter individuals
    may migrate to other islands for further reproduction. This class handles
    such message passing logic.

    Constructor:
    ---------------
    name    : name of the island
    ga      : ga engine. Refer to ga.py
    epoch   : number of cycles
    cycle   : number of epochs to run GA before migrating.
    
    """
    def __init__(self, name: str, ga: GAEngine, cycle: int):
        self.name = name
        self.ga = ga
        self.cycle = cycle
        self.handles = None

    def connect(self, handles):
        """
        Connect remote Island instance to other remote Island instances.
        """
        self.handles = handles
    
    async def send_migrant(self) -> Chromosome:
        # currently designed to send migrants to ALL neighboring islands.
        # we can use the "self.name" variable to filter in the future.
        return self.ga.updated_result()
    
    def get_name(self) -> str:
        return self.name

    def get_best(self) -> Chromosome:
        return self.ga.result()

    async def request_migrants(self):
        migrants = await asyncio.gather(*(
            h.send_migrant.remote() for h in self.handles
        ))
        self.ga.add_population(migrants)

    def start(self):
        assert self.handles is not None
        self.ga.start(self.cycle)

    def proceed(self):
        self.ga.proceed(self.cycle)

class Archipelago:
    """
    Archipelago is the execution engine for remote islands. As the name
    suggests, this executes on a group of remote island handles. Think of it
    as the coordinator in processing engines such as pregel (pregel also has
    a processing stage, supersteps, and a data exchange stage). Likewise, 
    islands execute GA cycles in parallel, and are coordinated briefly to
    exchange the best chromosomes. 

    Constructor:
    ---------------
    handles : ray remote handles to islands
    epoch   : number of epochs to run GA. Best (newly found) chromosomes will
              be exchanged between epochs.
    
    """
    def __init__(self, handles, epoch: int):
        self.handles = handles
        self.epoch = epoch
    
    def execute(self):
        ray.get([h.start.remote() for h in self.handles])
        for _ in range(self.epoch - 1):
            ray.get([h.request_migrants.remote() for h in self.handles])
            ray.get([h.proceed.remote() for h in self.handles])
        return ray.get([h.get_best.remote() for h in self.handles])
