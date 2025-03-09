import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 游戏配置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[3:]:
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0

    def render(self, surface):
        for p in self.positions:
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE),
                              (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, rect)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        while True:
            self.position = (random.randint(0, GRID_WIDTH-1),
                            random.randint(0, GRID_HEIGHT-1))
            if self.position not in snake_positions:
                break

    def render(self, surface):
        rect = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.color, rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('贪吃蛇')
        self.clock = pygame.time.Clock()
        try:
            self.font = pygame.font.Font("../font/xingwei.TTF", 36)
        except:
            try:
                self.font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 36)
            except:
                try:
                    self.font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", 36)
                except:
                    try:
                        self.font = pygame.font.Font("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 36)
                    except:
                        print("请将中文字体文件放入项目根目录的font文件夹")
                        self.font = pygame.font.Font(None, 36)
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.food.randomize_position(self.snake.positions)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.direction = (1, 0)
                elif event.key == pygame.K_r and not self.is_running:
                    self.reset()
                    self.is_running = True

    def run(self):
        self.is_running = True
        while True:
            self.handle_keys()
            if self.is_running:
                if not self.snake.update():
                    self.is_running = False
                    continue

                if self.snake.get_head_position() == self.food.position:
                    self.snake.length += 1
                    self.snake.score += 1
                    self.food.randomize_position(self.snake.positions)

            self.screen.fill(BLACK)
            self.snake.render(self.screen)
            self.food.render(self.screen)
            
            # 显示分数
            score_text = self.font.render(f'得分: {self.snake.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if not self.is_running:
                game_over_text = self.font.render('游戏结束！按 R 键重新开始', True, WHITE)
                text_rect = game_over_text.get_rect()
                text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                self.screen.blit(game_over_text, text_rect)

            pygame.display.update()
            self.clock.tick(10)

if __name__ == '__main__':
    game = Game()
    game.run()