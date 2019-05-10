import math

class Triangle:
    """ Contains three vertices """
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def contains(self, p):
        return a == p or b == p or c == p

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
        If there is an intersection, returns the point of intersection.
        If there are no intersections, returns an empty list.
        """
        for u in self.vertices:
            for v in other.vertices:
                if u==v:
                    return u
        return None

    def intersects(self, other):
        return self.intersection(other) is not None

    # need a better hashing function
    def __hash__(self):
        return self.vertices.__hash__()

    def __str__(self):
        return "({},{},{})".format(*self.vertices)

class Line:

    def __init__(self, m, b):
        self.m = m
        self.b = b
    
    def intersect(self, other):
        # returns intersection point of self with other
        x = (other.b - self.b)/(self.m - other.m)
        y = self.m * x + self.b
        return Point(x, y)

    def contains(self, x, y):
        return y == self.m * x + self.b

    def __str__(self):
        return "y = {}x + {}".format(self.m, self.b)

    def __eq__(self, other):
        return self.m == other.m and self.b == other.b

    # need a better hashing function
    def __hash__(self):
        return self.m.__hash__() + self.b.__hash__()

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    @property
    def pos(self):
        return (self.x, self.y)

    def dist(self, other):
        (x1, y1) = self.pos
        (x2, y2) = other.pos
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def __eq__(self, other):
        return self.dist(other) <= 0.00001 #TODO

    def __hash__(self):
        return self.pos.__hash__()

    def __str__(self):
        return "({:4.2f},{:4.2f})".format(self.x, self.y)


if __name__ == '__main__':
    pass
