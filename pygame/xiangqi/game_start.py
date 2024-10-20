import pygame
import sys

# 初始化 pygame
pygame.init()

# 设置棋盘参数
WIDTH, HEIGHT = 800, 1000
ROWS, COLS = 7, 9
SQUARE_SIZE = (WIDTH - 150) // ROWS
MARGIN = 80

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)

# 创建窗口
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('中国象棋小游戏')

# 定义字体
FONT = pygame.font.SysFont('simhei', 36)
BUTTON_FONT = pygame.font.SysFont('simhei', 30)

# 棋子类
class ChessPiece:
    def __init__(self, name, color, x, y):
        self.name = name
        self.color = color
        self.x = x
        self.y = y

    def draw(self, win):
        # 画外部圆圈
        pygame.draw.circle(win, WHITE, (MARGIN + self.x * SQUARE_SIZE, MARGIN + self.y * SQUARE_SIZE), SQUARE_SIZE // 3)
        pygame.draw.circle(win, self.color, (MARGIN + self.x * SQUARE_SIZE, MARGIN + self.y * SQUARE_SIZE), SQUARE_SIZE // 3, 3)
        # 在圆圈中间绘制汉字
        text_surface = FONT.render(self.name, True, self.color)
        text_rect = text_surface.get_rect(center=(MARGIN + self.x * SQUARE_SIZE, MARGIN + self.y * SQUARE_SIZE))
        win.blit(text_surface, text_rect)

    def move(self, new_x, new_y):
        if 0 <= new_x < ROWS and 0 <= new_y < COLS:
            self.x = new_x
            self.y = new_y

    def can_capture(self, target_piece):
        # 每个棋子的走法与吃法
        if self.name == '车':
            return self.x == target_piece.x or self.y == target_piece.y
        elif self.name == '马':
            return (abs(self.x - target_piece.x), abs(self.y - target_piece.y)) in [(1, 2), (2, 1)]
        elif self.name == '跑':
            return (self.x == target_piece.x or self.y == target_piece.y) and abs(self.x - target_piece.x + self.y - target_piece.y) > 1
        elif self.name == '兵' or self.name == '帅':
            return abs(self.x - target_piece.x) + abs(self.y - target_piece.y) == 1
        elif self.name == '象':
            return abs(self.x - target_piece.x) == 2 and abs(self.y - target_piece.y) == 2
        elif self.name == '士':
            return abs(self.x - target_piece.x) == 1 and abs(self.y - target_piece.y) == 1
        return False

# 棋手类
class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = []

    def add_piece(self, piece):
        self.pieces.append(piece)

    def draw_pieces(self, win):
        for piece in self.pieces:
            piece.draw(win)

# 画棋盘
def draw_board(win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(MARGIN + row * SQUARE_SIZE, MARGIN + col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, BLACK, rect, 1)

# 画按钮
def draw_buttons(win):
    red_button_rect = pygame.Rect(50, 20, 100, 40)
    black_button_rect = pygame.Rect(200, 20, 100, 40)
    pygame.draw.rect(win, LIGHT_GRAY, red_button_rect)
    pygame.draw.rect(win, LIGHT_GRAY, black_button_rect)
    red_text_surface = BUTTON_FONT.render('红方', True, RED)
    black_text_surface = BUTTON_FONT.render('黑方', True, BLUE)
    win.blit(red_text_surface, red_button_rect.topleft)
    win.blit(black_text_surface, black_button_rect.topleft)
    return red_button_rect, black_button_rect

# 主游戏循环
def main():
    red_player = Player(RED)
    black_player = Player(BLUE)

    players = [red_player, black_player]
    selected_piece = None
    current_player = None
    selected_name = None

    while True:
        draw_board(WIN)
        red_button_rect, black_button_rect = draw_buttons(WIN)
        for player in players:
            player.draw_pieces(WIN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # 处理鼠标点击选择玩家或放置棋子
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if red_button_rect.collidepoint(mouse_x, mouse_y):
                    current_player = red_player
                    # 弹出选择棋子的图片
                    print("请选择要放置的棋子: 车, 马, 跑, 兵, 象, 士, 帅")
                    # 模拟选择棋子图片的过程，可以在此处替换为图形化选择逻辑
                    selected_name = '车'  # 这里使用硬编码的选择，未来可改为基于图片的选择
                elif current_player == red_player and selected_name:
                    # 放置红方的棋子
                    grid_x = (mouse_x - MARGIN + SQUARE_SIZE // 2) // SQUARE_SIZE
                    grid_y = (mouse_y - MARGIN + SQUARE_SIZE // 2) // SQUARE_SIZE
                    if 0 <= grid_x < ROWS and 0 <= grid_y < COLS:
                        piece = ChessPiece(selected_name, RED, grid_x, grid_y)
                        red_player.add_piece(piece)
                        selected_name = None  # 重置选择状态，确保每次点击按钮只放置一个棋子

if __name__ == "__main__":
    main()
