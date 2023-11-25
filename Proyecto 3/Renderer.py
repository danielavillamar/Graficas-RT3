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

modelos = [
    Model("models/Kettle.obj", glm.vec3(0, -2, -15), glm.vec3(0, 0, 0), glm.vec3(0.2, 0.2, 0.2)),
    Model("models/jarron.obj", glm.vec3(0, -1.5, -5), glm.vec3(0, 0, 0), glm.vec3(0.3, 0.3, 0.3)),
    Model("models/Mortar.obj", glm.vec3(0, -0.5, -5), glm.vec3(0, 0, 0), glm.vec3(0.3, 0.3, 0.3)),
    Model("models/Sword.obj", glm.vec3(0, 5, -5), glm.vec3(0, 90, 0), glm.vec3(12, 12, 12)),
    Model("models/model.obj", glm.vec3(0, 0, -5), glm.vec3(0, 0, 0), glm.vec3(4, 4, 4))
]

modelos[0].loadTexture("textures/Kettle.bmp")
modelos[1].loadTexture("textures/jarron.bmp")
modelos[2].loadTexture("textures/Mortar.bmp")
modelos[3].loadTexture("textures/Sword.bmp")
modelos[4].loadTexture("textures/model.bmp")

rend.scene.append(modelos[0])

# Variables para controlar la cámara
angulo_horizontal = 0
angulo_vertical = 0 
radio = 10 
zoom_min = 0.1
zoom_max = 10 
modelo_actual = 0
shader_actual = 0 

zoom_inicial = (zoom_min + zoom_max) / 2

zoom = zoom_inicial

# Bucle principal
isRunning = True
while isRunning:
    deltaTime = clock.tick(60)/1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[2]:  # Botón derecho del mouse presionado
                xoffset = event.rel[0] * 0.1
                yoffset = -event.rel[1] * 0.1
                angulo_horizontal += xoffset
                angulo_vertical = max(-89, min(89, angulo_vertical + yoffset))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll Up
                radio = max(zoom_min, radio - 1)
            elif event.button == 5:  # Scroll Down
                radio = min(zoom_max, radio + 1)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key==pygame.K_SPACE:
                rend.toggleFilledMode()
            elif event.key==pygame.K_6:
                rend.setShaders(vertex_shader, fragment_shader)
            elif event.key==pygame.K_7:
                rend.setShaders(vertex_shader, wave_shader)
            elif event.key==pygame.K_8:
                rend.setShaders(vertex_shader, checkerbord_shader)
            elif event.key==pygame.K_9:
                rend.setShaders(vertex_shader, ripple_shader)
            elif event.key == pygame.K_0:
                rend.setShaders(vertex_shader, noise_shader)
            elif event.key >= pygame.K_1 and event.key <= pygame.K_6:
                # Actualizar el modelo actual
                num_modelo = event.key - pygame.K_1
                if num_modelo < len(modelos):
                    rend.scene.clear()
                    rend.scene.append(modelos[num_modelo])
                    modelo_actual = num_modelo

    rend.camPosition.x = radio * glm.sin(glm.radians(angulo_horizontal)) * glm.cos(glm.radians(angulo_vertical))
    rend.camPosition.y = radio * glm.sin(glm.radians(angulo_vertical))
    rend.camPosition.z = radio * glm.cos(glm.radians(angulo_horizontal)) * glm.cos(glm.radians(angulo_vertical))
    rend.update()

    if keys[K_w]:
        modelos[modelo_actual].rotate(glm.vec3(1, 0, 0))
    if keys[K_s]:
        modelos[modelo_actual].rotate(glm.vec3(-1, 0, 0))
    if keys[K_a]:
        modelos[modelo_actual].rotate(glm.vec3(0, 1, 0))
    if keys[K_d]:
        modelos[modelo_actual].rotate(glm.vec3(0, -1, 0))

    rend.elapsedTime += deltaTime
    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()
