""" We could get rid of the complex 'list1' and 'list2' args for
    the snowball/obstacle creator functions by using 'global game' and passing
    them to game.list... i just can't be bothered right now.
        ^---Actually we can't for create_obstacle() because it's called within
        the Game() init function. So it obviously can't find the list, which
        is also created by Game(). Beyond using a global list (not doing that)
        the current way stands.

    Next up: Countdown timer and game over / score screen. That's the game
    structure done - from there it's just about balancing.

    Snowballs could use a little random x movement back.

    Maybe play withthe general y position of the obstacles. y += 20?

    Randomise plasma ball colour a bit
"""

#imports and inits
import pygame
import random
import os

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY1 = (230, 230, 230)
GREY2 = (220, 220, 220)
GREY3 = (210, 210, 210)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE1 = (255, 210, 0)
ORANGE2 = (255, 180, 0)
ORANGE3 = (255, 130, 0)

PLASMA_COLORS = (YELLOW, ORANGE1, ORANGE2, ORANGE3)
SNOWBALL_COLORS = (WHITE, GREY1, GREY2, GREY3)

#define the classes
class Game(object):
    """ Represents an instance of the game. To reset the game
        we can apparently just create a new instance of this class."""

    def __init__(self):
        """Create all attributes and initialise the game"""
        self.score = 0
        self.antiscore = 0
        self.spawn_ticker = 0
        self.SPAWN_TICKER_LIMIT = 500
        self.font = pygame.font.SysFont("Arial", 20, False, False)
        self.game_state = "menu"
        self.done = False
        self.start_ticks = pygame.time.get_ticks()
        #create the sprite lists
        self.snowball_list = pygame.sprite.Group()
        self.obstacle_list = pygame.sprite.Group()
        self.plasma_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        #create player
        self.player = Player()
        self.player.rect.centerx = 350
        self.player.rect.centery = 450
        self.player.beam = False
        self.all_sprites_list.add(self.player)


    def process_events(self):
        """Event handling. Return True to close window/quit."""
        if self.game_state == "menu":
            # --- Main event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.game_state = "playing"
                    return False
        elif self.game_state == "playing":
                # --- Main event handling loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        return True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.player.beam = True
                        return False
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.player.beam = False
                        return False

    def game_logic(self):
        global mouse_pos #Global because things like plasma update function will refer to it
        """Main game logic - updates positions and checks for collides"""
        if self.game_state == "playing":
            mouse_pos = pygame.mouse.get_pos()
            #handle spawning
            self.spawn_ticker += 1
            if self.spawn_ticker == self.SPAWN_TICKER_LIMIT/4:
                create_snowballs()
            if self.spawn_ticker == self.SPAWN_TICKER_LIMIT:
                self.spawn_ticker = 0
            if self.player.beam == True:
                create_plasma()
            #update sprites + check collides
            self.all_sprites_list.update()
            self.snowballs_melted_list = pygame.sprite.groupcollide(self.obstacle_list, self.snowball_list, False, True)
            self.snowballs_hit_list = pygame.sprite.spritecollide(self.player, self.snowball_list, True)
            #remove shitty objects
            for x in self.snowball_list:
                if x.rect.y > 500:
                    self.snowball_list.remove(x)
                    self.all_sprites_list.remove(x)
                    self.antiscore += 1

            for x in self.plasma_list:
                if self.player.beam == False or x.ticker < 1:
                    self.plasma_list.remove(x)
                    self.all_sprites_list.remove(x)
            #update score for items in hit list
            for x in self.snowballs_hit_list:
                self.score += 1
            for x in self.snowballs_melted_list:
                self.antiscore += 1

    def display_frame(self, screen):
        """Do all the display stuff"""
        if self.game_state == "menu":
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
        elif self.game_state == "playing":
            #screen clearing/flashing code
            if self.snowballs_melted_list:
                screen.fill(RED)
            elif self.snowballs_hit_list:
                screen.fill(WHITE)
            else:
                screen.fill(BLACK)
            #draw all sprites
            self.all_sprites_list.draw(screen)

            #text stuff
            font = pygame.font.SysFont("Arial", 20, False, False)
            score_text = str(self.score)
            score_display = font.render(score_text, True, WHITE)
            screen.blit(score_display, [0, 0])

            antiscore_text = str(self.antiscore)
            antiscore_display = font.render(antiscore_text, True, RED)
            screen.blit(antiscore_display, [650, 0])
        #Update display
        pygame.display.flip()


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
        pygame.draw.circle(self.image, SNOWBALL_COLORS[random.randrange(len(SNOWBALL_COLORS))], (10, 10), 10, 0)

    def update(self):
        global game
        """ Called each frame """
        #downwards motion
        if game.player.beam == False:
            self.rect.centery += self.yvelocity + random.randrange(-3,4)
        else:
            #x axis motion
            if self.rect.centerx < game.player.rect.centerx:
                self.rect.centerx += self.xvelocity + random.randrange(-3,4)
            if self.rect.centerx > game.player.rect.centerx:
                self.rect.centerx -= self.xvelocity - random.randrange(-3,4)


class Plasma(pygame.sprite.Sprite):
    def __init__(self):
        """initialises a beam plasma ball"""
        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.ticker = 15
        pygame.draw.circle(self.image, PLASMA_COLORS[random.randrange(len(PLASMA_COLORS))], (5, 5), 5, 0)

    def update(self):
        self.ticker -= 1


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
    global mouse_pos
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

#define functions
def create_snowballs():
    """ spawns a volley of snowballs at the top of the screen"""
    global game
    for i in range(25):
        #create one
        snowball = Snowball()
        #set its x-y coords
        snowball.rect.x = random.randrange(700)
        snowball.rect.y = 0
        #add it to the lists
        game.snowball_list.add(snowball)
        game.all_sprites_list.add(snowball)

def create_plasma():
    """spawns a brace of searing plasma near the player"""
    global game
    for i in range(5):
        plasma = Plasma()
        plasma.rect.x = game.player.rect.x + random.randrange(-20, 21)
        plasma.rect.y = game.player.rect.y - (20 + random.randrange(10))
        game.plasma_list.add(plasma)
        game.all_sprites_list.add(plasma)

def create_obstacle(x, y, right):
    """spawns an obstacle. (xpos, ypos, True/False)
    The list stuff is a cludge because we can't call game.methods() on init"""
    obstacle = Obstacle()
    obstacle.rect.centerx = x
    obstacle.rect.centery = y
    obstacle.right = right
    game.obstacle_list.add(obstacle)
    game.all_sprites_list.add(obstacle)

#main loop----------------------------------------------------------------------
def main():
    #make game global cause we are going to be referring to it from inside
    #other functions... a lot
    global game
    #Init stuff not handled by game class
    pygame.init()
    #screen init
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Snowball's Chance")
    #create important objects and set data
    done = False
    clock = pygame.time.Clock()
    #create an instance of the Game class (remember, it's global)
    game = Game()
    #stuff we couldnt easily do in game.__init__()
    create_obstacle(500, 100, True)
    create_obstacle(100, 150, False)
    create_obstacle(200, 200, True)
    create_obstacle(300, 250, False)
    create_obstacle(400, 300, True)

    #Main game loop
    while not done:
        #Process events (remember - the funtion returns True at quit time)
        done = game.process_events()
        #Run game logic
        game.game_logic()
        #Update display
        game.display_frame(screen)
        #Debug console shit
        os.system('cls')
        print("spawn:", game.spawn_ticker)
        print(clock)
        print("ticks:", game.start_ticks)
        print(game.player.beam)
        #pause for next frame
        clock.tick(60)
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()
