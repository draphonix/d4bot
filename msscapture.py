import mss
import win32gui
import numpy as np
from threading import Thread, Lock

class MssWindowCapture:
    window_rect = None
    w = 0
    h= 0  
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
     # threading properties
    stopped = True
    lock = None
    screenshot = None

    def __init__(self, window_name):
        self.lock = Lock()
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        # win32gui.SetForegroundWindow(self.hwnd)
        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        print(window_rect)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        

        # account for the window border and titlebar and cut them off
        # account for the window border and titlebar and cut them off
        border_pixels = 0
        titlebar_pixels = 0
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

        self.window_rect = window_rect
        self.monitor = {"top": self.window_rect[1], "left": self.window_rect[0], "width": self.w, "height": self.h}
        
    def get_screenshot(self):
        with mss.mss() as sct:
            img = sct.grab(self.monitor)
            img = np.array(img)
            img = img[...,:3]
            img = np.ascontiguousarray(img)
            return img                         # Convert to NumPy array                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y) 
    

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            # get an updated image of the game
            screenshot = self.get_screenshot()
            # lock the thread while updating the results
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()    