import EntityLister as el
import numpy as np

filex = open('text.txt', 'r')
genes = np.array([x.strip('\n') for x in filex.readlines()])
el = el.EntityLister(3, 3, genes)
el.printPopulationHash()
