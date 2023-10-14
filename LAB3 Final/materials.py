import pygame

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material:
    def __init__(self, diffuse=(1, 1, 1), spec=1.0, ks=0.0, ior=1.0, type=OPAQUE, texture=None):
        self.diffuse = diffuse
        self.spec = spec
        self.ks = ks
        self.ior = ior
        self.type = type
        self.texture = texture


def glassy():
    return Material(diffuse=(0.8, 0.8, 0.8), spec=64, ks=0.15, ior=1.5, type=TRANSPARENT)

def ladrillo():
    return Material(diffuse=(1, 0.3, 0.2), spec=8, ks=0.01)

def metal():
    return Material(diffuse=(0.8, 0.8, 0.8), spec=64, ks=0.2, type=REFLECTIVE)

def pelotitas():
    return Material(texture=pygame.image.load("textures/pelotitas.jpg"), type=OPAQUE)
