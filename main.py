import cv2 as cv
import numpy as np
import os
from time import time
from msscapture import MssWindowCapture
from vision import Vision
from d4bot import DiabloBot, BotState
from hsvfilter import HsvFilter
# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their 
# own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


DEBUG = True
TEST_MODE = False

# initialize the WindowCapture class
wincap = MssWindowCapture('Diablo IV')
vision = Vision()
vision.init_control_gui()
# initialize the bot
bot = DiabloBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h), vision=vision)
hsv_filter = HsvFilter(0, 203, 37, 8, 255, 255, 0, 0, 0, 0)
wincap.start()
bot.start()
try:           
    while(True):
        # if we don't have a screenshot yet, don't run the code below this point yet
        if wincap.screenshot is None:
            continue
        
        if TEST_MODE:
            output_image = vision.apply_hsv_filter(wincap.screenshot)
            cv.imshow('Matches', output_image)
        else:
            # pre-process the image
            processed_image = vision.apply_hsv_filter(wincap.screenshot, hsv_filter)
            bot.update_screenshot(processed_image)
            # bot is in idle mode when it first starts up
            # if bot.state == BotState.IDLE:
            #     # if we've been in idle mode long enough, start initializing
            #     if time() - bot.timestamp > bot.INITIALIZING_SECONDS:
            #         bot.state = BotState.INITIALIZING
            if DEBUG:
                # if bot.debugPoint is None:
                #     continue
                # rectangles = vision.find(processed_image, cv.imread('./images/mob.jpg', cv.IMREAD_UNCHANGED), 0.56)
                # output_image = vision.draw_rectangles(wincap.screenshot, rectangles)
                raw = vision.apply_hsv_filter(wincap.screenshot)
                # cv.imshow('Matches', output_image)
                cv.imshow('Raw', raw)

            
        
        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        key = cv.waitKey(1)
        if key == ord('='):
            wincap.stop()
            # detector.stop()
            bot.stop()
            cv.destroyAllWindows()
            break
except KeyboardInterrupt:
    wincap.stop()
    # detector.stop()
    bot.stop()
    cv.destroyAllWindows()

print('Done.')
