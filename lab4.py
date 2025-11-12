import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 25
        
    def get_rect(self):
        return QRectF(self.x - self.size/2, self.y - self.size/2, self.size, self.size)


class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.size = 30
        self.vx = speed * random.choice([-1, 1])
        self.vy = speed * random.choice([-1, 1])
        
    def get_rect(self):
        return QRectF(self.x, self.y, self.size, self.size)


class Obstacle:
    def __init__(self, x, y, w, h):
        self.rect = QRectF(x, y, w, h)


class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DODGE")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: black;")
        
        self.player = Player(400, 300)
        self.enemies = []
        self.obstacles = []
        self.score = 0
        self.game_over = False
        
        self.init_game()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)
        
        self.score_timer = QTimer()
        self.score_timer.timeout.connect(self.increase_score)
        self.score_timer.start(100)
        
    def init_game(self):
        self.obstacles = [
            Obstacle(150, 100, 80, 80),
            Obstacle(550, 400, 100, 60),
            Obstacle(300, 350, 60, 100)
        ]
        
        for i in range(3):
            x = random.randint(50, 700)
            y = random.randint(50, 500)
            while self.check_spawn_collision(x, y):
                x = random.randint(50, 700)
                y = random.randint(50, 500)
            speed = random.choice([2, 3, 4])
            self.enemies.append(Enemy(x, y, speed))
    
    def check_spawn_collision(self, x, y):
        test_rect = QRectF(x, y, 30, 30)
        if test_rect.intersects(self.player.get_rect()):
            return True
        for obs in self.obstacles:
            if test_rect.intersects(obs.rect):
                return True
        return False
    
    def increase_score(self):
        if not self.game_over:
            self.score += 1
            
            if self.score % 100 == 0 and self.score > 0:
                x = random.randint(50, 700)
                y = random.randint(50, 500)
                while self.check_spawn_collision(x, y):
                    x = random.randint(50, 700)
                    y = random.randint(50, 500)
                speed = random.randint(3, 5)
                self.enemies.append(Enemy(x, y, speed))
    
    def update_game(self):
        if self.game_over:
            return
            
        for enemy in self.enemies:
            new_x = enemy.x + enemy.vx
            new_y = enemy.y + enemy.vy
            
            if new_x <= 0 or new_x + enemy.size >= self.width():
                enemy.vx = -enemy.vx
                new_x = enemy.x + enemy.vx
                
            if new_y <= 0 or new_y + enemy.size >= self.height():
                enemy.vy = -enemy.vy
                new_y = enemy.y + enemy.vy
            
            test_enemy = Enemy(new_x, new_y, 0)
            test_enemy.size = enemy.size
            collision = False
            
            for obstacle in self.obstacles:
                if test_enemy.get_rect().intersects(obstacle.rect):
                    collision = True
                    enemy_rect = enemy.get_rect()
                    obs_rect = obstacle.rect
                    
                    dx_left = abs(enemy_rect.right() - obs_rect.left())
                    dx_right = abs(enemy_rect.left() - obs_rect.right())
                    dy_top = abs(enemy_rect.bottom() - obs_rect.top())
                    dy_bottom = abs(enemy_rect.top() - obs_rect.bottom())
                    
                    min_dist = min(dx_left, dx_right, dy_top, dy_bottom)
                    
                    if min_dist in (dx_left, dx_right):
                        enemy.vx = -enemy.vx
                    else:
                        enemy.vy = -enemy.vy
                    break
            
            if not collision:
                enemy.x = new_x
                enemy.y = new_y
            
            if enemy.get_rect().intersects(self.player.get_rect()):
                self.game_over = True
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(QPen(QColor(80, 80, 80), 2))
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        for obstacle in self.obstacles:
            painter.drawRect(obstacle.rect)
        
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.setBrush(QBrush(QColor(200, 0, 0)))
        for enemy in self.enemies:
            painter.drawRect(enemy.get_rect())
        
        painter.setPen(QPen(QColor(255, 255, 255), 3))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(QPointF(self.player.x, self.player.y), 
                          self.player.size/2, self.player.size/2)
        
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.drawText(20, 40, str(self.score))
        
        if self.game_over:
            painter.fillRect(self.rect(), QColor(0, 0, 0, 200))
            
            painter.setPen(QPen(QColor(255, 0, 0)))
            painter.setFont(QFont("Arial", 60, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignCenter, "GAME OVER")
            
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.setFont(QFont("Arial", 24))
            painter.drawText(self.rect().adjusted(0, 100, 0, 0), Qt.AlignCenter, 
                           f"SCORE: {self.score}")
            
            painter.setFont(QFont("Arial", 16))
            painter.drawText(self.rect().adjusted(0, 150, 0, 0), Qt.AlignCenter, 
                           "PRESS SPACE TO RESTART")
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            return
            
        if self.game_over:
            if event.key() == Qt.Key_Space:
                self.player = Player(400, 300)
                self.enemies = []
                self.obstacles = []
                self.score = 0
                self.game_over = False
                self.init_game()
            return
        
        old_x, old_y = self.player.x, self.player.y
        step = 15
        
        if event.key() == Qt.Key_Left:
            self.player.x -= step
        elif event.key() == Qt.Key_Right:
            self.player.x += step
        elif event.key() == Qt.Key_Up:
            self.player.y -= step
        elif event.key() == Qt.Key_Down:
            self.player.y += step
        else:
            return
        
        if self.player.x - self.player.size/2 < 0:
            self.player.x = self.player.size/2
        elif self.player.x + self.player.size/2 > self.width():
            self.player.x = self.width() - self.player.size/2
            
        if self.player.y - self.player.size/2 < 0:
            self.player.y = self.player.size/2
        elif self.player.y + self.player.size/2 > self.height():
            self.player.y = self.height() - self.player.size/2
        
        for obstacle in self.obstacles:
            if self.player.get_rect().intersects(obstacle.rect):
                self.player.x, self.player.y = old_x, old_y
                break
    
    def mousePressEvent(self, event):
        if self.game_over:
            return
            
        modifiers = QApplication.keyboardModifiers()
        if modifiers != Qt.ShiftModifier:
            return
            
        old_x, old_y = self.player.x, self.player.y
        
        self.player.x = event.pos().x()
        self.player.y = event.pos().y()
        
        if self.player.x - self.player.size/2 < 0:
            self.player.x = self.player.size/2
        elif self.player.x + self.player.size/2 > self.width():
            self.player.x = self.width() - self.player.size/2
            
        if self.player.y - self.player.size/2 < 0:
            self.player.y = self.player.size/2
        elif self.player.y + self.player.size/2 > self.height():
            self.player.y = self.height() - self.player.size/2
        
        for obstacle in self.obstacles:
            if self.player.get_rect().intersects(obstacle.rect):
                self.player.x, self.player.y = old_x, old_y
                break


def main():
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()