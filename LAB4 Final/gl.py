# pip install PyGLM
# Libreria de matematicas compatible con OpenGL
import glm

import random

# pip install PyOpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer(object):
    def __init__(self,screen):
        self.screen = screen
        _,_,self.width,self.height = screen.get_rect()
        
        self.clearColor = [0,0,0]
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glViewport(0,0,self.width,self.height)
        
        self.elapsedTime = 0.0
        self.target = glm.vec3(0,0,0)
        
        self.fatness = 0.0
        
        self.filledMode = True
        
        self.scene = []

        self.activeShader = None
        
        self.dirLight = glm.vec3(1,0,0)
        
        #View Matrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0)
        self.viewMatrix = self.getViewMatrix()
        
        #Projection matrix
        self.projectionMatrix = glm.perspective(glm.radians(60),#FOV
                                                self.width/self.height, #Aspect Ratio
                                                0.1, #Near Plane
                                                1000 #Far Plane
                                                )  
    def toggleFilledMode(self):
        self.filledMode = not self.filledMode
        
        if self.filledMode:
            glEnable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT,GL_FILL)
        else:
            glDisable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)

    def getViewMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity,self.camPosition)
        
        pitch = glm.rotate(identity,glm.radians(self.camRotation.x),glm.vec3(1,0,0))
        yaw = glm.rotate(identity,glm.radians(self.camRotation.y),glm.vec3(0,1,0))
        roll = glm.rotate(identity,glm.radians(self.camRotation.z),glm.vec3(0,0,1))
        
        rotationMat = pitch*yaw*roll
        
        camMatrix = translateMat*rotationMat
        
        return glm.inverse(camMatrix)
    
    def setShaders(self,vertexShader,fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.activeShader = compileProgram(compileShader(vertexShader,GL_VERTEX_SHADER),compileShader(fragmentShader,GL_FRAGMENT_SHADER))
        else:
            self.activeShader = None
            
    def update(self):
        self.viewMatrix = glm.lookAt(self.camPosition,self.target,glm.vec3(0,1,0))
        
    def render(self):
        glClearColor(self.clearColor[0],self.clearColor[1],self.clearColor[2],1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        if self.activeShader is not None:
            glUseProgram(self.activeShader)
            glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"viewMatrix"),
                                                    1,GL_FALSE,glm.value_ptr(self.viewMatrix))
            glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"projectionMatrix"),
                                                    1,GL_FALSE,glm.value_ptr(self.projectionMatrix))
            glUniform1f(glGetUniformLocation(self.activeShader,"time"),self.elapsedTime)
            glUniform1f(glGetUniformLocation(self.activeShader,"fatness"),self.fatness)
            glUniform3fv(glGetUniformLocation(self.activeShader,"dirLight"),1,glm.value_ptr(self.dirLight))

        for obj in self.scene:
            if self.activeShader is not None:
                glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"modelMatrix"),
                                                    1,GL_FALSE,glm.value_ptr(obj.getModelMatrix()))
                

            obj.render()