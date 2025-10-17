import pygame
import sys
import random
import numpy as np
from pygame import gfxdraw

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador de Camadas Geológicas")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

TERRAIN_TYPES = {
    "Argila": (194, 178, 128),
    "Rocha": (136, 140, 141),
    "Areia": (237, 201, 175),
    "Cascalho": (179, 158, 181),
    "Silte": (209, 206, 190),
    "Calcário": (220, 215, 210),
    "Basalto": (78, 84, 94),
    "Granito": (167, 162, 162)
}

font = pygame.font.SysFont('Arial', 14)
title_font = pygame.font.SysFont('Arial', 18, bold=True)

class GeologicalLayer:
    def __init__(self, name, points, elevation, color, terrain_type):
        self.name = name
        self.points = points
        self.elevation = elevation
        self.color = color
        self.terrain_type = terrain_type
        self.selected = False
        self.dragging = False
        self.drag_offset = (0, 0)
        
    def draw(self, surface):
        if len(self.points) >= 3:
            temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            
            pygame.draw.polygon(temp_surface, (*self.color, 200), self.points)
            
            border_color = BLACK if not self.selected else RED
            pygame.draw.polygon(temp_surface, (*border_color, 255), self.points, 2)
            
            surface.blit(temp_surface, (0, 0))

            if self.selected:
                center = self.calculate_center()
                elevation_text = font.render(f"Z: {self.elevation}", True, BLACK)
                surface.blit(elevation_text, (center[0] - 20, center[1] - 10))
    
    def calculate_center(self):
        if not self.points:
            return (0, 0)
        x = sum(p[0] for p in self.points) / len(self.points)
        y = sum(p[1] for p in self.points) / len(self.points)
        return (x, y)
    
    def contains_point(self, point):
        if len(self.points) < 3:
            return False
            
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
    
    def move(self, dx, dy):
        self.points = [(x + dx, y + dy) for (x, y) in self.points]

class LayerVisualizer:
    def __init__(self):
        self.layers = []
        self.selected_layer = None
        self.z_buffer = []
        self.next_layer_id = 1
        self.show_legend = True
        self.drawing_new_layer = False
        self.new_layer_points = []
        self.new_layer_elevation = 0
        self.new_layer_color = random.choice(list(TERRAIN_TYPES.values()))
        self.new_layer_terrain = random.choice(list(TERRAIN_TYPES.keys()))
        
    def add_layer(self, layer):
        self.layers.append(layer)
        self.update_z_buffer()
        
    def remove_layer(self, layer):
        if layer in self.layers:
            self.layers.remove(layer)
            if self.selected_layer == layer:
                self.selected_layer = None
            self.update_z_buffer()
    
    def update_z_buffer(self):
        self.layers.sort(key=lambda x: x.elevation)
        
    def select_layer(self, pos):
        for layer in reversed(self.layers):
            if layer.contains_point(pos):
                self.selected_layer = layer
                layer.selected = True
                
                max_elevation = max(l.elevation for l in self.layers) if self.layers else 0
                layer.elevation = max_elevation + 1
                self.update_z_buffer()
                return
        
        for layer in self.layers:
            layer.selected = False
        self.selected_layer = None
    
    def start_dragging(self, pos):
        if self.selected_layer:
            self.selected_layer.dragging = True
            center = self.selected_layer.calculate_center()
            self.selected_layer.drag_offset = (center[0] - pos[0], center[1] - pos[1])
    
    def drag_layer(self, pos):
        if self.selected_layer and self.selected_layer.dragging:
            dx = pos[0] + self.selected_layer.drag_offset[0] - self.selected_layer.calculate_center()[0]
            dy = pos[1] + self.selected_layer.drag_offset[1] - self.selected_layer.calculate_center()[1]
            self.selected_layer.move(dx, dy)
    
    def stop_dragging(self):
        if self.selected_layer:
            self.selected_layer.dragging = False
    
    def change_elevation(self, delta):
        if self.selected_layer:
            self.selected_layer.elevation += delta
            self.update_z_buffer()
    
    def draw(self, surface):
        surface.fill(WHITE)
        
        for layer in self.layers:
            layer.draw(surface)
        
        if self.drawing_new_layer and len(self.new_layer_points) >= 2:
            pygame.draw.lines(surface, BLUE, False, self.new_layer_points, 2)
            if len(self.new_layer_points) >= 3:
                temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(temp_surface, (*self.new_layer_color, 150), self.new_layer_points)
                surface.blit(temp_surface, (0, 0))
        
        if self.show_legend:
            self.draw_legend(surface)
        
        self.draw_ui(surface)
    
    def draw_legend(self, surface):
        legend_width = 200
        legend_height = 50 + len(TERRAIN_TYPES) * 25
        
        pygame.draw.rect(surface, LIGHT_GRAY, (WIDTH - legend_width - 20, 20, legend_width, legend_height))
        pygame.draw.rect(surface, GRAY, (WIDTH - legend_width - 20, 20, legend_width, legend_height), 2)
        
        title = title_font.render("Legenda de Terrenos", True, BLACK)
        surface.blit(title, (WIDTH - legend_width - 10, 25))
        
        y_offset = 50
        for i, (terrain, color) in enumerate(TERRAIN_TYPES.items()):
            pygame.draw.rect(surface, color, (WIDTH - legend_width - 10, y_offset, 20, 20))
            pygame.draw.rect(surface, GRAY, (WIDTH - legend_width - 10, y_offset, 20, 20), 1)
            
            text = font.render(terrain, True, BLACK)
            surface.blit(text, (WIDTH - legend_width + 15, y_offset + 4))
            
            y_offset += 25
    
    def draw_ui(self, surface):
        pygame.draw.rect(surface, LIGHT_GRAY, (10, 10, 250, 180))
        pygame.draw.rect(surface, GRAY, (10, 10, 250, 180), 2)

        title = title_font.render("Controles", True, BLACK)
        surface.blit(title, (20, 15))
        
        instructions = [
            "Botão Esquerdo: Selecionar/Mover",
            "Botão Direito: Adicionar pontos",
            "Tecla +/-: Alterar elevação (Z)",
            "Tecla DEL: Remover camada",
            "Tecla L: Alternar legenda",
            "Tecla N: Nova camada",
            "Tecla ENTER: Finalizar camada",
            "Tecla ESC: Cancelar criação"
        ]
        
        y_offset = 40
        for line in instructions:
            text = font.render(line, True, BLACK)
            surface.blit(text, (20, y_offset))
            y_offset += 20

        if self.selected_layer:
            info_y = 200
            pygame.draw.rect(surface, LIGHT_GRAY, (10, info_y, 250, 80))
            pygame.draw.rect(surface, GRAY, (10, info_y, 250, 80), 2)
            
            info_title = title_font.render("Camada Selecionada", True, BLACK)
            surface.blit(info_title, (20, info_y + 5))
            
            name_text = font.render(f"Nome: {self.selected_layer.name}", True, BLACK)
            surface.blit(name_text, (20, info_y + 30))
            
            elev_text = font.render(f"Elevação: {self.selected_layer.elevation}", True, BLACK)
            surface.blit(elev_text, (20, info_y + 50))

        if self.drawing_new_layer:
            mode_y = HEIGHT - 60
            pygame.draw.rect(surface, LIGHT_GRAY, (10, mode_y, 300, 50))
            pygame.draw.rect(surface, BLUE, (10, mode_y, 300, 50), 2)
            
            mode_text = title_font.render("Modo: Criando Nova Camada", True, BLUE)
            surface.blit(mode_text, (20, mode_y + 5))
            
            points_text = font.render(f"Pontos: {len(self.new_layer_points)}", True, BLACK)
            surface.blit(points_text, (20, mode_y + 30))

def generate_random_polygon(center, avg_radius, irregularity, spikiness, num_vertices):
    """Gera um polígono irregular aleatório"""
    points = []
    
    angle_steps = []
    lower = (2 * np.pi / num_vertices) * (1 - irregularity)
    upper = (2 * np.pi / num_vertices) * (1 + irregularity)
    angle_sum = 0
    
    for i in range(num_vertices):
        angle = random.uniform(lower, upper)
        angle_steps.append(angle)
        angle_sum += angle
    
    angle_steps = [angle * (2 * np.pi / angle_sum) for angle in angle_steps]
    
    angle = 0
    for i in range(num_vertices):
        radius = random.uniform(avg_radius * (1 - spikiness), avg_radius)
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        points.append((x, y))
        angle += angle_steps[i]
    
    return points

def main():
    visualizer = LayerVisualizer()
    clock = pygame.time.Clock()
    
    for i, terrain in enumerate(TERRAIN_TYPES.keys()):
        center = (random.randint(200, WIDTH - 200), random.randint(100, HEIGHT - 100))
        points = generate_random_polygon(center, random.randint(50, 100), 0.5, 0.5, random.randint(5, 10))
        elevation = i * 10
        color = TERRAIN_TYPES[terrain]
        layer = GeologicalLayer(f"Camada {i+1}", points, elevation, color, terrain)
        visualizer.add_layer(layer)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if visualizer.drawing_new_layer:
                        visualizer.new_layer_points.append(event.pos)
                    else:
                        visualizer.select_layer(event.pos)
                        visualizer.start_dragging(event.pos)
                
                elif event.button == 3:
                    if not visualizer.drawing_new_layer and visualizer.selected_layer:
                        visualizer.selected_layer.points.append(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    visualizer.stop_dragging()
            
            elif event.type == pygame.MOUSEMOTION:
                visualizer.drag_layer(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    if visualizer.selected_layer:
                        visualizer.remove_layer(visualizer.selected_layer)
                
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    visualizer.change_elevation(1)
                
                elif event.key == pygame.K_MINUS:
                    visualizer.change_elevation(-1)
                
                elif event.key == pygame.K_l:
                    visualizer.show_legend = not visualizer.show_legend
                
                elif event.key == pygame.K_n:
                    visualizer.drawing_new_layer = True
                    visualizer.new_layer_points = []
                    visualizer.new_layer_elevation = max(l.elevation for l in visualizer.layers) + 10 if visualizer.layers else 10
                    visualizer.new_layer_color = random.choice(list(TERRAIN_TYPES.values()))
                    visualizer.new_layer_terrain = random.choice(list(TERRAIN_TYPES.keys()))
                
                elif event.key == pygame.K_RETURN:
                    if visualizer.drawing_new_layer and len(visualizer.new_layer_points) >= 3:
                        name = f"Camada {visualizer.next_layer_id}"
                        visualizer.next_layer_id += 1
                        layer = GeologicalLayer(
                            name,
                            visualizer.new_layer_points,
                            visualizer.new_layer_elevation,
                            visualizer.new_layer_color,
                            visualizer.new_layer_terrain
                        )
                        visualizer.add_layer(layer)
                        visualizer.selected_layer = layer
                        layer.selected = True
                        visualizer.drawing_new_layer = False
                
                elif event.key == pygame.K_ESCAPE:
                    visualizer.drawing_new_layer = False
        
        visualizer.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()