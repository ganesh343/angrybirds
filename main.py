#print("hello world")

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



#creatiing our iterations
run = True
while run:
    
    clock.tick(fps)
    
    #draw background
    screen.blit(bg, (0,0))
    
    #draw and scroll ground
    screen.blit(ground_img, (ground_scroll,768))
    ground_scroll -= scroll_speed
    
    if abs(ground_scroll) > 35:
        ground_scroll = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
            

pygame.quit()

