import random as rnd
import openpyxl
import pandas as pd
import numpy as np
from random import choices
import Model.Entity


class EntityLister:

    def __init__(self, sol_per_pop: int, num_weights: int, genes: np.array):
        self.class_EvolutionDF = pd.DataFrame(
            columns=['mate1', 'mate2', 'fitness', 'mutation_chance', 'body', 'childhash'])
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

    def start_evolution(self, generation_limit: int = 100) -> []:
        for generation in range(generation_limit):
            mate1 = rnd.choice(self.newPop.flat)
            mate = rnd.choice(self.newPop.flat)
            fitness = self.__fitness(mate1, self.newPop.flat,
                                     rnd.randrange(0, 50))
            num_mutations = rnd.randrange(1, 5)
            prob_mutation = rnd.randrange(1, 5)
            child = self.__mutation(self.__crossover(mate1, mate))
            mate1.add_children(child)
            mate.add_children(child)
            np.append(self.newPop, child)
            self.class_EvolutionDF = self.class_EvolutionDF.append(
                {'mate1': str(mate.get_body()), 'mate2': str(mate1.get_body()), 'fitness': fitness,
                 'mutation_chance': prob_mutation, 'body': str(child.get_body()), 'childhash': child.get_hash()}, ignore_index = True)

    def __fitness(self, entity: 'Model.Entity', entities: ['Model.Entity'], weight_limit: int) -> int:
        weight = 0  # weight = length of bodytext
        value = 0
        for i, chunk in enumerate(entities):
            for child in chunk.get_children():
                if entity.get_body() == child.get_body():
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
        cycle1 = rnd.choice(a.get_body()[0])
        cycle2 = rnd.choice(b.get_body()[0])
        if len(cycle1) > len(cycle2):
            diff = len(cycle1) - len(cycle2)
        else:
            diff = len(cycle1) - len(cycle2)
        halfa = str(cycle1[0:diff] + cycle2[diff:len(cycle2)])
        halfb = str(cycle2[0:diff] + cycle1[diff:len(cycle1)])
        x = Model.Entity.Entity('')
        if halfa > halfb:
            x.set_body(halfa)
        else:
            x.set_body(halfb)
        return x

    def __mutation(self, entity: 'Model.Entity', num_ofmutations: int = 1, probability: float = 1.5) -> 'Model.Entity':
        f = None
        for _ in range(num_ofmutations):
            index = rnd.randint(0, len(entity.get_body()[0]))
            f = entity.get_body()
            if index != 0:
                f = f[0:rnd.randrange(0, index)]
        x = Model.Entity.Entity(f)
        return x

    def __exportPopulation(self):
        pd.DataFrame(self.newPop).to_excel('Exported.xlsx')
