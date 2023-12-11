# Pygame sprite Example
import pygame
import random
vec = pygame.math.Vector2
# from os import path

WIDTH = 1200
HEIGHT = 900
FPS = 30

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
        # self.rect.center = (WIDTH/2, HEIGHT/2)
        self.rot = -90
        self.clockwise_rot_speed = 5
        self.anticlockwise_rot_speed = -5
    
    def rot_clockwise(self):
        self.rot += self.clockwise_rot_speed
        self.vel.rotate(self.clockwise_rot_speed)
        self.image = pygame.transform.rotate(self.image_org, self.rot+90)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def rot_anticlockwise(self):
        self.rot += self.anticlockwise_rot_speed
        self.vel.rotate(self.anticlockwise_rot_speed)
        self.image = pygame.transform.rotate(self.image_org, self.rot+90)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def move_forward(self):
        self.vel = vec(self.thrust * dt, 0).rotate(-self.rot)
        self.pos += self.vel
        self.rect.center = self.pos

    def move_backward(self):
        self.vel = vec(-self.thrust * dt, 0).rotate(-self.rot)
        self.pos += self.vel
        self.rect.center = self.pos

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
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rot_clockwise()
        if key[pygame.K_RIGHT]:
            self.rot_anticlockwise()
        if key[pygame.K_UP]:
            self.move_forward()
        if key[pygame.K_DOWN]:
            self.move_backward()

        if key[pygame.K_z] and key[pygame.K_s]:
            self.rot_clockwise()
        if key[pygame.K_x] and key[pygame.K_a]:
            self.rot_anticlockwise()
        if key[pygame.K_a] and key[pygame.K_s]:
            self.move_forward()
        if key[pygame.K_z] and key[pygame.K_x]:
            self.move_backward()


    def update(self, dt):
        self.get_keys()
        
        self.boundary_constraints()


# initialize pygame and create window
pygame.init()
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

pygame.quit()
