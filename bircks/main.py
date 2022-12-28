import sys
import pygame
import random
import math
from pygame.locals import *

#常數
SCREENWIDTH = 800
SCREENHEIGHT = 500
FPS = 60

raw_NSSH = pygame.image.load("./assets/objects/NSSH.png")
NSSH = pygame.transform.scale(raw_NSSH, (84, 46))

raw_bg = pygame.image.load("./assets/objects/bg.png")
bg = pygame.transform.scale(raw_bg, (SCREENWIDTH, SCREENHEIGHT))

icon = pygame.image.load('./assets/icon.png')
pygame.display.set_icon(icon)

high_score = 0

with open('./assets/high_score.txt', 'r') as high_score_r:
    for line in high_score_r:
        high_score = int(line)
        
print(high_score)

class Player():
    def __init__(self):
        super().__init__()

        self.width = 150
        self.height = 20

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.raw_image = pygame.image.load("./assets/objects/player.png")
        self.image = pygame.transform.scale(self.raw_image, (self.width, self.height))

        self.x = SCREENWIDTH / 2 - 75
        self.y = 450

        self.rect.size = self.image.get_size()
        self.rect.topleft = (self.x, self.y)

    def Draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

    def Move_to(self, x, y):
        self.x = x
        self.y = y

class Ball():
    def __init__(self):
        super().__init__()

        self.width = 20
        self.height = 20

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.raw_image = pygame.image.load("./assets/objects/Ball.png")
        self.image = pygame.transform.scale(self.raw_image, (self.width, self.height))

        self.x = SCREENWIDTH / 2 - self.width / 2
        self.y = 400
        self.speed = 5
        self.angle = 30
        self.quadrant = 1

        self.rect.size = self.image.get_size()
        self.rect.topleft = (self.x, self.y)

    def Draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

    def Move_to(self, x, y):
        self.x = x
        self.y = y

    def Move(self, angle, Displacement):
        radian = math.radians(angle - 90)

        x = math.cos(radian) * Displacement
        y = math.sin(radian) * Displacement
        self.x += x
        self.y += y
        
        #print(x, y)
        print(self.angle)

    def Update(self):
        self.Move(self.angle, self.speed)

        if self.x <= 0 or self.x >= SCREENWIDTH - self.width:
            self.angle *= -1
            self.angle += random.randint(-20, 20)

        if self.y <= 0:
            self.angle += 180 - self.angle * 2
            self.angle += random.randint(-20, 20)
            self.y += 5

class Brick():
    def __init__(self, x, y):
        super().__init__()

        self.width = 100
        self.height = 20

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.raw_image = pygame.image.load("./assets/objects/brick.png")
        self.image = pygame.transform.scale(self.raw_image, (self.width, self.height))

        self.x = x
        self.y = y

        self.rect.size = self.image.get_size()
        self.rect.topleft = (self.x, self.y)

    def Draw(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

#high_score_w =  open('./assets/high_score.txt', 'w')

# 遊戲結束
def Gameover():
    bump_audio = pygame.mixer.Sound('./assets/audios/bump.wav')
    bump_audio.play()

    raw_gameover = pygame.image.load('./assets/objects/gameover.png')
    gameover = pygame.transform.scale(raw_gameover, (200, 150))

    SCREEN.blit(gameover, (200, 325))

def Escape():
    high_score_w = open('./assets/high_score.txt', 'w')
    high_score_w.write(str(high_score))
    high_score_w.close()

    pygame.quit()
    sys.exit()

#遊戲主迴圈
def mainGame():
    global SCREEN, FPSCLOCK, high_score
    pygame.init() # 初始化
    score = 0 # 得分
    over = False
    is_start = False

    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('BricksGame')
    score_font = pygame.font.SysFont(None, 30)
    my_font = pygame.font.SysFont(None, 20)
    pygame.key.set_repeat(10, 15)

    bricks = []
    for i in range(7):
        for j in range(6):
            bricks.append(Brick(20 + 110 * i, 10 + j * 40))

    ball = Ball()
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                Escape()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Escape()

                elif over == True:
                    mainGame()
                
                elif is_start == False:
                    is_start = True

                else:
                    if event.key == K_RIGHT or event.key == ord('d'):
                        if player.x < SCREENWIDTH - 150:
                            player.x += 5                            

                    elif event.key == K_LEFT or event.key == ord('a'):
                        if player.x > 0:
                            player.x += -5

        if over == False:    
            if is_start:
                ball.Update()

                if ball.y >= player.y - player.height - 5 and abs(ball.y - player.y) < ball.height / 2 and abs(ball.x - player.x - player.width / 2) < player.width / 2:
                    ball.angle += 180 - ball.angle * 2 + random.randint(-20, 20)
                    ball.y -= 5

                if ball.y > SCREENHEIGHT - ball.height:
                    over = True
                    Gameover()

            for brick in bricks:
                if pygame.sprite.collide_rect(brick, ball):
                    ball.angle += 180 - ball.angle * 2
                    ball.angle += random.randint(-20, 20)
                    ball.y += 5

            SCREEN.blit(bg, (0, 0))

            player.Draw()
            ball.Draw()

            for brick in bricks:
                brick.Draw()

            score_surface = score_font.render('Scores: %d | High Score: %d' %(score, high_score), True, (7, 74, 40)) #顯示分數
            text_surface = my_font.render('Made by nssh jnr177 22 Alan, 33 Ray'.format(score), True, (7, 74, 40))

            SCREEN.blit(score_surface, (10, 5))
            SCREEN.blit(text_surface, (150, 580))
            
            SCREEN.blit(NSSH, (SCREENWIDTH - 100, 8))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
                
if __name__ == '__main__':
    mainGame()
