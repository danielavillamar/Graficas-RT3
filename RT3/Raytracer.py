import pygame

from Shapes.Sphere import Sphere
from Lights.Ambient import Ambient as AmbientLight
from Lights.Directional import Directional as DirectionalLight
from Lights.Point import Point as PointLight
from rt import RayTracer
import Materials.Material as Material
from Shapes.Plane import Plane
from Shapes.Disk import Disk
from Shapes.Shape2 import Shape2

# Tamaño Pantalla
width = 720
height = 720

pygame.init()

# Crear pantalla con pygame
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

# New RayTracer
rayTracer = RayTracer(screen)
rayTracer.rtClearColor(0.2, 0.7, 0.8)
rayTracer.rtColor(1, 1, 1)

# Renderizado de las figuras en pantalla con su material

# Planos
rayTracer.scene.append(
    Plane(position=(0, -2, 0), normal=(0, 1, -0.2), material=Material.grass())  
)
rayTracer.scene.append(
    Plane(position=(0, 5, 0), normal=(0, 1, 0.2), material=Material.ceiling()) 
)
rayTracer.scene.append(
    Plane(position=(4, 0, 0), normal=(1, 0, 0.2), material=Material.ladrillo()) 
)
rayTracer.scene.append(
    Plane(position=(-4, 0, 0), normal=(1, 0, -0.2), material=Material.agua()) 
)
rayTracer.scene.append(
    Plane(position=(0, 0, 5), normal=(0, 0, 1), material=Material.nieve()) 
)

# Disco
rayTracer.scene.append(
    Disk(position=(-2, 1, -5), normal=(1, 0, 0.2), radius=1, material=Material.mirror())
)
rayTracer.scene.append(
    Disk(position=(2, -1, -5), normal=(1, 0, -0.2), radius=1, material=Material.mirror())
)
rayTracer.scene.append(
    Disk(position=(0, 0, -7), normal=(0, 0, 1), radius=1, material=Material.mirror())
)

rayTracer.scene.append(
    Shape2(position=(-1, 0, -6), size=(1, 1, 1), material=Material.moon())
)
rayTracer.scene.append(
    Shape2(position=(1, 0, -6), size=(1, 1, 1), material=Material.floor())
)
rayTracer.scene.append(
    Shape2(position=(0, -1.5, -6), size=(1, 1, 1), material=Material.diamond())
)

# Lights on scene
rayTracer.lights.append(
    AmbientLight(intensity=0.7)
)

rayTracer.rtClear()
rayTracer.rtRender()

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

pygame.quit()
