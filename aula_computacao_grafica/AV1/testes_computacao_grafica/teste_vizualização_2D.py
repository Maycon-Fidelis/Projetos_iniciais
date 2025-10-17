import pygame  # Importa a biblioteca Pygame para criar jogos e aplicações gráficas

pygame.init()  # Inicializa todos os módulos do Pygame

# Define as dimensões da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))  # Cria uma janela com as dimensões especificadas
pygame.display.set_caption("Transformações 2D")  # Define o título da janela

# Posição inicial do objeto (um retângulo)
x, y = 200, 200
velocidade = 5  # Velocidade de movimentação do objeto

rodando = True  # Variável para controlar o loop principal do jogo
while rodando:
    TELA.fill((0, 0, 0))  # Preenche a tela com a cor preta (RGB: 0, 0, 0)

    # Verifica os eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Se o usuário clicar no botão de fechar a janela
            rodando = False  # Encerra o loop principal

    # Captura as teclas pressionadas para movimentar o objeto (translação)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  # Se a seta para a esquerda for pressionada
        x -= velocidade  # Move o objeto para a esquerda
    if keys[pygame.K_RIGHT]:  # Se a seta para a direita for pressionada
        x += velocidade  # Move o objeto para a direita
    if keys[pygame.K_UP]:  # Se a seta para cima for pressionada
        y -= velocidade  # Move o objeto para cima
    if keys[pygame.K_DOWN]:  # Se a seta para baixo for pressionada
        y += velocidade  # Move o objeto para baixo

    # Desenha um retângulo na tela na posição (x, y) com largura e altura de 50 pixels
    pygame.draw.rect(TELA, (255, 255, 255), (x, y, 50, 50))

    pygame.display.flip()  # Atualiza a tela para mostrar as mudanças

pygame.quit()  # Encerra o Pygame e fecha a janela