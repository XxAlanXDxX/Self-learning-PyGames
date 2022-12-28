import sys
import pygame
import random
from pygame.locals import *

#常數
SCREENWIDTH = 500
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

#high_score_w =  open('./assets/high_score.txt', 'w')

#蛇
class Snake():
    def __init__(self,x, y, is_head):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)

        if is_head:
            self.raw_head = pygame.image.load("./assets/objects/head.png")
            self.head = pygame.transform.scale(self.raw_head, (25, 25))
            self.head_vertical = pygame.transform.rotate(self.head, 90)
            self.head_horizontal = self.head
            self.image = self.head_horizontal

            self.score_audio = pygame.mixer.Sound('./assets/audios/score.wav')
            self.score_audio.set_volume(0.5)
            
        else:
            self.raw_image = pygame.image.load("./assets/objects/snake.png")
            self.image = pygame.transform.scale(self.raw_image, (25, 25))

        self.x = x
        self.y = y

        self.rect.center = (self.x, self.y)

    #移動 1: 向右 -1: 向左 2: 向上 -2: 向下
    def move(self, direction):
        if direction == 1:
            self.x += 25
            self.image = self.head_horizontal

        elif direction == -1:
            self.x -= 25
            self.image = self.head_horizontal

        if direction == 2:
            self.y -= 25
            self.image = self.head_vertical

        elif direction == -2:
            self.y += 25
            self.image = self.head_vertical

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def GetCoordinate(self):
        return self.x , self.y

    #繪製蛇
    def Draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

class Food():
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.raw_image = pygame.image.load("./assets/objects/food.png")
        self.image = pygame.transform.scale(self.raw_image, (25, 25))

        self.x = 400
        self.y = 250

        self.rect.center = (self.x, self.y)

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def GetCoordinate(self):
        return self.x , self.y

    def Draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

# 遊戲結束
def Gameover():
    bump_audio = pygame.mixer.Sound('./assets/audios/bump.wav')
    bump_audio.play()

    raw_gameover = pygame.image.load('./assets/objects/gameover.png').convert_alpha()
    gameover = pygame.transform.scale(raw_gameover, (200, 150))

    SCREEN.blit(gameover, (150, 175))

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
    tick = 0

    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('SnakeGame')
    score_font = pygame.font.SysFont(None, 30)
    my_font = pygame.font.SysFont(None, 20)

    snake_head = Snake(100, 250, True)
    snake_bodys = []
    snake_bodys.append(Snake(75, 250, False))
    snake_bodys.append(Snake(1000, 1000, False))

    food = Food()    

    direction_now = 1
    direction_next = direction_now

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                Escape()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Escape()

                elif over == True:
                    mainGame()

                else:
                    # 判斷鍵盤事件
                    if event.key == K_RIGHT or event.key == ord('d'):
                        direction_next = 1

                    elif event.key == K_LEFT or event.key == ord('a'):
                        direction_next = -1

                    elif event.key == K_UP or event.key == ord('w'):
                        direction_next = 2

                    elif event.key == K_DOWN or event.key == ord('s'):
                        direction_next = -2

        if direction_now != -direction_next and direction_now != direction_next:
            direction_now = direction_next

        if tick == 12:
            if over == False:
                SCREEN.blit(bg, (0, 0))

                head_x, head_y = snake_head.GetCoordinate()
                snake_head.move(direction_now)
                temp_x, temp_y = snake_bodys[0].GetCoordinate()
                snake_bodys[0].move_to(head_x, head_y)

                if head_x > 500 or head_x < 0 or head_y >= 500 or head_y < 0:
                    over = True
                    Gameover()

                if snake_head.GetCoordinate() == food.GetCoordinate(): #吃到食物
                    food.move_to(random.randint(0, 19) * 25, random.randint(0, 19) * 25)
                    print(food.GetCoordinate())

                    snake_bodys.append(Snake(1000, 1000, False)) 
                    score += 1
                    snake_head.score_audio.play()

                    if score > high_score:
                        high_score = score
                
            
                for body in snake_bodys:
                    if body.GetCoordinate() == snake_head.GetCoordinate():
                        over = True
                        Gameover()

                for i in range(1, len(snake_bodys) -1):
                    to_x, to_y = temp_x, temp_y
                    temp_x, temp_y = snake_bodys[i].GetCoordinate()
                    snake_bodys[i].move_to(to_x, to_y)

            tick = 0
            
        score_surface = score_font.render('Scores: %d | High Score: %d' %(score, high_score), True, (7, 74, 40)) #顯示分數
        text_surface = my_font.render('Made by nssh jnr177 22 Alan, 33 Ray'.format(score), True, (7, 74, 40))

        SCREEN.blit(score_surface, (10, 5))
        SCREEN.blit(text_surface, (250, 480))
        
        SCREEN.blit(NSSH, (SCREENWIDTH - 100, 8))
        snake_head.Draw()
        food.Draw()

        for body in snake_bodys:
            body.Draw()
        
        tick += 1
        pygame.display.update()
        FPSCLOCK.tick(FPS)
                
if __name__ == '__main__':
    mainGame()
