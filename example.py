# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):               

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')    
        self.isShown = False
        #self.show()
        
    def toggleShowWindow(self):
        self.isShown = not self.isShown
        if self.isShown: 
            self.show()
        else:
            self.hide()


# def main():

    # app = QtGui.QApplication(sys.argv)
    # ex = Example()
    # sys.exit(app.exec_())
    
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()    
    w = QtGui.QWidget()
    trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("bomb.png"), w)
    menu = QtGui.QMenu(ex)
    exitAction = menu.addAction("Show")
    #exitAction.triggered.connect(QtGui.qApp.quit)
    exitAction.triggered.connect(ex.toggleShowWindow)
    trayIcon.setContextMenu(menu)

    trayIcon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
