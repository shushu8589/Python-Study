import pygame
from pygame.sprite import Sprite

#外星人类
class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #加载图像
        self.image = pygame.image.load(self.settings.alien_image)
        self.rect = self.image.get_rect()

        #初始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储位置
        self.x = float(self.rect.x)
    
    def update(self):
        """向右移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
    
    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回true"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
