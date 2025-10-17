import pygame
import math

pygame.init()
largura, altura = 800,600
screen = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Ativdade Revisão")

BRANCO = (255,255,255)
AZUL = (0,0,255)
AMARELO = (0,255,0)
VERMELHO = (255,0,0)

posicoes = []
vertices = []
poligonos = []
pontosCaptura = True

def gerarVertices(pontos):
    centrox = sum([p[0] for p in pontos]) / len(pontos)
    centroy = sum([p[1] for p in pontos]) / len(pontos)
    return sorted(pontos,key=lambda v: math.atan2(v[1]-centroy,v[0] - centrox))
                  
def scanline(polygon):
    ymin = min([p[1] for p in polygon])
    ymax = max([p[1] for p in polygon])

    for y in range(ymin,ymax+1):
        interseccoes = []

        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]

            if p1[1] == p2[1]:
                continue
            if (y >= min(p1[1], p2[1])) and (y < max(p1[1], p2[1])):
                # Interseção da aresta com a scanline
                x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])

                interseccoes.append(x)


        interseccoes.sort()

        for i in range(0,len(interseccoes),2):
            if i + 1 < len(interseccoes):
                x1 = int(interseccoes[i])
                x2 = int(interseccoes[i+1])
                pygame.draw.line(screen,AMARELO,(x1,y),(x2,y))

rodando = True
while rodando:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            rodando = False
    
        if event.type == pygame.MOUSEBUTTONDOWN and pontosCaptura == True:
            pos = pygame.mouse.get_pos()
            posicoes.append(pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(posicoes) >= 3:
                novo_poligono = gerarVertices(posicoes)
                poligonos.append(novo_poligono)  # Armazena o novo polígono
                posicoes = []  # Limpa para capturar outro polígono
                pontosCaptura = True


        screen.fill(BRANCO)  

        for ponto in posicoes:
            pygame.draw.circle(screen,VERMELHO,ponto,10)

        for poly in poligonos:
            scanline(poly)
            pygame.draw.polygon(screen,AZUL,poly,5)

        pygame.display.flip()

pygame.quit()