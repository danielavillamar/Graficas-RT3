import numpy as np
from math import tan, pi, atan2, acos, sqrt
import mathLib as ml


class Intercept:
    def __init__(self, distance, point, normal, obj, texcoords):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj

class Shape:
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def intersect(self, origin, direction):
        return None

    def normal(self, point):
        raise NotImplementedError()

class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius

    def intersect(self, origin, direction):
        L = ml.sub_vector(self.position, origin)
        lengthL = ml.VectorMag(L)
        tca = ml.producto_punto(L, direction)
        d = (lengthL ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        point = ml.AddVec(origin, ml.MultVectorEsc(t0, direction))
        normal = ml.sub_vector(point, self.position)
        normal = ml.norm_vector(normal)

        u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
        v = acos(normal[1]) / pi

        return Intercept(distance=t0,
                        point=point,
                        normal=normal,
                        texcoords=(u, v),
                        obj=self)

class Plane(Shape):
    def __init__(self, position, normal, material, repeat_texture=True):
        self.normal = ml.norm_vector(normal)
        super().__init__(position, material)
        self.repeat_texture = repeat_texture

    def intersect(self, origin, direction):
        denom = ml.producto_punto(direction, self.normal)

        if abs(denom) <=0.0001:
            return None

        num = ml.producto_punto(ml.sub_vector(self.position, origin), self.normal)
        t= num / denom

        if t < 0 :
            return None
        
        P = ml.AddVec(origin, ml.MultVectorEsc(t, direction))

        return Intercept(distance=t,
                         point=P,
                         normal=self.normal,
                         texcoords=None,
                         obj=self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius

    def intersect(self, origin, direction):
        intersect = super().intersect(origin, direction)

        if intersect is None:
            return None

        distance = ml.sub_vector(intersect.point, self.position)     
        distance = ml.VectorMag(distance)

        if distance > self.radius:
            return None
        
        return Intercept(distance=intersect.distance,
                        point=intersect.point,
                        normal=intersect.normal,
                        texcoords=None,
                        obj=self)


class Shape2(Shape):
    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)

        self.planes = []

        self.size = size

        leftPlane = Plane(ml.AddVec(position, (-size[0] / 2, 0, 0)), (-1, 0, 0), material)
        rightPlane = Plane(ml.AddVec(position, (size[0] / 2, 0, 0)), (1, 0, 0), material)

        topPlane = Plane(ml.AddVec(position, (0, size[1] / 2, 0)), (0, 1, 0), material)
        bottomPlane = Plane(ml.AddVec(position, (0, -size[1] / 2, 0)), (0, -1, 0), material)

        frontPlane = Plane(ml.AddVec(position, (0, 0, size[2]/ 2)), (0, 0, 1), material)
        backPlane = Plane(ml.AddVec(position, (0, 0, -size[2]/ 2)), (0, 0, -1), material)

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(topPlane)
        self.planes.append(bottomPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        self.boundsMin =[0,0,0]
        self.boundsMax =[0,0,0]

        bias = 0.0001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (self.size[i] / 2 + bias)
            self.boundsMax[i] = self.position[i] + self.size[i] / 2 + bias

    def intersect(self, origin, direction):
        intersect = None
        t = float("inf")

        u=0
        v=0

        for plane in self.planes:

            planeIntersect = plane.intersect(origin, direction)

            if planeIntersect is not None:

                planePoint = planeIntersect.point

                if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect

                                if abs(plane.normal[0])>0:
                                    u= (planePoint[1]-self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v= (planePoint[2]-self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[1])>0:
                                    u= (planePoint[0]-self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[2]-self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[2])>0:
                                    u= (planePoint[0]-self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[1]-self.boundsMin[1]) / (self.size[1] + 0.002)


        if intersect is None:
            return None

        return Intercept(distance=t,
                            point=intersect.point,
                            normal=intersect.normal,
                            texcoords=(u,v),
                            obj=self)    

class Triangle(Shape): #EN USOOO
    def __init__(self, vertices, material):
        super().__init__(position=vertices[0], material=material)
        self.vertices = vertices

    def intersect(self, origin, direction):
        v0, v1, v2 = self.vertices

        edge1 = ml.sub_vector(v1, v0)
        edge2 = ml.sub_vector(v2, v0)
        normal = ml.norm_vector(ml.cross_product(edge1, edge2))

        d = ml.producto_punto(normal, v0)

        denominator = ml.producto_punto(normal, direction)
        if abs(denominator) < 0.0001:
            return None

        t = (d - ml.producto_punto(normal, origin)) / denominator
        if t < 0:
            return None

        point = ml.AddVec(origin, ml.MultVectorEsc(t, direction))

        edge0 = ml.sub_vector(v0, v2)
        edge2 = ml.sub_vector(v2, v1)

        if ml.producto_punto(normal, ml.cross_product(edge0, ml.sub_vector(point, v2))) < 0:
            return None
        
        if ml.producto_punto(normal, ml.cross_product(edge1, ml.sub_vector(point, v0))) < 0:
            return None
        
        if ml.producto_punto(normal, ml.cross_product(edge2, ml.sub_vector(point, v1))) < 0:
            return None


        c0 = ml.producto_punto(edge0, ml.sub_vector(point, v2))
        c1 = ml.producto_punto(edge1, ml.sub_vector(point, v0))
        c2 = ml.producto_punto(edge2, ml.sub_vector(point, v1))
        total = c0 + c1 + c2
        u = c1 / total
        v = c2 / total

        u *= 1.8
        v *= 1.3

        return Intercept(distance=t,
                         point=point,
                         normal=normal,
                         texcoords=(u, 1-v),
                         obj=self)

class Pyramid(Shape): #EN USOOO
    def __init__(self, position, width, height, depth, rotation, material):
        super().__init__(position=position, material=material)
        self.width = width
        self.height = height
        self.depth = depth
        self.rotation = rotation

    def intersect(self, origin, direction):
        v0 = (-self.width / 2, 0, -self.depth / 2)
        v1 = (-self.width / 2, 0, self.depth / 2)
        v2 = (self.width / 2, 0, self.depth / 2)
        v3 = (self.width / 2, 0, -self.depth / 2)

        apex = (0, self.height, 0)

        v0 = ml.rotate_vector(v0, self.rotation)
        v1 = ml.rotate_vector(v1, self.rotation)
        v2 = ml.rotate_vector(v2, self.rotation)
        v3 = ml.rotate_vector(v3, self.rotation)
        apex = ml.rotate_vector(apex, self.rotation)

        v0 = ml.AddVec(v0, self.position)
        v1 = ml.AddVec(v1, self.position)
        v2 = ml.AddVec(v2, self.position)
        v3 = ml.AddVec(v3, self.position)
        apex = ml.AddVec(apex, self.position)

        triangles = []
   
        triangles.append(Triangle((v0, v1, v2), self.material))
        triangles.append(Triangle((v0, v2, v3), self.material))


        triangles.append(Triangle((v0, v1, apex), self.material))
        triangles.append(Triangle((v1, v2, apex), self.material))
        triangles.append(Triangle((v2, v3, apex), self.material))
        triangles.append(Triangle((v3, v0, apex), self.material))

        closestIntercept = None
        for triangle in triangles:
            intercept = triangle.intersect(origin, direction)
            if intercept is not None:
                if closestIntercept is None or intercept.distance < closestIntercept.distance:
                    closestIntercept = intercept

        if closestIntercept:
            return Intercept(distance=closestIntercept.distance,
                            point=closestIntercept.point,
                            normal=closestIntercept.normal,
                            texcoords=closestIntercept.texcoords,
                            obj=self)
        return None


