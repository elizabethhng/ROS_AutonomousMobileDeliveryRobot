#-------------------------------------------------------------------------------
# Camera display using PyQt and PiCamera
# Copyright (c) 2019
#-------------------------------------------------------------------------------

VERSION = "SPF_Display v0.10"

import sys, time, threading
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QPoint, pyqtSignal, QRect, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel,QPushButton,QMessageBox
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor, QPixmap, QIcon

#-------------------------------------------------------------------------------
# Global Settings
#-------------------------------------------------------------------------------

IMG_SIZE = 640,480          # 640,480 or 1280,720 or 1920,1080
TEXT_FONT   = QFont("Courier", 16)
     
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
        self.textbox.setMinimumSize(300, 50)
        self.text_update.connect(self.append_text)
        sys.stdout = self
        print("Image size %u x %u" % IMG_SIZE)
        
        self.mainvlayout = QVBoxLayout()		
        self.vlayout = QVBoxLayout()        # Window layout
        self.displays = QHBoxLayout()
        
        self.dispMap = MapWidget(self)    # Map display
        self.vlayout.addWidget(self.dispMap)  
              
        self.startButton = QPushButton(' Start') #Start Button
        self.vlayout.addWidget(self.startButton)
        self.startButton.clicked.connect(self.start)
        self.startButton.show()
        self.startButton.setIcon(QIcon(QPixmap('start.png')))
        self.startButton.setIconSize(QtCore.QSize(60,60))
        self.startButton.setStyleSheet("text-align: left;font-size: 24px")
        
        self.returnButton = QPushButton(' Return') #Return button
        self.vlayout.addWidget(self.returnButton)
        self.returnButton.clicked.connect(self.returnclicked)
        self.returnButton.show()
        self.returnButton.setIcon(QIcon(QPixmap('return.jpg')))
        self.returnButton.setIconSize(QtCore.QSize(60,60))
        self.returnButton.setStyleSheet("text-align: left;font-size: 24px")
        self.returnButton.setEnabled(False)

        self.stopButton = QPushButton(' STOP') #Stop button
        self.vlayout.addWidget(self.stopButton)
        self.displays.addLayout(self.vlayout)
        self.mainvlayout.addLayout(self.displays)
        self.stopButton.clicked.connect(self.stopclicked)
        self.stopButton.show()
        self.stopButton.setIcon(QIcon(QPixmap('stop.jpg')))
        self.stopButton.setIconSize(QtCore.QSize(60,60))
        self.stopButton.setStyleSheet("text-align: left; font-size: 24px;")
        self.stopButton.setEnabled(False)
        
        self.mainvlayout.addWidget(self.textbox) #Textbox display
        self.disp = ImageWidget(self)    
        self.displays.addWidget(self.disp)
        self.central.setLayout(self.mainvlayout)
        self.setCentralWidget(self.central)

        self.mainMenu = self.menuBar()      # Menu bar
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(exitAction)
        self.w = None
        
        print "To set current location as Home, select Start" 

        
    def start(self):
		QWidget.__init__(self)
		buttonReply = QMessageBox.question(self, 'Start', " Current location will be set as Home. Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		self.text_update.connect(self.append_text) ###
		sys.stdout = self ###
		if buttonReply == QMessageBox.Yes:
			print('Drive robot to desired destination. To return Home, select Return')
			self.startButton.setEnabled(False)
			self.returnButton.setEnabled(True)
			self.stopButton.setEnabled(True)
			self.stopButton.setStyleSheet("text-align: left;background-color: red; font-size: 36px; color: white")
		else:
			print('Do nothing.')

    def returnclicked(self):
		QWidget.__init__(self)
		buttonReply = QMessageBox.question(self, 'Return to Home', "Robot will return Home. Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		self.text_update.connect(self.append_text) ###
		sys.stdout = self ###
		
		if buttonReply == QMessageBox.Yes:
			print('Robot is returning home')
			self.startButton.setEnabled(False)
			self.returnButton.setEnabled(False)
			self.stopButton.setEnabled(True)
			self.stopButton.setStyleSheet("text-align: left;background-color: red; font-size: 36px; color: white")
		else:
			print('Do nothing.')
		
		
    def stopclicked(self):
        QWidget.__init__(self)  
        self.text_update.connect(self.append_text) ###
        sys.stdout = self ###
        print('Stop.')
        self.startButton.setEnabled(True)
        self.returnButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.stopButton.setStyleSheet("text-align: left; font-size: 36px;")
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
