import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        # coordinate vector
        self.x = x
        self.y = y
        # max value of vector difference
        self.thresh = 0.000001

    # methods arithmetic
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        # avoid division by 0
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None
    
    # python 3
    def __truediv__(self, scalar):
        return self.__div__(scalar)

    # check the similarity of 2 vectors
    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    # squared distance vector (root avoidance)
    def magnitudeSquared(self):
        return self.x**2 + self.y**2
    
    # distance vector
    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())

    # vector duplication 
    # so you can modify the new vector without touching the old vector
    def copy(self):
        return Vector2(self.x, self.y)

    def asTuple(self):
        return self.x, self.y

    def asInt(self):
        return int(self.x), int(self.y)

    # print vector position
    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"