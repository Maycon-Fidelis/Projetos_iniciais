import pygame

pygame.init()

#configuração da tela
largura, altura = 1200,600
screnn = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Animação 2D com python")

#cores
azul = (50,150,255)
branco = (255,255,255)

#Posição e velocidade do objeto
x,y = 100, 300
vel_x = 5
vel_y = 0

# "clock" para o controle do FPS
clock = pygame.time.Clock()

rodando = True
while rodando:
    screnn.fill(azul)

    #captura de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    #atualiza posição do círculo
    x += vel_x

    #mantém dentro da tela
    if x > largura - 50 or x < 50:
        vel_x = -vel_x

    #desenho do círculo
    pygame.draw.circle(screnn,branco,(x,y),50)

    pygame.display.flip()
    clock.tick(60) #FPS

pygame.quit()