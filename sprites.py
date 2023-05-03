import pygame as pg 



class Static(pg.sprite.Sprite):
    def __init__(self,x,y,filename):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top=x,y