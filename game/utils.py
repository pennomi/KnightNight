class Point(object):
    """Basic Point class with x and y components.
    Can construct using iterable or two numbers.
    """
    def __init__(self, *args):
        if len(args) == 1: # iterable
            self.x, self.y = args[0][0], args[0][1]
        elif len(args) == 2: # values
            self.x, self.y = args[0], args[1]
        else:
            raise TypeError("Point requires two numbers or a 2-tuple.")

    def __eq__(self, obj):
        return self.x == obj.x and self.y == obj.y

    def __add__(self, obj):
        return Point(self.x + obj.x, self.y + obj.y)

    def __sub__(self, obj):
        return Point(self.x - obj.x, self.y - obj.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __str__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)

    def round(self):
        return Point(int(round(self.x)), int(round(self.y)))
