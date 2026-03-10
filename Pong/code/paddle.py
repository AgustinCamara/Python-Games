import pygame

from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups, x_pos):
        super().__init__(groups)

        # Image
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0,0), SIZE['paddle']), 0, 4)

        # Shadow
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf, COLORS['paddle shadow'], pygame.FRect((0,0), SIZE['paddle']), 0, 4)

        # Rect and movement
        self.rect = self.image.get_frect(center = x_pos)
        self.old_rect = self.rect.copy()
        self.direction = 0

    def move(self, dt):
        self.rect.y += self.direction * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)

class Player(Paddle):
    def __init__(self, groups, x_pos):
        super().__init__(groups, x_pos)
        self.speed = SPEED['player']

    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

class Opponent(Paddle):
    def __init__(self, groups, x_pos, ball):
        super().__init__(groups, x_pos)
        self.speed = SPEED['opponent']
        self.ball = ball

    def get_direction(self):
        self.direction = 1 if self.rect.centery < self.ball.rect.centery else -1