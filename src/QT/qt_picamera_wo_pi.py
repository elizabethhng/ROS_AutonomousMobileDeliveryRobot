#-------------------------------------------------------------------------------
# Camera display using PyQt and PiCamera
# Copyright (c) 2019
#-------------------------------------------------------------------------------

VERSION = "SPF_Display v0.10"

import sys, time, threading

from PyQt5.QtCore import QTimer, QPoint, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor, QPixmap

#-------------------------------------------------------------------------------
# Global Settings
#-------------------------------------------------------------------------------

IMG_SIZE = 640,480          # 640,480 or 1280,720 or 1920,1080
TEXT_FONT   = QFont("Courier", 10)
     
#-------------------------------------------------------------------------------
# Image widget
#-------------------------------------------------------------------------------
class ImageWidget(QLabel):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        pixmap = QPixmap('test.jpg')
        self.setMinimumSize(IMG_SIZE[0], IMG_SIZE[1])
        self.setPixmap(pixmap)

#-------------------------------------------------------------------------------
# Main window
#-------------------------------------------------------------------------------
class MyWindow(QMainWindow):
    text_update = pyqtSignal(str)

    # Create main window
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.central = QWidget(self)
        self.textbox = QTextEdit(self.central)
        self.textbox.setFont(TEXT_FONT)
        self.textbox.setMinimumSize(300, 100)
        self.text_update.connect(self.append_text)
        sys.stdout = self
        print("Image size %u x %u" % IMG_SIZE)


        self.vlayout = QVBoxLayout()        # Window layout
        self.displays = QHBoxLayout()
        self.disp = ImageWidget(self)    
        self.displays.addWidget(self.disp)
        self.vlayout.addLayout(self.displays)
        self.label = QLabel(self)
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.textbox)
        self.central.setLayout(self.vlayout)
        self.setCentralWidget(self.central)

        self.mainMenu = self.menuBar()      # Menu bar
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(exitAction)

    

    # Handle sys.stdout.write: update text display
    def write(self, text):
        self.text_update.emit(str(text))
    def flush(self):
        pass

    # Append to text display
    def append_text(self, text):
        cur = self.textbox.textCursor()     # Move cursor to end of text
        cur.movePosition(QTextCursor.End) 
        s = str(text)
        while s:
            head,sep,s = s.partition("\n")  # Split line at LF
            cur.insertText(head)            # Insert text at cursor
            if sep:                         # New line if LF
                cur.insertBlock()
        self.textbox.setTextCursor(cur)     # Update visible cursor


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    win.setWindowTitle(VERSION)
    #win.start()
    sys.exit(app.exec_())
#-------------------------------------------------------------------------------
#EOF
#-------------------------------------------------------------------------------
