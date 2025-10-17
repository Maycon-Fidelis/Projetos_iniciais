import pygame  # Importa a biblioteca Pygame para criar aplicações gráficas
import colorsys  # Importa a biblioteca colorsys para conversão de cores (RGB para HSV e vice-versa)

# Inicializa o Pygame
pygame.init()

# Configuração da tela
LARGURA, ALTURA = 800, 600  # Define a largura e altura da tela
TELA = pygame.display.set_mode((LARGURA, ALTURA))  # Cria a janela do programa
pygame.display.set_caption("Modelos de Cores")  # Define o título da janela

# Cores iniciais
cor_rgb = (255, 0, 0)  # Define a cor inicial como vermelho (RGB)
modo_cor = "RGB"  # Define o modo de cor inicial como RGB


def rgb_para_cmy(rgb):
    """Converte uma cor de RGB para CMY"""
    r, g, b = rgb  # Extrai os componentes R, G, B
    return (255 - r, 255 - g, 255 - b)  # Retorna a cor em CMY


def rgb_para_hsv(rgb):
    """Converte uma cor de RGB para HSV"""
    r, g, b = rgb  # Extrai os componentes R, G, B
    # Converte RGB para HSV (usa valores normalizados entre 0 e 1)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return (int(h * 360), int(s * 100), int(v * 100))  # Retorna HSV em escalas de 0-360, 0-100, 0-100


def hsv_para_rgb(h, s, v):
    """Converte uma cor de HSV para RGB"""
    # Converte HSV para RGB (usa valores normalizados)
    r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
    return (int(r * 255), int(g * 255), int(b * 255))  # Retorna RGB em escalas de 0-255


def desenha_interface():
    """Desenha a interface gráfica do programa"""
    TELA.fill((30, 30, 30))  # Preenche a tela com uma cor de fundo escura

    # Exibe um retângulo com a cor atual
    pygame.draw.rect(TELA, cor_rgb, (250, 150, 300, 300))

    # Texto informativo
    fonte = pygame.font.Font(None, 36)  # Define a fonte para exibir texto
    texto_modo = fonte.render(f"Modo: {modo_cor}", True, (255, 255, 255))  # Renderiza o texto do modo de cor
    TELA.blit(texto_modo, (50, 50))  # Exibe o texto na tela

    # Exibe as informações de cor de acordo com o modo atual
    if modo_cor == "RGB":
        texto_rgb = fonte.render(f"RGB: {cor_rgb}", True, (255, 255, 255))  # Renderiza o texto RGB
        TELA.blit(texto_rgb, (50, 500))  # Exibe o texto na tela

    elif modo_cor == "CMY":
        cor_cmy = rgb_para_cmy(cor_rgb)  # Converte a cor atual para CMY
        texto_cmy = fonte.render(f"CMY: {cor_cmy}", True, (255, 255, 255))  # Renderiza o texto CMY
        TELA.blit(texto_cmy, (50, 500))  # Exibe o texto na tela

    elif modo_cor == "HSV":
        cor_hsv = rgb_para_hsv(cor_rgb)  # Converte a cor atual para HSV
        texto_hsv = fonte.render(f"HSV: {cor_hsv}", True, (255, 255, 255))  # Renderiza o texto HSV
        TELA.blit(texto_hsv, (50, 500))  # Exibe o texto na tela

    pygame.display.flip()  # Atualiza a tela para mostrar as mudanças


def main():
    global cor_rgb, modo_cor  # Permite modificar as variáveis globais
    rodando = True  # Variável para controlar o loop principal

    while rodando:
        for evento in pygame.event.get():  # Verifica os eventos do Pygame
            if evento.type == pygame.QUIT:  # Se o usuário fechar a janela
                rodando = False  # Encerra o loop principal
            elif evento.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                if evento.key == pygame.K_r:
                    cor_rgb = (255, 0, 0)  # Define a cor como vermelho (RGB)
                elif evento.key == pygame.K_g:
                    cor_rgb = (0, 255, 0)  # Define a cor como verde (RGB)
                elif evento.key == pygame.K_b:
                    cor_rgb = (0, 0, 255)  # Define a cor como azul (RGB)
                elif evento.key == pygame.K_c:
                    modo_cor = "CMY"  # Altera o modo de cor para CMY
                elif evento.key == pygame.K_h:
                    modo_cor = "HSV"  # Altera o modo de cor para HSV
                elif evento.key == pygame.K_m:
                    modo_cor = "RGB"  # Altera o modo de cor para RGB

        desenha_interface()  # Desenha a interface gráfica

    pygame.quit()  # Encerra o Pygame


if __name__ == "__main__":
    main()  # Executa a função principal