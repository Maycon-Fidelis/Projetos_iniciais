import pygame
print(pygame.version)

pygame.init()

largura, altura = 2000,1000   
screen = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Cena simples')

#Definindo cores
azul=(135,206,235)
amarelo=(255,255,0)
verde=(34,139,34)
marrom=(139,69,19)
vermelho=(255,0,0)

screen.fill(azul)

desenhando = True

while desenhando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           desenhando = False
    pygame.display.flip()

pygame.quit()