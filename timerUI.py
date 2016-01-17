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
        
    @QtCore.pyqtSlot(QSystemTrayIcon.ActivationReason)
    def on_systemTrayIcon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showAction.setText("Hide")
            self.showNormal()
            self.isShown = True
        
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() and QtCore.Qt.WindowMinimized:
                event.ignore()
                self.hide()
                return 
        
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
