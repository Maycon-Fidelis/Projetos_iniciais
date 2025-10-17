import pygame
import random
import math
from pygame import gfxdraw

# Inicialização do Pygame
pygame.init()

# Configurações da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mapa Térmico 3D com Z-buffer (sem NumPy)")

# Cores para as camadas térmicas (vermelho, laranja, amarelo, azul claro, azul escuro)
COLORS = [
    (255, 0, 0, 180),    # Vermelho - mais quente
    (255, 165, 0, 160),  # Laranja
    (255, 255, 0, 140),  # Amarelo
    (0, 191, 255, 120),  # Azul claro
    (0, 0, 139, 100)     # Azul escuro - mais frio
]

# Classe para representar uma camada térmica
class ThermalLayer:
    def __init__(self, z_depth):
        self.z_depth = z_depth  # Profundidade da camada (valores menores são mais próximos)
        self.points = []
        self.color = random.choice(COLORS)
        self.generate_shape()
        
    def generate_shape(self):
        # Gera um polígono convexo irregular
        num_points = random.randint(5, 10)
        center_x = random.randint(100, WIDTH - 100)
        center_y = random.randint(100, HEIGHT - 100)
        radius = random.randint(50, 150)
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            # Varia o raio para criar formas irregulares
            var_radius = radius * (0.7 + 0.6 * random.random())
            x = center_x + var_radius * math.cos(angle)
            y = center_y + var_radius * math.sin(angle)
            self.points.append((x, y))
    
    def draw(self, surface, z_buffer):
        # Ordena os pontos em sentido horário para desenho correto
        center = (sum(p[0] for p in self.points)/len(self.points), 
                 sum(p[1] for p in self.points)/len(self.points))
        self.points.sort(key=lambda p: -math.atan2(p[1]-center[1], p[0]-center[0]))
        
        # Cria uma superfície temporária para desenhar o polígono
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(temp_surface, self.color, self.points)
        
        # Encontra os limites do polígono para otimização
        min_x = max(0, min(p[0] for p in self.points) - 1)
        max_x = min(WIDTH, max(p[0] for p in self.points) + 1)
        min_y = max(0, min(p[1] for p in self.points) - 1)
        max_y = min(HEIGHT, max(p[1] for p in self.points) + 1)
        
        # Atualiza o z-buffer apenas onde o polígono está mais próximo
        for x in range(int(min_x), int(max_x)):
            for y in range(int(min_y), int(max_y)):
                # Verifica se o ponto (x,y) está dentro do polígono
                if self.point_in_polygon((x, y)):
                    if z_buffer[y][x] > self.z_depth:
                        z_buffer[y][x] = self.z_depth
                        # Desenha o pixel na superfície principal
                        surface.set_at((x, y), self.color)
        
    def point_in_polygon(self, point):
        # Algoritmo ray casting para verificar se o ponto está dentro do polígono
        x, y = point
        inside = False
        n = len(self.points)
        p1x, p1y = self.points[0]
        for i in range(n + 1):
            p2x, p2y = self.points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

# Função para criar um Z-buffer sem usar NumPy
def create_z_buffer(width, height, initial_value=float('inf')):
    return [[initial_value for _ in range(width)] for _ in range(height)]

# Função principal
def main():
    clock = pygame.time.Clock()
    running = True
    
    # Cria 5 camadas térmicas com profundidades aleatórias
    layers = [ThermalLayer(random.uniform(0.1, 0.9)) for _ in range(5)]
    # Ordena as camadas pela profundidade (mais próximo primeiro)
    layers.sort(key=lambda layer: layer.z_depth)
    
    # Inicializa o Z-buffer sem NumPy
    z_buffer = create_z_buffer(WIDTH, HEIGHT)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Recria as camadas térmicas quando 'R' é pressionado
                    layers = [ThermalLayer(random.uniform(0.1, 0.9)) for _ in range(5)]
                    layers.sort(key=lambda layer: layer.z_depth)
                    z_buffer = create_z_buffer(WIDTH, HEIGHT)
        
        # Preenche a tela com preto
        screen.fill((0, 0, 0))
        
        # Redesenha todas as camadas (mais distantes primeiro)
        for layer in reversed(layers):
            layer.draw(screen, z_buffer)
        
        # Reseta o Z-buffer para a próxima frame
        z_buffer = create_z_buffer(WIDTH, HEIGHT)
        
        # Exibe instruções
        font = pygame.font.SysFont('Arial', 16)
        text = font.render("Pressione 'R' para gerar novo mapa térmico", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()