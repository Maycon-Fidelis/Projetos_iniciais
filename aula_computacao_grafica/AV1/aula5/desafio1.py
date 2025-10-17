import pygame
import sys

pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1200, 900
TILE_SIZE = 40  # Tamanho dos blocos do nível
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Animação com Sprites')

WHITE = (255, 255, 255)
GRAVITY = 0.5
JUMP_STRENGTH = -10
SPEED = 5

# Definição do nível
level = [
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P                                                       P",
    "P                                                       P",
    "P                                                       P",
    "P                                                       P",
    "P           PPPPPP                                      P",
    "P                                                       P",
    "P                     PPPPPP                            P",
    "P                                                       P",
    "P                                     PPPPPPPPPP        P",
    "P                                                       P",
    "P                    PPPPPPPPPPP                        P",
    "P                                                       P",
    "P                                                       P",
    "P      PPPPPPPPPPP                                      P",
    "P                                                       P",
    "P                                                       P",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
]

class Level:
    def __init__(self, level_data):
        self.tiles = []
        for row_index, row in enumerate(level_data):
            for col_index, tile in enumerate(row):
                if tile == 'P':  # Se for uma plataforma
                    rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.tiles.append(rect)
    
    def draw(self, screen):
        for tile in self.tiles:
            pygame.draw.rect(screen, (100, 100, 100), tile)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, images_idle, images_run, images_run_flipped, image_jump, x, y, level):
        super().__init__()
        self.images_idle = images_idle
        self.images_run = images_run
        self.images_run_flipped = images_run_flipped
        self.image_jump = image_jump
        self.images = self.images_idle  # Começa parado
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200
        
        # Movimento
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.level = level

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -SPEED
            if self.facing_right:
                self.facing_right = False
            self.images = self.images_run_flipped
        elif keys[pygame.K_RIGHT]:
            self.vel_x = SPEED
            if not self.facing_right:
                self.facing_right = True
            self.images = self.images_run
        else:
            self.images = self.images_idle
        
        # Pulo
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
        
        # Aplicar gravidade
        self.vel_y += GRAVITY
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Verificar colisão com plataformas
        self.on_ground = False
        for tile in self.level.tiles:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:  # Caindo
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Batendo a cabeça
                    self.rect.top = tile.bottom
                    self.vel_y = 0
        
        # Atualizar animação
        if not self.on_ground:
            self.image = self.image_jump
        else:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images)
                self.image = self.images[self.current_frame]

# Carregar imagens do sprite
images_idle = [pygame.image.load(f'mario.jpeg')]
images_run = [pygame.image.load(f'mario_run.jpeg')]
images_run_flipped = [pygame.transform.flip(img, True, False) for img in images_run]
image_jump = pygame.image.load('mario_jump.jpeg')

level_data = Level(level)
sprite = AnimatedSprite(images_idle, images_run, images_run_flipped, image_jump, 100, HEIGHT - 200, level_data)
all_sprites = pygame.sprite.Group(sprite)

clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    level_data.draw(screen)  # Desenhar o nível
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)
