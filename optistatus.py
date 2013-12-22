#!/usr/bin/env python2
#
# Optistatus 
# @author fluffymadness
#
import subprocess
import time
import threading
import sys
from PyQt4 import QtGui, QtCore

app = QtGui.QApplication(sys.argv)
class SystemTrayIcon(QtGui.QSystemTrayIcon):	
    ALREADY_ON = 0
    TRAY_TOOLTIP = 'Optistatus'
    TRAY_ICON = '/usr/share/pixmaps/optistatus-inactive.png'
    TRAY_ICON_ACTIVE = '/usr/share/pixmaps/optistatus-active.png'
    turnOn = QtCore.pyqtSignal() 
    turnOff = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        self.optirunchecker = OptirunChecker(self)
        self.connect(self.optirunchecker, self.optirunchecker.turnOn,self.turn_on)
        self.connect(self.optirunchecker, self.optirunchecker.turnOff,self.turn_off)
        self.optirunchecker.start()
    
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.set_icon(self.TRAY_ICON)
        self.menu = QtGui.QMenu(parent)
        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.on_exit)
        self.setContextMenu(self.menu)   
        
    def on_exit(self, event):
        self.optirunchecker.stop()
        sys.exit(1)
        
    def set_icon(self, trayicon):
        icon = QtGui.QIcon(trayicon)  
        self.setIcon(icon)
        
    def turn_on(self):
		self.set_icon(self.TRAY_ICON_ACTIVE)
		self.ALREADY_ON = 1
	
    def turn_off(self):
        self.set_icon(self.TRAY_ICON)
        self.ALREADY_ON = 0
        
class OptirunChecker(QtCore.QThread):
    running = 1
    uiObject = ""
    def __init__(self, uiObject):
        QtCore.QThread.__init__(self, parent=app)
        self.uiObject = uiObject
        self.turnOn = QtCore.SIGNAL("turnOn")
        self.turnOff = QtCore.SIGNAL("turnOff")

    def run(self):
        while(self.running == 1):
            p = subprocess.Popen(["cat", "/proc/acpi/bbswitch"], stdout=subprocess.PIPE)
            out, err = p.communicate()
            if ("ON" in out):
                if (self.uiObject.ALREADY_ON == 0):
					self.emit(self.turnOn)

            else:
			    if (self.uiObject.ALREADY_ON == 1):
					self.emit(self.turnOff)
				    
            time.sleep(2)    
    def stop(self):
        running = 0
def main():    
    trayIcon = SystemTrayIcon()
    trayIcon.show()
    sys.exit(app.exec_())  
if __name__ == '__main__':
    main()
