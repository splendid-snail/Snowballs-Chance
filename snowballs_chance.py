""" Snowballs could use a little random x movement back.

    Maybe play withthe general y position of the obstacles. Then we can work on
    a timer countdown - we've already got the start_ticks var in place. Then a
    game over screen giving you your silvers, golds and net total!

    Plasm needs work. A short ticker attribute could make them disappear after
    a few ticks (without having to move)"""

#imports and inits
import pygame
import random
import os

pygame.init()

pygame.mouse.set_visible(False)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set the display stuff
size = (700, 500)
screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()

pygame.display.set_caption("Snowball's Chance")

#create the sprite lists
snowball_list = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
plasma_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

#store scores + other init vars
score = 0
antiscore = 0

spawn_ticker = 0
SPAWN_TICKER_LIMIT = 500

font = pygame.font.SysFont("Arial", 20, False, False)

game_state = "menu"

done = False

clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

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
        self.yvelocity = 2
        self.xvelocity = 1
        #draw the circle
        pygame.draw.circle(self.image, WHITE, (10, 10), 10, 0)

    def update(self):
        """ Called each frame """
        #downwards motion
        if player.beam == False:
            self.rect.centery += self.yvelocity + random.randrange(-3,4)
        else:
            #x axis motion
            if self.rect.centerx < player.rect.centerx:
                self.rect.centerx += self.xvelocity + random.randrange(-3,4)
            if self.rect.centerx > player.rect.centerx:
                self.rect.centerx -= self.xvelocity - random.randrange(-3,4)

class Plasma(pygame.sprite.Sprite):
    def __init__(self):
        """initialises a beam plasma ball"""
        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, YELLOW, (5, 5), 5, 0)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        """initialise obstacle objects"""
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(BLUE)
        self.right = True
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, BLUE, self.rect, 0)

    def update(self):
        """called each frame"""
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
        """called per frame"""
        self.rect.centerx = mouse_pos[0]

#create stuff

#this isn't a function cause i can't be bothered to change how movement works
#just yet...
player = Player()
player.rect.centerx = 350
player.rect.centery = 450
player.beam = False
all_sprites_list.add(player)

def create_snowballs():
    """ spawns a volley of snowballs at the top of the screen"""
    for i in range(25):
        #create one
        snowball = Snowball()
        #set its x-y coords
        snowball.rect.x = random.randrange(700)
        snowball.rect.y = 0
        #add it to the lists
        snowball_list.add(snowball)
        all_sprites_list.add(snowball)

def create_plasma():
    """spawns a brace of searing plasma near the player"""
    for i in range(5):
        plasma = Plasma()
        plasma.rect.x = player.rect.x + random.randrange(-20, 21)
        plasma.rect.y = player.rect.y - 20
        plasma_list.add(plasma)
        all_sprites_list.add(plasma)


def create_obstacle(x, y, right):
    """spawns an obstacle. (xpos, ypos, True/False)"""
    obstacle = Obstacle()
    obstacle.rect.centerx = x
    obstacle.rect.centery = y
    obstacle.right = right
    obstacle_list.add(obstacle)
    all_sprites_list.add(obstacle)

create_obstacle(500, 100, True)
create_obstacle(100, 150, False)
create_obstacle(200, 200, True)
create_obstacle(300, 250, False)
create_obstacle(400, 300, True)

#main loop----------------------------------------------------------------------
while not done:

    if game_state == "menu":
        # --- Main event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "playing"

        # ---game logic

        # ---drawing code
        font = pygame.font.SysFont("Arial", 40, False, False)
        title_headline_text1 = "Snowball's"
        title_headline_display1 = font.render(title_headline_text1, False, WHITE)
        screen.blit(title_headline_display1, [184, 150])

        title_headline_text2 = "Chance"
        title_headline_display2 = font.render(title_headline_text2, False, RED)
        screen.blit(title_headline_display2, [375, 150])

        font = pygame.font.SysFont("Arial", 20, False, False)
        title_sub_text = "Press return to play"
        title_sub_display = font.render(title_sub_text, False, WHITE)
        screen.blit(title_sub_display, [263, 200])

        clock.tick(60)
        #update screen
        pygame.display.flip()

    elif game_state == "playing":
        # --- Main event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.beam = True
            elif event.type == pygame.MOUSEBUTTONUP:
                player.beam = False

        # --- Game logic
        #get the mouse position this frame
        mouse_pos = pygame.mouse.get_pos()

        #handle spawning
        spawn_ticker += 1
        if spawn_ticker == SPAWN_TICKER_LIMIT/4:
            create_snowballs()
        if spawn_ticker == SPAWN_TICKER_LIMIT:
            spawn_ticker = 0

        if player.beam == True:
            create_plasma()

        #probably won't work if the list contains sprites
        #without an update() method
        all_sprites_list.update()

        #create collision lists - no real use for melted rn but might be useful later
        snowballs_melted_list = pygame.sprite.groupcollide(obstacle_list, snowball_list, False, True)
        snowballs_hit_list = pygame.sprite.spritecollide(player, snowball_list, True)

        #remove shitty objects
        for x in snowball_list:
            if x.rect.y > 500:
                snowball_list.remove(x)
                all_sprites_list.remove(x)

        for x in plasma_list:
            if player.beam == False:
                plasma_list.remove(x)
                all_sprites_list.remove(x)

        #update score for each item in hit list
        for x in snowballs_hit_list:
            score += 1
        for x in snowballs_melted_list:
            antiscore += 1

        #Screen clearing/flashing code
        if snowballs_melted_list:
            screen.fill(RED)
        elif snowballs_hit_list:
            screen.fill(WHITE)
        else:
            screen.fill(BLACK)

        # --- Drawing code
        all_sprites_list.draw(screen)

        #text stuff
        font = pygame.font.SysFont("Arial", 20, False, False)
        score_text = str(score)
        score_display = font.render(score_text, True, WHITE)
        screen.blit(score_display, [0, 0])

        antiscore_text = str(antiscore)
        antiscore_display = font.render(antiscore_text, True, RED)
        screen.blit(antiscore_display, [650, 0])

        #console/debug stuff
        os.system('cls')
        print("spawn:", spawn_ticker)
        print(clock)
        print("ticks:", start_ticks)
        print(player.beam)

        pygame.display.flip()

        clock.tick(60)

pygame.quit()
