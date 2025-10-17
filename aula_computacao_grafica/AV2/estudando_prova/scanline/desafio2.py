import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scanline Polygon Fill")

VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

SCREEN.fill(VERDE)

polygon = [(350, 350), (480, 350), (400, 250)]

import pygame

def scanline_fill(screen, polygon, color):
    # Ordena os pontos pela coordenada y
    min_y = min(polygon, key=lambda p: p[1])[1]
    max_y = max(polygon, key=lambda p: p[1])[1]

    for y in range(int(min_y), int(max_y) + 1):
        intersecoes = []

        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]  # próximo vértice (fechando o polígono)

            if p1[1] == p2[1]:  # ignorar arestas horizontais
                continue

            if p1[1] < p2[1]:
                y1, y2 = p1[1], p2[1]
                x1, x2 = p1[0], p2[0]
            else:
                y1, y2 = p2[1], p1[1]
                x1, x2 = p2[0], p1[0]

            # Verifica se a linha y cruza essa aresta
            if y1 <= y < y2:
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersecoes.append(x)

        # Ordena os pontos de interseção
        intersecoes.sort()

        # Desenha pares de linhas horizontais entre as interseções
        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                x1 = int(intersecoes[i])
                x2 = int(intersecoes[i + 1])
                pygame.draw.line(screen, color, (x1, y), (x2, y))

scanline_fill(SCREEN, polygon, VERMELHO)

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    pygame.display.flip()

pygame.quit()
