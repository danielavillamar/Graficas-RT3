from Shapes.Plane import Plane
from Shapes.Intercept import Intercept
import mathLib as np


class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius

    def intersect(self, origin, direction):
        intercept = super().intersect(origin, direction)

        if intercept is None:
            return None

        if np.linalg_norm(np.subtract(intercept.point, self.position)) > self.radius:
            return None

        return Intercept(
            distance=intercept.distance,
            point=intercept.point,
            normal=self.normal,
            obj=self,
            textureCoordinates=None
        )
