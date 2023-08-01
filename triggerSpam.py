from spam import Spam
import cv2 as cv
import tkinter as tk



class App:
    def __init__(self, window):
        self.spam = Spam('Diablo IV')
        self.window = window
        self.running = False

        self.start_button = tk.Button(window, text='Start', width=25, command=self.start_command)
        self.start_button.pack()

        self.stop_button = tk.Button(window, text='Stop', width=25, command=self.stop_command)
        self.stop_button.pack()
        
        
    def start_command(self):
        self.spam.start()
        print('Start Button Pressed')
        self.running = True
        
        self.loop()
        

    def stop_command(self):
        print('Stop Button Pressed')
        self.running = False
        self.spam.stop()

    def loop(self):
        try: 
            if self.running:
                # Replace with your code
                print('Loop iteration')
                self.spam.found = True
                # Schedule the next iteration; 1000 ms = 1 s
                self.window.after(1000, self.loop)
        except KeyboardInterrupt:
            self.running = False
            self.spam.stop()
            print('Exiting')
            exit(0)

window = tk.Tk()
window.title('My App')
app = App(window)
window.mainloop()