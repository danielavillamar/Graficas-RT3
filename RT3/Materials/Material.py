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

def floor():
    return Material(diffuse=(0.7373, 0.561, 1), spec=64, ks=0.15, type=REFLECTIVE)

def wall():
    return Material(diffuse=(0.7373, 0.561, 1))

def ceiling():
    return Material(diffuse=(1, 0.561, 1))

def moon():
    return Material(texture=pygame.image.load("Textures/moon.png"))

def glass():
    return Material(diffuse=(0.8, 0.8, 0.8), spec=64, ks=0.15, ior=1.5, type=TRANSPARENT)

def diamond():
    return Material(diffuse=(0.6196, 1, 0.9608), spec=128, ks=0.2, ior=2.417, type=TRANSPARENT)

def mirror():
    return Material(diffuse=(0.8, 0.8, 0.8), spec=64, ks=0.2, type=REFLECTIVE)

def ladrillo():
    return Material(diffuse=(1, 0.3, 0.2), spec=8, ks=0.01)

def agua():
    return Material(diffuse=(0.2, 0.2, 0.8), spec=256, ks=0.5)

def nieve():
    return Material(diffuse=(0.9373, 0.8941, 0.8235), spec=2, ks=0.01)

def grass():
    return Material(diffuse=(0.2, 0.8, 0.2), spec=32, ks=0.1)