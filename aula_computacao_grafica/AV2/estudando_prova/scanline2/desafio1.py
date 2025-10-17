import pygame

pygame.init()

WIDTH, HEIGHT = 800,600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Desafio")

VERMELHO = (255,0,0)
VERDE = (0,255,0)


SCREEN.fill(VERMELHO)

#pontos do triangulo
p1 = [300,400]
p2 = [400,400]
p3 = [350,300]

#Pegando os valores de top,mid,bot
pontos = sorted(([p1,p2,p3]), key=lambda p: p[1])
top,mid,bot = pontos[0], pontos[1], pontos[2]

#interpolando o valor de x
def interpolar_x(y,p1,p2):
    if p1[1] == p2[1]:
        return p1[0]
    return p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])

# indo do top ao mid
for y in range(int(top[1]),int(mid[1]) +1):
    x1 = interpolar_x(y,top,mid)
    x2 = interpolar_x(y,top,bot)
    pygame.draw.line(SCREEN,VERDE,(int(x1),y),(int(x2),y))

#indo do mid ao bot

for y in range(int(mid[1]),int(bot[1]) +1):
    x1 = interpolar_x(y,mid,bot)
    x2 = interpolar_x(y,top,bot)
    pygame.draw.line(SCREEN,VERDE,(int(x1),y),(int(x2),y))

rodando = True
while rodando:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
pygame.quit()