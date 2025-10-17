import pygame 
import sys
import numpy as np 
from class_polygon import Polygon
from polygons import polygons
from pygame.locals import *

pygame.init()

FPS = 60
width = 800
height = 600
zBuffer = np.full((width, height), 999.99)

pygame.display.set_caption("Revisão")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

p1 = Polygon(1, "Azul", screen, polygons[0], (zBuffer,1), (0, 0, 128))
p2 = Polygon(1, "Verde", screen, polygons[1], (zBuffer,2), (0, 255, 0))
p3 = Polygon(1, "Amarelo", screen, polygons[2], (zBuffer,3), (255, 255, 0))
p4 = Polygon(1, "Laranja", screen, polygons[3], (zBuffer,4), (255, 165, 0))
p5 = Polygon(1, "Vermelho", screen, polygons[4], (zBuffer,5), (255, 0, 0))

polygons_arr = [p1,p2,p3,p4,p5]

running = True

while running: 
    screen.fill((255,255,255))
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for layer in polygons_arr:
        layer.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()



