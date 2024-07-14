import pygame
from pygame.sprite import Sprite

#管理飞船类
class Ship(Sprite):
    #ai_game为AlienInvasion类对象
    def __init__(self, ai_game) -> None:
        #初始化飞船并设置其初始位置
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(self.settings.ship_image)
        self.rect = self.image.get_rect()

        #每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        #飞船的x坐标
        self.x = float(self.rect.x)

        #移动标志（飞船一开始不移动）
        self.moving_right = False
        self.moving_left = False

    #根据移动标志调整飞船位置
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
    
    def blitme(self):
        #在置顶位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """充值飞船位置"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)