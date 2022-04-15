import random as rnd
from collections import Callable

import pandas as pd
import numpy as np
from random import choices
import Model.Entity


class EntityLister:

    def __init__(self, sol_per_pop: int, num_weights: int, genes: np.array):
        self.EvolutionDF = pd.DataFrame(columns=['mate1', 'mate2', 'fitness', 'mutation_chance', 'body', 'childhash'])
        self.newPop = np.empty((sol_per_pop, num_weights), dtype=object)
        self.newPop.flat = [Model.Entity.Entity(np.random.choice(genes, size=1)) for _ in self.newPop.flat]

    def getEvolutionDF(self) -> pd.DataFrame:
        if self.EvolutionDF.empty:
            ValueError('You have to start the evolution before pulling data out!')
        else:
            return self.EvolutionDF
    def getEntityBody(self, index: int) -> str:
        return str(self.newPop.flat[index].get_body())

    def getEntityHash(self, index: int) -> str:
        return str(self.newPop.flat[index].get_hash())

    def start_evolution(self, generation_limit: int = 100) -> []:
        for generation in range(generation_limit):
            mate1 = rnd.choice(self.newPop.flat)
            mate = rnd.choice(self.newPop.flat)
            fitness = self.__fitness(mate1, self.newPop.flat,
                                   rnd.randrange(0, 50))
            num_mutations = rnd.randrange(1, 5)
            prob_mutation = rnd.randrange(1.5, 5)
            child = self.__mutation(self.__crossover(mate1, mate))
            mate1.add_children(child)
            mate.add_children(child)
            self.newPop.__add__(child)
            self.EvolutionDF.append([mate.get_body(), mate1.get_body(), fitness,
                                     prob_mutation, child.get_body(), child.get_hash()])

    def __fitness(self, entity: 'Model.Entity', entities: ['Model.Entity'], weight_limit: int) -> int:
        weight = 0  # weight = length of bodytext
        value = 0
        for i, child in enumerate(entities):
            if entity.get_body()[i] == child.get_body()[i]:
                weight += len(child.get_body())
                value += child.get_body()
                if weight > weight_limit:
                    return 0
        return value

    def __selection_pair(self, Population: ['Model.Entity'], weight_limit: int) -> 'Model.Entity':
        return choices(
            population=Population,  # The passed in population
            weights=[self.__fitness(gene, Population, weight_limit) for gene in Population],
            # amount of weights from matching population
            k=2  # number of parents
        )

    def __crossover(self, a: 'Model.Entity', b: 'Model.Entity') -> 'Model.Entity':
        diff = None
        if len(a.get_body()) > len(b.get_body()):
            diff = len(a.get_body()) - len(b.get_body())
        else:
            diff = len(b.get_body()) - len(a.get_body())
        halfa = a.get_body()[0:diff] + b.get_body()[diff:len(b.get_body())]
        halfb = b.get_body()[0:diff] + a.get_body()[diff:len(a.get_body())]
        x = Model.Entity.Entity('')
        if halfa > halfb:
            x.set_body(halfa)
        else:
            x.set_body(halfb)
        return x
    def __mutation(self, entity: 'Model.Entity', num_ofmutations: int = 1, probability: float = 1.5) -> 'Model.Entity':
        f = None
        for _ in range(num_ofmutations):
            index = rnd.randrange(len(entity.get_body()))
            f = entity.get_body()[index]
            f = f[index] if rnd.random() > probability else abs(entity[index] - 1)  # because abs(0-1) is 1
        return f

    def __exportPopulation(self):
        pd.DataFrame(self.newPop).to_excel('Exported.xlsx')
