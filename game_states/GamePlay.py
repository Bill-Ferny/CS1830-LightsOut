import pygame
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
from lib.state_machine.states import States
from lib.map.map import Map

CANVASWIDTH = 1000
CANVASHEIGHT = 750


class GamePlay(States):
    def __init__(self, settings):
        States.__init__(self)
        self.zoom = 2
        self.mapPos = [CANVASWIDTH/2,CANVASHEIGHT/2]
        self.mousePos = [0,0]

    def draw(self, canvas):

        mousePosStart = pygame.mouse.get_pos()
        self.mousePos[0] = mousePosStart[0]-252
        self.mousePos[1] = mousePosStart[1]-27
        self.drawMap(canvas)


if __name__ == '__main__':
    settings = {
        'width': 1000,
        'height': 750,
        'font': 'monospace',
        'fps': 60
    }
    frame = simplegui.create_frame("LightsOut", CANVASWIDTH, CANVASHEIGHT)
    gamePlay = GamePlay(settings)
    frame.set_draw_handler(gamePlay.draw)
    frame.start()
