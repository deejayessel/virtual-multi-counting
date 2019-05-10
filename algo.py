from data import *
import networkx as nx
import numpy as np
import itertools as it
import matplotlib.pyplot as plt
from random import choice

def makeLines(n):
    k = np.pi / (2*n) 
    def strand(i):
        theta = i*k
        return Line(m = -1/np.tan(theta),
                    b = 1/np.sin(theta))

    return [strand(i) for i in range(1,n+1)]

def _intersections(a, b, c):
    """ Return intersections of lines a, b, c"""
    return (a.intersect(b), b.intersect(c), c.intersect(a))

def makeGraph(lines):
    """ 
    For each 3-pair of the n-lines in `lines`, 
      take the intersections between them,
      use to make a triangle node,
      connect by common vertices
    """
    g = nx.Graph()
    for (a,b,c) in it.combinations(lines, 3):
        r,s,t = _intersections(a,b,c)
        tri1 = Triangle(r,s,t)
        g.add_node(tri1)
        for tri2 in g.nodes:
            if tri1.intersects(tri2):
                p = tri1.intersection(tri2)
                g.add_edge(tri1, tri2, label=p )
    return g

def drawGraph(g):
    #pos = nx.spring_layout(g)
    pos = { tri : tri.centroid.pos for tri in g.nodes }
    nx.draw(g, pos, with_labels = True)
    labels= nx.get_edge_attributes(g, 'label')
    #nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    plt.show()

mapping = {
    'CVV': ['CVV'],
    '_V_': ['VVC', 'VVV', 'CVV'],
    'V__': ['VVV','VCV','VVC'],
    'CV_': ['CVV'],
    '__V': ['CVV','VCV','VVV'],
    'C_V': ['CVV'],
    'C__': ['CVV','CCC'],
    'VVV': ['VVV'],
    '__C': ['VVC','CCC'],
    'VCV': ['VCV'],
    '_CC': ['CCC'],
    '___': ['CCC','CVV','VCV','VVC','VVV'],
    'VVC': ['VVC'],
    'VV_': ['VVV','VVC'],
    '_CV': ['VCV'],
    'CVC': [],
    'CCV': [],
    'V_C': ['VVC'],
    'CCC': ['CCC'],
    '_VV': ['VVV','CVV'],
    'VCC': [],
    'C_C': ['CCC'],
    '_C_': ['CCC','VCV'],
    'VC_': ['VCV'],
    'V_V': ['VVV','VCV'],
    'CC_': ['CCC'],
    '_VC': ['VVC']
}

from copy import deepcopy

def extend(coloring, tri):
    """
    Takes in a coloring (a mapping from Points to colors) and a triangle, 
    determines and returns valid colorings for the triangle.
    This gives an extension of the original coloring (a list of color mappings),
    which we return.
    """
    initial = "".join([coloring[v] for v in tri.vertices])
    #set of new colorings to return
    output = []
    for child in mapping[initial]:
        newcoloring = deepcopy(coloring)
        a,b,c = tri.vertices
        newcoloring[a] = child[0]
        newcoloring[b] = child[1]        
        newcoloring[c] = child[2]
        output.append(deepcopy(newcoloring))
    return output
    
def colorGraph(g, root):
    """
    Come up with a set of valid colorations of the graph, i.e.,
    a set of valid choices of virtual and classical crossings 
    for the n-crossing
    """
    # coloring map collection: List[{Point -> Color}]
    colorings = []
    blankcoloring = {v:'_' for tri in g.nodes for v in tri.vertices}
    colorings.append(blankcoloring)

    edges = nx.bfs_edges(g, root)
    nodes = [root] + [v for u,v in edges]
    for tri in nodes: #for each triangle-node
        colorings = [newc
                     for oldc in colorings
                     for newc in extend(oldc, tri)]
    return colorings

def strColoring(colorings):
    return ", ".join([str(k)+str(v) for c in colorings for (k,v) in c.items()])

if __name__ == '__main__':
    for i in range(3,20):
        g = makeGraph(makeLines(i))
        root = list(g.nodes)[0]
        print(i, len(g.nodes))
