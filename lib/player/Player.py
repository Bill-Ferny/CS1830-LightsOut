import sys, pygame, os, math
try:
    import simplegui
except ImportError:
    sys.argv.append('--no-controlpanel')
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from lib.player.interactions.player_move import PlayerMove
from lib.player.interactions.change_slot import ChangeSlot
from lib.player.inventory import Inventory
from lib.util.vector import Vector
from lib.player.interactions.Quit import Quit



class Player:

    def __init__(self, x_pos, y_pos, lives, kbd):
        self.inven = Inventory(3, 100, 2 * x_pos, 2 * y_pos)
        # self.kbd = Keyboard()
        self.kbd = kbd
        self.player_move = PlayerMove(self, self.kbd)
        self.change_slot = ChangeSlot(self.inven, self.kbd)
        self.quit = Quit(self, self.kbd)
        self.x = x_pos
        self.y = y_pos
        self.pos = (x_pos, y_pos)
        self.max_health = 100
        self.health = self.max_health
        self.lives = lives
        self.dead = False
        self.game_over = False
        self.is_moving = False
        self.mouse_pos = pygame.mouse.get_pos()
        x = os.path.join(os.path.dirname(__file__), "../../textures/sprite_sheets/player/playersprite.png")
        y = os.path.join(os.path.dirname(__file__), "../../textures/sprite_sheets/player/heart.png")
        self.img = simplegui._load_local_image(x)
        self.hpimg = simplegui._load_local_image(y)
        self.height = 180
        self.width = 411
        self.frame_width = self.width / 3
        self.frame_centre = self.frame_width / 2
        self.frame_index = 0
        self.frame_up = True
        self.clock = 0
        self.rot = 0
        self.speed = 5  # amount of frames per sprite update
        self.score = 0

    def draw(self, canvas):
        # inventory
        self.inven.draw(canvas)
        # sprite
        canvas.draw_image(self.img, (self.frame_width * self.frame_index + self.frame_centre, self.height / 2),
                          (self.frame_width, self.height), self.pos, (50, 50), self.rot)
        # health bar
        canvas.draw_line((9 * self.health + 50, 2 * self.y - 150), (9 * self.max_health + 50, 2 * self.y - 150),
                         10, 'White')
        canvas.draw_line((50, 2 * self.y - 150), (9 * self.health + 50, 2 * self.y - 150), 10, 'Red')
        # lives
        for i in range(0, self.lives):
            canvas.draw_image(self.hpimg, (112.5, 112.5), (225, 225), (60 * i + 50, 50), (50, 50))
        # score
        canvas.draw_text('Score: ' + str(self.score), (self.width * 2 - 20, 50), 40, 'White')

    def update(self):
        self.player_move.update()
        self.change_slot.update()
        self.quit.update()
        self.inven.update()
        self.update_rot()
        self.clock += 1
        if self.clock % self.speed == 0:
            self.update_sprite()
        if self.clock % 20 == 0:
            self.update_score()

    def update_score(self, increase=1):
        self.score += increase
        self.inven.score += increase

    def update_rot(self):
        if Vector(self.x, self.y).copy().subtract(Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])).length() >= self.inven.torch.lightRadius-20:
            self.mouse_pos = pygame.mouse.get_pos()
        if self.mouse_pos[0] > self.x and self.mouse_pos[1] > self.y:
            self.rot = -(math.pi + math.asin(
                (self.mouse_pos[0] - self.x) / math.sqrt(math.pow(self.mouse_pos[0] - self. x, 2) +
                                                         math.pow(self.mouse_pos[1] - self.y, 2))))
        if self.mouse_pos[0] > self.x and self.mouse_pos[1] < self.y:
            self.rot = math.asin(
                (self.mouse_pos[0] - self.x) / math.sqrt(math.pow(self.mouse_pos[0] - self. x, 2) +
                                                         math.pow(self.mouse_pos[1] - self.y, 2)))
        if self.mouse_pos[0] < self.x and self.mouse_pos[1] < self.y:
            self.rot = math.asin(
                (self.mouse_pos[0] - self.x) / math.sqrt(math.pow(self.mouse_pos[0] - self. x, 2) +
                                                         math.pow(self.mouse_pos[1] - self.y, 2)))
        if self.mouse_pos[0] < self.x and self.mouse_pos[1] > self.y:
            self.rot = -(math.pi + math.asin(
                (self.mouse_pos[0] - self.x) / math.sqrt(math.pow(self.mouse_pos[0] - self. x, 2) +
                                                         math.pow(self.mouse_pos[1] - self.y, 2))))

    def update_sprite(self):
        if self.is_moving:
            if self.frame_up:
                self.frame_index += 1
                if self.frame_index == 3:
                    self.frame_up = False
            if not self.frame_up:
                self.frame_index -= 1
                if self.frame_index == 0:
                    self.frame_up = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.lives -= 1
            self.health = self.max_health
        if self.lives == -1:
            self.final_score = self.score
            self.game_over = True

    def get_score(self):
        return self.final_score

if __name__ == '__main__':
    CANVASWIDTH = 1000
    CANVASHEIGHT = 750

    player = Player(CANVASWIDTH / 2, CANVASHEIGHT / 2, 3)


    def draw(canvas):

        player.update()
        player.draw(canvas)

    frame = simplegui.create_frame("Game", CANVASWIDTH, CANVASHEIGHT)
    frame.set_canvas_background('Grey')
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(player.kbd.key_down)
    frame.set_keyup_handler(player.kbd.key_up)
    frame.start()
