from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QCursor
from PySide6.QtCore import QTimer
import sys

app = QApplication(sys.argv)

def print_cursor_pos():
    pos = QCursor.pos()
    print(f"Cursor: ({pos.x()}, {pos.y()})")

timer = QTimer()
timer.timeout.connect(print_cursor_pos)
timer.start(1000)  # every 1000ms

sys.exit(app.exec())