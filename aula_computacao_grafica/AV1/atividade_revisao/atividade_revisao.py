import pygame
import math

pygame.init()
largura, altura = 800, 600
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Atividade de Revisão")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
AMARELO = (255, 255, 0)

vertices = []
desenhar = False

def ordenar_vertices(vertices):
    centro_x = sum([v[0] for v in vertices]) / len(vertices)
    centro_y = sum([v[1] for v in vertices]) / len(vertices)
    return sorted(vertices, key=lambda v: math.atan2(v[1] - centro_y, v[0] - centro_x))

def scanline_fill(polygon):
    ymin = min(p[1] for p in polygon)
    ymax = max(p[1] for p in polygon)

    for y in range(ymin, ymax + 1):
        interseccoes = []

        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]

            if p1[1] == p2[1]:
                continue
            if p1[1] > p2[1]:
                p1, p2 = p2, p1

            if p1[1] <= y < p2[1]:
                x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                interseccoes.append(x)

        interseccoes.sort()

        for i in range(0, len(interseccoes), 2):
            if i + 1 < len(interseccoes):
                x1 = int(interseccoes[i])
                x2 = int(interseccoes[i + 1])
                pygame.draw.line(screen, AMARELO, (x1, y), (x2, y))


# Loop principal
rodando = True
while rodando:
    screen.fill(WHITE)

    if desenhar and len(vertices) >= 3:
        poligono_ordenado = ordenar_vertices(vertices)
        scanline_fill(poligono_ordenado)  # Preenchimento manual (scanline)
        pygame.draw.polygon(screen, BLUE, poligono_ordenado, 3)  # Contorno azul

    # Desenha os pontos
    for v in vertices:
        pygame.draw.circle(screen, BLUE, v, 5)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not desenhar:
                pos = pygame.mouse.get_pos()
                vertices.append(pos)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Pressione ENTER para desenhar
                if len(vertices) >= 3:
                    desenhar = True
            elif event.key == pygame.K_SPACE:  # Pressione ESPAÇO para resetar
                vertices = []
                desenhar = False

pygame.quit()