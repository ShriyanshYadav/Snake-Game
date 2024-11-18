import math
import random
import pygame
from pygame.locals import * 


# Constants
GAME_WIDTH = 1600
GAME_HEIGHT = 900
PLAYER_WIDTH = 45
PLAYER_HEIGHT = 45
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = GREEN
ACCELERATION = 10
PLAYER_SPEED = 50
RED = (255, 0, 0)


# Player square 
class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
        self.surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surf.fill(PLAYER_COLOR)
        self.rect = self.surf.get_rect()

# FOOD square 
class FoodSquare(pygame.sprite.Sprite):
    def __init__(self):
        super(FoodSquare, self).__init__()
        self.surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect()

# Initialize Pygame
pygame.init()
# initialize text
pygame.font.init()
pygame.font.get_init()
# Game Screen
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
# caption for window
pygame.display.set_caption('SNAKE GAME')


# Instantiate square objects
Player = Square()
Food = FoodSquare()


# Set the initial state of the game
gameOn = True
Player_x = 300
Player_y = GAME_HEIGHT//2 - PLAYER_WIDTH - 5
direction = 'r'
speed = 150
score = 0
# for score
FONT = pygame.font.SysFont('freesanbold.ttf', 50)
Score = FONT.render(f'SCORE : {score}', True, WHITE)
ScoreRect = Score.get_rect()
ScoreRect.center = (GAME_WIDTH//2, 40)
Speed = FONT.render(f'SPEED : {0}', True, WHITE)
SpeedRect = Speed.get_rect()
SpeedRect.center = (GAME_WIDTH//2, 80)
HighScore = 0
with open("HighScore.txt", "r") as file:
    HighScore = file.readline()
NoPlayers = [[Player_x,Player_y], [Player_x+45, Player_y]]
prev = [[Player_x,Player_y], [Player_x+45, Player_y]]

# for FOOD
rx = list(range(0, 1550, 50))
ry = list(range(0, 850, 50))
Food_x = random.choice(rx)
Food_y = random.choice(ry)


def reset():
    global score, speed, Player_x, Player_y, direction, NoPlayers, prev, HighScore
 #  with open("HighScore.txt", "r") as file:
  #      HighScore = file.readline()
    if score > int(HighScore):
        with open("HighScore.txt", "w") as file:
            HighScore = score
            file.write(str(math.floor(score)))
    score = 0
    speed = 150
    NoPlayers[0][0] = Player_x
    NoPlayers[0][1] = Player_y
    NoPlayers = [[Player_x,Player_y], [Player_x+45, Player_y]]
    prev = [[Player_x,Player_y], [Player_x+45, Player_y]]
    direction = 'r'  



# Main game loop
while gameOn:
    pygame.time.delay(int(speed)) 

    # score update
    score += 0.1

    # Updating speed
    if int(score) % ACCELERATION == 0:
        speed = max(10, speed - 2)
        score += 1



    # Player moving in direction
    match direction:
        case 'l':
           NoPlayers[0][0] -= PLAYER_SPEED
        case 'r':
           NoPlayers[0][0] += PLAYER_SPEED
        case 'u':
          NoPlayers[0][1] -= PLAYER_SPEED
        case 'd':
           NoPlayers[0][1] += PLAYER_SPEED


    
    # update every player piece to tthe one ahead
    for i in range(len(NoPlayers)):
        if i == 0:
            continue
        NoPlayers[i][0] = prev[i-1][0] 
        NoPlayers[i][1] = prev[i-1][1]


    head_x = NoPlayers[0][0]
    head_y = NoPlayers[0][1]   
    # death if out of bounds
    if head_x < 0 or head_x > GAME_WIDTH-PLAYER_WIDTH or head_y < 0 or head_y > GAME_HEIGHT-PLAYER_HEIGHT:
        reset()


    # death if collision with itself
    for x,y in NoPlayers[1:]:
        if head_x == x and head_y == y:
            reset()
    
    # FOOOOOD collision
    if head_x == Food_x and head_y == Food_y:
        combi = []
        for x in rx:
            for y in ry:
                combi.append([x, y])

        for z in combi:
            if z in NoPlayers:
                combi.remove(z)

        Food_x,Food_y = random.choice(combi)
        NoPlayers.append([prev[-1][0],NoPlayers[-1][1]])
        prev.append([NoPlayers[-1][0],NoPlayers[-1][1]])
        score += 10
    
    # Handle events
    for event in pygame.event.get():
        if event.type == KEYDOWN:

            # exit game
            if event.key == K_BACKSPACE:
                gameOn = False

            # Movements
            if event.key == K_a or event.key == K_LEFT:
                if direction != 'r':  # Prevent reversing direction
                    direction = 'l'
            if event.key == K_d or event.key == K_RIGHT:
                if direction != 'l':
                    direction = 'r'
            if event.key == K_w or event.key == K_UP:
                if direction != 'd':
                    direction = 'u'
            if event.key == K_s or event.key == K_DOWN:
                if direction != 'u':
                    direction = 'd'
        
        # exit game 
        elif event.type == QUIT:
                gameOn = False 

    

    # getting prev player positions
    for i in range(len(NoPlayers)):
        prev[i][0] = NoPlayers[i][0]
        prev[i][1] = NoPlayers[i][1]


    # Fill the screen with a black background
    screen.fill((0, 0, 0))

    # Draw Player
    for x,y in NoPlayers:
       screen.blit(Player.surf, (x, y))
    # FOOOOOD
    screen.blit(Food.surf, (Food_x, Food_y))
    # Draw Score
    screen.blit(FONT.render(f'SCORE : {int(score)}', True, WHITE), ScoreRect)
    screen.blit(FONT.render(f'HighScore : {int(HighScore)}', True, WHITE), SpeedRect)

    # Update the display
    pygame.display.update()


# Quit the game when exiting the loop
pygame.quit()


