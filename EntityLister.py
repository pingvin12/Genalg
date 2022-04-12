import pandas as pd
import numpy as np
import Model.Entity
class EntityLister:
    def __init__(self,sol_per_pop : int, num_weights : int, genes : np.array):
        print('New Entity List created!')
        self.newPop = np.empty((sol_per_pop, num_weights), dtype=object)
        self.newPop.flat = [Model.Entity.Entity(np.random.choice(genes, size=1)) for _ in self.newPop.flat]

    def getPopulationbody(self):
        s = np.array([_.get_body() for _ in self.newPop.flat])
        return s[0][0]
    def printPopulationHash(self):
        for x in self.newPop.flat:
            print(x.get_hash())
    def start(self):
        print('NotImplemented')
    def exportPopulation(self):
        pd.DataFrame(self.newPop).to_excel('Exported.xlsx')