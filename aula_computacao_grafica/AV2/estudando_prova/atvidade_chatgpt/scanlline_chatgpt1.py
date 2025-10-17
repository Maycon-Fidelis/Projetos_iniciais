import pygame, random, math

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desafio chatgpt 1")

BRANCO = (255, 255, 255)

CORES = [
    (255, 0, 0),     # Vermelho
    (0, 255, 0),     # Verde
    (0, 0, 255),     # Azul
    (255, 255, 0),   # Amarelo
    (155, 0, 255)    # Roxo
]

SCREEN.fill((255,255,255))

def gerar_poligonos_convexos(center_x,center_y,radius,num_vertices):
    angulos = sorted([random.uniform(0,2 * math.pi) for _ in range(num_vertices)])
    pontos = [
        (
            int(center_x + radius * math.cos(a)),
            int(center_y + radius * math.sin(a))
        ) for a in angulos
    ]
    return pontos

#Gerando os poligonos
poligonos = []
cores = []
num_poligonos = 5

for i in range(num_poligonos):
    num_vertices = random.randint(4,8)
    radius = random.randint(40,80)

    margin = 100
    center_x = random.randint(margin, WIDTH - margin)
    center_y = random.randint(margin, HEIGHT - margin)

    poligono = gerar_poligonos_convexos(center_x,center_y,radius,num_vertices)
    cor = [random.randint(0,255) for _ in range(3)]

    poligonos.append(poligono)
    cores.append(cor)

def preenchendo_scanline(screen, poligono, cor):
    y_min = min(p[1] for p in poligono)
    y_max = max(p[1] for p in poligono)

    for y in range(int(y_min), int(y_max) + 1):
        intersecoes = []

        for i in range(len(poligono)):
            p1 = poligono[i]
            p2 = poligono[(i + 1) % len(poligono)]  # conecta o último ao primeiro

            if p1[1] == p2[1]:
                continue  # ignora arestas horizontais

            if p1[1] < p2[1]:
                y1, y2 = p1[1], p2[1]
                x1, x2 = p1[0], p2[0]
            else:
                y1, y2 = p2[1], p1[1]
                x1, x2 = p2[0], p1[0]

            if y1 <= y < y2:  # inclui y1 mas exclui y2 para evitar duplicação
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersecoes.append(x)

        intersecoes.sort()

        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                x1 = int(intersecoes[i])
                x2 = int(intersecoes[i + 1])
                pygame.draw.line(screen, cor, (x1, y), (x2, y))

for i in range(num_poligonos):
    preenchendo_scanline(SCREEN,poligonos[i],cores[i])
    # pygame.draw.polygon(SCREEN, cores[i], poligonos[i])
    pygame.draw.polygon(SCREEN,(0,0,0),poligonos[i],2)


# Loop principal
rodando = True
while rodando:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

pygame.quit()
