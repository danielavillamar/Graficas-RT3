import mathLib as np
from Shapes.Intercept import Intercept
from Shapes.Shape import Shape
from Shapes.Plane import Plane


class Shape2(Shape):
    def __init__(self, position, size, material):
        super().__init__(position, material)
        self.size = size
        self.planes = []

        leftPlane = Plane(
            np.add(self.position, (-size[0] / 2, 0, 0)),
            (-1, 0, 0),
            self.material
        )
        rightPlane = Plane(
            np.add(self.position, (size[0] / 2, 0, 0)),
            (1, 0, 0),
            self.material
        )
        bottomPlane = Plane(
            np.add(self.position, (0, -size[1] / 2, 0)),
            (0, -1, 0),
            self.material
        )
        topPlane = Plane(
            np.add(self.position, (0, size[1] / 2, 0)),
            (0, 1, 0),
            self.material
        )
        backPlane = Plane(
            np.add(self.position, (0, 0, -size[2] / 2)),
            (0, 0, -1),
            self.material
        )
        frontPlane = Plane(
            np.add(self.position, (0, 0, size[2] / 2)),
            (0, 0, 1),
            self.material
        )

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)

        # BOUNDS
        bias = 0.001
        self.boundsMin = [position[i] - (bias + size[i] / 2) for i in range(3)]
        self.boundsMax = [position[i] + (bias + size[i] / 2) for i in range(3)]

    def intersect(self, origin, direction):
        intersect = None
        t = float('inf')
        u = 0
        v = 0

        for plane in self.planes:
            planeIntersect = plane.intersect(origin, direction)
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect

                                if abs(plane.normal[0]) > 0:
                                    u = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                if abs(plane.normal[1]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                if abs(plane.normal[2]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)

        if intersect is None:
            return None

        return Intercept(
            distance=t,
            point=intersect.point,
            normal=intersect.normal,
            obj=self,
            textureCoordinates=(u, v)
        )
