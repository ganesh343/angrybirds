#angrybirds game
#part-1 = create background
#part-2 = create bird
#part-3 = create physics
#part-4 = adding pipes and collison
#part-5 = addiing score and polishing the game
#part-6 =


#import modules
import pygame
from pygame.locals import *
import random


#create game
pygame.init()

#create game timeframe
clock = pygame.time.Clock()
fps = 60

#create game screen size
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)
#font color
white = (255, 255, 255)


# create game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#load images
bg = pygame.image.load('image/bg.png')
ground_img = pygame.image.load('image/ground.png')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

#use sprit class
#Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'image/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
#Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/pipe.png')
        self.rect = self.image.get_rect()
        #pos = 1 from top, -1 from bottom
        if position ==1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
    
#bird size
bird_group = pygame.sprite.Group()
pipe_group =pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)



run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0,0))
    #bird bg
    bird_group.draw(screen)
    bird_group.update()
    #pipe bg
    pipe_group.draw(screen)
    #pipe_group.update()

    #draw the ground
    screen.blit(ground_img, (ground_scroll, 768))
    
    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
                pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
                
    #print(score)
    draw_text(str(score), font, white, int(screen_width / 2), 20)
            
    #collison
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    
    #check if bird has hit the ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False


    if game_over == False and flying == True:
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            #pipe size
            btm_pipe = Pipe(screen_width, int(screen_height / 2), -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2), 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
            
        #draw and scroll the ground because of gravity
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()