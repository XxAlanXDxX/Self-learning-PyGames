import sys
import pygame
from pygame.locals import *

#常數
SCREENWIDTH = 822
SCREENHEIGHT = 260
FPS = 120

DINOWIDTH = 60
DINOHEIGHT = 70
GRAVITY = 0.3
BGSPEED = 2
BARRIERSPEED = 4
JUMPVALUE = 10

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

#背景
class MyMap():
    def __init__(self, x, y):
        self.raw_bg = pygame.image.load("./assets/objects/bg.png").convert_alpha()
        self.bg = pygame.transform.scale(self.raw_bg, (SCREENWIDTH, SCREENHEIGHT))
        self.x = x
        self.y = y

    def map_rolling(self):
        if self.x < -SCREENWIDTH + 10:
            self.x = SCREENWIDTH
        else:
            self.x -= BGSPEED

    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))


from itertools import cycle

# 恐龍
class Dinosaur():
    def __init__(self):

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.jumpState = False
        self.gravity = GRAVITY #模擬重力
        self.lowest_y = 160
        self.jumpValue = 0 

        self.dinosaurIndex = 0
        self.dinosaurIndexGen = cycle([0, 1, 2])

        self.raw_dino1 = pygame.image.load("./assets/objects/dinosaur1.png").convert_alpha()
        self.raw_dino2 = pygame.image.load("./assets/objects/dinosaur2.png").convert_alpha()
        self.raw_dino2 = pygame.image.load("./assets/objects/dinosaur3.png").convert_alpha()

        self.dinosaur_img = (
            pygame.transform.scale(self.raw_dino1, (DINOWIDTH, DINOHEIGHT)),
            pygame.transform.scale(self.raw_dino2, (DINOWIDTH, DINOHEIGHT)),
            pygame.transform.scale(self.raw_dino2, (DINOWIDTH, DINOHEIGHT))
        )
        self.jump_audio = pygame.mixer.Sound('./assets/audios/jump.wav')
        self.rect.size = self.dinosaur_img[0].get_size()
        self.x = 50
        self.y = self.lowest_y
        self.rect.topleft = (self.x, self.y)

    #跳躍狀態以確保不會空跳
    def jump(self):
        self.jumpState = True

    # 小恐龍移動
    def move(self):
        if self.jumpState:
            self.jumpValue = -JUMPVALUE
            self.jumpState = False

        elif self.rect.y >= self.lowest_y:
            self.rect.y = self.lowest_y
            self.jumpValue = 0

        else:
            self.jumpValue += self.gravity

        self.rect.y += self.jumpValue

    # 繪製恐龍
    def draw_dinosaur(self):
        dinosaurIndex = next(self.dinosaurIndexGen)
        SCREEN.blit(self.dinosaur_img[dinosaurIndex],
                    (self.x, self.rect.y))
import random
# 障礙物
class Barrier():
    score = 1
    def __init__(self, barrier_type, width, height):

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.raw_stone = pygame.image.load("./assets/objects/stone.png").convert_alpha()
        self.stone = pygame.transform.scale(self.raw_stone, (width, height))
        self.raw_cacti = pygame.image.load("./assets/objects/cacti.png").convert_alpha()
        self.cacti = pygame.transform.scale(self.raw_cacti, (width, height))

        self.score_audio = pygame.mixer.Sound('./assets/audios/score.wav')

        if barrier_type == 0:
            self.image = self.stone
        else:
            self.image = self.cacti

        self.rect.size = self.image.get_size()
        self.width, self.height = self.rect.size

        self.x = SCREENWIDTH
        self.y = 230 - (self.height / 2)
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
    pygame.display.set_caption('DinoGame')
    score_font = pygame.font.SysFont(None, 30)
    my_font = pygame.font.SysFont(None, 20)

    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)
    dinosaur = Dinosaur()
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
                if dinosaur.rect.y >= dinosaur.lowest_y:
                    dinosaur.jump()
                    dinosaur.jump_audio.play()

                if over == True:
                    mainGame()

        if over == False:
            bg1.map_update()
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()
            dinosaur.move()
            dinosaur.draw_dinosaur()

            SCREEN.blit(NSSH, (SCREENWIDTH - 100, 8))

            if barrier_timer >= 2100:
                rand_0 = random.randint(0, 100)
                
                if rand_0 > 40:
                    if rand_0 % 2 == 0:
                        rand_1 = random.randint(60, 80)
                        barrier = Barrier(rand_0 % 2, rand_1, rand_1)
                    else:
                        rand_1 = random.randint(30, 40)
                        barrier = Barrier(rand_0 % 2, rand_1, rand_1 * 2)

                    barriers.append(barrier)
                barrier_timer = 0

            for i in barriers:
                if i.rect.x < -100:
                    barriers.remove(i)

            for i in range(len(barriers)): #障礙物
                barriers[i].barrier_move()
                barriers[i].draw_barrier()
        
                if pygame.sprite.collide_rect(dinosaur, barriers[i]):  # 判斷恐龍與障礙物是否碰撞
                    over = True
                    Gameover()

                else:
                    if (barriers[i].rect.x + barriers[i].rect.width) < dinosaur.rect.x:
                        score += barriers[i].getScore()
                    
                    if score > high_score:
                        high_score = score

        # 顯示分數
        score_surface = score_font.render('Scores: %d | High Score: %d' %(score, high_score), True, (0, 0, 0))
        text_surface = my_font.render('Made by nssh jnr177 22 Alan, 33 Ray'.format(score), True, (0, 0, 0))

        SCREEN.blit(score_surface, (10, 5))
        SCREEN.blit(text_surface, (550, 240))

        barrier_timer += random.randint(10, 40)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    mainGame()