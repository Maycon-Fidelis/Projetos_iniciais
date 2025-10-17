import pygame, time

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scanline - Polígono Convexo")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Limpar a tela
SCREEN.fill(VERDE)

# Lista de pontos do polígono (em ordem)
pontos = [
    (300, 100),
    (500, 150),
    (550, 300),
    (400, 400),
    (250, 300),
]

y_min = min(p[1] for p in pontos)
y_max = max(p[1] for p in pontos)

#Interpolando x
def interpolar_x(y,p1,p2):
    if p1[1] == p2[1]:
        return p1[0]
    return p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[0] - p1[0])

#scanline (linha horizontal)
for y in range(y_min,y_max + 1):
    intersecsoes = []

    for i in range(len(pontos) - 1):
        p1 = pontos[i]
        p2 = pontos[i + 1]

        if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
            x = interpolar_x(y,p1,p2)
            intersecsoes.append(x)
    
    intersecsoes.sort()

    for i in range(0,len(intersecsoes),2):
        if i + 1 < len(intersecsoes):
            x1 = int(intersecsoes[i])
            x2 = int(intersecsoes[i + 1])
            pygame.draw.line(SCREEN,VERMELHO,(x1,y),(x2,y))
    
    time.sleep(1)

# Loop principal
rodando = True
while rodando:
    pygame.display.flip()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

pygame.quit()
