import pygame
import math

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, RED, BLUE, GREEN, YELLOW = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rasterização - Computação Gráfica")

# Algoritmo de Bresenham para desenhar linhas
def bresenham_line(x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        screen.set_at((x1, y1), color)
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# Algoritmo do ponto médio para desenhar círculos
def midpoint_circle(cx, cy, r, color):
    x, y = r, 0
    p = 1 - r

    while x >= y:
        for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]:
            screen.set_at((cx + dx, cy + dy), color)
        y += 1
        if p <= 0:
            p += 2 * y + 1
        else:
            x -= 1
            p += 2 * (y - x) + 1

# Algoritmo de preenchimento Scanline para polígonos
def scanline_fill(polygon, color):
    edges = sorted(polygon, key=lambda p: p[1])  # Ordena por Y
    y_min, y_max = edges[0][1], edges[-1][1]
    
    for y in range(y_min, y_max + 1):
        intersec = []
        for i in range(len(polygon)):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % len(polygon)]
            
            if y1 > y2:
                x1, x2, y1, y2 = x2, x1, y2, y1  # Ordena os pontos

            if y1 <= y < y2:
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersec.append(int(x))
        
        intersec.sort()
        for i in range(0, len(intersec) - 1, 2):
            for x in range(intersec[i], intersec[i + 1] + 1):
                screen.set_at((x, y), color)

# Interpolação de cores para Gouraud Shading
def gouraud_shading(triangle, colors):
    triangle = sorted(triangle, key=lambda p: p[1])  # Ordena por Y
    y_min, y_max = triangle[0][1], triangle[-1][1]

    for y in range(y_min, y_max + 1):
        intersec = []
        inter_colors = []
        for i in range(len(triangle)):
            x1, y1 = triangle[i]
            x2, y2 = triangle[(i + 1) % len(triangle)]
            c1, c2 = colors[i], colors[(i + 1) % len(triangle)]
            
            if y1 > y2:
                x1, x2, y1, y2 = x2, x1, y2, y1
                c1, c2 = c2, c1
            
            if y1 <= y < y2:
                alpha = (y - y1) / (y2 - y1)
                x = int(x1 + alpha * (x2 - x1))
                color = (
                    int(c1[0] + alpha * (c2[0] - c1[0])),
                    int(c1[1] + alpha * (c2[1] - c1[1])),
                    int(c1[2] + alpha * (c2[2] - c1[2])),
                )
                intersec.append(x)
                inter_colors.append(color)
        
        intersec, inter_colors = zip(*sorted(zip(intersec, inter_colors)))
        for i in range(0, len(intersec) - 1, 2):
            for x in range(intersec[i], intersec[i + 1] + 1):
                alpha = (x - intersec[i]) / (intersec[i + 1] - intersec[i])
                color = (
                    int(inter_colors[i][0] + alpha * (inter_colors[i + 1][0] - inter_colors[i][0])),
                    int(inter_colors[i][1] + alpha * (inter_colors[i + 1][1] - inter_colors[i][1])),
                    int(inter_colors[i][2] + alpha * (inter_colors[i + 1][2] - inter_colors[i][2])),
                )
                screen.set_at((x, y), color)

# Loop principal
rodando = True
while rodando:
    screen.fill(WHITE)

    # Rasterização de uma linha
    bresenham_line(50, 100, 300, 400, RED)

    # Rasterização de um círculo
    midpoint_circle(600, 300, 80, BLUE)

    # Preenchimento de um polígono
    poligono = [(400, 200), (500, 150), (600, 300), (450, 350)]
    scanline_fill(poligono, GREEN)

    # Gouraud Shading em um triângulo
    triangulo = [(200, 400), (300, 200), (400, 450)]
    cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    gouraud_shading(triangulo, cores)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

pygame.quit()
