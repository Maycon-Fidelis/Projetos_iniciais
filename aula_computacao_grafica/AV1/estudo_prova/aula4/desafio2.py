import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Teste")

WHITE = (255,255,255)

# Carregando os sprites
marioParado  = pygame.image.load("mario1.jpeg").convert_alpha()
marioAndando = pygame.image.load("mario2.jpeg").convert_alpha()
x, y = 400, 300

clock = pygame.time.Clock()
direcao = "direita"

# Loop principal
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    clock.tick(60)
    teclas = pygame.key.get_pressed()
    andando = False

    if teclas[pygame.K_LEFT]:
        andando = True
        x -= 5
        direcao = "esquerda"
    elif teclas[pygame.K_RIGHT]:
        andando = True
        x += 5
        direcao = "direita"

    # Atualiza o sprite com base na direção e se está andando
    if direcao == "direita":
        SpriteMario = marioAndando if andando else marioParado
    else:
        SpriteMario = pygame.transform.flip(marioAndando if andando else marioParado, True, False)

    screen.fill(WHITE)
    screen.blit(SpriteMario, (x, y))
    pygame.display.flip()

pygame.quit()
