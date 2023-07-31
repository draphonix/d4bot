import cv2 as cv
import numpy as np
import os
from vision import Vision


vision = Vision(method=cv.TM_CCOEFF_NORMED)
stack = cv.imread('./images/newfilter.jpg', cv.IMREAD_REDUCED_COLOR_2)
target = cv.imread('./images/mob3.jpg', cv.IMREAD_REDUCED_COLOR_2)
rectangles = vision.find(stack, target, 0.55)
output_image = vision.draw_rectangles(stack, rectangles)
cv.imshow('Matches', output_image)
cv.waitKey()


