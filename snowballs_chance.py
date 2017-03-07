"""
Can we finally use our screen_rect to centre some text??

Just balancing and shit after that. I think there should be a bit more than a
snowball's space between the obstacles - part of the game's challenge can be
holding them there...?
"""

#imports and inits
import pygame
import random
import math
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
    """ Represents an instance of the game."""

    def __init__(self):
        """Create all attributes and initialise the game"""
        self.score = 0
        self.antiscore = 0
        self.your_final_score = 0
        self.old_high_score = -999
        self.spawn_ticker = 0
        self.dec_ticker = 0
        self.SPAWN_TICKER_LIMIT = 500
        self.font = pygame.font.SysFont("Arial", 20, False, False)
        self.game_state = "menu"
        self.scored = False
        self.countdown_ticks = 0
        self.obstacles_spawned = False
        self.mouse_pos = pygame.mouse.get_pos()
        #create the sprite lists
        self.snowball_list = pygame.sprite.Group()
        self.obstacle_list = pygame.sprite.Group()
        self.plasma_list = pygame.sprite.Group()
        self.decball_list = pygame.sprite.Group()
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
                    for x in self.decball_list:
                        self.decball_list.remove(x)
                        self.all_sprites_list.remove(x)
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

        elif self.game_state == "over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.__init__()


    def game_logic(self):
        """Main game logic - updates positions and checks for collides"""
        if self.game_state == "menu":
            self.countdown_ticks = pygame.time.get_ticks()
            #decball spawning
            self.dec_ticker += 1
            if self.dec_ticker > 59:
                self.dec_ticker = 0
            if (self.dec_ticker % 3) == 0:
                create_decball()
            #update sprites
            self.all_sprites_list.update()
            #remove shitty decballs
            for x in self.decball_list:
                if x.rect.top > 500:
                    self.decball_list.remove(x)
                    self.all_sprites_list.remove(x)

        elif self.game_state == "playing":
            #spawn obstacles
            while not self.obstacles_spawned:
                spawn_all_obstacles()
                self.obstacles_spawned = True
            #handle spawning
            self.spawn_ticker += 1
            if self.spawn_ticker == 20 or self.spawn_ticker == 270:
                create_snowballs()
            if self.spawn_ticker == self.SPAWN_TICKER_LIMIT:
                self.spawn_ticker = 0
            if self.player.beam == True:
                create_plasma()
            #update mouse_pos
            self.mouse_pos = pygame.mouse.get_pos()
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
            #countdown stuff
            self.seconds = (pygame.time.get_ticks() - self.countdown_ticks) / 1000
            self.minus = 0 - self.seconds
            self.countdown_from_this = 5 + self.minus #tweak this one for game length
            #game over if countdown over
            if self.countdown_from_this < 0:
                self.game_state = "over"

        elif self.game_state == "over":
            #decballs
            self.dec_ticker += 1
            if self.dec_ticker > 59:
                self.dec_ticker = 0

            if self.dec_ticker == 0 or self.dec_ticker == 29:
                create_decball()
            #update sprites
            self.all_sprites_list.update()
            #remove shitty decballs
            for x in self.decball_list:
                if x.rect.top > 500:
                    self.decball_list.remove(x)
                    self.all_sprites_list.remove(x)
            #scoring shit
            game.your_final_score = game.score - game.antiscore
            high_scores()


    def display_frame(self, screen):
        """Do all the display stuff"""
        if self.game_state == "menu":
            #clear the screen
            screen.fill(BLACK)
            #draw the decballs
            self.decball_list.draw(screen)

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

            timer_text = (str(math.ceil(self.countdown_from_this)))
            timer_display = font.render(timer_text, True, WHITE)
            screen.blit(timer_display, [300, 0])

        elif self.game_state == "over":
            screen.fill(BLACK)

            #decballs
            self.decball_list.draw(screen)
            #text stuff
            game_over_header_x = 175
            game_over_header_y = 50

            game_over_text_x = 200

            font = pygame.font.SysFont("Arial", 60, False, False)
            title_headline_text1 = "Game"
            title_headline_display1 = font.render(title_headline_text1, False, WHITE)
            screen.blit(title_headline_display1, [game_over_header_x, game_over_header_y])

            title_headline_text2 = "Over"
            title_headline_display2 = font.render(title_headline_text2, False, RED)
            screen.blit(title_headline_display2, [game_over_header_x + 175, game_over_header_y])


            font = pygame.font.SysFont("Arial", 20, False, False)
            if self.score > 1:
                title_sub_text1 = "You saved " + str(self.score) + " snowballs."
            else:
                title_sub_text1 = "You saved no snowballs... you monster."
            title_sub_display1 = font.render(title_sub_text1, False, WHITE)
            screen.blit(title_sub_display1, [game_over_text_x, 200])

            title_sub_text2 = "Meanwhile, you lost " + str(self.antiscore) + "..."
            title_sub_display2 = font.render(title_sub_text2, False, WHITE)
            screen.blit(title_sub_display2, [game_over_text_x + 25, 250])

            title_sub_text3 = "...so your score is " + str(self.your_final_score) + "."
            title_sub_display3 = font.render(title_sub_text3, False, WHITE)
            screen.blit(title_sub_display3, [game_over_text_x + 50, 300])

            if self.your_final_score > int(self.old_high_score):
                title_sub_text4 = "A new high score!"
            else:
                title_sub_text4 = "High score: " + str(self.old_high_score)
            title_sub_display4 = font.render(title_sub_text4, False, RED)
            screen.blit(title_sub_display4, [game_over_text_x + 50, 350])

            title_sub_text5 = "Press return to play again or escape to quit."
            title_sub_display5 = font.render(title_sub_text5, False, WHITE)
            screen.blit(title_sub_display5, [game_over_text_x - 50, 450])

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
        self.yvelocity = 3
        self.xvelocity = 2
        self.right = random.randrange(2)
        #draw the circle
        pygame.draw.circle(self.image, SNOWBALL_COLORS[random.randrange(len(SNOWBALL_COLORS))], (10, 10), 10, 0)

    def update(self):
        global game
        """ Called each frame """
        #downwards motion
        if game.player.beam == False:
            self.rect.centery += 2
            if self.right:
                if not random.randrange(2):
                    self.rect.centerx += self.xvelocity
                if not random.randrange(32):
                    self.right = False
            else:
                if not random.randrange(2):
                    self.rect.centerx -= self.xvelocity
                if not random.randrange(64):
                    self.right = True
        #if the player is beaming
        else:
            #x axis motion
            if self.rect.centerx < game.player.rect.centerx:
                self.rect.centerx += self.xvelocity + random.randrange(-3,4)
            if self.rect.centerx > game.player.rect.centerx:
                self.rect.centerx -= self.xvelocity - random.randrange(-3,4)


class Decball(pygame.sprite.Sprite):
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
        self.right = random.randrange(2)
        #draw the circle
        pygame.draw.circle(self.image, SNOWBALL_COLORS[random.randrange(len(SNOWBALL_COLORS))], (10, 10), 10, 0)

    def update(self):
        #downwards
        self.rect.centery += 1
        if self.right:
            if not random.randrange(2):
                self.rect.centerx += 1
            if not random.randrange(32):
                self.right = False
        else:
            if not random.randrange(2):
                self.rect.centerx -= 1
            if not random.randrange(64):
                self.right = True


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
        self.rect.centerx = game.mouse_pos[0]

#define functions
def high_scores():
    global game
    if not game.scored:
        try:
            game.hi_scores = open("high_scores.txt", "r")
            game.old_high_score = int(game.hi_scores.read())
            game.hi_scores.close()
        except IOError:
            print("No HS file! Will create one on write.")
        except ValueError:
            print("Can't read HS value! Resorting to default -999")

        if int(game.old_high_score) < game.your_final_score:
            game.hi_scores = open("high_scores.txt", "w")
            game.hi_scores.write(str(game.score - game.antiscore))
            game.hi_scores.close()
        game.scored = True


def create_snowballs():
    """ spawns a volley of snowballs at the top of the screen"""
    global game
    for i in range(25):
        #create one
        snowball = Snowball()
        #set its x-y coords
        snowball.rect.x = random.randrange(700)
        snowball.rect.y = 0
        snowball.right = True
        #add it to the lists
        game.snowball_list.add(snowball)
        game.all_sprites_list.add(snowball)


def create_decball():
    """ creates a single decball"""
    global game
    decball = Decball()
    decball.rect.x = random.randrange(700)
    decball.rect.bottom = 0
    #lists
    game.decball_list.add(decball)
    game.all_sprites_list.add(decball)


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


def spawn_all_obstacles():
    create_obstacle(100, 100, False)
    create_obstacle(200, 175, True)
    create_obstacle(300, 250, False)
    create_obstacle(400, 325, True)

#main loop----------------------------------------------------------------------
def main():
    #make game global cause we are going to be referring to it from inside
    #other functions... a lot
    global game, screen_rect

    #Init stuff not handled by game class
    pygame.init()

    size = (700, 500)
    screen = pygame.display.set_mode(size)
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Snowball's Chance")

    done = False

    clock = pygame.time.Clock()

    #create an instance of the Game class (remember, it's global)
    game = Game()

    #Main game loop
    while not done:
        #Process events (remember - the funtion returns True at quit time)
        done = game.process_events()
        #Run game logic
        game.game_logic()
        #Update display
        game.display_frame(screen)
        #Debug console shit can go below if required

        #pause for next frame
        clock.tick(60)
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
