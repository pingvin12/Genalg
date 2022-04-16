import random as rnd
import pandas as pd
import numpy as np
import openpyxl
from difflib import SequenceMatcher
import Model.Entity as en

class EntitySolver:
    def __init__(self, arr = np.array):
        self.population = arr
        self.class_FamilyProbability = pd.DataFrame(columns=['child_genes','mate1','mate2','probability_mate1','probability_mate2'])
    def runSimulation(self):
        i = 0
        print('Please wait! this could take a while...')
        print(f'Counting {len(self.population)*len(self.population)*len(self.population)} amount of probabilities...')
        for mate1 in self.population:
            for mate2 in self.population:
                for child in self.population:
                    self.class_FamilyProbability.loc[i] = [child,mate1,
                                                           mate2,SequenceMatcher(None, child ,mate1).ratio(), SequenceMatcher(None, child,mate2).ratio()]
                    i = i + 1
        self.class_FamilyProbability.to_excel('Probabilities.xlsx')