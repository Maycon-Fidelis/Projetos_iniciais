import pygame

pygame.init()

WIDTH, HEIGHT = 800,600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Desafio")

VERMELHO = (255,0,0)
VERDE = (0,255,0)

SCREEN.fill(VERMELHO)

#PONTOS
p1 = [400,300]
p2 = [500,300]
p3 = [450,200]

#pegando o top,mid,bot
pontos = sorted(([p1,p2,p3]), key=lambda p :p[1])
top,mid,bot = pontos[0],pontos[1],pontos[2]

#Interpolar o valor de X
def interpolar_x(y,p1,p2):
    if p1[1] == p2[1]:
        return p1[1]
    return p1[1] + (y- p1[1]) * (p2[0] - p1[0])/(p2[1] - p1[2])

#do top ao mid
for y in range(int(top), int(mid) + 1):
    x1 = (y,top,mid)
    x2 = (y,top,bot)
    pygame.draw.line(SCREEN,VERDE,(int(x1),int(y)),(int(x2),y))

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    pygame.display.flip()
pygame.quit()