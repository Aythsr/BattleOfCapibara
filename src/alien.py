from typing import Any
import pygame
import random

from pygame.sprite import Sprite

class Alien( Sprite ):
    def __init__(self, Win : pygame.Surface, pos : tuple[int, int] = None, id : int = 0) -> None:
        super().__init__()
        self.Win = Win
        self.image = pygame.transform.scale(
            pygame.image.load(r'./imgs/alien.png'),
            (50, 50)
            ) 
        tmpfont = pygame.font.Font(r'/System/Library/Fonts/PingFang.ttc', 15)
        self.id_ft = tmpfont.render(str(id), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        
        self.rect.center = Win.get_rect().center
        self.speed = (random.randint(-2, 2), random.randint(-2, 2))
        self.spcnt = 300
        pass
    
    def change_dirc(self, Fts: bool = False):
        if Fts:
            self.speed = (random.randint(-2, 2), random.randint(-2, 2))
        while (not self.Win.get_rect().contains(self.rect.move(*self.speed))) or self.speed == (0, 0):
            # print("xxxxxxxx")
            self.speed = (random.randint(-2, 2), random.randint(-2, 2))
        pass
    
    def rand_move(self):
        self.change_dirc()
        self.rect.move_ip(*self.speed)
        self.spcnt -= 1
        if self.spcnt <= 0:
            self.change_dirc(True)
            self.spcnt = 300
        pass
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rand_move()
        self.Win.blit(self.id_ft, self.rect)
        self.Win.blit(self.image, self.rect)
        
        

