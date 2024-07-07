import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    #管理游戏资源和行为的类
    def __init__(self) -> None:
        #初始化游戏并创建游戏资源
        pygame.init()
        self.clock = pygame.time.Clock() #控制刷新率
        self.settings = Settings() #载入设置

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.title)
        self.ship = Ship(self) #飞船对象

    def run_game(self):
        #开始游戏的主循环
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(self.settings.clock_hz)

    #事件监听
    def _check_events(self):
        #侦听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
    #屏幕刷新绘制
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color) #设置屏幕颜色
        self.ship.blitme() #绘制飞船

        #让最近绘制的屏幕可见
        pygame.display.flip()

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()