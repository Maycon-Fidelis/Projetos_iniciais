import pygame

pygame.init()

WIDTH,HEIGHT = 800,600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Desafio 1")

VERMELHO = (255,0,0)
VERDE = (0,255,0)

SCREEN.fill(VERDE)

# pygame.draw.polygon(SCREEN,VERMELHO,[[350,350],[480,350],[400,250]])
#vertices do triangulo
p1 = [350,450]
p2 = [480,370]
p3 = [400,250]

#Ordenando os pontos de y
pontos = sorted(([p1,p2,p3]), key=lambda p: p[1])
top, mid, bot = pontos[0],pontos[1],pontos[2]

print(top,mid,bot)
def interpolar_x(y, p1, p2):
    if p1[1] == p2[1]:  # linha horizontal
        return p1[0]
    return p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])

#Preenchendo do top ao mid
for y in range(int(top[1]), int(mid[1]) + 1):
    x1 = interpolar_x(y,top,mid)
    x2 = interpolar_x(y,top,bot)
    pygame.draw.line(SCREEN,VERMELHO,(int(x1), y),(int(x2), y))

# #Preenchendo do mid ao bot
for y in range(int(mid[1]) + 1,int(bot[1]) + 1):
    x1 = interpolar_x(y,mid,bot)
    x2 = interpolar_x(y,top,bot)
    pygame.draw.line(SCREEN,VERMELHO,(int(x1), y),(int(x2), y))

# pygame.draw.polygon(SCREEN,VERMELHO,[[400,400],[500,400],[450,300]])
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    pygame.display.flip()

pygame.quit()