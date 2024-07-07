import pygame

#管理飞船类
class Ship:
    #ai_game为AlienInvasion类对象
    def __init__(self, ai_game) -> None:
        #初始化飞船并设置其初始位置
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(ai_game.settings.ship_image)
        self.rect = self.image.get_rect()

        #每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
    
    def blitme(self):
        #在置顶位置绘制飞船
        self.screen.blit(self.image, self.rect)