import cv2 as cv
import pyautogui
import random
from time import sleep, time
from threading import Thread, Lock
from math import sqrt
from vision import Vision

class BotState:
    INITIALIZING = 0
    SEARCH_FOR_MOB = 1
    SEARCH_FOR_BOSS = 2
    SEARCH_FOR_REVIVE = 3
    SEARCH_FOR_BROKEN_GEAR = 4
    FIGHT = 5
    IDLE = 6

class DiabloBot:
    # constants
    INITIALIZING_SECONDS = 6
    MATCH_THRESHOLD = 0.8
    IGNORE_RADIUS = 130
    # threading properties
    stopped = True
    lock = None

    # properties
    state = None
    targets = []
    screenshot = None
    timestamp = None
    movement_screenshot = None
    window_offset = (0,0)
    window_w = 0
    window_h = 0
    click_history = []

    # preload images
    revive_button = None
    broken_gear = None
    vision = None
    capture = None

    def __init__(self, window_offset, window_size, vision):
        # create a thread lock object
        self.lock = Lock()

        # for translating window positions into screen positions, it's easier to just
        # get the offsets and window size from WindowCapture rather than passing in 
        # the whole object
        self.window_offset = window_offset
        self.window_w = window_size[0]
        self.window_h = window_size[1]

        # pre-load the needle image used to confirm our object detection
        self.revive_button = cv.imread('./images/reviveButton.jpg', cv.IMREAD_UNCHANGED)
        self.broken_gear = cv.imread('./images/brokenGear.jpg', cv.IMREAD_UNCHANGED)
        self.mob_health_bar = cv.imread('./images/mobHealthBar.jpg', cv.IMREAD_UNCHANGED)
        self.boss_health_bar = cv.imread('./images/bossHealthBar.jpg', cv.IMREAD_UNCHANGED)


        # start bot in the initializing mode to allow us time to get setup.
        # mark the time at which this started so we know when to complete it
        self.state = BotState.IDLE
        self.timestamp = time()
        self.vision = vision

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True
    
    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def find_revive_button(self):
        rectangles = self.vision.find(self.screenshot, self.revive_button, self.MATCH_THRESHOLD)
        points = self.vision.get_click_points(rectangles)
        return points

    def find_broken_gear(self):
        rectangles = self.vision.find(self.screenshot, self.broken_gear, self.MATCH_THRESHOLD)
        points = self.vision.get_click_points(rectangles)
        return points
    
    def find_mobs(self):
        rectangles = self.vision.find(self.screenshot, self.mob_health_bar, self.MATCH_THRESHOLD)
        points = self.vision.get_click_points(rectangles)
        nearest_targets = self.targets_ordered_by_distance(points)
        return nearest_targets
    
    def find_boss(self):
        rectangles = self.vision.find(self.screenshot, self.boss_health_bar, self.MATCH_THRESHOLD)
        points = self.vision.get_click_points(rectangles)
        nearest_targets = self.targets_ordered_by_distance(points)
        return nearest_targets
    
    def perform_actions(self, point):
        pyautogui.moveTo(point[0], point[1])
        pyautogui.keyDown('shift')
        pyautogui.typewrite(['q', 'w', 'e', '3', '3', '2', '2', '2', 'r', '3', '3'], interval=random.uniform(0.1, 0.2))
        pyautogui.keyUp('shift')
        
    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the WindowCapture __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.window_offset[0], pos[1] + self.window_offset[1])

    def targets_ordered_by_distance(self, targets):
        # our character is always in the center of the screen
        my_pos = (self.window_w / 2, self.window_h / 2)
        # searched "python order points by distance from point"
        # simply uses the pythagorean theorem
        # https://stackoverflow.com/a/30636138/4655368
        def pythagorean_distance(pos):
            return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
        targets.sort(key=pythagorean_distance)

        # print(my_pos)
        # print(targets)
        # for t in targets:
        #    print(pythagorean_distance(t))

        # ignore targets at are too close to our character (within 130 pixels) to avoid 
        # re-clicking a deposit we just mined
        targets = [t for t in targets if pythagorean_distance(t) > self.IGNORE_RADIUS]

        return targets
     # main logic controller
    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                # do no bot actions until the startup waiting period is complete
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    # start searching when the waiting period is over
                    self.lock.acquire()
                    self.state = BotState.SEARCH_FOR_REVIVE
                    self.lock.release()

            elif self.state == BotState.SEARCH_FOR_REVIVE:
                # check the given click point targets, confirm a limestone deposit,
                # then click it.
                points = self.find_revive_button()
                
                # if the points list is empty, we didn't find any targets
                if len(points) == 0:
                    # switch state to searching
                    self.lock.acquire()
                    self.state = BotState.SEARCH_FOR_MOB
                    self.lock.release()
                else:
                    # points should contain only one item
                    # click the first point in the list
                    self.lock.acquire()
                    pyautogui.click(self.get_screen_position(points[0]))
                    sleep(1)
                    self.state = BotState.SEARCH_FOR_BROKEN_GEAR
                    self.lock.release()
            elif self.state == BotState.SEARCH_FOR_BROKEN_GEAR:
                # This is the case where you have been death for multiple times and your gear might be broken.
                # Shouldnt continue fighting, should go back to town
                points = self.find_broken_gear()
                if(len(points) == 0):
                    self.lock.acquire()
                    self.state = BotState.SEARCH_FOR_MOB
                    self.lock.release()
                else:
                    self.lock.acquire()
                    # Go back to town
                    pyautogui.typewrite("t")
                    sleep(1)
                    # Todo: repair gear, go back to fight
                    self.state = BotState.IDLE
                    self.lock.release()
            elif self.state == BotState.SEARCH_FOR_MOB:
                self.lock.acquire()
                points = self.find_mobs()
                if(len(points) == 0):
                    self.state = BotState.SEARCH_FOR_BOSS
                    self.lock.release()
                else:
                    for point in points:
                        self.perform_actions(point)
                    self.state = BotState.SEARCH_FOR_MOB
                    self.lock.release()
            elif self.state == BotState.SEARCH_FOR_BOSS:
                self.lock.acquire()
                points = self.find_boss()
                if(len(points) == 0):
                    self.state = BotState.SEARCH_FOR_MOB
                    self.lock.release()
                else:
                    for point in points:
                        self.perform_actions(point)
                    self.state = BotState.SEARCH_FOR_BOSS
                    self.lock.release()