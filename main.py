import cv2 as cv
import numpy as np
import os
from time import time
from msscapture import MssWindowCapture
from vision import Vision
from d4bot import DiabloBot, BotState
# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their 
# own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


DEBUG = True


# initialize the WindowCapture class
wincap = MssWindowCapture('Diablo IV')
vision = Vision()
vision.init_control_gui();
# initialize the bot
bot = DiabloBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h), vision=vision)

wincap.start()
bot.start()

while(True):

    # if we don't have a screenshot yet, don't run the code below this point yet
    if wincap.screenshot is None:
        continue

    if DEBUG:
        output_image = vision.apply_hsv_filter(wincap.screenshot)
        cv.imshow('Matches', output_image)
    else:
        bot.update_screenshot(wincap.screenshot)

        # bot is in idle mode when it first starts up
        if bot.state == BotState.IDLE:
            # if we've been in idle mode long enough, start initializing
            if time() - bot.timestamp > bot.INITIALIZING_SECONDS:
                bot.state = BotState.INITIALIZING

    # if DEBUG:
    #     # draw the detection results onto the original image
    #     detection_image = vision.draw_rectangles(wincap.screenshot, detector.rectangles)
    #     # display the images
    #     cv.imshow('Matches', detection_image)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        wincap.stop()
        # detector.stop()
        bot.stop()
        cv.destroyAllWindows()
        break

print('Done.')