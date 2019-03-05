try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math, random
from lib.util.Vector import Vector

CANVASWIDTH = 500
CANVASHEIGHT = 500


class Button:
    def __init__(self, canvas, pos, txt):
        self.canvas = canvas
        self.pos = pos
        self.xRat = 1.045
        self.yRat = 6
        self.width = 5
        self.colour = "White"
        self.txt = txt
        self.point1 = pos
        self.point2 = [self.pos[0] + CANVASWIDTH / self.xRat, self.pos[1]]
        self.point3 = [self.pos[0] + CANVASWIDTH / self.xRat, self.pos[1] + CANVASHEIGHT / self.yRat]
        self.point4 = [self.pos[0], self.pos[1] + CANVASHEIGHT / self.yRat]

    def draw(self):
        self.canvas.draw_polygon([self.point1, self.point2, self.point3, self.point4], self.width, self.colour)
        self.canvas.draw_text(self.txt, [self.pos[0] * 4, self.pos[1] + CANVASHEIGHT / self.yRat / 1.5], 50,
                              self.colour, 'monospace')


class Menu:
    def __init__(self):
        print("INIT")

    def draw(self, canvas):
        self.canvas = canvas
        button = Button(self.canvas, [CANVASWIDTH / 50, CANVASHEIGHT / 2.5], "Start")
        button1 = Button(self.canvas, [CANVASWIDTH / 50, CANVASHEIGHT / 1.67], "LeaderBoard")
        button2 = Button(self.canvas, [CANVASWIDTH / 50, CANVASHEIGHT / 1.25], "Exit")
        button.draw()
        button1.draw()
        button2.draw()


frame = simplegui.create_frame("Game", CANVASWIDTH, CANVASHEIGHT)
menu = Menu()
frame.set_draw_handler(menu.draw)
frame.start()