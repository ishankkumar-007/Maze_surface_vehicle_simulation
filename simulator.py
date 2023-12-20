import pygame
import random
from os import path
vec = pygame.math.Vector2

WIDTH = 1216   # 38 x 32
HEIGHT = 896   # 28 x 32
FPS = 30
TILESIZE = 32
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

# in px/s
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 150
# DRAG = 10
# ROT_DRAG = 7
DRAG_COEFF = 0.11

# define colors
WHITE = (255, 255, 255)
LIGHTGREY = (40, 40, 40)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# load game_map
game_folder = path.dirname(__file__)
map_data = []
with open(path.join(game_folder, 'map.txt'), 'rt') as f:
    for line in f:
        map_data.append(line)


# boat
boat_2 = pygame.image.load("./images/boat_2.png")
boat_2 = pygame.transform.scale(boat_2, (30, 91))
boat_2_width = 30
boat_2_height = 91

# background 
background = pygame.image.load("./images/background_main.jpeg")

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_org = boat_2
        self.image = boat_2
        self.rect = self.image.get_rect()
        self.pos = vec(4*TILESIZE, 4*TILESIZE)
        self.rect.center = self.pos
        self.rect.center = (40, 50)
        self.thrust = 260  # in px/s
        self.vel = vec(0, 0)
        self.rot = -90
        self.rot_speed = 0

    def boundary_constraints(self):
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
        if self.pos.y < 0:
            self.pos.y = 0

    def get_keys(self): 
        # changes due to drag
        if abs(self.rot_speed) <= abs(DRAG_COEFF * self.rot_speed):
            self.rot_speed = 0
        else:
            self.rot_speed -= DRAG_COEFF * self.rot_speed
        
        if pygame.math.Vector2.length(self.vel) <= DRAG_COEFF * pygame.math.Vector2.length(self.vel):
            self.vel = vec(0, 0)
        elif pygame.math.Vector2.length(self.vel) > DRAG_COEFF * pygame.math.Vector2.length(self.vel) and round(pygame.math.Vector2.length(self.vel)) != 0:
            self.vel.scale_to_length(pygame.math.Vector2.length(self.vel) - DRAG_COEFF * pygame.math.Vector2.length(self.vel))

        # motor input
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rot_speed = PLAYER_ROT_SPEED
        if key[pygame.K_RIGHT]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if key[pygame.K_UP]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if key[pygame.K_DOWN]:
            self.vel = vec(-PLAYER_SPEED, 0).rotate(-self.rot)

        # joystick control
        if event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN:
            # axis 0, b3 and b0
            rudder = round(joystick.get_axis(0), 1)   # for left and right rotation
            up = joystick.get_button(3)
            down = joystick.get_button(0)
            # rotation left
            if rudder < -0.5 and (up or down):
                self.rot_speed = PLAYER_ROT_SPEED
            # rotation right
            if rudder > 0.5 and (up or down):
                self.rot_speed = -PLAYER_ROT_SPEED
            # forward
            if up:
                self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            # forward single motor
            if down:
                self.vel = vec(-PLAYER_SPEED, 0).rotate(-self.rot)

    def collide_with_walls(self):
        self.rect.centerx = self.pos.x
        for wall in pygame.sprite.spritecollide(self, walls, False):
            if self.vel.x > 0:
                self.rect.right = wall.rect.left
            elif self.vel.x < 0:
                self.rect.left = wall.rect.right
            self.pos.x = self.rect.centerx

        self.rect.centery = self.pos.y
        for wall in pygame.sprite.spritecollide(self, walls, False):
            if self.vel.y > 0:
                self.rect.bottom = wall.rect.top
            elif self.vel.y < 0:
                self.rect.top = wall.rect.bottom
            self.pos.y = self.rect.centery


    def update(self, dt):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * dt) % 360
        self.image = pygame.transform.rotate(self.image_org, self.rot+90)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # self.pos = self.pos + self.vel
        self.pos += (self.vel[0] * dt, self.vel[1] * dt)
        self.boundary_constraints()
        self.collide_with_walls()
        self.rect.center = self.pos
        # self.rect.x = self.pos[0]
        # self.rect.y = self.pos[1]
        # self.collide_with_walls('y')


class Wall(pygame.sprite.Sprite):
    # sprite for the Wall
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE



# initialize pygame and create window
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joystick = pygame.joystick.Joystick(0)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
Icon = pygame.image.load('./images/auv.png')
pygame.display.set_caption("SIMULATOR")
pygame.display.set_icon(Icon)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# making the walls
for row, tiles in enumerate(map_data):
    for col, tile in enumerate(tiles):
        if tile == '1':
            wall = Wall(col, row)
            walls.add(wall)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pygame.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pygame.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False 

    # Update
    all_sprites.update(dt)

    # Draw / render
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    walls.draw(screen)
    draw_grid()
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.joystick.quit()
pygame.quit()
