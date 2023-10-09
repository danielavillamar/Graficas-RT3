class Shape:
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def intersect(self, origin, direction):
        return None

    def normal(self, point):
        raise NotImplementedError()