import pygame

pygame.init()

# Configurações da tela
largura, altura = 800, 600
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Cena Simples")

# Definir cores
AZUL = (135, 206, 235)
AMARELO = (255, 255, 0)
VERDE = (34, 139, 34)
MARROM = (139, 69, 19)
VERMELHO = (255, 0, 0)

# Preencher fundo com céu azul
screen.fill(AZUL)

# Desenhar o sol
pygame.draw.circle(screen, AMARELO, (700, 100), 50)

# Desenhar a casa
pygame.draw.rect(screen, MARROM, (300, 300, 200, 150))
pygame.draw.polygon(screen, VERMELHO, [(275, 300), (525, 300), (400, 200)])

# Desenhar árvore
pygame.draw.rect(screen, MARROM, (100, 350, 30, 100))
pygame.draw.circle(screen, VERDE, (115, 330), 50)

# Atualizar a tela
pygame.display.flip()

# Manter a janela aberta
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

pygame.quit()