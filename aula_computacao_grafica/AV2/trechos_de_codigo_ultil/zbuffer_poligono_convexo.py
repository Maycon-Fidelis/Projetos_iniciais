import pygame
import random
import math

# --- Configurações iniciais ---
WIDTH, HEIGHT = 800, 600
FPS = 60
NUM_POLYGONS = 5
NUM_VERTICES = 8
POLYGON_RADIUS = 100

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Z-Buffer com Polígonos")
clock = pygame.time.Clock()

# --- Geração de polígono convexo ---
def generate_convex_polygon(n, radius=200, center=(WIDTH // 2, HEIGHT // 2)):
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n)])
    points = []

    for angle in angles:
        r = radius * random.uniform(0.2, 1.0)
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        points.append((int(x), int(y)))

    return points

# --- Geração de múltiplos polígonos com Z-buffer ---
def generate_multiple_polygons(count, same_position=True, fixed_center=(WIDTH // 2, HEIGHT // 2)):
    polygons = []
    for _ in range(count):
        center = fixed_center if same_position else (
            random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        )
        points = generate_convex_polygon(NUM_VERTICES, POLYGON_RADIUS, center)
        z = random.uniform(0, 1)  # profundidade aleatória
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        polygons.append({
            "points": points,
            "z": z,
            "color": color
        })
    return polygons

# --- Desenhar os polígonos ordenados por Z ---
def draw_polygons_with_zbuffer(surface, polygon_list):
    sorted_polygons = sorted(polygon_list, key=lambda p: p["z"], reverse=True)
    for poly in sorted_polygons:
        pygame.draw.polygon(surface, poly["color"], poly["points"], 0)  # preenchido
        pygame.draw.polygon(surface, (0, 0, 0), poly["points"], 2)      # contorno

# --- Inicialização dos polígonos ---
polygon_objects = generate_multiple_polygons(NUM_POLYGONS)

# --- Loop principal ---
running = True
while running:
    clock.tick(FPS)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pressionar espaço para gerar novos polígonos
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            polygon_objects = generate_multiple_polygons(NUM_POLYGONS)

    # Desenhar com Z-buffer
    draw_polygons_with_zbuffer(screen, polygon_objects)

    pygame.display.flip()

pygame.quit()
