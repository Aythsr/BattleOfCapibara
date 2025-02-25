from typing import Any, Iterable
import pygame
from pygame.sprite import AbstractGroup, Sprite, Group

def chk_BBB(a : Sprite, b : Sprite) -> bool:
    if pygame.sprite.collide_mask(a, b) is None:
        return False
    return True

class objx( Sprite ):
    """基础物品信息
    Win: Surface -> the game windows
    img_path: str
    scales: tuple[int, int]
    init_pos: tuple[int, int]
    """
    def __init__(self, 
                 Win : pygame.Surface, 
                 img_path : str, 
                 scales : tuple[int, int] = None, 
                 init_pos: tuple[int, int] = None,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        if scales: 
            self.image = pygame.transform.scale(pygame.image.load(img_path), scales)
            # print("noooo")
        else:
            self.image = pygame.image.load(img_path)
            # print("noooo")
            
        self.screen = Win
        self.screen_rect = Win.get_rect()
        self.rect = self.image.get_rect()
        if not init_pos:
            self.rect.center = self.screen_rect.center
        else:
            self.rect.center = init_pos
        print('center', self.rect.center)
        self.move_dx = 0
        self.move_dy = 0
        pass
     
    def out_screen(self):
        return not self.rect.colliderect(self.screen_rect)
        return self.rect.bottom < 0 or self.rect.right < 0 or \
            self.rect.top > self.screen_rect.bottom or self.rect.left > self.screen_rect.right
    
    def set_fdx(self, x : int = 0):
        self.move_dx += x

    def set_fdy(self, y : int = 0):
        self.move_dy += y

    def set_f_0(self):
        self.move_dx = 0
        self.move_dy = 0
    
    def move(self):
        self.rect.y += self.move_dy
        self.rect.x += self.move_dx
    
    def update(self):
        self.move()
        self.screen.blit(self.image, self.rect)

class Bullet(objx):
    def __init__(self, Win: pygame.Surface, init_pos: tuple[int, int] = None, *args, **kwargs) -> None:
        super().__init__(Win = Win, img_path = r'./imgs/bullet.png',
                         scales = [50, 50], init_pos=init_pos, *args, **kwargs)
    

class BulletGroup( Group ):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def add_bullet(self, x : Bullet):
        x.set_f_0()
        x.set_fdy(-3)
        super().add(x)
    
    def update(self, *args: Any, **kwargs: Any) -> None: 
        print('buttet nums: ', len(self.sprites()))
        for x in self.sprites():
            if x.out_screen():
                self.remove(x)

        return super().update(*args, **kwargs)
