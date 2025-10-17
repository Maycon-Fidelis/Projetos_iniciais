import pygame
print(pygame.version)

pygame.init()

largura, altura = 800,600   
screen = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Cena simples')

#Definindo cores
azul=(135,206,235)
amarelo=(255,255,0)
verde=(34,139,34)
marrom=(139,69,19)
vermelho=(255,0,0)

screen.fill(azul)

pygame.draw.circle(screen,amarelo,(650,100),50)
pygame.draw.rect(screen,marrom,pygame.Rect(300,350,180,180))
pygame.draw.rect(screen,marrom,pygame.Rect(80,350,40,180))
pygame.draw.circle(screen,verde,(100,350), 50,100)
pygame.draw.polygon(screen, vermelho, [[300,350], [480, 350], [400, 250]])

desenhando = True

while desenhando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           desenhando = False
    pygame.display.flip()

pygame.quit()