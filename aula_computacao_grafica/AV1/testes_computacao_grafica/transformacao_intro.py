import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Translação de Quadrado por Clique com Pygame")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Função para aplicar uma translação a um ponto
def transladar_ponto(ponto, tx, ty):
    x, y = ponto
    return (x + tx, y + ty)

# Função para aplicar uma translação a uma lista de pontos
def transladar_objeto(objeto, tx, ty):
    return [transladar_ponto(ponto, tx, ty) for ponto in objeto]

# Define o quadrado como uma lista de vértices (pontos)
quadrado = [
    (50, 50),  # Vértice superior esquerdo
    (150, 50),  # Vértice superior direito
    (150, 150),  # Vértice inferior direito
    (50, 150)   # Vértice inferior esquerdo
]

# Parâmetros da translação inicial
tx, ty = 0, 0  # Inicialmente sem translação

# Função principal
def main():
    global tx, ty, quadrado  # Permite modificar tx, ty e quadrado dentro da função

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Detecta clique do mouse
                if event.button == 1:  # Botão esquerdo do mouse
                    # Aumenta a translação em 20 unidades no eixo X e 20 no eixo Y
                    tx += 20
                    ty += 20
                    # Aplica a translação ao quadrado
                    quadrado = transladar_objeto(quadrado, 20, 20)

        # Limpa a tela
        screen.fill(WHITE)

        # Desenha o quadrado transladado
        pygame.draw.polygon(screen, RED, quadrado, 2)

        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()

# Executa o programa
if __name__ == "__main__":
    main()    