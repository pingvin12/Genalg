import numpy as np
import EntityLister as eli

if __name__ == '__main__':
    filex = open('text.txt', 'r') # Everything is loaded from a text file
    genes = []
    for x in filex.readlines():
        s = x.split()
        if len(s) == 0: # loading every sentence to an array for better handling
            continue
        else:
            for f in s:
                genes.append(f)
    genes = np.array(genes, dtype=object)
    el = eli.EntityLister(3, 3, genes) # creating a lister instance for main logic
    el.start_evolution(2)
    el.getEvolutionDF().to_excel('Evolution.xlsx')
