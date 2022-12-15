import sys, time
import random

import pygame
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
IMAGEWIDTH = 80
IMAGEHEIGHT = 100
FPS = 60

def get_random_position(widow_width, window_height, image_width, image_height):
    random_x = random.randint(image_width, widow_width - image_width)
    random_y = random.randint(image_height, window_height - image_height)

    return random_x, random_y

class Mosquito(pygame.sprite.Sprite):
    def __init__(self, width, height, random_x, random_y, widow_width, window_height):
        super().__init__()
        self.raw_image = pygame.image.load('./assets/objects/mosquito.png').convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (random_x, random_y)
        self.width = width
        self.height = height
        self.widow_width = widow_width
        self.window_height = window_height

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)

    # load window surface
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Mosquito War')
    random_x, random_y = get_random_position(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
    mosquito = Mosquito(IMAGEWIDTH, IMAGEHEIGHT, random_x, random_y, WINDOW_WIDTH, WINDOW_HEIGHT)
    reload_mosquito_event = USEREVENT + 1
    pygame.time.set_timer(reload_mosquito_event, 300)
    points = 0
    my_font = pygame.font.SysFont(None, 30)
    my_hit_font = pygame.font.SysFont(None, 40)
    hit_text_surface = None
    main_clock = pygame.time.Clock()

    while True:
        
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('./assets/audios/bgm.mp3')
            pygame.mixer.music.play(-1)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == MOUSEBUTTONDOWN:
                if random_x < pygame.mouse.get_pos()[0] < random_x + IMAGEWIDTH and random_y < pygame.mouse.get_pos()[1] < random_y + IMAGEHEIGHT:
                    mosquito.kill()
                    random_x, random_y = get_random_position(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
                    mosquito = Mosquito(IMAGEWIDTH, IMAGEHEIGHT, random_x, random_y, WINDOW_WIDTH, WINDOW_HEIGHT)
                    hit_text_surface = my_hit_font.render('Hit!!', True, (0, 0, 0))
                    points += 5

                else:
                    hit_text_surface = my_hit_font.render('.w.', True, (0, 0, 0))
                    
                    if points >= 5:
                        points -= 5

                    else:
                        points = 0

        window_surface.fill(WHITE)

        text_surface = my_font.render('Points: {}'.format(points), True, (0, 0, 0))
        
        window_surface.blit(mosquito.image, mosquito.rect)
        window_surface.blit(text_surface, (10, 0))

        if hit_text_surface:
            window_surface.blit(hit_text_surface, (10, 10))
            hit_text_surface = None

        pygame.display.update()
        
        main_clock.tick(FPS)

if __name__ == '__main__':    
    main()
