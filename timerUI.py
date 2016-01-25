# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore
from PyQt4.QtGui import *
from interface import Ui_MainWindow
from PyQt4.Qt import QMessageBox, QObject

class Example(QMainWindow):

    def __init__(self):
        super(Example, self).__init__()
        
        self.systemTrayIcon = QSystemTrayIcon(QIcon("bomb.png"), self)  
        self.trayMenu = QMenu(self)

        self.showAction = self.trayMenu.addAction("Show")
        self.showAction.triggered.connect(self.toggleShowWindow)
        
        self.trayMenu.addSeparator()
        
        self.quitAction = self.trayMenu.addAction("Quit")
        self.quitAction.triggered.connect(qApp.quit);
        
        self.systemTrayIcon.setContextMenu(self.trayMenu)
        self.systemTrayIcon.activated.connect(self.on_systemTrayIcon_activated)
        self.systemTrayIcon.show()
        
        self.initUI()
        
        self.timeout = 0
        self.info_timeout = 0;
       
        self.ui.lineEdit.textChanged.connect(self.on_text_edit_changed)
        self.ui.lineEdit.setValidator(QRegExpValidator(QtCore.QRegExp("[0-9]+")))
        
        self.ui.pushButton.clicked.connect(self.on_start_timer)
        
        self.timer = QtCore.QTimer(self)
        
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_timeout)
        
        self.infoTimer = QtCore.QTimer(self)
        self.infoTimer.timeout.connect(self.on_info_timeout)
        
    @QtCore.pyqtSlot(QSystemTrayIcon.ActivationReason)
    def on_systemTrayIcon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showAction.setText("Hide")
            self.showNormal()
            self.isShown = True
    
    def on_text_edit_changed(self, text):
        #print ("Input %s" % text)
        if len(text) == 0: self.timeout = 0
        else: self.timeout = int(text)
        self.ui.lcdNumber.display(self.timeout * 60) #display timeout in seconds
        
    def on_start_timer(self, triggered):
        #print ("On start timer")
        self.timer.start(self.timeout * 60 * 1000)
        self.info_timeout = self.timeout * 60
        self.infoTimer.start(1000) # 1 sec duration
        
    def on_timeout(self):
        self.timer.stop()
        self.infoTimer.stop()
        self.ui.lcdNumber.display(self.timeout)
        self.info_timeout = self.timeout * 60
        self.isShown = True
        self.showNormal()
        #print("!On timer!") 
        msgBox = QMessageBox()
        msgBox.setWindowTitle("== Notification ==")
        msgBox.setText("On timer!")
        msgBox.exec_()
        
    def on_info_timeout(self):
        self.info_timeout -= 1
        self.ui.lcdNumber.display(self.info_timeout)
        
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:                
                event.accept()
                self.hide()                
                event.ignore()
            #if self.windowState() and QtCore.Qt.WindowMinimized:
                #print("minimize")
                
                #item.setText("Show")
                #self.showAction.setText("Show")                
                #self.hide()
                #event.ignore()
                #event.ignore()                
        
    def initUI(self):  
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setWindowTitle('Timer')    
        self.isShown = False
        
    def toggleShowWindow(self):
        self.isShown = not self.isShown
        item = QObject.sender(self)
        if self.isShown:            
            item.setText("Hide") 
            self.showNormal()
        else:
            item.setText("Show") 
            self.hide()

    
def main():
    app = QApplication(sys.argv)
    
    if QSystemTrayIcon.isSystemTrayAvailable() == False:
        QMessageBox("Error", "<b> No system systemTrayIcon is available!</b>", QMessageBox.Critical,
                    QMessageBox.Yes | QMessageBox.Escape, QMessageBox.NoButton, QMessageBox.NoButton).exec_()
        
        exit(-1) 

    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
