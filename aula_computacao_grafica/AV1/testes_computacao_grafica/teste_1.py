import pygame

#inicializa o Pygame
pygame.init()

#configuração da tela
largura,  altura = 800,600
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Primitivas Gráficas 2D")

#loop principal
desenhando = True
while desenhando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            desenhando = False
    pygame.display.flip()

pygame.quit()