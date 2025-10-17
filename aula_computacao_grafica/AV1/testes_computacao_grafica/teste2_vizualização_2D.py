import pygame  # Importa a biblioteca Pygame para criar aplicações gráficas
import random  # Importa a biblioteca random para gerar números aleatórios

# Definições iniciais
LARGURA, ALTURA = 800, 600  # Dimensões da tela
PRETO = (0, 0, 0)  # Cor preta em RGB
BRANCO = (255, 255, 255)  # Cor branca em RGB
VERMELHO = (255, 0, 0)  # Cor vermelha em RGB

# Definição da região de recorte (window)
X_MIN, Y_MIN = 200, 150  # Canto superior esquerdo da região de recorte
X_MAX, Y_MAX = 600, 450  # Canto inferior direito da região de recorte

# Códigos de região para o algoritmo de Cohen-Sutherland
INSIDE = 0  # 0000: ponto dentro da região
ESQUERDA = 1  # 0001: ponto à esquerda da região
DIREITA = 2  # 0010: ponto à direita da região
ABAIXO = 4  # 0100: ponto abaixo da região
ACIMA = 8  # 1000: ponto acima da região

# Inicializa o Pygame
pygame.init()
TELA = pygame.display.set_mode((LARGURA, ALTURA))  # Cria a janela do jogo
pygame.display.set_caption("Recorte de Linhas - Cohen-Sutherland")  # Define o título da janela


def get_code(x, y):
    """Retorna o código de região para um ponto (x, y)"""
    code = INSIDE  # Inicializa o código como INSIDE (dentro da região)
    if x < X_MIN:  # Se o ponto estiver à esquerda da região
        code |= ESQUERDA
    elif x > X_MAX:  # Se o ponto estiver à direita da região
        code |= DIREITA
    if y < Y_MIN:  # Se o ponto estiver acima da região
        code |= ACIMA
    elif y > Y_MAX:  # Se o ponto estiver abaixo da região
        code |= ABAIXO
    return code  # Retorna o código calculado


def cohen_sutherland(x1, y1, x2, y2):
    """Aplica o algoritmo de recorte de linha Cohen-Sutherland"""
    code1 = get_code(x1, y1)  # Código de região para o primeiro ponto
    code2 = get_code(x2, y2)  # Código de região para o segundo ponto
    aceita = False  # Flag para indicar se a linha deve ser desenhada

    while True:
        if code1 == 0 and code2 == 0:
            # Ambos os pontos estão dentro da região
            aceita = True
            break
        elif (code1 & code2) != 0:
            # Ambos os pontos estão fora e na mesma região (não há interseção)
            break
        else:
            # A linha precisa ser cortada
            x, y = 0, 0  # Ponto de interseção
            code_out = code1 if code1 != 0 else code2  # Escolhe o ponto fora da região

            # Calcula o ponto de interseção com base no código de região
            if code_out & ACIMA:
                x = x1 + (x2 - x1) * (Y_MIN - y1) / (y2 - y1)
                y = Y_MIN
            elif code_out & ABAIXO:
                x = x1 + (x2 - x1) * (Y_MAX - y1) / (y2 - y1)
                y = Y_MAX
            elif code_out & DIREITA:
                y = y1 + (y2 - y1) * (X_MAX - x1) / (x2 - x1)
                x = X_MAX
            elif code_out & ESQUERDA:
                y = y1 + (y2 - y1) * (X_MIN - x1) / (x2 - x1)
                x = X_MIN

            # Atualiza o ponto fora da região com o ponto de interseção
            if code_out == code1:
                x1, y1 = x, y
                code1 = get_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = get_code(x2, y2)

    if aceita:
        # Retorna as coordenadas recortadas da linha
        return int(x1), int(y1), int(x2), int(y2)
    else:
        # Retorna None se a linha estiver completamente fora da região
        return None


def desenha_linhas():
    """Desenha linhas aleatórias e aplica o recorte"""
    for _ in range(10):  # Desenha 10 linhas aleatórias
        x1, y1 = random.randint(0, LARGURA), random.randint(0, ALTURA)  # Ponto inicial
        x2, y2 = random.randint(0, LARGURA), random.randint(0, ALTURA)  # Ponto final

        # Desenha a linha original em vermelho
        pygame.draw.line(TELA, VERMELHO, (x1, y1), (x2, y2), 2)

        # Aplica o algoritmo de recorte
        linha_recortada = cohen_sutherland(x1, y1, x2, y2)

        if linha_recortada:
            # Desenha apenas a parte visível da linha em branco
            pygame.draw.line(TELA, BRANCO, (linha_recortada[0], linha_recortada[1]),
                             (linha_recortada[2], linha_recortada[3]), 3)


def main():
    rodando = True
    while rodando:
        TELA.fill(PRETO)  # Preenche a tela com a cor preta

        # Desenha a janela de recorte
        pygame.draw.rect(TELA, BRANCO, (X_MIN, Y_MIN, X_MAX - X_MIN, Y_MAX - Y_MIN), 2)

        # Desenha as linhas e aplica recorte
        desenha_linhas()

        # Verifica eventos do Pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Se o usuário fechar a janela
                rodando = False  # Encerra o loop principal

        pygame.display.flip()  # Atualiza a tela
        pygame.time.delay(500)  # Pequeno delay para atualização das linhas

    pygame.quit()  # Encerra o Pygame


if __name__ == "__main__":
    main()  # Executa a função principal