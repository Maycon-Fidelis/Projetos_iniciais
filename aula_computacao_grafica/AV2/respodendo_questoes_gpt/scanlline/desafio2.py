import pygame
import random
import math

# --- Configurações iniciais ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# --- Inicializar Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Polígonos em Posições Diferentes")
clock = pygame.time.Clock()

# --- Função para gerar polígono convexo ---
def generate_convex_polygon(n, radius=200, center=(WIDTH // 2, HEIGHT // 2)):
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n)])
    points = []

    for angle in angles:
        r = radius * random.uniform(0.2, 1.0)
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        points.append((int(x), int(y)))

    return points

# --- Função para desenhar polígono ---
def draw_polygon(surface, points, color):
    if len(points) >= 3:
        pygame.draw.polygon(surface, color, points, 3)

# --- Inicialização de parâmetros ---
num_vertices = 8
polygon_color = (0, 200, 255)
polygon_radius = 100

# --- Geração inicial dos polígonos em diferentes posições ---
def generate_multiple_polygons(count, same_position=False, fixed_center=(WIDTH // 2, HEIGHT // 2)):
    polygons = []
    for _ in range(count):
        # Se same_position=True, usa o mesmo centro. Caso contrário, gera um centro aleatório.
        center = fixed_center if same_position else (
            random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        )
        poly = generate_convex_polygon(num_vertices, polygon_radius, center)
        polygons.append(poly)
    return polygons

polygon_points_list = generate_multiple_polygons(3)

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

#gerando cor de forma aleatoria
cores = []
def gerando_cores(quantidade):
    for i in range(quantidade):

        r = random.randint(0,256)
        g = random.randint(0,256)
        b = random.randint(0,256)

        cores.append([r,g,b])
    
    return cores

coresss = gerando_cores(3)
print(coresss)

# --- Loop principal ---
running = True
while running:
    clock.tick(FPS)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pressionar espaço para gerar novos polígonos em novas posições
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            polygon_points_list = generate_multiple_polygons(3)

for i, poly in enumerate(polygon_points_list):
    # 1. Desenhar borda
    draw_polygon(screen, poly, cores[i])
    pygame.time.delay(50)  # espera 300 ms antes de preencher

    # 2. Preencher com scanline
    scanline_fill(screen, poly, cores[i])
    pygame.time.delay(50)  # opcional: mais um delay depois


pygame.quit()
