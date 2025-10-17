import pygame, random, math

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desafio")

BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)

def generate_convex_polygon(n, radius=50, center=(0, 0)):
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n)])
    points = []
    for angle in angles:
        r = radius * random.uniform(0.7, 1.0)
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

# Número de polígonos a desenhar
num_poligonos = random.randint(3, 6)

SCREEN.fill(BRANCO)

for _ in range(num_poligonos):
    # Número de vértices aleatório entre 4 e 8
    num_vertices = random.randint(4, 8)

    # Centro aleatório dentro da tela (com margem)
    center = (
        random.randint(100, WIDTH - 100),
        random.randint(100, HEIGHT - 100)
    )

    pontos = generate_convex_polygon(num_vertices, radius=60, center=center)
    pontos = make_polygon_concave(pontos)

    pontos_int = [(int(x), int(y)) for x, y in pontos]

    pygame.draw.polygon(SCREEN, VERDE, pontos_int)

# Loop principal
rodando = True
while rodando:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

pygame.quit()
