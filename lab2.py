import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt


class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = 1
        self.setFixedSize(700, 500)
        self.setStyleSheet("background-color: black; border: 2px solid #2c3e50;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(255, 255, 255), 2))

        if self.mode == 1:
            self.draw_squares(painter)
        elif self.mode == 2:
            self.draw_sierpinski(painter)

    def draw_squares(self, painter):
        size = 400
        x1, y1 = 150, 50
        x2, y2 = x1 + size, y1
        x3, y3 = x2, y1 + size
        x4, y4 = x1, y3
        
        P = 0.08
        
        for _ in range(50):
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            painter.drawLine(int(x2), int(y2), int(x3), int(y3))
            painter.drawLine(int(x3), int(y3), int(x4), int(y4))
            painter.drawLine(int(x4), int(y4), int(x1), int(y1))
            
            nx1 = x1 + (x2 - x1) * P
            ny1 = y1 + (y2 - y1) * P
            
            nx2 = x2 + (x3 - x2) * P
            ny2 = y2 + (y3 - y2) * P
            
            nx3 = x3 + (x4 - x3) * P
            ny3 = y3 + (y4 - y3) * P
            
            nx4 = x4 + (x1 - x4) * P
            ny4 = y4 + (y1 - y4) * P
            
            x1, y1 = nx1, ny1
            x2, y2 = nx2, ny2
            x3, y3 = nx3, ny3
            x4, y4 = nx4, ny4

    def draw_sierpinski(self, painter):
        x1, y1 = 350, 30
        x2, y2 = 50, 450
        x3, y3 = 650, 450
        self.sierpinski_recursive(painter, x1, y1, x2, y2, x3, y3, 5)

    def sierpinski_recursive(self, painter, x1, y1, x2, y2, x3, y3, depth):
        if depth == 0:
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            painter.drawLine(int(x2), int(y2), int(x3), int(y3))
            painter.drawLine(int(x3), int(y3), int(x1), int(y1))
        else:
            mx1 = (x1 + x2) / 2
            my1 = (y1 + y2) / 2
            
            mx2 = (x2 + x3) / 2
            my2 = (y2 + y3) / 2
            if math.sqrt((mx2-mx1)**2+(my2-my1)**2)<=1:
                print(depth)
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
                painter.drawLine(int(x2), int(y2), int(x3), int(y3))
                painter.drawLine(int(x3), int(y3), int(x1), int(y1))
                return
            
            mx3 = (x3 + x1) / 2
            my3 = (y3 + y1) / 2
            
            self.sierpinski_recursive(painter, x1, y1, mx1, my1, mx3, my3, depth - 1)
            self.sierpinski_recursive(painter, mx1, my1, x2, y2, mx2, my2, depth - 1)
            self.sierpinski_recursive(painter, mx3, my3, mx2, my2, x3, y3, depth - 1)


class GraphicsForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Lab №2")
        self.setFixedSize(750, 750)
        
        self.setWindowIcon(self.createIcon())
        
        self.setStyleSheet("background-color: black")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("Lab №2")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: white; margin: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        
        student_label = QLabel("Student: Yashchenko Oleksandra, Group IC-34")
        student_label.setFont(QFont("Arial", 12, QFont.StyleItalic))
        student_label.setStyleSheet("color: #bdc3c7; margin: 5px;")
        student_label.setAlignment(Qt.AlignCenter)
        
        self.drawing_widget = DrawingWidget()
        
        btn1 = QPushButton("50 Nested Squares")
        btn1.setFont(QFont("Arial", 12))
        btn1.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                margin: 5px;
                border: 1px solid #3498db;
                border-radius: 20px;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                border: none;
            }
        """)
        btn1.clicked.connect(lambda: self.change_mode(1))
        
        btn2 = QPushButton("Sierpinski Triangle")
        btn2.setFont(QFont("Arial", 12))
        btn2.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                margin: 5px;
                border: 1px solid #2ecc71;
                border-radius: 20px;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                border: none;
            }
        """)
        btn2.clicked.connect(lambda: self.change_mode(2))
        
        close_button = QPushButton("Close")
        close_button.setFont(QFont("Arial", 12))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                margin: 5px;
                border: 1px solid red;
                border-radius: 20px;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                border: none;
            }
        """)
        close_button.clicked.connect(self.close)
        
        layout.addWidget(title_label)
        layout.addWidget(student_label)
        layout.addWidget(self.drawing_widget)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(close_button)
        
        central_widget.setLayout(layout)
    
    def createIcon(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#3498db"))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor("white"), 2))
        painter.drawEllipse(8, 8, 16, 16)
        painter.end()
        
        return QIcon(pixmap)
    
    def change_mode(self, mode):
        self.drawing_widget.mode = mode
        self.drawing_widget.update()


def main():
    app = QApplication(sys.argv)
    form = GraphicsForm()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()