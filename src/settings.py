import pygame


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(Settings)
            pass
        return cls._instance
    
    def __init__(self) -> None:
        if hasattr(self, 'initialized'):
            return
        self.initialized = True
        self.screen_width = 1200
        self.screen_height = 800
        self.bgcolosr = (230, 230, 230)
        self.game_name = 'dome'
        self.fontFont = pygame.font.Font(r'./font/STXINWEI.TTF', 30)
        
        