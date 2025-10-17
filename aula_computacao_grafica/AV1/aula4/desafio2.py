import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Animação com Sprites')

WHITE = (255, 255, 255)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, image_list, x, y):
        super().__init__()
        self.images = image_list
        self.image = self.images[0]
        self.rect = self.image.get_rect() 
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 500

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.current_frame = 0
            self.image = self.images[self.current_frame] 

image_list = [pygame.image.load(f'mario{i}.jpeg') for i in range(1, 3)]

sprite = AnimatedSprite(image_list, 100, 100)
all_sprites = pygame.sprite.Group(sprite)

clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)
