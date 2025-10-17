import pygame, random 

LARGURA, ALTURA = 800, 600 
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255) 
VERMELHO = (255, 0, 0) 

X_MIN, Y_MIN = 200, 150 
X_MAX, Y_MAX = 600, 450 

INSIDE = 0 
ESQUERDA = 1
DIREITA = 2  
ABAIXO = 4 
ACIMA = 8 

pygame.init()
TELA = pygame.display.set_mode((LARGURA, ALTURA)) 
pygame.display.set_caption("Questão 5 prova")


def get_code(x, y):
    """Retorna o código de região para um ponto (x, y)"""
    code = INSIDE  
    if x < X_MIN:  
        code |= ESQUERDA
    elif x > X_MAX:
        code |= DIREITA
    if y < Y_MIN:  
        code |= ACIMA
    elif y > Y_MAX:
        code |= ABAIXO
    return code  

def cohen_sutherland(x1, y1, x2, y2):
    """Aplica o algoritmo de recorte de linha Cohen-Sutherland"""
    code1 = get_code(x1, y1)
    code2 = get_code(x2, y2)  
    aceita = False

    while True:
        if code1 == 0 and code2 == 0:
            aceita = True
            break
        elif (code1 & code2) != 0:
            break
        else:
            x, y = 0, 0 
            code_out = code1 if code1 != 0 else code2

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

            if code_out == code1:
                x1, y1 = x, y
                code1 = get_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = get_code(x2, y2)

    if aceita:
        return int(x1), int(y1), int(x2), int(y2)
    else:
        return None


def desenha_linhas():
    """Desenha linhas aleatórias e aplica o recorte"""
    for _ in range(10):
        x1, y1 = random.randint(0, LARGURA), random.randint(0, ALTURA)
        x2, y2 = random.randint(0, LARGURA), random.randint(0, ALTURA)

        pygame.draw.line(TELA, VERMELHO, (x1, y1), (x2, y2), 2)

        linha_recortada = cohen_sutherland(x1, y1, x2, y2)

        if linha_recortada:
            pygame.draw.line(TELA, BRANCO, (linha_recortada[0], linha_recortada[1]),
                             (linha_recortada[2], linha_recortada[3]), 3)


def main():
    rodando = True
    while rodando:
        TELA.fill(PRETO)  
        pygame.draw.rect(TELA, BRANCO, (X_MIN, Y_MIN, X_MAX - X_MIN, Y_MAX - Y_MIN), 2)

        desenha_linhas()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        pygame.display.flip()
        pygame.time.delay(500)

    pygame.quit()


if __name__ == "__main__":
    main()