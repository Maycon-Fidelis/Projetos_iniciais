import pygame

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Teste")

#Cores
AZUL = (135, 206, 235)
VERMELHO = (255, 0, 0)

clock = pygame.time.Clock()

#Dados da bola
x,y = 400, 300
raio = 100
gravidade = 0.5
velocidade_y = 0

#Loop do código rodando
rodando = True
while rodando:
    clock.tick(60) #Rodando em 60 frames
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    velocidade_y += gravidade
    y += velocidade_y

    if y + raio > 550:
        y = 550 - raio
        velocidade_y = 0
    
    screen.fill(AZUL)
    pygame.draw.circle(screen,VERMELHO,(x,y),raio)
    pygame.display.flip()

pygame.quit()