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
genes = np.array(genes)
el = eli.EntityLister(3, 3, genes)


@app.route('/save')
def save():
    s = pd.DataFrame(genes)
    return s.to_html()


@app.route('/')
def onstart():
    return el.getPopulationbody()


if __name__ == '__main__':
    app.run()
