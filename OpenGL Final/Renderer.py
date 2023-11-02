import pygame
from pygame.locals import *
import glm
from gl import Renderer
from model import Model
from shaders import *

width = 1080
height = 720

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(vertex_shader, fragment_shader)

modelo = Model(filename="models/Kettle.obj", 
    translate=glm.vec3(0, -1, -5), 
    rotation=glm.vec3(0, 0, 0), 
    scale=glm.vec3(0.06, 0.06, 0.06)
)

modelo.loadTexture("textures/Kettle.bmp")

rend.scene.append(modelo)

isRunning = True
while isRunning:
    deltaTime = clock.tick(60)/1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    if keys[K_d]:
        rend.camPosition.x += 5 * deltaTime
    elif keys[K_a]:
        rend.camPosition.x -= 5 * deltaTime

    if keys[K_w]:
        rend.camPosition.y += 5 * deltaTime
    elif keys[K_s]:
        rend.camPosition.y -= 5 * deltaTime

    if keys[K_q]:
        rend.camPosition.z += 5 * deltaTime
    elif keys[K_e]:
        rend.camPosition.z -= 5 * deltaTime

    rend.render()
    pygame.display.flip()

pygame.quit()
