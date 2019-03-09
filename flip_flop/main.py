import pygame
import random
from settings import *
from sprites import *
from os import path


class Game:

    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_data()
        self.font_name = pygame.font.match_font('arial')
        self.last_update = pygame.time.get_ticks()
        self.pause_time = pygame.time.get_ticks()

    def bottom_plats(self, group):
        self.bottom = BottomPlat(self, WIDTH / 2, HEIGHT, 0)
        group.add(self.bottom)

        self.bottom = BottomPlat(self, WIDTH, HEIGHT, WIDTH)
        group.add(self.bottom)

    def draw(self):
        # Game Loop - draw
        # self.screen.fill(BLACK)
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        self.bottoms.draw(self.screen)
        self.draw_text(self.screen, str(self.player.score), 32, WIDTH/2, 100)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def draw_text(self, surface, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_p:
                    self.pause()

    def load_data(self):
        # load highscore
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        try:
            with open(path.join(self.dir, HS_FILE), 'r') as fin:
                self.highscore = int(fin.read())
        except FileNotFoundError:
            self.highscore = 0
        self.background = pygame.image.load(path.join(img_dir, 'bg.png')).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()
        self.player_img = pygame.image.load(path.join(img_dir, 'flap.png')).convert()
        self.player_img = pygame.transform.scale(self.player_img, (45, 35))
        self.player_img1 = pygame.image.load(path.join(img_dir, 'bluebird-downflap.png')).convert()
        self.player_img1 = pygame.transform.scale(self.player_img1, (45, 35))
        self.player_img2 = pygame.image.load(path.join(img_dir, 'bluebird-midflap.png')).convert()
        self.player_img2 = pygame.transform.scale(self.player_img2, (45, 35))
        self.player_img3 = pygame.image.load(path.join(img_dir, 'bluebird-upflap.png')).convert()
        self.player_img3 = pygame.transform.scale(self.player_img3, (45, 35))
        self.plat_img = pygame.image.load(path.join(img_dir, 'pipe-green.png')).convert()
        self.plat_img = pygame.transform.scale(self.plat_img, (80, 380))
        self.plat_img_rev = pygame.image.load(path.join(img_dir, 'pipe-green-rev.png')).convert()
        self.plat_img_rev = pygame.transform.scale(self.plat_img_rev, (80, 380))

        # self.plat_img_rev = pygame.transform.flip(self.plat_img, False, True)
        self.bottom_img = pygame.image.load(path.join(img_dir, 'base.png')).convert()
        self.bottom_img = pygame.transform.scale(self.bottom_img, (WIDTH, 75))

        self.gameover_img = pygame.image.load(path.join(img_dir, 'gameover4.png')).convert()
        # self.gameover_img = pygame.transform.scale(self.gameover_img, (200, 125))
        self.gameover_img.set_colorkey(BLACK)

        self.bird_images = []
        for i in range(10):
            self.bird_img = pygame.image.load(path.join(img_dir, 'bird{}.png'.format(i))).convert()
            w = self.bird_img.get_width()
            h = self.bird_img.get_height()
            self.bird_img = pygame.transform.scale(self.bird_img, (round(w * .17), round(h * .17)))
            self.bird_img.set_colorkey(BLACK)
            self.bird_images.append(self.bird_img)

        # load sound
        self.snd_dir = path.join(self.dir, 'snd')

    def new(self):
        # start a new game
        now = pygame.time.get_ticks()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bottoms = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.spawn_starting_pipes()
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.bottom_plats(self.bottoms)
        self.run()

    def pause(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        waiting = False

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def spawn_platforms(self):
        num = random.randrange(75, HEIGHT - 275)
        p = Platform(self, WIDTH + 190, 0, num)
        self.all_sprites.add(p)
        self.platforms.add(p)
        p = Platform(self, WIDTH + 190, num + 170, num + 275, False)
        self.all_sprites.add(p)
        self.platforms.add(p)

    def spawn_starting_pipes(self):
        global PLATFORM_LIST
        PLATFORM_LIST = []
        plat_len_delay = 500
        for i in range(3):
            num = random.randrange(75, HEIGHT - 275)
            PLATFORM_LIST.append((WIDTH + plat_len_delay, 0, num))
            PLATFORM_LIST.append((WIDTH + plat_len_delay, num + 170, num + 350, False))
            plat_len_delay += 260

    def save_highscore(self):
        if self.player.score > self.highscore:
            self.highscore = self.player.score
        with open('highscrore.txt', 'w') as fout:
            fout.write(str(self.highscore))

    def show_go_screen(self):
        # game over/continue
        if self.running:
            self.rect = self.gameover_img.get_rect()
            self.rect.center = (WIDTH / 2, HEIGHT / 2)
            self.screen.blit(self.gameover_img, self.rect)
            pygame.display.flip()
        # if self.running:
            self.wait_for_key()

    def show_start_screen(self):
        self.start_sprites = pygame.sprite.Group()
        self.birds = []
        self.p = StartPlayer(self)
        self.bird = Bird(self, WIDTH + 135, 140)
        self.bird1 = Bird(self, WIDTH + 125, 150)
        self.bird2 = Bird(self, WIDTH + 135, 160)
        self.start_sprites.add(self.bird)
        self.birds.append(self.bird)
        self.start_sprites.add(self.bird1)
        self.birds.append(self.bird1)
        self.start_sprites.add(self.bird2)
        self.birds.append(self.bird2)
        self.start_sprites.add(self.p)
        self.bottom_plats(self.start_sprites)

        waiting = True
        while waiting:

            # Draw to the start screen
            self.screen.fill(BLACK)
            self.screen.blit(self.background, self.background_rect)
            self.clock.tick(FPS)
            self.start_sprites.update()
            self.start_sprites.draw(self.screen)
            self.draw_text(self.screen, 'Flip Flop', 64, WIDTH / 2, 35)
            self.draw_text(self.screen, 'Highscore : ' + str(self.highscore), 32, WIDTH / 2, 150)
            self.draw_text(self.screen, 'Press Space To Jump', 32, WIDTH / 2, HEIGHT - 225)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

            if self.birds[-1].rect.right < 0:
                for bird in self.birds:
                    bird.rect.x = bird.x + 100
                    bird.current_frame = random.randrange(9)

            pygame.display.flip()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.bottoms.update()

        # Check to see if player and platform collide (Pixel perfect)
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False, pygame.sprite.collide_mask)
        if hits:
            self.playing = False
            self.save_highscore()

        # Add more pipes
        if len(self.platforms) <= 4:
            self.spawn_platforms()

        # check if player hits bottom
        hits = pygame.sprite.spritecollide(self.player, self.bottoms, False)
        if hits:
            self.player.rect.bottom = hits[0].rect.top

        # give points to player
        for plat in self.platforms:
            if plat.rect.right < ((WIDTH/2) - 15) and not plat.marked and not plat.down:
                self.player.score += 1
                plat.marked = True
                break

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
