import pygame
import os
from .config import GlobalConfig


def create_rounded_surface(surface, radius):
    """创建一个带有圆角的Surface"""
    size = surface.get_size()
    mask = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)
    target = pygame.Surface(size, pygame.SRCALPHA)
    target.blit(surface, (0, 0))
    target.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return target


def run():
    pygame.init()
    config = GlobalConfig()
    
    # 设置窗口
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption(config.game_name)
    
    # 加载图片
    images = []
    image_files = ['K.png', 'Q.png', 'J.png']
    for img_file in image_files:
        img_path = os.path.join(config.img_dir, img_file)
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (200, 300))  # 统一图片大小
        img = create_rounded_surface(img, 20)  # 添加圆角效果
        # 设置图片透明度
        # img.set_alpha(180)
        images.append(img)
    
    # 加载字体
    font_path = os.path.join(config.font_dir, 'font1.ttf')
    font = pygame.font.Font(font_path, 36)  # 调整字体大小
    card_texts = ['K', 'Q', 'j']
    
    # 计算图片位置
    spacing = (1200 - (5 * 200)) // 4  # 计算间距
    card_positions = [(spacing + i * (200 + spacing), 250) for i in range(5)]
    
    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((34, 139, 34))  # 设置背景色为绿色
        
        # 绘制图片和文字
        for i, (img, pos, text) in enumerate(zip(images, card_positions, card_texts)):
            screen.blit(img, pos)
            
            # 左上角文字（黑色带阴影）
            shadow_surface = font.render(text, True, (0, 0, 0, 128))
            shadow_rect = shadow_surface.get_rect(topleft=(pos[0] + 22, pos[1] + 22))
            screen.blit(shadow_surface, shadow_rect)
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(pos[0] + 20, pos[1] + 20))
            screen.blit(text_surface, text_rect)
            
            # 右下角文字（旋转180度，黑色带阴影）
            shadow_surface_rotated = pygame.transform.rotate(shadow_surface, 180)
            shadow_rect_rotated = shadow_surface_rotated.get_rect(bottomright=(pos[0] + 182, pos[1] + 282))
            screen.blit(shadow_surface_rotated, shadow_rect_rotated)
            text_surface_rotated = pygame.transform.rotate(text_surface, 180)
            text_rect_rotated = text_surface_rotated.get_rect(bottomright=(pos[0] + 180, pos[1] + 280))
            screen.blit(text_surface_rotated, text_rect_rotated)
        
        pygame.display.flip()
    
    pygame.quit()