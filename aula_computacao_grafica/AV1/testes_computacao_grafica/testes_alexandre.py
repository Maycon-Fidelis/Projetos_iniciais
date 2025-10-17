import pygame

pygame.init()

LARGURA, ALTURA = 800, 600

TELA = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption('Translações')

CLOCK = pygame.time.Clock()

x, y = 400, 300

ANGULO = 0

SPEED = 10

DIMENSION = 5

X_LARGURA, Y_ALTURA = 40, 50

rodando = True
while rodando:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    TELA.fill((255, 255, 255))
    
    CLOCK.tick(60)

    RETANGULO_VERMELHO = pygame.draw.rect(TELA, (0,0,0), (x, y, X_LARGURA, Y_ALTURA))

    pygame.transform.rotate(RETANGULO_VERMELHO, ANGULO)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x -= SPEED
    if keys[pygame.K_d]:
        x += SPEED
    if keys[pygame.K_w]:
        y -= SPEED
    if keys[pygame.K_s]:
        y += SPEED
    if keys[pygame.K_ESCAPE]:
        rodando = False
    if keys[pygame.K_EQUALS]:
        X_LARGURA += DIMENSION
        Y_ALTURA += DIMENSION
    if keys[pygame.K_MINUS]:
        X_LARGURA -= DIMENSION
        Y_ALTURA  -= DIMENSION
    if keys[pygame.K_e]:
        ANGULO +=1
        if ANGULO > 360:
            ANGULO = 0

    pygame.display.update()
pygame.quit()