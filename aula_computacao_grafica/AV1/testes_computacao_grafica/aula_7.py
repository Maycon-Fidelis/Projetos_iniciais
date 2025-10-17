import pygame
import math

# Configuração inicial
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, RED, BLUE, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modelagem 2D - Manipulação de Polígonos")

# Variáveis globais
poligono = []
selecionado = None
modo_desenho = True

def desenhar_poligono():
    """Desenha o polígono e seus vértices"""
    if len(poligono) > 1:
        pygame.draw.polygon(screen, BLUE, poligono, 2)
    for ponto in poligono:
        pygame.draw.circle(screen, RED, ponto, 5)

def encontrar_vertice(pos):
    """Verifica se um vértice foi clicado"""
    for i, ponto in enumerate(poligono):
        if math.dist(pos, ponto) < 10:
            return i
    return None

def transladar(dx, dy):
    """Aplica translação ao polígono"""
    global poligono
    poligono = [(x + dx, y + dy) for x, y in poligono]

def escalar(sx, sy):
    """Aplica escalonamento ao polígono"""
    global poligono
    if len(poligono) < 1:
        return
    cx, cy = poligono[0]  # Ponto de referência
    poligono = [(cx + (x - cx) * sx, cy + (y - cy) * sy) for x, y in poligono]

def rotacionar(angulo):
    """Aplica rotação ao polígono"""
    global poligono
    if len(poligono) < 1:
        return
    cx, cy = poligono[0]  # Centro da rotação
    rad = math.radians(angulo)
    poligono = [
        (
            int(cx + (x - cx) * math.cos(rad) - (y - cy) * math.sin(rad)),
            int(cy + (x - cx) * math.sin(rad) + (y - cy) * math.cos(rad))
        ) 
        for x, y in poligono
    ]

# Loop principal
rodando = True
while rodando:
    screen.fill(WHITE)
    desenhar_poligono()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if modo_desenho:
                poligono.append(event.pos)
            else:
                selecionado = encontrar_vertice(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            selecionado = None

        elif event.type == pygame.MOUSEMOTION and selecionado is not None:
            poligono[selecionado] = event.pos

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                modo_desenho = False
            elif event.key == pygame.K_r:
                rotacionar(15)
            elif event.key == pygame.K_t:
                transladar(10, 0)
            elif event.key == pygame.K_s:
                escalar(1.1, 1.1)

pygame.quit()
