import pygame
import math

pygame.init()
largura, altura = 800, 600
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Atividade Revisão")

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)

# Variáveis principais
posicoes = []
vertices = []
pontosCaptura = True

# --- Funções de geometria ---
def gerarVertices(pontos):
    centrox = sum([p[0] for p in pontos]) / len(pontos)
    centroy = sum([p[1] for p in pontos]) / len(pontos)
    return sorted(pontos, key=lambda v: math.atan2(v[1] - centroy, v[0] - centrox))

def scanline(polygon):
    ymin = int(min([p[1] for p in polygon]))
    ymax = int(max([p[1] for p in polygon]))

    for y in range(ymin, ymax + 1):
        interseccoes = []

        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]

            if p1[1] == p2[1]:
                continue
            if p1[1] > p2[1]:
                p1, p2 = p2, p1
            if p1[1] <= y <= p2[1]:
                x = p1[0] + (y - p1[1]) * ((p2[0] - p1[0]) / (p2[1] - p1[1]))
                interseccoes.append(x)

        interseccoes.sort()

        for i in range(0, len(interseccoes), 2):
            if i + 1 < len(interseccoes):
                x1 = int(interseccoes[i])
                x2 = int(interseccoes[i + 1])
                pygame.draw.line(screen, AMARELO, (x1, y), (x2, y))

def transladar(pontos, dx, dy):
    return [(x + dx, y + dy) for (x, y) in pontos]

def rotacionar(pontos, angulo, centro=None):
    if centro is None:
        cx = sum([p[0] for p in pontos]) / len(pontos)
        cy = sum([p[1] for p in pontos]) / len(pontos)
    else:
        cx, cy = centro

    rad = math.radians(angulo)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    novos_pontos = []
    for (x, y) in pontos:
        x -= cx
        y -= cy
        x_new = x * cos_a - y * sin_a + cx
        y_new = x * sin_a + y * cos_a + cy
        novos_pontos.append((x_new, y_new))
    return novos_pontos

def escalonar(pontos, sx, sy, centro=None):
    if centro is None:
        cx = sum([p[0] for p in pontos]) / len(pontos)
        cy = sum([p[1] for p in pontos]) / len(pontos)
    else:
        cx, cy = centro

    return [((x - cx) * sx + cx, (y - cy) * sy + cy) for (x, y) in pontos]

# --- Loop principal ---
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == pygame.MOUSEBUTTONDOWN and pontosCaptura:
            pos = pygame.mouse.get_pos()
            posicoes.append(pos)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and pontosCaptura:
                vertices = gerarVertices(posicoes)
                pontosCaptura = False

            if not pontosCaptura:
                if event.key == pygame.K_RIGHT:
                    vertices = transladar(vertices, 10, 0)
                elif event.key == pygame.K_LEFT:
                    vertices = transladar(vertices, -10, 0)
                elif event.key == pygame.K_UP:
                    vertices = transladar(vertices, 0, -10)
                elif event.key == pygame.K_DOWN:
                    vertices = transladar(vertices, 0, 10)
                elif event.key == pygame.K_r:
                    vertices = rotacionar(vertices, 10)
                elif event.key == pygame.K_e:
                    vertices = escalonar(vertices, 1.1, 1.1)
                elif event.key == pygame.K_q:
                    vertices = escalonar(vertices, 0.9, 0.9)

    # --- Desenho na tela ---
    screen.fill(BRANCO)

    for ponto in posicoes:
        pygame.draw.circle(screen, VERMELHO, ponto, 10)

    if not pontosCaptura:
        scanline(vertices)
        pygame.draw.polygon(screen, AZUL, vertices, 5)

    pygame.display.flip()

pygame.quit()
