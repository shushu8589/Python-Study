import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from time import sleep
from game_stats import GameStats
from button import Button

class AlienInvasion:
    #管理游戏资源和行为的类
    def __init__(self) -> None:
        #初始化游戏并创建游戏资源
        pygame.init()
        self.clock = pygame.time.Clock() #控制刷新率
        self.settings = Settings() #载入设置

        # #全屏模式
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        
        pygame.display.set_caption(self.settings.title)
        
        #创建一个用于存储游戏统计信息都实例
        self.stats = GameStats(self)

        self.ship = Ship(self) #飞船对象
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #游戏状态
        self.game_active = False

        self.play_button = Button(self, "Play")

    def run_game(self):
        #开始游戏的主循环
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(self.settings.clock_hz)

    #事件监听
    def _check_events(self):
        #侦听键盘和鼠标事件
        for event in pygame.event.get():
            #关闭窗口触发
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            #按键触发
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
    
    def _check_play_button(self, mouse_pos):
        """玩家单机play按钮时开始新游戏"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.game_active = True
            
    #按键按下响应
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullent()

    #按键抬起响应
    def _check_keyup_event(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    #绘制子弹
    def _fire_bullent(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    #更新子弹位置，并删除已消失的子弹
    def _update_bullets(self):
        self.bullets.update()
        #删除超出屏幕子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # 如果外星人都被消灭，删除全部子弹，并重新创建外星人舰队
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
    
    #创建一个外星人舰队
    def _create_fleet(self):
        #创建一个外星人，再不断添加，直到没有空间添加外星人为止
        #外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, currnet_y = alien_width, alien_height
        while currnet_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, currnet_y)
                current_x += 2 *alien_width
            current_x = alien_width
            currnet_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并将其放到当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """更新外星人舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        #检查是否有外星人达到下边缘
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """在有外星人达到边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将 ships_left 减 1
            self.stats.ships_left -= 1

            #清空外星人列表和子弹
            self.bullets.empty()
            self.aliens.empty()

            #创建新的舰队，并把飞船重置位置
            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """检查是否有外星人达到屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    #屏幕刷新绘制
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color) #设置屏幕颜色
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme() #绘制飞船
        self.aliens.draw(self.screen)

        if not self.game_active:
            self.play_button.draw_button()
        #让最近绘制的屏幕可见
        pygame.display.flip()

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()