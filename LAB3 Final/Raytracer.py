import pygame
from pygame.locals import *

from rt import Raytracer

from figures import *
from lights import Ambient 
from lights import Directional
from lights import Point
import materials as Material

# Tamaño Pantalla
width = 720
height = 720

pygame.init()

# Crear pantalla con pygame
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

# New RayTracer
raytracer = Raytracer(screen)

background = pygame.image.load("textures/chiquitin.jpg")
background = pygame.transform.scale(background, (width, height))

raytracer.envMap = background

raytracer.rtClearColor(0.5, 0.5, 0.5)
raytracer.rtColor(1, 1, 1)


# Render de las piramides

# Glassy
raytracer.scene.append(
    Pyramid(position=(-3, -2.2, -7), width=1, height=1, depth=1, rotation=(0,0,0), material=Material.glassy())
)
# Pelotitas
raytracer.scene.append(
    Pyramid(position=(0, -1.8, -7), width=1.7, height=1.7, depth=1.7, rotation=(0,45,0), material=Material.pelotitas())
)
# Metalic
raytracer.scene.append(
    Pyramid(position=(3, 0, -7), width=2.1, height=2.1, depth=2.1, rotation=(0,180,0), material=Material.metal())
)

# Lights on scene
raytracer.lights.append(
    Ambient(intensity=0.5)
)
raytracer.lights.append(
    Point(position=(2.5, 0, -5), intensity=1)
)

isRunning = True
raytracer.rtClear()
raytracer.rtRender()

# Guardar resultado
rect = pygame.Rect(0, 0, width, height)
sub = screen.subsurface(rect)

pygame.image.save(sub, "output.png")

pygame.quit()