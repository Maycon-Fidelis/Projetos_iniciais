import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
NUM_POINTS = 8
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scanline Fill")
clock = pygame.time.Clock()

# --- Geração de polígono côncavo (como antes) ---
def generate_convex_polygon(n, radius=200, center=(WIDTH // 2, HEIGHT // 2)):
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n)])
    points = []

    for angle in angles:
        r = radius * random.uniform(0.8, 1.0)
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        points.append([x, y])

    return points

def make_polygon_concave(points):
    if len(points) < 4:
        return points
    i = random.randint(1, len(points) - 2)
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    points[i][0] = (points[i][0] + cx) / 2
    points[i][1] = (points[i][1] + cy) / 2
    return points

# --- Algoritmo de Scanline Fill ---
def scanline_fill(surface, polygon, color):
    # Ordenar o polígono como tuplas (inteiros)
    polygon = [(int(x), int(y)) for x, y in polygon]
    min_y = min(p[1] for p in polygon)
    max_y = max(p[1] for p in polygon)

    for y in range(min_y, max_y + 1):
        intersections = []

        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]

            if p1[1] == p2[1]:  # Ignorar linhas horizontais
                continue

            if (y >= min(p1[1], p2[1])) and (y < max(p1[1], p2[1])):
                # Interseção da aresta com a scanline
                x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                intersections.append(x)

        intersections.sort()

        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x1 = int(intersections[i])
                x2 = int(intersections[i + 1])
                pygame.draw.line(surface, color, (x1, y), (x2, y))

# --- Inicialização do polígono ---
polygon_points = make_polygon_concave(generate_convex_polygon(NUM_POINTS))

# --- Loop principal ---
running = True
while running:
    clock.tick(FPS)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            polygon_points = make_polygon_concave(generate_convex_polygon(NUM_POINTS))

    # Preencher polígono
    scanline_fill(screen, polygon_points, (100, 200, 255))

    # Desenhar bordas
    pygame.draw.polygon(screen, (0, 0, 0), polygon_points, 2)

    pygame.display.flip()

pygame.quit()
