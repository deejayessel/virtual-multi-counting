from data import *
import networkx as nx
import numpy as np
import itertools as it
import matplotlib.pyplot as plt
from random import choice
from copy import deepcopy
from mapping import mapping

"""
Contains the functions necessary to run Reuben's algorithm
"""

def makeLines(n):
    """
    Set up the n-crossing as a set of evenly-spread lines tangent to 
    the first quadrang of the unit circle
    """
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
    Makes the graph representing the virtual n-crossing.

    For each 3-pair of lines, take their intersections
    and add these as triangle nodes to the graph.  Connect nodes
    sharing intersection points by edges labeled by the shared point.
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
    """ Draws the input graph g """
    #pos = nx.spring_layout(g)
    pos = { tri : tri.centroid.pos for tri in g.nodes }
    nx.draw(g, pos, with_labels = True)
    labels= nx.get_edge_attributes(g, 'label')
    #nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    plt.show()


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
    
def colorGraph(g):
    """
    Come up with a set of valid colorations of the graph, i.e.,
    a set of valid choices of virtual and classical crossings 
    for the n-crossing
    """
    root = list(g.nodes)[0]
    blankcoloring = {v:'_' for tri in g.nodes for v in tri.vertices}
    colorings = [blankcoloring] # coloring map collection: List[{Point -> Color}]

    edges = nx.bfs_edges(g, root)
    nodes = [root] + [v for u,v in edges]
    for tri in nodes: #for each triangle-node
        colorings = [newc
                     for oldc in colorings
                     for newc in extend(oldc, tri)]
    return colorings

def strColoring(coloring):
    return "".join([str(v) for (k,v) in coloring.items()])

def strList(cs):
    xs = [strColoring(c) for c in cs]
    ys = [(x.count('C'),x) for x in xs]
    return [b for a,b in sorted(ys)]

def isPerm(a, b):
    """ Checks if a is a permutation of b """
    return a in b+b

def filterPerms(cs):
    def inserted(l, x):
        for elt in l:
            if isPerm(elt, x):
                return l
        return l+[x]

    xs = strList(cs)
    l = []
    for x in xs:
        l = inserted(l, x)
    return l

if __name__ == '__main__':
    for i in range(3, 8):
        g = makeGraph(makeLines(i))
        cs = colorGraph(g)
        print(i, len(cs))

    # for i in range(3,20):
    #     g = makeGraph(makeLines(i))
    #     root = list(g.nodes)[0]
    #     print(i, len(colorGraph(g, root)))
