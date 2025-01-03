class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game) -> None:
        """初始化信息"""
        self.settings = ai_game.settings
        self.reset_stats()

        self.ships_left = 0
        """生命数量"""
        self.score = 0
        """计算分数"""
        self.high_score = 0
        """最高得分"""
        self.level = 1
        """等级"""

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0

        