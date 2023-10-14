import mathLib as ml
from math import acos, asin, sin, cos   

class Light:
    def __init__(self, intensity=1, color=(1, 1, 1), lightType="LIGHT"):
        self.intensity = intensity
        self.color = color
        self.type = lightType

    def getColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]

    def getDiffuseColor(self, intercept):
        return None

    def getSpecularColor(self, intercept, viewPosition):
        return None
    

class Ambient(Light):
    def __init__(self, intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "AMBIENT")


def reflect(normal, direction):
    reflectValue = ml.sub_vector(ml.MultVectorEsc(2 * ml.producto_punto(normal, direction), normal), direction)
    return ml.norm_vector(reflectValue)

def refract(normal, incident , n1, n2):
    c1 = ml.producto_punto(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        normal = ml.negative_tuple(normal)
        n1, n2 = n2, n1

    n = n1 / n2

    T = ml.sub_vector(ml.MultVectorEsc(n , ml.AddVec(incident, ml.MultVectorEsc(c1, normal))) , ml.MultVectorEsc((1 - n **2 * (1-c1**2)) ** 0.5 ,normal))
    T = ml.norm_vector(T)
    return T

def fresnel(normal, incident,n1, n2):
    c1 = ml.producto_punto(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    s2 = (n1 * (1 - c1 ** 2) ** 0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5

    f1 = ((n2 * c1 - n1 * c2) / (n2 * c1 + n1 * c2)) ** 2
    f2 = ((n1 * c2 - n2 * c1) / (n1 * c2 + n2 * c1)) ** 2

    kr = (f1 + f2) / 2
    kt = 1 - kr
    return kr, kt

def totalInternalReflection(incident, normal , n1, n2):
    c1 = ml.producto_punto(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        normal = ml.negative_tuple(normal)
        n1, n2 = n2, n1
    
    if n1 < n2:
        return False
    
    theta1 = acos(c1)
    thetaC = asin(n2/n1)

    return theta1 >= thetaC

class Directional(Light):
    def __init__(self, direction=(0, 1, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "DIRECTIONAL")
        self.direction = ml.norm_vector(direction)

    def getDiffuseColor(self, intercept):
        direction = [i * -1 for i in self.direction]

        intensity = ml.producto_punto(intercept.normal, direction) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = [i * -1 for i in self.direction]

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = ml.sub_vector(viewPosition, intercept.point)
        viewDirection = ml.norm_vector(viewDirection)

        intensity = max(0, min(1, ml.producto_punto(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.ks

        return [i * intensity for i in self.color]


class Point(Light):
    def __init__(self, position=(0, 0, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "POINT")
        self.position = position

    def getDiffuseColor(self, intercept):
        direction = ml.sub_vector(self.position, intercept.point)
        radius = ml.VectorMag(direction)
        direction = ml.DivVectorEsc(direction, radius)

        intensity = ml.producto_punto(intercept.normal, direction) * self.intensity
        intensity *= 1 - intercept.obj.material.ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = ml.sub_vector(self.position, intercept.point)
        radius = ml.VectorMag(direction)
        direction = ml.DivVectorEsc(direction, radius)

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = ml.sub_vector(viewPosition, intercept.point)
        viewDirection = ml.norm_vector(viewDirection)

        intensity = max(0, min(1, ml.producto_punto(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]