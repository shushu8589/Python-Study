#存储游戏所有设置
class Settings:
    #初始化设置
    def __init__(self) -> None:
        self.screen_width = 1200 #窗口宽度像素
        self.screen_height = 800 #窗口高度像素
        self.bg_color = (230,230,230) #背景颜色
        self.clock_hz = 60 #游戏帧数
        self.title = '外星人入侵' #标题名称

        #飞船设置
        self.ship_image = R'pygame\外星人入侵\images\ship.bmp' #飞机图形
        self.ship_speed = 1.5 #飞船移动速度
        self.ship_limit = 3 # 初始生命次数

        #外星人设置
        self.alien_image = R'pygame\外星人入侵\images\alien.bmp' #外星人图形
        self.alien_speed = 100.0 # 外星人移动速度
        self.fleet_drop_speed = 10 # 外星人向下移动距离
        # fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1

        #子弹参数
        self.bullet_speed = 3.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 30

        
