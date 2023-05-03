from settings import *
from sprites import *
import pygame
import os


class Battle:
    def __init__(self):
        self.game_width, self.game_height = PORTRAIT_WIDTH,PORTRAIT_HEIGHT
        os.environ['SDL_VIDEO_WINDOW_POS']='%d,%d' %(50,50)
        self.screen=pygame.display.set_mode((self.game_width,self.game_height))
        self.clock = pygame.time.Clock()
        self.running=True
        self.playing=True
        self.fps=FPS

        # pygame.font.init()
        # pygame.mixer.init()

        self.player_team= "Alpha"
        self.enemy_team="Beta"

        self.all_sprites=pygame.sprite.Group()
        self.player_unit_sprites= pygame.sprite.Group()
        self.enemy_unit_sprites = pygame.sprite.Group()

    def new(self):
            self.background=Static(0,0, "battleground.png")
            self.all_sprites.add(self.background)
            self.run()
    def events(self):
        pass
    def update(self):
        pass
    def run(self):
        pass

b = Battle()
b.new()   