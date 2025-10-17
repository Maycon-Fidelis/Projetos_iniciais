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
def generate_concave_polygon(n, radius=200, center=(WIDTH // 2, HEIGHT // 2)):
    points = []
    for _ in range(n):
        angle = random.uniform(0, 2 * math.pi)
        r = radius * random.uniform(0.4, 1.0)
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        points.append((x, y))
    
    # Ordena os pontos por ângulo em relação ao centro
    points.sort(key=lambda p: math.atan2(p[1] - center[1], p[0] - center[0]))

    # Converte para inteiros só depois de ordenar
    return [(int(x), int(y)) for x, y in points]


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
        poly = generate_concave_polygon(num_vertices, polygon_radius, center)
        polygons.append(poly)
    return polygons

polygon_points_list = generate_multiple_polygons(3)

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

    # Desenhar os polígonos
    for points in polygon_points_list:
        draw_polygon(screen, points, polygon_color)

    pygame.display.flip()

pygame.quit()
