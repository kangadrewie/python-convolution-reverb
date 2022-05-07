from concurrent.futures.process import _system_limits_checked
from ..base.base import BaseComponent
from tkinter import Canvas
import math
class FunctionalControls(BaseComponent):
    WIDTH, HEIGHT = 300, 300
    MID_X, MID_Y = WIDTH/2, HEIGHT/2
    MIN_ANGLE, DEFAULT_ANGLE, MAX_ANGLE = -160, 0, 160
    CURRENT_VALUE = DEFAULT_ANGLE
    LAST_X_MOUSE_POS, LAST_Y_MOUSE_POS = 0, 0
    START_POS = (0, 0)

    def __init__(self, app, audioController):
        super().__init__(app)
        self.audioController = audioController
        self.canvas = Canvas(self.root, relief='flat', width=self.WIDTH, height=self.HEIGHT)

        self.bezel_coords = [self.MID_X, self.MID_Y, 100, 0, 0, 0, 0, 0]
        self.bezel_id = self.createObject(self.bezel_coords, 'grey40')

        self.base_coords = [self.MID_X, self.MID_Y, 85, 0, 0, 0, 0, 0]
        self.base_id = self.createObject(self.base_coords, 'grey60')

        self.knob_coords = [self.MID_X, self.MID_Y, 10, 60, self.DEFAULT_ANGLE, 0, 0, 0]
        self.knob_id = self.createObject(self.knob_coords, 'white')

        self.value = self.canvas.create_text(self.MID_Y, self.HEIGHT-30, font='Helvetica 12', text='50.0', fill='white')

        self.canvas.bind('<B1-Motion>', self.onVolumeChange)
        self.canvas.bind('<Button-1>', self.onPress)
        self.canvas.grid(column=1, row=0, sticky='ew', rowspan=4)

        self.volume = 50

    def createObject(self, data, color):
        x1, y1, x2, y2 = self.calculatePosition(data)
        return self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline='grey50')

    def onPress(self, event):
        print(event)
        x, y = event.x, event.y
        self.START_POS = (x,y)
    
    def slope(self, startPos, newPos):
        # Not perfect but works ok for now
        x1, y1 = startPos
        x2, y2 = newPos

        slope = (y1 - y2) / (x1 - x2)
        if (slope < 0 and x1 > 0 and x2 > self.MID_X) or (slope > 0 and x1 > 0 and x2 > self.MID_X) or slope == 0:
            return 1
        else:
            return -1

    def onVolumeChange(self, event):
        # Determine whether user is increasing/decreasing knob value
        x, y = event.x, event.y
        slope = self.slope((x,y), self.START_POS)
        if slope == 1 and self.CURRENT_VALUE < self.MAX_ANGLE:
            self.CURRENT_VALUE += 5
        if slope == -1 and self.CURRENT_VALUE > self.MIN_ANGLE:
            self.CURRENT_VALUE -= 5

        # set new knob angle
        self.knob_coords[4] = self.CURRENT_VALUE
        self.moveObject(self.knob_id, self.knob_coords)
        self.LAST_X_MOUSE_POS, self.LAST_Y_MOUSE_POS = x, y

        # Calculate volume based on current knob position
        scaler = 100 / (abs(self.MIN_ANGLE) + abs(self.MAX_ANGLE))
        self.volume = (self.CURRENT_VALUE * scaler) + 50
        self.canvas.itemconfig(self.value, text=self.volume)
        if self.audioController.isPlayable:
            self.audioController.onVolumeChange(self.volume)
    
    def calculatePosition(self, data):
        # Largely taken from - https://stackoverflow.com/questions/41451690/how-to-make-tkinter-object-move-in-circlular-path
        center_x, center_y, radius, distance, angle, angle_speed, x, y = data

        # calculate new position of object
        x = center_x - distance * math.sin(math.radians(-angle))
        y = center_y - distance * math.cos(math.radians(-angle))

        # save positon so other object can use it as its center of rotation
        data[5] = x
        data[6] = y

        # calcuate oval coordinates
        x1 = x - radius
        y1 = y - radius
        x2 = x + radius
        y2 = y + radius

        return x1, y1, x2, y2
        
    def moveObject(self, object_id, data):
        # Largely taken from - https://stackoverflow.com/questions/41451690/how-to-make-tkinter-object-move-in-circlular-path
        # calculate oval coordinates
        x1, y1, x2, y2 = self.calculatePosition(data)
        self.canvas.coords(object_id, x1, y1, x2, y2)
