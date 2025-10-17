import pygame
import random
import time

# Inicializa o Pygame
pygame.init()

# Tamanho da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Scanline - Polígonos Aleatórios")

# Cores
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)

# Função para gerar um polígono aleatório
def gerar_poligono():
    qtd_vertices = random.randint(3, 7)
    vertices = []
    for _ in range(qtd_vertices):
        x = random.randint(100, largura - 100)
        y = random.randint(100, altura - 100)
        vertices.append((x, y))

    # Ordena os vértices pelo ângulo em relação ao centro para evitar auto-interseções
    centro_x = sum([v[0] for v in vertices]) / qtd_vertices
    centro_y = sum([v[1] for v in vertices]) / qtd_vertices
    vertices.sort(key=lambda v: (math.atan2(v[1] - centro_y, v[0] - centro_x)))
    return vertices

# Algoritmo de preenchimento Scanline
def scanline_fill(surface, polygon, color):
    ymin = min(p[1] for p in polygon)
    ymax = max(p[1] for p in polygon)

    for y in range(ymin, ymax + 1):
        intersecoes = []

        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]

            if p1[1] == p2[1]:
                continue
            if p1[1] > p2[1]:
                p1, p2 = p2, p1
            
            if p1[1] <= y < p2[1]:
                x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                intersecoes.append(x)

        intersecoes.sort()

        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                x1 = int(intersecoes[i])
                x2 = int(intersecoes[i + 1])
                pygame.draw.line(surface, color, (x1, y), (x2, y))

# Biblioteca necessária para ordenar por ângulo
import math

# Variáveis de controle
poligono = gerar_poligono()
tempo_ultimo = time.time()

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Verifica se passou 5 segundos para gerar novo polígono
    tempo_atual = time.time()
    if tempo_atual - tempo_ultimo >= 5:
        poligono = gerar_poligono()
        tempo_ultimo = tempo_atual

    # Preenche e desenha o polígono
    scanline_fill(tela, poligono, AMARELO)
    pygame.draw.polygon(tela, AZUL, poligono, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
    