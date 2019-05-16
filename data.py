import math
from decimal import *

"""
Contains data structures necessary to run Reuben's algorithm
"""

class Triangle:
    """ Contains three vertices """
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def contains(self, p):
        return p in [a, b, c]

    @property
    def vertices(self):
        return (self.a, self.b, self.c)

    @property
    def centroid(self):
        return Point(sum(v.x for v in self.vertices)/3,
                     sum(v.y for v in self.vertices)/3)

    def intersection(self, other):
        """ 
        Checks if this triangle intersects another triangle.
        If there is an intersection, returns the first discovered point of intersection.
        If there are no intersections, returns None.
        """
        for u in self.vertices:
            for v in other.vertices:
                if u==v:
                    return u
        return None

    def intersects(self, other):
        return self.intersection(other) is not None

    def __hash__(self):
        return self.vertices.__hash__()

    def __str__(self):
        return "({},{},{})".format(*self.vertices)

class Line:
    """ 
    Represents a line in slope-intercept form (y = mx + b)
    """

    def __init__(self, m, b):
        self.m = Decimal(m).quantize(Decimal('.0001'))
        self.b = Decimal(b).quantize(Decimal('.0001'))
    
    def intersect(self, other):
        """ Returns intersection point of self with other """
        x = Decimal(other.b - self.b)/Decimal(self.m - other.m)
        y = self.m * x + self.b
        return Point(x, y)

    def contains(self, x, y):
        return y == self.m * x + self.b

    def __str__(self):
        return "y = {}x + {}".format(self.m, self.b)

    def __eq__(self, other):
        return self.m == other.m and self.b == other.b

    def __hash__(self):
        return (self.m, self.b).__hash__()

class Point:

    def __init__(self, x, y):
        self.x = Decimal(x).quantize(Decimal('.0001'))
        self.y = Decimal(y).quantize(Decimal('.0001'))
        
    @property
    def pos(self):
        return (self.x, self.y)

    def dist(self, other):
        (x1, y1) = self.pos
        (x2, y2) = other.pos
        return Decimal((x1 - x2)**2 + (y1 - y2)**2).sqrt()

    def __eq__(self, other): #FIX
        return 0 <= self.dist(other) <= 0.0001

    def __hash__(self):
        return self.pos.__hash__()

    def __str__(self):
        return "({:4.2f},{:4.2f})".format(self.x, self.y)


# Testing
if __name__ == '__main__':

    import itertools as it
    import numpy as np

    n = 5
    k = np.pi / (2*n) 
    def strand(i):
        theta = i*k
        return Line(m = -1/np.tan(theta),
                    b = 1/np.sin(theta))
    ls = [strand(i) for i in range(1,n+1)]

    def _intersect(a,b,c):
        return (a.intersect(b), b.intersect(c), c.intersect(a))

    ps = [p
          for a,b,c in it.combinations(ls, 3)
          for p in _intersect(a,b,c)]

    for a,b in it.combinations(ps, 2):
        if a == b and a.__hash__() != b.__hash__():
            print(a.pos, b.pos)
            

