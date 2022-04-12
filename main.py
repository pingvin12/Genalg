import numpy as np
from flask import Flask
import EntityLister as eli
app = Flask(__name__)
@app.route('/')
def hello_world():
    filex = open('text.txt', 'r')
    genes = np.array([x.strip('\n') for x in filex.readlines()])
    el = eli.EntityLister(3, 3, genes)
    return el.getPopulationbody()


if __name__ == '__main__':
    app.run()