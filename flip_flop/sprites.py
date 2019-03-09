# Sprite classes for platform game
import pygame
from settings import *
vec = pygame.math.Vector2



class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.score = 0
        self.falling = False
        # self.image = pygame.Surface((30, 30))
        # self.image.fill(RED)
        self.moving_images = [game.player_img2, game.player_img1, game.player_img2, game.player_img3]
        # self.image = game.player_img
        self.image = self.moving_images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # self.radius = 17
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_update = pygame.time.get_ticks()
        self.falling_update = pygame.time.get_ticks()
        self.current_frame = 0

    def jump(self):
        self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()

        self.acc = vec(0, PLAYER_GRAV)
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
        if self.pos.y < 40:
            self.pos.y = 40

        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.moving_images)
            self.image = self.moving_images[self.current_frame]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)


class StartPlayer(Player):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.moving_images = [game.player_img2, game.player_img1, game.player_img2, game.player_img3]
        self.image = self.moving_images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.animate()

        self.acc = vec(0, PLAYER_GRAV)
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.y > HEIGHT - 275:
            self.jump()

        self.rect.midbottom = self.pos


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, num, down=True):
        pygame.sprite.Sprite.__init__(self)
        self.marked = False
        self.down = down
        self.game = game
        if self.down:
            self.image = game.plat_img_rev
        else:
            self.image = game.plat_img

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speedx = 3
        self.rect.x = x
        self.rect.y = y
        if down:
            self.rect.bottom = num

    def update(self):
        self.rect.x -= self.speedx

        if self.rect.right < 0:
            self.kill()


class BottomPlat(pygame.sprite.Sprite):

    def __init__(self, game, w, h, x):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.bottom_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = (w, h)
        self.rect.x = x
        self.speedx = 3

    def update(self):
        self.rect.x -= self.speedx

        if self.rect.right < 0:
            self.rect.left = WIDTH - 5


class Bird(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.bird_images[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.last_update = pygame.time.get_ticks()
        self.current_frame = random.randrange(9)
        self.speedx = 1

    def update(self):
        self.animate()

        self.rect.x -= self.speedx

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 100:
            self.last_update = now
            center = self.rect.center
            self.current_frame = (self.current_frame + 1) % len(self.game.bird_images)
            self.image = self.game.bird_images[self.current_frame]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = center

