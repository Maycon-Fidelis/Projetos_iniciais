import pygame

# Inicialização
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Marcar Pontos com o Mouse")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen.fill(WHITE)

pontos = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            pontos.append((x, y))

    for ponto in pontos:
        pygame.draw.circle(screen, RED, ponto, 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
