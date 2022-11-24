import win32gui
import win32.lib.win32con as win32con
import pyautogui
from time import sleep

class Operate():
    
    def __init__(self):
        jantama = win32gui.FindWindow(None,'jantama')
        win32gui.SetForegroundWindow(jantama)
        win32gui.ShowWindow(jantama, win32con.SW_MAXIMIZE)

    def screenshot(self):
        sleep(1)
        s = pyautogui.screenshot()
        s.save('screenshot1.png')

if __name__ == "__main__":
    operate = Operate()
    operate.screenshot()