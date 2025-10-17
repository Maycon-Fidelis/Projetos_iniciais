import pygame
import numpy as np

# Inicializar Pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Z-Buffer com Pygame")

# Inicializar Z-buffer com valores infinitos
z_buffer = np.full((WIDTH, HEIGHT), np.inf)

# Função para desenhar "à mão" um retângulo com Z-buffer
def draw_rect_zbuffer(x1, y1, x2, y2, z_depth, color):
    for y in range(y1, y2):
        for x in range(x1, x2):
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                if z_depth < z_buffer[x, y]:
                    z_buffer[x, y] = z_depth
                    screen.set_at((x, y), color)

# Cores em RGB
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Loop principal
running = True
drawn = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not drawn:
        screen.fill((0, 0, 0))

        # Retângulo vermelho no fundo
        draw_rect_zbuffer(50, 50, 300, 300, z_depth=0.8, color=RED)

        # Retângulo azul na frente, parcialmente sobreposto
        draw_rect_zbuffer(100, 100, 350, 350, z_depth=0.5, color=BLUE)

        pygame.display.flip()
        drawn = True

# Finalizar
pygame.quit()
