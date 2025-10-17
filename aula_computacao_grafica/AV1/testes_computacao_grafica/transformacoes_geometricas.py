import pygame  # Biblioteca para criar gráficos 2D e jogos
import math  # Biblioteca para operações matemáticas

# Inicializa o pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600  # Define o tamanho da janela
screen = pygame.display.set_mode((largura, altura))  # Cria a tela com as dimensões definidas
pygame.display.set_caption("Transformações Geométricas 2D")  # Define o título da janela

# Definição de cores no formato RGB
tela_azul = (135, 206, 235)  # Azul claro para o fundo
branco = (255, 255, 255)  # Branco para um dos retângulos
vermelho = (255, 0, 0)  # Vermelho para o retângulo original
verde = (0, 255, 0)  # Verde para o retângulo transladado
azul = (0, 0, 255)  # Azul para o retângulo rotacionado

# Função para aplicar translação
# Move todos os pontos de um objeto na direção (tx, ty)
def transladar(pontos, tx, ty):
    return [(x + tx, y + ty) for x, y in pontos]  # Soma tx a x e ty a y

# Função para aplicar rotação
# Gira todos os pontos do objeto em torno de um ponto de origem
# O ângulo deve ser dado em graus
def rotacionar(pontos, angulo, origem=(0, 0)):
    angulo_rad = math.radians(angulo)  # Converte o ângulo de graus para radianos
    cos_a = math.cos(angulo_rad)  # Calcula o cosseno do ângulo
    sin_a = math.sin(angulo_rad)  # Calcula o seno do ângulo
    ox, oy = origem  # Define o ponto de origem da rotação
    return [
        ((x - ox) * cos_a - (y - oy) * sin_a + ox,  # Cálculo da nova coordenada X
         (x - ox) * sin_a + (y - oy) * cos_a + oy)  # Cálculo da nova coordenada Y
        for x, y in pontos
    ]

# Função para aplicar escala
# Aumenta ou diminui o tamanho do objeto em relação a um ponto de origem
def escalar(pontos, sx, sy, origem=(0, 0)):
    ox, oy = origem  # Define o ponto de origem da escala
    return [
        ((x - ox) * sx + ox,  # Multiplica a distância de x para ox por sx
         (y - oy) * sy + oy)  # Multiplica a distância de y para oy por sy
        for x, y in pontos
    ]

# Loop principal da aplicação
desenhando = True  # Variável de controle do loop
while desenhando:
    screen.fill(tela_azul)  # Preenche o fundo da tela com azul
    
    # Definição de um retângulo base como uma lista de pontos (x, y)
    retangulo = [(300, 300), (400, 300), (400, 400), (300, 400)]
    
    # Aplicar transformações geométricas
    retangulo_transladado = transladar(retangulo, 100, 50)  # Move o retângulo 100px para a direita e 50px para baixo
    retangulo_rotacionado = rotacionar(retangulo, 45, origem=(350, 350))  # Rotaciona 45° em torno do centro do retângulo
    retangulo_escalado = escalar(retangulo, 1.5, 1.5, origem=(350, 350))  # Aumenta 50% em relação ao centro
    
    # Desenhar os retângulos na tela
    pygame.draw.polygon(screen, vermelho, retangulo, 2)  # Retângulo original em vermelho
    pygame.draw.polygon(screen, verde, retangulo_transladado, 2)  # Retângulo transladado em verde
    pygame.draw.polygon(screen, azul, retangulo_rotacionado, 2)  # Retângulo rotacionado em azul
    pygame.draw.polygon(screen, branco, retangulo_escalado, 2)  # Retângulo escalado em branco
    
    # Captura eventos do pygame, como fechar a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Se o usuário fechar a janela
            desenhando = False  # Sai do loop principal
    
    pygame.display.flip()  # Atualiza a tela para mostrar os desenhos

# Encerra o pygame quando o loop termina
pygame.quit()
