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
    print(f'Please type in the input values in the following order:\n initial population amount, max amount of weight, generation limit, offspring multiplier\n don\'t worry error messages may appear, it\'s completely normal.')
    init_pop = int(input())
    weight = int(input())
    generationlimit = int(input())
    offspringmultiplier = int(input())

    el = eli.EntityLister(init_pop, weight, genes) # creating a lister instance for main logic
    el.start_evolution(generationlimit, offspringmultiplier)
    el.getEvolutionDF().to_excel('Evolution.xlsx')
    print('You can now view the simulation in the Evolution.xlsx file.')