import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Cenas simples em pygame")

#Cores
AZUL = (135, 206, 235)
AMARELO = (255, 255, 0)
VERDE = (34, 139, 34)
MARROM = (139, 69, 19)
VERMELHO = (255, 0, 0)

#Fundo
screen.fill(AZUL)

#Formas geometricas
#Sol
pygame.draw.circle(screen,AMARELO,(150,120),radius=80)

#Grama
pygame.draw.rect(screen,VERDE,(0,500,800,100))

#casa
#Base
pygame.draw.rect(screen,MARROM,(500,350,150,150))

#Telado
pygame.draw.polygon(screen,VERMELHO,[(500,350),(575,250),(650,350)])

pygame.display.flip()
#Loop para rodar 
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

pygame.quit()