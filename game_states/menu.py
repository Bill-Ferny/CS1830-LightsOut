import pygame
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from lib.state_machine.states import States
import os
from lib.player.inventory import Inventory
from game_states.Torch import Torch

class Button:
    def __init__(self, canvas, pos, txt, colour_txt, colour_back, settings):
        self.settings = settings
        self.canvas = canvas
        self.pos = pos
        self.xRat = 1.045
        self.yRat = 6
        self.width = 10
        self.colourTxt = colour_txt
        self.colourBack = colour_back
        self.txt = txt
        self.point1 = pos
        self.point2 = [self.pos[0] + self.settings.get('width')/self.xRat, self.pos[1]]
        self.point3 = [self.pos[0] + self.settings.get('width')/self.xRat, self.pos[1] + self.settings.get('height')/self.yRat]
        self.point4 = [self.pos[0], self.pos[1] + self.settings.get('height')/self.yRat]

    def draw(self):
        self.canvas.draw_polygon([self.point1, self.point2, self.point3, self.point4], self.width, self.colourTxt,
                                 self.colourBack)
        self.canvas.draw_text(self.txt, [self.pos[0] * 4, self.pos[1] + self.settings.get('height') / self.yRat / 2],
                              50, self.colourTxt, self.settings.get('font'))


class Menu(States):
    def __init__(self, settings):
        States.__init__(self)
        self.settings = settings
        self.font = self.settings.get('font')
        self.next = None
        self.startPos = [self.settings.get('width') / 50, self.settings.get('height') / 2.5]
        self.helpPos = [self.settings.get('width') / 50, self.settings.get('height') / 1.67]
        self.exitPos = [self.settings.get('width') / 50, self.settings.get('height') / 1.25]
        self.backPos = [[10, 10], [10, 50], [50, 50], [50, 10]]
        self.arrowPos = [[20, 30], [30, 40], [30, 20]]
        self.arrowShaftPos = [[30, 30], [40, 30]]
        self.backX = 50
        self.backY = 50
        self.isStart = False
        self.isHelp = False
        self.isLeader = False
        self.isMenu = True
        self.isExit = False
        self.pos = None
        self.torch = Torch()
        self.inven = Inventory(3, 100, 1000, 750)
#        self.player = Player(1000/2, 750/2, 3, self.inven)

    def drag(self, pos):
        self.pos = pos

    # Override
    def click(self, pos):
        self.pos = pos

        if self.isMenu and self.startButton.point1[1] < self.pos[1] < self.startButton.point4[1]:
            self.next = 'gamePlay'
            self.done = True

        if self.isMenu and self.helpButton.point1[1] < self.pos[1] < self.helpButton.point4[1]:
            self.isStart = False
            self.isHelp = True
            self.isLeader = False
            self.isMenu = False

        if self.isMenu and self.leaderButton.point1[1] < self.pos[1] < self.leaderButton.point4[1]:
            self.next = 'leaderboard'
            self.done = True

        if self.isMenu and self.pos[0] < self.backX and self.pos[1] < self.backY:
            self.isExit = True

        if (self.isStart or self.isHelp or self.isLeader) and self.pos[0] < self.backX and self.pos[1] < self.backY:
            self.isStart = False
            self.isHelp = False
            self.isLeader = False
            self.isMenu = True

    # Override
    def draw(self, canvas):
        self.pos = pygame.mouse.get_pos()
        self.startButton = Button(canvas, self.startPos, "Start", 'White', 'Black', self.settings)
        self.helpButton = Button(canvas, self.helpPos, "Help", 'White', 'Black', self.settings)
        self.leaderButton = Button(canvas, self.exitPos, "LeaderBoard", 'White', 'Black', self.settings)
        if self.startButton.point1[1] < self.pos[1] < self.startButton.point4[1] * 1.1:
            self.startButton.colourBack = 'White'
            self.helpButton.colourBack = 'Black'
            self.leaderButton.colourBack = 'Black'
            self.startButton.colourTxt = 'Black'
            self.helpButton.colourTxt = 'White'
            self.leaderButton.colourTxt = 'White'
        elif self.helpButton.point1[1] < self.pos[1] < self.helpButton.point4[1] * 1.1:
            self.startButton.colourBack = 'Black'
            self.helpButton.colourBack = 'White'
            self.leaderButton.colourBack = 'Black'
            self.startButton.colourTxt = 'White'
            self.helpButton.colourTxt = 'Black'
            self.leaderButton.colourTxt = 'White'
        elif self.leaderButton.point1[1] < self.pos[1] < self.leaderButton.point4[1] * 1.1:
            self.startButton.colourBack = 'Black'
            self.helpButton.colourBack = 'Black'
            self.leaderButton.colourBack = 'White'
            self.startButton.colourTxt = 'White'
            self.helpButton.colourTxt = 'White'
            self.leaderButton.colourTxt = 'Black'
        else:
            self.startButton.colourBack = 'Black'
            self.helpButton.colourBack = 'Black'
            self.leaderButton.colourBack = 'Black'
            self.startButton.colourTxt = 'White'
            self.helpButton.colourTxt = 'White'
            self.leaderButton.colourTxt = 'White'

        if self.isMenu:
            #canvas.draw_text("LightsOut", (self.settings.get('width') / 7, self.settings.get('height') / 4), self.settings.get('width')
             #                / 7.5, "White", self.font)
            img = simplegui._load_local_image(os.path.join(os.path.dirname(__file__), "../logo.png"))
            canvas.draw_image(img, (img.get_width()/2, img.get_height()/2), (img.get_width(), img.get_height()), (self.settings.get('width')/2 , 100), (800, 400))
            self.startButton.draw()
            self.helpButton.draw()
            self.leaderButton.draw()
            canvas.draw_polygon(self.backPos, 4, "Red")
            canvas.draw_line(self.backPos[0], self.backPos[2], 2, 'Red')
            canvas.draw_line(self.backPos[1], self.backPos[3], 2, 'Red')

        if self.isStart:
            canvas.draw_polygon(self.backPos, 4, "White")
            canvas.draw_polygon(self.arrowPos, 4, "White")
            canvas.draw_polygon(self.arrowShaftPos, 4, "White")
            self.player.draw(canvas)

        if self.isHelp:
            canvas.draw_text("Press arrow keys to move the player", [15, 150], 30, 'White', 'monospace')
            canvas.draw_text("Move mouse to move the torch", [15, 225], 30, 'White', 'monospace')
            canvas.draw_text("Use 1, 2 and 3 to cycle through the inventory slots", [15, 300], 30, 'White', 'monospace')
            canvas.draw_text("Your score will increase the longer you survive", [15, 375], 30, 'White', 'monospace')
            canvas.draw_text("You can submit your score via the online leaderboard", [15, 450], 30, 'White', 'monospace')
            canvas.draw_text("And most importantly don't let the monsters catch you!", [15, 525], 30, 'White', 'monospace')
            canvas.draw_text("How to Play", [350, 75], 80, 'monospace')
            canvas.draw_polygon(self.backPos, 4, "White")
            canvas.draw_polygon(self.arrowPos, 4, "White")
            canvas.draw_polygon(self.arrowShaftPos, 4, "White")

        if self.isLeader:
            self.next = 'leaderboard'
            self.done = True

        if self.isExit:
            exit()
