import pygame
from os.path import join
from random import randint, uniform
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) # Set the working directory to the script's directory, so we can run the game from any location

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('..', 'images', 'player.png')).convert_alpha() # Use join to crossplatform
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)) # Could be any point of the rect
        self.direction = pygame.Vector2()
        self.speed = 300

        # Cooldown section
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 500

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, star_surf):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (randint(0,800), randint(0,600))) # Could be any point of the rect

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 2000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400, 500)

        # Rotation
        self.rotation = 0
        self.rotation_speed = randint(40, 150)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        # Continuous rotation
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask) # It's not necesary to create a mask in the class, it create it automatically
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, meteor_sprites, True):
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, 'white')
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, 'white', text_rect.inflate(15, 15).move(0, -3), 3, 10)

# General Setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

# Imports
star_surf = pygame.image.load(join('..', 'images', 'star.png')).convert_alpha() # Single import, more efficent
meteor_surf = pygame.image.load(join('..', 'images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('..', 'images', 'laser.png')).convert_alpha()
explosion_frames = [pygame.image.load(join('..', 'images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
font = pygame.font.Font(join('..', 'images', 'Oxanium-Bold.ttf'), 20)

laser_sound = pygame.mixer.Sound(join('..', 'audio', 'laser.wav'))
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(join('..', 'audio', 'explosion.wav'))
explosion_sound.set_volume(0.1)
game_music = pygame.mixer.Sound(join('..', 'audio', 'game_music.wav'))
game_music.set_volume(0.1)
game_music.play() # Specify the amounts loops it will play

# Sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# Custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = (randint(0, WINDOW_WIDTH), -50)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    # Update
    all_sprites.update(dt)
    collisions()

    # Draw the game
    screen.fill("#3a2e3f")
    display_score()
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()