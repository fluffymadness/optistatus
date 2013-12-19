#
# Optistatus 
# @author fluffymadness
#

import wx
import subprocess
import time
import threading

running = 1
def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item
    
class TaskBarIcon(wx.TaskBarIcon):
    ALREADY_ON = 0
    TRAY_TOOLTIP = 'Optistatus'
    TRAY_ICON = '/usr/share/pixmaps/optistatus-inactive.png'
    TRAY_ICON_ACTIVE = '/usr/share/pixmaps/optistatus-active.png'

    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(self.TRAY_ICON)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon, self.TRAY_TOOLTIP)

    def on_exit(self, event):
        global running
        running = 0
        for t in threads:
            t.join()
        wx.CallAfter(self.Destroy)
        
class OptirunChecker(threading.Thread):
    uiObject = ""
    def __init__(self, threadID, uiObject):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.uiObject = uiObject
    def run(self):
        # Get lock to synchronize threads
        threadLock.acquire()
        self.check_optirun()
        # Free lock to release next thread
        threadLock.release()

    def check_optirun(self):
        global running
        while(running == 1):
            p = subprocess.Popen(["cat", "/proc/acpi/bbswitch"], stdout=subprocess.PIPE)
            out, err = p.communicate()
            if ("ON" in out):
			    if (self.uiObject.ALREADY_ON == 0):
			        self.uiObject.set_icon(self.uiObject.TRAY_ICON_ACTIVE)
			        self.uiObject.ALREADY_ON = 1
            else:
			    if (self.uiObject.ALREADY_ON == 1):
				    self.uiObject.set_icon(self.uiObject.TRAY_ICON)
				    self.uiObject.ALREADY_ON = 0
            time.sleep(2)    
threadLock = threading.Lock()
threads = []

def main():
    app = wx.PySimpleApp()
    temp = TaskBarIcon()
    optirunchecker = OptirunChecker(1,temp)
    optirunchecker.start()
    app.MainLoop()

if __name__ == '__main__':
    main()
