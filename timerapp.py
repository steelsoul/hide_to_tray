#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore
from PyQt4.QtGui import *
from interface import Ui_MainWindow
from PyQt4.Qt import QMessageBox, QObject

TimerappStates = {"Run":1, "Pause":2, "Reset":3}
AppVersion = "Timer v. 0.0.1a"

class TimerWindow(QMainWindow):

	def __init__(self):
		super(TimerWindow, self).__init__()
		self.initUI()
		self.timerState = TimerappStates["Reset"]
		#print "TimerState: ", self.timerState
		self.systemTrayIcon = QSystemTrayIcon(QIcon("bomb.png"), self)
		self.setup_menu()
		self.systemTrayIcon.activated.connect(self.on_systemTrayIcon_activated)
		self.systemTrayIcon.show()
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setup_logic()		
		
	def setup_menu(self):
		self.traymenu = QMenu(self)
		self.combineAction = self.traymenu.addAction("Start")
		self.combineAction.triggered.connect(self.toggle_combined)
		self.combineAction.setVisible(False)
		self.showAction = self.traymenu.addAction("Show")
		self.showAction.triggered.connect(self.toggleShowWindow)
		self.traymenu.addSeparator()
		self.quitAction = self.traymenu.addAction("Quit")
		self.quitAction.triggered.connect(qApp.quit);
		self.systemTrayIcon.setContextMenu(self.traymenu)
		
	def setup_logic(self):
		self.FirstBtnStates = ("Start", "Pause", "Continue")
		self.ui.pushButton.setText(self.FirstBtnStates[0])
		self.ui.pushButton.setEnabled(False)
		self.timeout = 0
		self.info_timeout = 0;
		self.ui.lineEdit.textChanged.connect(self.on_text_edit_changed)
		self.ui.lineEdit.returnPressed.connect(self.on_return_pressed)
		self.ui.lineEdit.setValidator(QRegExpValidator(QtCore.QRegExp("[0-9]+")))
		self.ui.pushButton.clicked.connect(self.on_start_btn_pressed)
		self.ui.pushButton_2.clicked.connect(self.on_reset_timer)
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.on_timeout)
		self.infoTimer = QtCore.QTimer(self)
		self.infoTimer.timeout.connect(self.on_info_timeout)
		self.systemTrayIcon.setToolTip(AppVersion)		

	@QtCore.pyqtSlot(QSystemTrayIcon.ActivationReason)
	def on_systemTrayIcon_activated(self, reason):
		if reason == QSystemTrayIcon.DoubleClick:
			self.showAction.setText("Hide")
			self.showNormal()
			self.activateWindow()
			self.isShown = True

	def on_text_edit_changed(self, text):
		#print ("Input %s" % text)
		if len(text) == 0:
			self.timeout = 0
			self.ui.pushButton.setEnabled(False)
		else:
			self.timeout = int(text)
			self.ui.lcdNumber.display(self.timeout * 60) #display timeout in seconds
			if self.timeout != 0: 
				self.ui.pushButton.setEnabled(True)

	def on_return_pressed(self):
		#print ("on_return_pressed")
		if self.ui.pushButton.text() == self.FirstBtnStates[0]:
			self.timer.start(self.timeout * 60 * 1000)
			self.info_timeout = self.timeout * 60
			self.infoTimer.start(1000) # 1 sec duration
			self.ui.pushButton.setText(self.FirstBtnStates[1])
			self.systemTrayIcon.setIcon(QIcon("bomb_run.png"))
			
	def start_timer(self):
		self.timer.start(self.timeout * 60 * 1000)
		self.info_timeout = self.timeout * 60
		self.infoTimer.start(1000) # 1 sec duration
		self.ui.pushButton.setText(self.FirstBtnStates[1])
		self.systemTrayIcon.setIcon(QIcon("bomb_run.png"))
		self.ui.lineEdit.setReadOnly(True)
		self.timerState = TimerappStates["Run"]
		self.combineAction.setText("Pause")
		self.combineAction.setVisible(True)
		
	def pause_timer(self):
		self.timer.stop()
		self.infoTimer.stop()
		self.ui.pushButton.setText(self.FirstBtnStates[2])
		self.systemTrayIcon.setIcon(QIcon("bomb_paused.png"))
		self.systemTrayIcon.setToolTip("[Paused|%s" % (self.calc_time_info()))
		self.timerState = TimerappStates["Pause"]
		self.combineAction.setText("Resume")
		
	def continue_timer(self):
		self.timer.start(self.timeout * 60 * 1000)
		self.infoTimer.start(1000)
		self.ui.pushButton.setText(self.FirstBtnStates[1])
		self.systemTrayIcon.setIcon(QIcon("bomb_run.png"))	
		self.combineAction.setText("Pause")
		self.timerState = TimerappStates["Run"]	

	def on_start_btn_pressed(self, triggered):
		if self.timerState == TimerappStates["Reset"]:		# Start timer		
			self.start_timer()
		elif self.timerState == TimerappStates["Run"]: 		# Pause timer
			self.pause_timer()
		else: 												# Continue timer
			self.continue_timer()
			
	def reset_timer(self):
		self.ui.pushButton.setText(self.FirstBtnStates[0])
		self.timer.stop()
		self.infoTimer.stop()
		self.ui.lineEdit.setText("")
		self.timeout = 0
		self.info_timeout = 0
		self.ui.lcdNumber.display(self.timeout * 60)
		self.systemTrayIcon.setIcon(QIcon("bomb.png"))
		self.systemTrayIcon.setToolTip(AppVersion)	
		self.ui.lineEdit.setReadOnly(False)
		self.combineAction.setVisible(False)

	def on_reset_timer(self, triggered):
		self.reset_timer()

	def on_timeout(self):
		self.systemTrayIcon.setToolTip("TImeout")
		self.reset_timer()
		self.ui.lcdNumber.display(self.timeout * 60)
		self.isShown = True
		self.showNormal()
		msgBox = QMessageBox()		# TODO: Center message box
		msgBox.setWindowTitle("== Notification ==")
		msgBox.setText("On timer!")
		msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		msgBox.exec_()

		
	def calc_time_info(self):
		# if timeout less than 5 minutes then show seconds else show minutes
		result = "[%d min|" % self.timeout
		if self.timeout < 300:
			result += ("|left %d sec]" % self.info_timeout)
		else:
			result += ("|left %d min]" % self.info_timeout/60)
		return result
			

	def on_info_timeout(self):
		self.info_timeout -= 1
		self.ui.lcdNumber.display(self.info_timeout)
		self.systemTrayIcon.setToolTip(self.calc_time_info())

	def changeEvent(self, event):
		if event.type() == QtCore.QEvent.WindowStateChange:
			if self.windowState() & QtCore.Qt.WindowMinimized:
				QtCore.QTimer.singleShot(0, self, QtCore.SLOT("hide()"))
				self.showAction.setText("Show")
				self.isShown = False
		QMainWindow.changeEvent(self, event)

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
			self.activateWindow()
			self.showNormal()
		else:
			item.setText("Show")
			self.hide()
			
	def toggle_combined(self):
		if self.timerState == TimerappStates["Run"]: 		# Pause timer
			self.pause_timer()
		elif self.timerState == TimerappStates["Pause"]:	# Continue timer
			self.continue_timer()

def main():
	app = QApplication(sys.argv)

	if QSystemTrayIcon.isSystemTrayAvailable() == False:
		QMessageBox("Error", "<b> No system systemTrayIcon is available!</b>", QMessageBox.Critical,
					QMessageBox.Yes | QMessageBox.Escape, QMessageBox.NoButton, QMessageBox.NoButton).exec_()

		exit(-1)

	ex = TimerWindow()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
