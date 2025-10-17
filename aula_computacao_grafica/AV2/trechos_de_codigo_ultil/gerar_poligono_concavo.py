import pygame
import random
import math

# --- Configurações básicas ---
WIDTH, HEIGHT = 800, 600
FPS = 60
NUM_POINTS = 8
NUM_POLYGONS = 3  # Quantos polígonos desenhar
RADIUS = 100

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Polígonos Côncavos Aleatórios")
clock = pygame.time.Clock()

# --- Geração de polígono convexo base ---
def generate_convex_polygon(n, radius=200, center=(WIDTH // 2, HEIGHT // 2)):
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n)])
    points = []

    for angle in angles:
        r = radius * random.uniform(0.8, 1.0)
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        points.append([x, y])

    return points

# --- Criar concavidade ---
def make_polygon_concave(points):
    if len(points) < 4:
        return points

    i = random.randint(1, len(points) - 2)
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)

    points[i][0] = (points[i][0] + cx) / 2
    points[i][1] = (points[i][1] + cy) / 2

    return points

# --- Função para gerar múltiplos polígonos ---
def generate_multiple_concave_polygons(count, same_position=False, fixed_center=(WIDTH // 2, HEIGHT // 2)):
    polygons = []
    for _ in range(count):
        center = fixed_center if same_position else (
            random.randint(100, WIDTH - 100),
            random.randint(100, HEIGHT - 100)
        )
        convex = generate_convex_polygon(NUM_POINTS, RADIUS, center)
        concave = make_polygon_concave(convex)
        polygons.append(concave)
    return polygons

# --- Geração inicial ---
polygon_list = generate_multiple_concave_polygons(NUM_POLYGONS, same_position=False)

# --- Loop principal ---
running = True
while running:
    clock.tick(FPS)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Geração de novos polígonos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                polygon_list = generate_multiple_concave_polygons(NUM_POLYGONS, same_position=False)
            elif event.key == pygame.K_RETURN:
                polygon_list = generate_multiple_concave_polygons(NUM_POLYGONS, same_position=True)

    for polygon in polygon_list:
        if len(polygon) >= 3:
            pygame.draw.polygon(screen, (255, 100, 50), polygon, 3)

    pygame.display.flip()

pygame.quit()
