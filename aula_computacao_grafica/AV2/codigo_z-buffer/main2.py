import pygame
import math
import random
from pygame.locals import *
from pygame import Vector2

# Configurações
WIDTH, HEIGHT = 800, 600
FPS = 60
PARTICLE_COUNT = 100
BACKGROUND_COLOR = (10, 10, 20)
LIGHT_COLOR = (255, 220, 150)
LIGHT_RADIUS = 50

class ParticleSystem:
    def __init__(self, count):
        self.particles = []
        self.create_particles(count)
        
    def create_particles(self, count):
        for _ in range(count):
            position = Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(0.5, 2.0)
            size = random.randint(3, 8)
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            life = random.uniform(5, 10)
            
            self.particles.append({
                'position': position,
                'velocity': velocity,
                'size': size,
                'color': color,
                'original_color': color,
                'life': life,
                'max_life': life
            })
    
    def update(self, dt, light_pos):
        for particle in self.particles:
            # Atualiza posição
            particle['position'] += particle['velocity'] * dt * 60
            
            # Colisão com bordas
            if particle['position'].x < 0 or particle['position'].x > WIDTH:
                particle['velocity'].x *= -0.9
            if particle['position'].y < 0 or particle['position'].y > HEIGHT:
                particle['velocity'].y *= -0.9
            
            # Mantém dentro dos limites
            particle['position'].x = max(0, min(WIDTH, particle['position'].x))
            particle['position'].y = max(0, min(HEIGHT, particle['position'].y))
            
            # Aplica gravidade suave em direção ao centro
            center = Vector2(WIDTH/2, HEIGHT/2)
            direction = center - particle['position']
            if direction.length() > 0:
                direction = direction.normalize()
                particle['velocity'] += direction * 0.01 * dt
            
            # Limita velocidade máxima
            if particle['velocity'].length() > 3:
                particle['velocity'] = particle['velocity'].normalize() * 3
                
            # Diminui vida
            particle['life'] -= 0.01 * dt
            if particle['life'] <= 0:
                # Reinicia partícula
                particle['position'] = Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
                particle['velocity'] = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(0.5, 2.0)
                particle['life'] = particle['max_life']
            
            # Calcula iluminação
            distance = (particle['position'] - light_pos).length()
            if distance < LIGHT_RADIUS:
                # Fator de iluminação baseado na distância
                light_factor = 1.0 - (distance / LIGHT_RADIUS)
                
                # Mistura a cor original com a cor da luz
                r = min(255, int(particle['original_color'][0] + LIGHT_COLOR[0] * light_factor * 0.5))
                g = min(255, int(particle['original_color'][1] + LIGHT_COLOR[1] * light_factor * 0.5))
                b = min(255, int(particle['original_color'][2] + LIGHT_COLOR[2] * light_factor * 0.5))
                
                particle['color'] = (r, g, b)
                
                # Partículas mais próximas da luz ficam um pouco maiores
                particle['size'] = particle['size'] * (1 + light_factor * 0.3)
            else:
                particle['color'] = particle['original_color']
    
    def draw(self, surface):
        for particle in self.particles:
            # Calcula opacidade com base na vida
            alpha = int(255 * (particle['life'] / particle['max_life']))
            
            # Tamanho com base na vida
            size = int(particle['size'] * (0.7 + 0.3 * particle['life'] / particle['max_life']))
            
            # Desenha partícula
            pygame.draw.circle(surface, particle['color'], 
                              (int(particle['position'].x), int(particle['position'].y)), 
                              size)

class LightSource:
    def __init__(self):
        self.position = Vector2(WIDTH // 2, HEIGHT // 2)
        self.color = LIGHT_COLOR
        self.radius = LIGHT_RADIUS
        self.flicker_intensity = 0.1
        
    def update(self, dt, mouse_pos=None):
        if mouse_pos:
            # Move a luz suavemente em direção ao mouse
            direction = Vector2(mouse_pos) - self.position
            self.position += direction * 0.1 * dt
        
        # Efeito de cintilação
        self.radius = LIGHT_RADIUS * (1 + math.sin(pygame.time.get_ticks() * 0.002) * self.flicker_intensity)
        
    def draw(self, surface):
        # Cria uma superfície para o efeito de luz com canal alpha
        light_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Desenha gradiente radial de luz
        for radius in range(int(self.radius), 0, -4):
            alpha = int(100 * (radius / self.radius))
            color = (self.color[0], self.color[1], self.color[2], alpha)
            pygame.draw.circle(light_surface, color, 
                              (int(self.position.x), int(self.position.y)), 
                              radius)
        
        # Aplica a luz na tela com blending aditivo
        surface.blit(light_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

def render_text(surface, text, position, color=(255, 255, 255)):
    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sistema de Partículas com Iluminação Dinâmica")
    clock = pygame.time.Clock()
    
    particles = ParticleSystem(PARTICLE_COUNT)
    light = LightSource()
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Tempo em segundos desde o último frame
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        # Atualiza
        mouse_pos = pygame.mouse.get_pos()
        light.update(dt, mouse_pos)
        particles.update(dt, light.position)
        
        # Renderiza
        screen.fill(BACKGROUND_COLOR)
        
        # Desenha partículas
        particles.draw(screen)
        
        # Desenha luz
        light.draw(screen)
        
        # Informações de FPS
        fps_text = f"FPS: {int(clock.get_fps())}"
        render_text(screen, fps_text, (10, 10))
        render_text(screen, "Mova o mouse para controlar a luz", (10, 30))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()