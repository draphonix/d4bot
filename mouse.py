import pyautogui
#  print mouse location
while True:
        try:
                x, y = pyautogui.position()
                print("mouse location: ", x, y)
                # print("mouse location: ", pyautogui.position())
        except KeyboardInterrupt:
                print('\n')
                break