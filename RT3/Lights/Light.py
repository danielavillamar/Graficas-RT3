
import mathLib as np
from math import acos, asin, sin, cos


def reflect(normal, direction):
    r1 = np.dot(normal, direction)
    r2 = np.multiplyVectorScalar(normal, r1)
    r3 = np.multiplyVectorScalar(r2, 2)
    reflectValue = np.subtractVectorVector(r3, direction)
    return np.normalize(reflectValue)


def totalInternalReflection(incident, normal, n1, n2):
    c1 = np.dot(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    theta1 = acos(c1)
    thetaCritical = asin(n2 / n1)

    return theta1 >= thetaCritical


def refract(normal, incident, n1, n2):
    c1 = np.dot(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = np.negateVector(normal)
        n1, n2 = n2, n1

    n = n1 / n2

    t0 = np.add(incident, np.multiplyVectorScalar(normal, c1))
    t1 = np.subtract(np.multiplyVectorScalar(t0, n), normal)
    t2 = (1 - n ** 2 * (1 - c1 ** 2)) ** 0.5
    t = np.multiplyVectorScalar(t1, t2)
    return np.normalize(t)


def fresnel(normal, incident, n1, n2):
    c1 = np.dot(normal, incident)

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
