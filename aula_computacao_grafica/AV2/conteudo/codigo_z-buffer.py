import pygame
import math
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Demonstração de Preenchimento de Polígonos e Z-buffer")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
CIANO = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Lista de cores para polígonos
CORES = [VERMELHO, VERDE, AZUL, AMARELO, CIANO, MAGENTA]

# Classe para representar um polígono 3D
class Poligono3D:
    def __init__(self, vertices, cor, profundidade):
        self.vertices = vertices  # Lista de vértices (x, y)
        self.cor = cor
        self.profundidade = profundidade  # Valor Z (quanto maior, mais distante)
   
    def desenhar(self, superficie):
        # Desenha o contorno do polígono
        pygame.draw.polygon(superficie, self.cor, self.vertices)
       
        # Desenha uma pequena legenda com o valor Z
        fonte = pygame.font.SysFont('Arial', 16)
        texto = fonte.render(f"Z={self.profundidade}", True, PRETO)
        centro_x = sum(v[0] for v in self.vertices) / len(self.vertices)
        centro_y = sum(v[1] for v in self.vertices) / len(self.vertices)
        superficie.blit(texto, (centro_x - texto.get_width() // 2, centro_y - texto.get_height() // 2))

# Implementação simplificada do Z-buffer
class ZBuffer:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.buffer = [[float('inf') for _ in range(largura)] for _ in range(altura)]
        self.cor_buffer = [[PRETO for _ in range(largura)] for _ in range(altura)]
   
    def limpar(self):
        for y in range(self.altura):
            for x in range(self.largura):
                self.buffer[y][x] = float('inf')
                self.cor_buffer[y][x] = PRETO
   
    def renderizar_poligono(self, poligono):
        # Determina a caixa delimitadora do polígono
        min_x = max(0, min(v[0] for v in poligono.vertices))
        max_x = min(self.largura - 1, max(v[0] for v in poligono.vertices))
        min_y = max(0, min(v[1] for v in poligono.vertices))
        max_y = min(self.altura - 1, max(v[1] for v in poligono.vertices))
       
        # Converte para inteiros
        min_x, max_x = int(min_x), int(max_x)
        min_y, max_y = int(min_y), int(max_y)
       
        # Para cada pixel na caixa delimitadora
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                # Verifica se o ponto está dentro do polígono
                if self.ponto_dentro_poligono((x, y), poligono.vertices):
                    # Aplica o teste de profundidade (Z-buffer)
                    if poligono.profundidade < self.buffer[y][x]:
                        self.buffer[y][x] = poligono.profundidade
                        self.cor_buffer[y][x] = poligono.cor
   
    def ponto_dentro_poligono(self, ponto, vertices):
        """Verifica se um ponto está dentro de um polígono usando o algoritmo de Ray Casting"""
        x, y = ponto
        dentro = False
        j = len(vertices) - 1
       
        for i in range(len(vertices)):
            if ((vertices[i][1] > y) != (vertices[j][1] > y)) and \
               (x < vertices[i][0] + (vertices[j][0] - vertices[i][0]) * (y - vertices[i][1]) /
                (vertices[j][1] - vertices[i][1])):
                dentro = not dentro
            j = i
       
        return dentro
   
    def desenhar(self, superficie):
        # Desenha o buffer de cores na superfície
        for y in range(self.altura):
            for x in range(self.largura):
                if self.buffer[y][x] != float('inf'):
                    superficie.set_at((x, y), self.cor_buffer[y][x])

# Função para criar polígonos aleatórios
def criar_poligono_aleatorio():
    num_vertices = random.randint(3, 6)
    raio = random.randint(30, 80)
    angulo_inicial = random.uniform(0, 2 * math.pi)
   
    centro_x = random.randint(100, LARGURA - 100)
    centro_y = random.randint(100, ALTURA - 100)
    profundidade = random.randint(1, 10)
   
    vertices = []
    for i in range(num_vertices):
        angulo = angulo_inicial + (2 * math.pi * i / num_vertices)
        x = centro_x + raio * math.cos(angulo)
        y = centro_y + raio * math.sin(angulo)
        vertices.append((x, y))
   
    cor = random.choice(CORES)
    return Poligono3D(vertices, cor, profundidade)

# Implementação simples do algoritmo Scanline Fill
def scanline_fill(poligono, superficie, cor):
    vertices = poligono.vertices
   
    # Encontra os limites y
    min_y = int(min(v[1] for v in vertices))
    max_y = int(max(v[1] for v in vertices))
   
    # Para cada scanline (linha horizontal)
    for y in range(min_y, max_y + 1):
        intersecoes = []
       
        # Encontra todas as interseções com essa scanline
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
           
            if (y1 <= y < y2) or (y2 <= y < y1):  # A linha intersecta a aresta
                if y1 == y2:  # Evita divisão por zero
                    continue
               
                # Calcula o ponto de interseção
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersecoes.append(x)
       
        # Ordena as interseções
        intersecoes.sort()
       
        # Desenha entre pares de interseções
        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                pygame.draw.line(superficie, cor,
                                (int(intersecoes[i]), y),
                                (int(intersecoes[i+1]), y))

# Função principal
def main():
    relogio = pygame.time.Clock()
   
    # Criamos nosso Z-buffer
    zbuffer = ZBuffer(LARGURA, ALTURA)
   
    # Lista de polígonos
    poligonos = []
   
    # Modos de visualização
    modo_atual = 0  # 0: Z-buffer, 1: Ordem de desenho, 2: Demonstração Scanline
    poligono_scanline = None
   
    # Texto explicativo
    fonte = pygame.font.SysFont('Arial', 18)
   
    # Texto de ajuda
    texto_ajuda = [
        "Teclas:",
        "ESPAÇO - Adicionar polígono",
        "DELETE - Remover todos",
        "M - Mudar modo de visualização",
        "ESC - Sair"
    ]
   
    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
           
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False
               
                elif evento.key == pygame.K_SPACE:
                    # Adicionar novo polígono
                    poligonos.append(criar_poligono_aleatorio())
                    # Se estamos no modo Scanline, usar o último polígono adicionado
                    if modo_atual == 2:
                        poligono_scanline = poligonos[-1]
               
                elif evento.key == pygame.K_DELETE:
                    # Remover todos os polígonos
                    poligonos.clear()
                    poligono_scanline = None
               
                elif evento.key == pygame.K_m:
                    # Alternar entre modos
                    modo_atual = (modo_atual + 1) % 3
                    if modo_atual == 2 and poligonos:
                        poligono_scanline = poligonos[-1]
       
        # Limpar a tela
        tela.fill(BRANCO)
       
        # Desenhar de acordo com o modo atual
        if modo_atual == 0:  # Z-buffer
            zbuffer.limpar()
            for p in poligonos:
                zbuffer.renderizar_poligono(p)
            zbuffer.desenhar(tela)
           
            modo_texto = "Modo: Z-buffer (profundidade)"
       
        elif modo_atual == 1:  # Ordem de desenho (sem Z-buffer)
            # Ordenamos os polígonos por profundidade (do mais distante para o mais próximo)
            poligonos_ordenados = sorted(poligonos, key=lambda p: p.profundidade, reverse=True)
            for p in poligonos_ordenados:
                p.desenhar(tela)
           
            modo_texto = "Modo: Ordem de desenho (sem Z-buffer)"
       
        elif modo_atual == 2:  # Demonstração Scanline
            # Desenha todos os polígonos como contornos
            for p in poligonos:
                pygame.draw.polygon(tela, p.cor, p.vertices, 2)  # Desenha apenas o contorno
           
            # Se houver um polígono selecionado para demonstração do Scanline
            if poligono_scanline:
                scanline_fill(poligono_scanline, tela, poligono_scanline.cor)
           
            modo_texto = "Modo: Demonstração Scanline"
       
        # Desenhar texto de modo
        texto_modo = fonte.render(modo_texto, True, PRETO)
        tela.blit(texto_modo, (10, 10))
       
        # Desenhar texto de ajuda
        for i, linha in enumerate(texto_ajuda):
            texto = fonte.render(linha, True, PRETO)
            tela.blit(texto, (10, 40 + i * 25))
       
        # Desenhar contador de polígonos
        texto_contador = fonte.render(f"Polígonos: {len(poligonos)}", True, PRETO)
        tela.blit(texto_contador, (LARGURA - texto_contador.get_width() - 10, 10))
       
        # Atualizar a tela
        pygame.display.flip()
        relogio.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()