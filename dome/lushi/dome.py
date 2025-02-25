import pygame
import random
import math

# 初始化 Pygame
pygame.init()

# 设置窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("卡牌对战游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 卡牌类
class Card:
    def __init__(self, x, y, width=80, height=120):
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.width = width
        self.height = height
        self.original_width = width
        self.original_height = height
        self.moving = False
        self.target_x = x
        self.target_y = y
        self.speed = 10
        self.scale = 1.0
        self.shaking = False
        self.shake_time = 0
        self.shake_duration = 20
        self.shake_offset = 0
        self.attack_phase = 0  # 0: 开始放大, 1: 移动, 2: 碰撞震动, 3: 返回
        self.scale_speed = 0.1
        self.target_card = None  # 添加目标卡牌引用
        
        # 添加攻击力和生命值
        self.attack = random.randint(1, 10)
        self.health = random.randint(1, 10)
        self.original_health = self.health  # 保存初始生命值
        
        # 添加字体
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        current_x = self.x
        current_y = self.y
        
        # 添加震动效果
        if self.shaking:
            current_x += random.randint(-3, 3)
            current_y += random.randint(-3, 3)

        # 计算缩放后的尺寸和位置偏移
        scaled_width = self.width * self.scale
        scaled_height = self.height * self.scale
        x_offset = (scaled_width - self.width) / 2
        y_offset = (scaled_height - self.height) / 2

        # 绘制卡牌主体
        pygame.draw.rect(screen, WHITE, (
            current_x - x_offset,
            current_y - y_offset,
            scaled_width,
            scaled_height
        ))
        pygame.draw.rect(screen, BLACK, (
            current_x - x_offset,
            current_y - y_offset,
            scaled_width,
            scaled_height
        ), 2)

        # 绘制攻击力和生命值
        attack_text = self.font.render(str(self.attack), True, RED)
        health_text = self.font.render(str(self.health), True, RED)
        
        # 计算文字位置（考虑缩放）
        attack_x = current_x - x_offset + 10
        attack_y = current_y - y_offset + scaled_height - 30
        health_x = current_x - x_offset + scaled_width - 25
        health_y = current_y - y_offset + scaled_height - 30

        screen.blit(attack_text, (attack_x, attack_y))
        screen.blit(health_text, (health_x, health_y))

    def update_attack_animation(self):
        if not self.moving:
            return False

        if self.attack_phase == 0:  # 放大阶段
            self.scale += self.scale_speed
            if self.scale >= 1.3:
                self.attack_phase = 1
        
        elif self.attack_phase == 1:  # 移动阶段
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            # 检测碰撞（当距离小于两张牌宽度之和的一半时）
            if distance < (self.width + self.target_card.width) / 2:
                self.attack_phase = 2
                self.shaking = True
                self.target_card.shaking = True  # 让目标卡牌也开始震动
                self.shake_time = self.shake_duration
                self.target_card.shake_time = self.shake_duration
                
                # 在碰撞时处理伤害
                self.target_card.health -= self.attack
                self.health -= self.target_card.attack
            else:
                self.x += (dx/distance) * self.speed
                self.y += (dy/distance) * self.speed
        
        elif self.attack_phase == 2:  # 震动阶段
            self.shake_time -= 1
            if self.shake_time <= 0:
                self.shaking = False
                self.target_card.shaking = False
                self.attack_phase = 3
        
        elif self.attack_phase == 3:  # 返回阶段
            dx = self.original_x - self.x
            dy = self.original_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            self.scale -= self.scale_speed
            if self.scale < 1.0:
                self.scale = 1.0

            if distance < self.speed and self.scale <= 1.0:
                self.x = self.original_x
                self.y = self.original_y
                self.moving = False
                self.attack_phase = 0
                
                # 检查是否有卡牌死亡
                attacker_dead = self.health <= 0
                target_dead = self.target_card.health <= 0
                self.target_card = None  # 清除目标卡牌引用
                
                return True, attacker_dead, target_dead  # 返回战斗结果
            
            self.x += (dx/distance) * self.speed
            self.y += (dy/distance) * self.speed
        
        return False, False, False

    def take_damage(self, damage):
        """受到伤害并返回是否死亡"""
        self.health -= damage
        return self.health <= 0

# 游戏类
class Game:
    def __init__(self):
        self.player_cards = []
        self.enemy_cards = []
        self.current_turn = 0  # 0 为玩家回合，1 为敌方回合
        self.attacking_card = None
        self.attack_in_progress = False
        self.current_card_index = 0
        
        # 初始化卡牌
        card_spacing = 100
        for i in range(7):
            x = 50 + i * card_spacing
            self.player_cards.append(Card(x, WINDOW_HEIGHT - 150))
            self.enemy_cards.append(Card(x, 30))

    def update(self):
        if self.attack_in_progress and self.attacking_card:
            animation_complete, attacker_dead, target_dead = self.attacking_card.update_attack_animation()
            if animation_complete:
                # 处理死亡卡牌
                if attacker_dead:
                    if self.current_turn == 0:
                        self.player_cards.remove(self.attacking_card)
                    else:
                        self.enemy_cards.remove(self.attacking_card)
                
                if target_dead:
                    target = self.attacking_card.target_card
                    if self.current_turn == 0:
                        self.enemy_cards.remove(target)
                    else:
                        self.player_cards.remove(target)
                
                self.attack_in_progress = False
                self.current_turn = 1 - self.current_turn
                self.current_card_index = (self.current_card_index + 1) % max(1, len(self.player_cards))

    def draw(self, screen):
        screen.fill(BLACK)
        # 绘制分隔线
        pygame.draw.line(screen, WHITE, (0, WINDOW_HEIGHT//2), (WINDOW_WIDTH, WINDOW_HEIGHT//2))
        
        # 先绘制非攻击状态的卡牌
        for card in self.player_cards:
            if card != self.attacking_card:
                card.draw(screen)
        for card in self.enemy_cards:
            if card != self.attacking_card:
                card.draw(screen)
        
        # 最后绘制攻击中的卡牌，确保它在最上层
        if self.attacking_card:
            self.attacking_card.draw(screen)

    def start_attack(self):
        if not self.attack_in_progress:
            attacking_cards = self.player_cards if self.current_turn == 0 else self.enemy_cards
            target_cards = self.enemy_cards if self.current_turn == 0 else self.player_cards
            
            if len(attacking_cards) > 0 and len(target_cards) > 0:  # 确保双方都还有卡牌
                if self.current_card_index >= len(attacking_cards):
                    self.current_card_index = 0
                
                self.attacking_card = attacking_cards[self.current_card_index]
                target_card = random.choice(target_cards)
                
                self.attacking_card.moving = True
                self.attacking_card.target_x = target_card.x
                self.attacking_card.target_y = target_card.y
                self.attacking_card.target_card = target_card
                self.attack_in_progress = True

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.start_attack()

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
