import random as rnd
import openpyxl
import pandas as pd
import numpy as np
from random import choices
import Model.Entity


class EntityLister:

    def __init__(self, sol_per_pop: int, num_weights: int, genes: np.array):
        self.class_EvolutionDF = pd.DataFrame(
            columns=['mate1', 'mate2', 'fitness', 'mutation_chance', 'child_genes', 'childhash'])
        self.newPop = np.empty((sol_per_pop, num_weights), dtype=object)
        self.newPop.flat = [Model.Entity.Entity(np.random.choice(genes, size=1)) for _ in self.newPop.flat]

    def getEvolutionDF(self) -> pd.DataFrame():
        if self.class_EvolutionDF.empty:
            ValueError('You have to start the evolution before pulling data out!')
        else:
            return self.class_EvolutionDF

    def getEntityBody(self, index: int) -> str:
        return str(self.newPop.flat[index].get_body())

    def getEntityHash(self, index: int) -> str:
        return str(self.newPop.flat[index].get_hash())

    def start_evolution(self, generation_limit: int = 100, offspring_multiplier : int = 25) -> []:
        x = 0
        for generation in range(generation_limit):
            mate1 = rnd.choice(self.newPop.flat)
            mate = rnd.choice(self.newPop.flat)
            for offspring in range(offspring_multiplier):
                fitness = self.__fitness(mate1, self.newPop.flat,
                                         5000)
                prob_mutation = rnd.randrange(1, 5)
                child = self.__mutation(self.__crossover(mate1, mate), probability=prob_mutation)
                mate1.add_children(child)
                mate.add_children(child)
                np.append(self.newPop, child)
                self.class_EvolutionDF.loc[x] = [ str(mate.get_body()[0]), str(mate1.get_body()[0]), fitness, prob_mutation, str(child.get_body()), str(child.get_hash()) ]
                x = x + 1

    def __fitness(self, entity: 'Model.Entity', entities: ['Model.Entity'], weight_limit: int) -> int:
        weight = 0  # weight = length of bodytext
        for e in entities:
            for x in range(len(entity.get_body())):
                if e.get_body()[x] == entity.get_body()[x]:
                    weight += 1
            if weight > weight_limit:
                return 0
        return weight

    def __selection_pair(self, Population: ['Model.Entity'], weight_limit: int) -> 'Model.Entity':
        return choices(
            population=Population,  # The passed in population
            weights=[self.__fitness(gene, Population, weight_limit) for gene in Population],
            # amount of weights from matching population
            k=2  # number of parents
        )

    def __crossover(self, a: 'Model.Entity', b: 'Model.Entity') -> 'Model.Entity':
        diff = None
        cycle1 = a.get_body()[0][:len(a.get_body())//2]
        cycle2 = b.get_body()[0][len(b.get_body()[0])//2:]
        switch = rnd.randint(0,1)
        if len(cycle1) > len(cycle2):
            diff = len(cycle1) - len(cycle2)
        else:
            diff = len(cycle2) - len(cycle1)
        if len(cycle1) > 2 and len(cycle2) > 2:
            if switch > 0:
                cycle1 = cycle1.join((rnd.choice(cycle1)) for x in range(cycle1))
            else:
                cycle2 = cycle2.join((rnd.choice(cycle2)) for x in range(cycle2))
        half = cycle1 + cycle2
        return Model.Entity.Entity(half)

    def __mutation(self, entity: 'Model.Entity', num_ofmutations: int = 1, probability: float = 1.5) -> 'Model.Entity':
        f = None
        for _ in range(num_ofmutations):
            index = rnd.randint(0, len(entity.get_body())-1)
            f = entity.get_body()
            if len(entity.get_body()) == 0 : f[index] = rnd.choice([char for char in entity.get_body()])
        entity.set_body(f)
        return entity

    def __exportPopulation(self):
        pd.DataFrame(self.newPop).to_excel('Exported.xlsx')
