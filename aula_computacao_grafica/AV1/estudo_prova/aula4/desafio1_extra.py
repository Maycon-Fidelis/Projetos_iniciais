import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Teste")

#Cores
AZUL = (135, 206, 235)
VERMELHO = (255, 0, 0)

#Dados do quadrado
x,y = 350,250
gravidade = 0.1
velocidade_x = 0

clock = pygame.time.Clock()

#Loop para rodar
rodando = True
while rodando:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

            if event.mod == pygame.K_UP:
                gravidade += gravidade
            if event.mod == pygame.K_DOWN:
                gravidade -= gravidade

    velocidade_x += gravidade
    x += velocidade_x
    
    if x + 100 >= 800:
        x = 700
        velocidade_x = 0


    screen.fill(AZUL)
    pygame.draw.rect(screen,VERMELHO,(x,y,100,100))
    pygame.display.flip()

pygame.quit()