#-------------------------------------------------------------------------------
# Camera display using PyQt and PiCamera
# Copyright (c) 2019
#-------------------------------------------------------------------------------

VERSION = "SPF_Display v0.10"

import sys, time, threading

from PyQt5.QtCore import QTimer, QPoint, pyqtSignal, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel,QPushButton,QMessageBox
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
# Minimap image widget
#-------------------------------------------------------------------------------
class MapWidget(QLabel):
    def __init__(self, parent=None):
        super(MapWidget, self).__init__(parent)
        pixmap = QPixmap('map.png')
        self.setMinimumSize(100, 140)
        self.setPixmap(pixmap)
        
#-------------------------------------------------------------------------------
# popup window, run 
# 	roslaunch master stage_mapping.launch
# 	rosrun fake_localization fake_localization
#-------------------------------------------------------------------------------
class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        ans=QMessageBox.question(self, 'Start', "Current location will be set as Home. Continue?", QMessageBox.No, QMessageBox.Yes)
        if ans== QMessageBox.Yes:
			print "Set as home"
	
#-------------------------------------------------------------------------------
# Main window
#-------------------------------------------------------------------------------
class MyWindow(QMainWindow):
    text_update = pyqtSignal(str)
		
    # Create main window
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.central = QWidget(self)
				
        self.vlayout = QVBoxLayout()        # Window layout
        self.displays = QHBoxLayout()
        
        
        self.dispMap = MapWidget(self)    # Map display
        self.vlayout.addWidget(self.dispMap)

        self.startButton = QPushButton('Start') #Start Button
        self.vlayout.addWidget(self.startButton)
        self.startButton.clicked.connect(self.start)
        self.startButton.show()
        self.returnButton = QPushButton('Return')
        self.vlayout.addWidget(self.returnButton)
        self.stopButton = QPushButton('STOP') #Stop button
        self.vlayout.addWidget(self.stopButton)
        self.displays.addLayout(self.vlayout)
        self.disp = ImageWidget(self)    
        self.displays.addWidget(self.disp)
         
        self.central.setLayout(self.displays)
        self.setCentralWidget(self.central)

        self.mainMenu = self.menuBar()      # Menu bar
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(exitAction)
        self.w = None
        
        
    def start(self):
		print "Opening a new popup window..."
		self.w = MyPopup()
		self.w.setGeometry(QRect(100, 100, 400, 200))
		self.w.show()
		
        
	
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
#
 #   def __init__(self):
#		QWidget.__init__(self)
#		buttonReply = QMessageBox.question(self, 'Start', " Current location will be set as Home. Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#		
#		if buttonReply == QMessageBox.Yes:
#			print('Yes clicked.')
#		else:
#			print('No clicked.')

#		self.show()
	
#-------------------------------------------------------------------------------
