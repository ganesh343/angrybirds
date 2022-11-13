#print("hello world")
#part-1 create background
#part-2 create bird using sprite classes
#part-3 creating physics
#part-4
#part-5
#part-6

#import modules
import pygame
from pygame.locals import *

#creating game  
pygame.init()

clock = pygame.time.Clock()
fps = 60 #fixing time frame

#game screen size
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

#define game variables
ground_scroll = 0
scroll_speed = 4

#load images
bg = pygame.image.load('image/bg.png')
ground_img = pygame.image.load('image/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'image/bird{num}.png')
            self.images.append(img)   
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    
    def update(self):
        self.counter += 1
        flap_cooldown = 5
        
        if self.counter >flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
        
bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)
        



#creatiing our iterations
run = True
while run:
    
    #time frame to move the background
    clock.tick(fps)
    
    #draw background
    screen.blit(bg, (0,0))
    
    bird_group.draw(screen)
    bird_group.update()
    
    #draw and scroll ground
    #this scrolls the ground image at speed of 0 - scroll speed, 
    screen.blit(ground_img, (ground_scroll,768))
    ground_scroll -= scroll_speed
    
    if abs(ground_scroll) > 35:
        ground_scroll = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
            

pygame.quit()

