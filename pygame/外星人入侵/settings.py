#存储游戏所有设置
class Settings:
    #初始化设置
    def __init__(self) -> None:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.clock_hz = 60
        self.title = '外星人入侵'
        self.ship_image = 'pygame\外星人入侵\images\ship.bmp'
