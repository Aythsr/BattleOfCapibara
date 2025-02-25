import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('方块大战')

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # 添加绿色用于显示分数

# 初始化字体
pygame.font.init()
try:
    # 尝试使用系统中的中文字体
    font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 36)  # Windows 系统黑体
except:
    try:
        font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", 36)  # macOS 系统
    except:
        try:
            font = pygame.font.Font("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 36)  # Linux 系统
        except:
            print("未找到中文字体，使用系统默认字体")
            font = pygame.font.Font(None, 36)
score = 0  # 添加分数变量

# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > WINDOW_HEIGHT + 10:
            self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)
        if self.rect.left < -25 or self.rect.right > WINDOW_WIDTH + 25:
            self.speedx *= -1

# 创建精灵组
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# 创建玩家
player = Player()
all_sprites.add(player)

# 创建敌人
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# 游戏循环
clock = pygame.time.Clock()
running = True
game_over = False  # 添加游戏结束标志

while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:  # 只有在游戏未结束时才能发射子弹
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif event.key == pygame.K_r and game_over:  # 按R键重新开始游戏
                game_over = False
                score = 0
                # 重置玩家位置
                player.rect.centerx = WINDOW_WIDTH // 2
                player.rect.bottom = WINDOW_HEIGHT - 10
                # 清除所有敌人和子弹
                for sprite in enemies:
                    sprite.kill()
                for sprite in bullets:
                    sprite.kill()
                # 重新创建敌人
                for i in range(8):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)

    if not game_over:  # 只有在游戏未结束时才更新游戏状态
        # 更新
        all_sprites.update()

        # 碰撞检测
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1  # 击中敌人增加分数
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            game_over = True  # 设置游戏结束标志

    # 绘制
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # 显示分数
    score_text = font.render(f'得分: {score}', True, GREEN)
    screen.blit(score_text, (WINDOW_WIDTH - 120, 10))
    
    # 显示游戏结束画面
    if game_over:
        game_over_text = font.render('游戏结束！', True, RED)
        final_score_text = font.render(f'最终得分: {score}', True, RED)
        restart_text = font.render('按 R 键重新开始', True, RED)
        
        screen.blit(game_over_text, 
                   (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 
                    WINDOW_HEIGHT//2 - 60))
        screen.blit(final_score_text, 
                   (WINDOW_WIDTH//2 - final_score_text.get_width()//2, 
                    WINDOW_HEIGHT//2))
        screen.blit(restart_text, 
                   (WINDOW_WIDTH//2 - restart_text.get_width()//2, 
                    WINDOW_HEIGHT//2 + 60))

    pygame.display.flip()

    # 控制游戏速度
    clock.tick(60)

pygame.quit()
sys.exit()
