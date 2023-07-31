from threading import Thread, Lock
import pyautogui
import random
import win32gui, win32con
import time
class Spam:
    stopped = False
    windowName = None
    found = False
    def __init__(self, windowName):
        self.windowName = windowName
        self.hwnd = win32gui.FindWindow(None, self.windowName)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(self.hwnd)
        self.lock = Lock()
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if self.found:
                self.lock.acquire()
                # print('Executing spam')
                pyautogui.press('shift')
                # win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 0)
                pyautogui.typewrite(['q', 'w'], interval=random.uniform(0.1, 0.2))
                pyautogui.typewrite(['2', '2', '2'], interval=random.uniform(0.1, 0.2))
                pyautogui.typewrite(['e', '3', '3'], interval=random.uniform(0.1, 0.2))
                time.sleep(0.2)
                pyautogui.typewrite(['r', '3', '3'], interval=random.uniform(0.1, 0.2))
                pyautogui.press('shift')
                self.found = False
                time.sleep(1)
                # print('Finished spam')
                self.lock.release()