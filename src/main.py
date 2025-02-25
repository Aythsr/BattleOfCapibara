import pygame
import sys
from settings import Settings
from GameBaseObj import Bullet, BulletGroup, chk_BBB


class Ship:
    def __init__(self, ai_game) -> None:
        self.ship = pygame.transform.scale(pygame.image.load(r"./imgs/spaceship.png"),
                                      (50, 60))
        # self.ship = pygame.transform.scale(pygame.image.load(r"D:\code\pygame_project_dome\imgs\bullet.png"),
        #                               (50, 60))
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.ship_rect = self.ship.get_rect()
        self.ship_rect.midbottom = self.screen_rect.midbottom
        self.move_dx = 0
        self.move_dy = 0
        self.seepl = 1
        pass
    
    def blitme(self):
        self.move()
        self.screen.blit(self.ship, self.ship_rect)
        
    def set_fdx(self, x : int = 0):
        self.move_dx += x
    def set_fdy(self, y : int = 0):
        self.move_dy += y
    
    def move(self):
        # print(self.ship_rect.top, self.ship_rect.bottom, self.ship_rect.left, self.ship_rect.right)
        y = self.move_dy * self.seepl
        x = self.move_dx * self.seepl
        if self.ship_rect.top + y >= 0 and \
            self.ship_rect.bottom + y <= self.screen_rect.bottom:
            self.ship_rect.y += y
            # print('y')
            
        if self.ship_rect.left + x >= 0 and \
            self.ship_rect.right + x <= self.screen_rect.right:
            self.ship_rect.x += x
            # print("x")

from alien import Alien

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.setting = Settings()
        self.screen = pygame.display.set_mode(
            (self.setting.screen_width, self.setting.screen_height))
        pygame.display.set_caption(self.setting.game_name)
        self.screen_rect = self.screen.get_rect()
        print(self.screen_rect.top, self.screen_rect.bottom, self.screen_rect.left, self.screen_rect.right)
        print(self.screen_rect.midtop, self.screen_rect.bottom, self.screen_rect.left, self.screen_rect.right)
        self.clock = pygame.time.Clock()
        self.ship = Ship(self)
        self.alien = pygame.sprite.Group()
        self.al_cnt = 5
        for _ in range(self.al_cnt):
            self.alien.add(Alien(self.screen, id=_))
        self.running = True
        self.scol = 0
        pass
    
    def run_game(self):
        self.running = True
        bullets = BulletGroup()
        

        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    key=pygame.key.name(event.key)
                    print (key, "Key is pressed")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.ship.set_fdy(-1)
                    elif event.key == pygame.K_s:
                        self.ship.set_fdy(1)
                    elif event.key == pygame.K_a:
                        self.ship.set_fdx(-1)
                    elif event.key == pygame.K_d:
                        self.ship.set_fdx(1)
                    elif event.key == pygame.K_SPACE:
                        tmp = Bullet(Win=self.screen, 
                                     init_pos=self.ship.ship_rect.midtop)
                        bullets.add_bullet(tmp)
                    elif event.key == pygame.K_j:
                        self.ship.seepl = 3
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.ship.set_fdy(1)
                    elif event.key == pygame.K_s:
                        self.ship.set_fdy(-1)
                    elif event.key == pygame.K_a:
                        self.ship.set_fdx(1)
                    elif event.key == pygame.K_d:
                        self.ship.set_fdx(-1)
                    elif event.key == pygame.K_j:
                        self.ship.seepl = 1    
            
            self.screen.fill(self.setting.bgcolosr)
            self.ship.blitme()
            if len(self.alien.sprites()) == 0:
                self.al_cnt *= 2
                for _ in range(self.al_cnt):
                    self.alien.add(Alien(self.screen, id=_))
            bullets.update()
            self.alien.update()
            Suf_scol = self.setting.fontFont.render(str(self.scol), True, (0, 0, 0))
            self.screen.blit(Suf_scol, (0, 0))
            pygame.display.flip()
            rp = pygame.sprite.groupcollide(self.alien, bullets, True, True, collided=None)  
            for k, v in rp.items():
                self.scol += len(v)
            
            # if len(rp) > 0:
            #     for k, v in rp.items():
            #         print(k.rect, ":")
            #         for x in v:
            #             print(x.rect)
            #     break
            self.clock.tick(30)
        
        pygame.quit()
        
    
    

        


if __name__ == "__main__":
    
    game = Game()
    game.run_game()
    
    
