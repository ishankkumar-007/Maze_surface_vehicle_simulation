import pygame
import random
vec = pygame.math.Vector2

WIDTH = 1200
HEIGHT = 900
FPS = 30

# in px/s
PLAYER_SPEED = 260
PLAYER_ROT_SPEED = 150
DRAG = 10
ROT_DRAG = 7

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
        if abs(self.rot_speed) <= ROT_DRAG:
            self.rot_speed = 0
        elif self.rot_speed > ROT_DRAG:
            self.rot_speed -= ROT_DRAG
        elif self.rot_speed < ROT_DRAG:
            self.rot_speed -= -ROT_DRAG
        
        if pygame.math.Vector2.length(self.vel) <= DRAG:
            self.vel = vec(0, 0)
        elif pygame.math.Vector2.length(self.vel) > DRAG:
            self.vel.scale_to_length(pygame.math.Vector2.length(self.vel) - DRAG)

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
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
            # rotation left
            if joystick.get_button(6) and joystick.get_button(5):
                self.rot_speed = PLAYER_ROT_SPEED
            # rotation right
            if joystick.get_button(4) and joystick.get_button(7):
                self.rot_speed = -PLAYER_ROT_SPEED
            # backward
            if joystick.get_button(6) and joystick.get_button(7):
                self.vel = vec(-PLAYER_SPEED, 0).rotate(-self.rot)
            # # backward single motor
            # if joystick.get_button(6) and not joystick.get_button(7):
            #     self.vel = vec(-PLAYER_SPEED/2, 0).rotate(-self.rot)
            # if not joystick.get_button(6) and joystick.get_button(7):
            #     self.vel = vec(-PLAYER_SPEED/2, 0).rotate(-self.rot)
            # forward
            if joystick.get_button(4) and joystick.get_button(5):
                self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            # # forward single motor
            # if joystick.get_button(4) and not joystick.get_button(5):
            #     self.vel = vec(PLAYER_SPEED/2, 0).rotate(-self.rot)
            # if not joystick.get_button(4) and joystick.get_button(5):
            #     self.vel = vec(PLAYER_SPEED/2, 0).rotate(-self.rot)


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
