import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste")

AZUL = (135, 206, 235)

# MAPA
mapa = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Sprites
marioParado = pygame.image.load("mario.jpeg").convert_alpha()
marioAndando = pygame.image.load("mario_run.jpeg").convert_alpha()
marioPulando = pygame.image.load("mario_jump.jpeg").convert_alpha()
spriteMario = marioParado

# Escala dos blocos
TAMANHO = 40
bloco = pygame.image.load("bloco.png").convert_alpha()
imgBloco = pygame.transform.scale(bloco, (TAMANHO, TAMANHO))

# Player
mario_x = 100
mario_y = 520
velocidade = 5
pulando = False
gravidade = 0
forca_pulo = -15

clock = pygame.time.Clock()
rodando = True

while rodando:
    clock.tick(60)
    screen.fill(AZUL)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Controles
    teclas = pygame.key.get_pressed()
    
    if teclas[pygame.K_LEFT]:
        mario_x -= velocidade
        spriteMario = marioAndando
    elif teclas[pygame.K_RIGHT]:
        mario_x += velocidade
        spriteMario = marioAndando
    else:
        spriteMario = marioParado

    if teclas[pygame.K_SPACE] and not pulando:
        pulando = True
        gravidade = forca_pulo

    # Física do pulo
    if pulando:
        mario_y += gravidade
        gravidade += 1
        spriteMario = marioPulando

        if mario_y >= 520:  # chão
            mario_y = 520
            pulando = False

    # Desenhar o mapa
    for linha_idx, linha in enumerate(mapa):
        for col_idx, bloco in enumerate(linha):
            if bloco == 1:
                screen.blit(imgBloco, (col_idx * TAMANHO, linha_idx * TAMANHO))

    # Desenhar personagem
    screen.blit(spriteMario, (mario_x, mario_y))

    pygame.display.update()

pygame.quit()
