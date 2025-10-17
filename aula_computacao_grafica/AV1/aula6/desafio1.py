import pygame

pygame.init()

LARGURA, ALTURA = 800,600
TELA = pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption("Transformação 2D - aplicando")

x,y = 200,200
velocidade = 0.5
ALTURA_BLOCO, LARGURA_BLOCO = 50,50
angulo = 0

rodando = True
while rodando:
    TELA.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= velocidade
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += velocidade
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= velocidade
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += velocidade

    if keys[pygame.K_KP_PLUS]:
        ALTURA_BLOCO += 1
        LARGURA_BLOCO += 1
    if keys[pygame.K_KP_MINUS]:
        ALTURA_BLOCO -= 1
        LARGURA_BLOCO -= 1

    if keys[pygame.K_q]:
        angulo += 0.1
    if keys[pygame.K_e]:
        angulo -= 0.1
    if keys[pygame.K_r]:
        angulo = 0
        ALTURA_BLOCO, LARGURA_BLOCO = 50,50
        x,y = 200,200

    bloco = pygame.Surface((LARGURA_BLOCO, ALTURA_BLOCO), pygame.SRCALPHA)
    bloco.fill((255, 255, 255))

    image_rotacionar = pygame.transform.rotate(bloco, angulo)
    image_rot = image_rotacionar.get_rect(center=(x + LARGURA_BLOCO // 2, y + ALTURA_BLOCO // 2))
        
    TELA.blit(image_rotacionar,image_rot.topleft)

    pygame.display.flip()

pygame.quit()