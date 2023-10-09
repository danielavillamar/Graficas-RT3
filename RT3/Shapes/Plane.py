from Shapes.Shape import Shape
from Shapes.Intercept import Intercept
import mathLib as np


class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = np.normalize(normal)

    def intersect(self, origin, direction):
        denominator = np.dot(direction, self.normal)

        if abs(denominator) <= 0.0001:
            return None

        t = np.dot(np.subtract(self.position, origin), self.normal) / denominator

        if t < 0:
            return None

        point = np.add(origin, np.multiplyVectorScalar(direction, t))

        return Intercept(distance=t,
                         point=point,
                         normal=self.normal,
                         obj=self,
                         textureCoordinates=None)
