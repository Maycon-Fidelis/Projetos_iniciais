import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Primitivas Gráficas 2D")

# Loop principal
desenhando = True
while desenhando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            desenhando = False

    pygame.display.flip()

pygame.quit()