import numpy as np
from flask import Flask, render_template
import EntityLister as eli
import pandas as pd

app = Flask(__name__)
filex = open('text.txt', 'r')

genes = []
for x in filex.readlines():
    s = x.split()
    if len(s) == 0:
        continue
    else:
        genes.append(s)
genes = np.array(genes, dtype=object)
el = eli.EntityLister(3, 3, genes)

@app.route('/')
def onstart():
    el.start_evolution(10)
    return el.getEvolutionDF().to_html()


if __name__ == '__main__':
    app.run()
