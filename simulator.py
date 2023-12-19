import pygame
import random
vec = pygame.math.Vector2

WIDTH = 1200
HEIGHT = 900
FPS = 30

# in px/s
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 200
# DRAG = 10
# ROT_DRAG = 7
DRAG_COEFF = 0.11

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

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
        self.pos = vec(40, 50)
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
            if rudder < -0.5:
                self.rot_speed = PLAYER_ROT_SPEED
            # rotation right
            if rudder > 0.5:
                self.rot_speed = -PLAYER_ROT_SPEED
            # forward
            if up:
                self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            # forward single motor
            if down:
                self.vel = vec(-PLAYER_SPEED, 0).rotate(-self.rot)

    def update(self, dt):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * dt) % 360
        self.image = pygame.transform.rotate(self.image_org, self.rot+90)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # self.pos = self.pos + self.vel
        self.pos += (self.vel[0] * dt, self.vel[1] * dt)
        self.boundary_constraints()
        self.rect.center = self.pos


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
player = Player()
all_sprites.add(player)

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
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.joystick.quit()
pygame.quit()
