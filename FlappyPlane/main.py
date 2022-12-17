import sys
import pygame
from pygame.locals import *

#常數
SCREENWIDTH = 822
SCREENHEIGHT = 500
FPS = 120

PLAYERWIDTH = 160
PLAYERHEIGHT = 94
GRAVITY = 0.25
BGSPEED = 2
BARRIERSPEED = 3
JUMPVALUE = 6

raw_NSSH = pygame.image.load("./assets/objects/NSSH.png")
NSSH = pygame.transform.scale(raw_NSSH, (84, 46))

icon = pygame.image.load('./assets/icon.png')
pygame.display.set_icon(icon)

high_score = 0

with open('./assets/high_score.txt', 'r') as high_score_r:
    for line in high_score_r:
        high_score = int(line)
        
print(high_score)


#high_score_w =  open('./assets/high_score.txt', 'w')

from itertools import cycle

#背景
class MyMap():
    def __init__(self, x, y):
        self.raw_bg = pygame.image.load("./assets/objects/bg.png").convert_alpha()
        self.bg = pygame.transform.scale(self.raw_bg, (SCREENWIDTH, SCREENHEIGHT))
        self.x = x
        self.y = y

    def map_rolling(self):
        if self.x < -790:
            self.x = 800
        else:
            self.x -= BGSPEED

    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))

#玩家
class Player():
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.jumpState = False
        self.gravity = GRAVITY #模擬重力
        self.jumpValue = 0 

        self.raw_player1 = pygame.image.load("./assets/objects/player1.png").convert_alpha()
        self.player1 = pygame.transform.scale(self.raw_player1, (PLAYERWIDTH, PLAYERHEIGHT))
        self.player1 = pygame.transform.rotate(self.player1, 10)

        self.raw_player2 = pygame.image.load("./assets/objects/player2.png").convert_alpha()
        self.player2 = pygame.transform.scale(self.raw_player2, (PLAYERWIDTH, PLAYERHEIGHT))

        self.image = self.player1

        self.jump_audio = pygame.mixer.Sound('./assets/audios/jump.wav')
        self.rect.size = self.image.get_size()
        self.x = 50
        self.y = 160
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.jumpState = True

    #玩家移動
    def move(self):
        if self.jumpValue > 0:
            self.image = self.player1
        
        else:
            self.image = self.player2

        if self.jumpState:
            self.jumpValue = -JUMPVALUE
            self.jumpState = False

        else:
            self.jumpValue += self.gravity
            
        self.rect.y += self.jumpValue  

    #繪製玩家
    def draw_player(self):
        SCREEN.blit(self.image, (self.x, self.rect.y))

import random
# 障礙物
class Barrier():
    score = 1
    def __init__(self, start):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.raw_barrier1 = pygame.image.load("./assets/objects/barrier1.png").convert_alpha()
        self.raw_barrier2 = pygame.image.load("./assets/objects/barrier2.png").convert_alpha()
        self.raw_barrier3 = pygame.image.load("./assets/objects/barrier3.png").convert_alpha()

        self.barrier_img = (
            pygame.transform.scale(self.raw_barrier1, (200, SCREENHEIGHT)),
            pygame.transform.scale(self.raw_barrier2, (200, SCREENHEIGHT)),
            pygame.transform.scale(self.raw_barrier3, (200, SCREENHEIGHT))
        )

        self.score_audio = pygame.mixer.Sound('./assets/audios/score.wav')

        rand = random.randint(0, 2)
        self.image = self.barrier_img[rand]

        self.x = 800
        self.y = 0
        self.rect.center = (self.x, self.y)

    # 障礙物移動
    def barrier_move(self):
        self.rect.x -= BARRIERSPEED

    # 繪製障礙物
    def draw_barrier(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    # 獲取分數
    def getScore(self):
        self.score
        tmp = self.score

        if tmp == 1:
            self.score_audio.play()

        self.score = 0
        return tmp

# 遊戲結束
def Gameover():
    bump_audio = pygame.mixer.Sound('./assets/audios/bump.wav')
    bump_audio.play()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    raw_gameover = pygame.image.load('./assets/objects/gameover.png').convert_alpha()
    gameover = pygame.transform.scale(raw_gameover, (200, 150))

    SCREEN.blit(gameover, ((screen_w - gameover.get_width()) / 2,
                                       (screen_h - gameover.get_height()) / 2))

#遊戲主迴圈
def mainGame():
    global SCREEN, FPSCLOCK, high_score
    pygame.init() # 初始化
    score = 0 # 得分
    over = False

    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('FlappyPlane')
    score_font = pygame.font.SysFont(None, 30)
    my_font = pygame.font.SysFont(None, 20)
    
    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)

    player = Player()
    barrier_timer = 0
    barriers = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                
                high_score_w = open('./assets/high_score.txt', 'w')
                high_score_w.write(str(high_score))
                high_score_w.close()

                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE: #跳躍

                player.jump()
                player.jump_audio.play()

                if over == True:
                    mainGame()

        if over == False:
            bg1.map_rolling()
            bg1.map_update()
            bg2.map_rolling()
            bg2.map_update()
            player.move()
            player.draw_player()
            
            SCREEN.blit(NSSH, (SCREENWIDTH - 100, 8))

            if barrier_timer >= 2600: #生成障礙物
                
                rand = random.randint(80, SCREENHEIGHT - 80)
                barrier = Barrier(rand)
                barriers.append(barrier)

                barrier_timer = 0

            for i in barriers:
                if i.rect.x < -100:
                    barriers.remove(i)

            for i in range(len(barriers)): #障礙物
                barriers[i].barrier_move()
                barriers[i].draw_barrier()
        
                if pygame.sprite.collide_mask(player, barriers[i]) or player.rect.y >= SCREENHEIGHT or player.rect.y < 0 - PLAYERHEIGHT:  # 判斷玩家與障礙物是否碰撞
                    over = True
                    Gameover()

                else:
                    if (barriers[i].rect.x + barriers[i].rect.width) < player.rect.x:
                        score += barriers[i].getScore()
                    
                    if score > high_score:
                        high_score = score

        # 顯示分數
        score_surface = score_font.render('Scores: %d | High Score: %d' %(score, high_score), True, (150, 150, 150))
        text_surface = my_font.render('Made by nssh jnr177 22 Alan, 33 Ray'.format(score), True, (150, 150, 150))

        SCREEN.blit(score_surface, (10, 5))
        SCREEN.blit(text_surface, (550, 480))

        barrier_timer += 20
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    mainGame()