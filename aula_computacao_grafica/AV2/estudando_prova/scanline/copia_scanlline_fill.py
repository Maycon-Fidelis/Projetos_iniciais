import pygame

pygame.init()

WIDTH, HEIGHT = 800,600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Desafio")

VERMELHO = (255,0,0)
VERDE = (0,255,0)

SCREEN.fill(VERDE)

#pontos poligonos convexos
p1 = [350,350]
p2 = [480,350]
p3 = [400,250]

polygon = [p1,p2,p3]

#Interpolando X
def interpolar_x(y,p1,p2):
    if p1[1] == p2[1]:
        return None
    return p1[1] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])

#Função scanlline fill
def scanline_fill(polygon: list[tuple[int,int]]):

    min_y = min(p[1] for p in polygon)
    max_y = max(p[1] for p in polygon)

    for y in range(min_y,max_y + 1):
        intersecsoes = []

        for i in range(len(polygon)):
            p1 = polygon[1]
            p2 = polygon[(i + 1) % len(polygon)]

        if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
            x = interpolar_x(y,p1,p2)
            if x is not None:
                intersecsoes.append(x)

    intersecsoes.sort()

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    pygame.display.flip()
pygame.quit()
