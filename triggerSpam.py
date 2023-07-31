from spam import Spam
import cv2 as cv
import tkinter as tk

spam = Spam('Diablo IV')

try:
    spam.start()
    while(True):
        spam.found = True
except KeyboardInterrupt:
    spam.stop()