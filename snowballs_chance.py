""" What this needs now is a fifth obstacle, lower down. Then a title screen. Then we can work on a timer countdown and a game over screen giving you
your silvers, golds and net total!

And perhaps... PERHAPS... a funky background image?"""

import pygame
import random
import os

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()

pygame.display.set_caption("Snowball's Chance")

# Set the font
font = pygame.font.SysFont("Arial", 20, False, False)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#make mouse cursor invisible
pygame.mouse.set_visible(False)

#create the list of snowballs
snowball_list = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

#store scores
score = 0
antiscore = 0

spawn_ticker = 0

#define the classes
class Snowball(pygame.sprite.Sprite):
    def __init__(self):
        """ initialises a Snowball object """
        #initialise parent class constructor
        super().__init__()
        #create the surface and give it a black background
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        #other attributes
        self.rect = self.image.get_rect()
        self.velocity = 2
        #draw the circle
        pygame.draw.circle(self.image, WHITE, (10, 10), 10, 0)

    def update(self):
        """ Called each frame """
        if self.rect.centerx < player.rect.centerx:
            self.rect.centerx += self.velocity + random.randrange(-3,4)
        if self.rect.centerx > player.rect.centerx:
            self.rect.centerx -= self.velocity - random.randrange(-3,4)
        self.rect.centery += self.velocity + random.randrange(-3,4)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(BLUE)
        self.right = True
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, BLUE, self.rect, 0)

    def update(self):
        if self.right:
            self.rect.x += 2
            if self.rect.right >= 700:
                self.right = False
        else:
            self.rect.x -= 2
            if self.rect.left <= 0:
                self.right = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """initialises the player object"""
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #draw the player
        pygame.draw.rect(self.image, RED, self.rect, 0)

    def update(self):
        self.rect.centerx = mouse_pos[0]

#create the snowballs
def create_snowballs():
    for i in range(25):
        #create one
        snowball = Snowball()
        #set its x-y coords
        snowball.rect.x = random.randrange(700)
        snowball.rect.y = 0
        #add it to the list
        snowball_list.add(snowball)
        all_sprites_list.add(snowball)

#create the player
player = Player()
player.rect.centerx = 350
player.rect.centery = 450
all_sprites_list.add(player)

#create the obstacles
def create_obstacle(x, y, right):
    obstacle = Obstacle()
    obstacle.rect.centerx = x
    obstacle.rect.centery = y
    obstacle.right = right
    obstacle_list.add(obstacle)
    all_sprites_list.add(obstacle)

create_obstacle(100, 150, False)
create_obstacle(200, 200, True)
create_obstacle(300, 250, False)
create_obstacle(400, 300, True)

# -------- Main Program Loop -----------
while not done:
    # --- Main event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True

    # --- Game logic
    #get the mouse position this frame
    mouse_pos = pygame.mouse.get_pos()

    #handle spawning
    spawn_ticker += 1
    if spawn_ticker == 120:
        create_snowballs()
    if spawn_ticker == 500:
        spawn_ticker = 0

    #update each item on the list(bear in mind this
    #probably won't work if the list contains sprites
    #without an update() method
    all_sprites_list.update()

    #create collision lists - no real use for melted rn but might be useful later
    snowballs_melted_list = pygame.sprite.groupcollide(obstacle_list, snowball_list, False, True)
    snowballs_hit_list = pygame.sprite.spritecollide(player, snowball_list, True)
    #snowballs_missed_list =

    #remove low balls
    for x in snowball_list:
        if x.rect.y > 500:
            snowball_list.remove(x)
            all_sprites_list.remove(x)

    #update score for each item in hit list
    for x in snowballs_hit_list:
        score += 1
    for x in snowballs_melted_list:
        antiscore += 1


    # --- Screen-clearing code
    if snowballs_melted_list:
        screen.fill(RED)
    elif snowballs_hit_list:
        screen.fill(WHITE)
    else:
        screen.fill(BLACK)

    # --- Drawing code should go here
    all_sprites_list.draw(screen)

    score_text = str(score)
    score_display = font.render(score_text, True, WHITE)
    screen.blit(score_display, [0, 0])

    antiscore_text = str(antiscore)
    antiscore_display = font.render(antiscore_text, True, RED)
    screen.blit(antiscore_display, [650, 0])

    #console/debug stuff
    os.system('cls')
    print(spawn_ticker)
    print(clock)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
