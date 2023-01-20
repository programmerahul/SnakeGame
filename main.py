import pygame
import random
import os

pygame.mixer.init()
pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
orange = (232 ,136 ,32)
yellow = (194, 190, 68)
darkGreen =(11, 41, 18)

screen_width = 900
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width, screen_height))

bgimg = pygame.image.load("background.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
welcomeimg = pygame.image.load("welcome.png")
welcomeimg = pygame.transform.scale(welcomeimg, (screen_width, screen_height)).convert_alpha()
gameoverimg = pygame.image.load("gameover.jpg")
gameoverimg = pygame.transform.scale(gameoverimg, (screen_width, screen_height)).convert_alpha()
pygame.display.set_caption("Snake Game")
pygame.display.update()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size,velocity):
    i=0
    for x,y in snk_list:
        if x==snk_list[-1][0] and y==snk_list[-1][1]:
            if velocity[0]<0:
                pygame.draw.circle(gameWindow, color, [x,y+snake_size/2] ,snake_size/2)
                pygame.draw.circle(gameWindow, darkGreen, [x,y+snake_size/4] ,snake_size/4)
                pygame.draw.circle(gameWindow, darkGreen, [x,y+(snake_size-snake_size/4)] ,snake_size/4)
            elif velocity[1]>0:
                pygame.draw.circle(gameWindow, color, [x+snake_size/2,y+snake_size] ,snake_size/2)
                pygame.draw.circle(gameWindow, darkGreen, [x+snake_size/4,y+snake_size] ,snake_size/4)
                pygame.draw.circle(gameWindow, darkGreen, [x+(snake_size-snake_size/4),y+snake_size] ,snake_size/4)
            elif velocity[1]<0:
                  pygame.draw.circle(gameWindow, color, [x+snake_size/2,y] ,snake_size/2)
                  pygame.draw.circle(gameWindow, darkGreen, [x+snake_size/4,y] ,snake_size/4)
                  pygame.draw.circle(gameWindow, darkGreen, [x+(snake_size-snake_size/4),y] ,snake_size/4)
            else:
             pygame.draw.circle(gameWindow, color, [x+snake_size,y+snake_size/2] ,snake_size/2)
             pygame.draw.circle(gameWindow, darkGreen, [x+snake_size,y+snake_size/4] ,snake_size/4)
             pygame.draw.circle(gameWindow, darkGreen, [x+snake_size,y+(snake_size-snake_size/4)] ,snake_size/4)
            pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])
        
        elif i%2==0:
            pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])
        else:
            pygame.draw.rect(gameWindow, darkGreen, [x, y, snake_size, snake_size])
        i+=1

bgMusic = pygame.mixer.Sound('back.mp3')


def welcome():
    exit_game = False
    bgMusic.play(100)
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(welcomeimg, (0, 0))
        text_screen("Press Enter To Start!", black, 260, 660)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                    exit_game = True
        pygame.display.update()
        clock.tick(60)

# game loop


def game_loop():
    snk_list = []
    snk_length = 1
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 100
    snake_size = 30
    fps = 60
    velocity_x = 0
    velocity_y = 0
    init_velocity = 3
    food_x = random.randint(100,800)
    food_y = random.randint(200,600)
    score = 0
    if not os.path.exists("highScore.txt"):
        with open("highScore.txt","w") as f:
            f.write("0")
    with open("highScore.txt", "r") as f:
        hiscore = f.read()
    while not exit_game:

        if game_over:
            with open("highScore.txt", "w") as f:
                f.write(hiscore)
            gameWindow.fill(white)
            gameWindow.blit(gameoverimg, (0, -45))
            text_screen("Press Enter To Continue", orange, 220, 660)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.music.load('turn.mp3')
                    pygame.mixer.music.play()
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score += 5
            snake_x += velocity_x
            snake_y += velocity_y

            if abs((snake_x+snake_size/2) - food_x) < 10 and abs((snake_y+snake_size/2) - food_y) < 10:
                pygame.mixer.music.load('eat.mp3')
                pygame.mixer.music.play()
                score += 10
                food_x = random.randint(100,800)
                food_y = random.randint(200,600)
                snk_length += 5
                if score > int(hiscore):
                    hiscore = str(score)

            if snake_x < 0 or snake_x > screen_width or snake_y < 67 or snake_y > screen_height:
                game_over = True
                bgMusic.stop()
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("SCORE: " + str(score)+"                               HIGHSCORE: " + hiscore, darkGreen, 30, 18)
            pygame.draw.circle(gameWindow, red, [food_x, food_y] ,snake_size/2)
            pygame.draw.circle(gameWindow, orange, [food_x, food_y] ,snake_size/3  )


            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                game_over = True
                bgMusic.stop()
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()
            plot_snake(gameWindow, green, snk_list, snake_size,[velocity_x,velocity_y])
        pygame.display.update()
        clock.tick(fps)


welcome()
pygame.quit()
quit()
