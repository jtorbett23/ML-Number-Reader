import pygame, sys
from pygame.locals import *
from use_model import predict_number
import numpy as np

pygame.init()

size_draw = width_draw, height_draw = 28, 28
size_view = width_view, height_view = 336, 336

scale = int(width_view/width_draw)

screen = pygame.display.set_mode(size_view)
pygame.display.set_caption('MNIST Numbers')

WHITE = (255,255,255)
BLACK = (0,0,0)

drawing = False
last_pos = None
screen.fill(BLACK)
screenshot_path = "screenshot.png"



green = (0, 255, 0)
blue = (0, 0, 128)
 
font = pygame.font.Font('freesansbold.ttf', 16)
 
# create a text surface object,
# on which text is drawn on it.
text = font.render('Prediction: None', True, green, blue)
 
# create a rectangular object for the
# text surface object
textRect = text.get_rect()

class Button:
    def __init__(self,text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        colour = (170,170,170) 
        pygame.draw.rect(screen,colour,[self.x,self.y,self.width,self.height]) 
        text = font.render(self.text, True, green)
        text_rect = text.get_rect()
        x_offset = (self.width - text_rect.width) / 2 
        y_offset = (self.height - text_rect.height) / 2 
        screen.blit(text, (self.x + x_offset, self.y + y_offset))
    
    def is_mouse_over(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.x and x <= self.x + self.width) and (y >= self.y and self.y + self.height):
            return True
        return False
# set the center of the rectangular object.
screen.blit(text, textRect)
clear_button = Button("Clear", 0 + 10, 336 - 30 - 10, 80, 30)
predict_button = Button("Predict", 336 -80 - 10, 336 - 30 - 10, 80, 30)
clear_button.draw(screen)
predict_button.draw(screen)
run = True
while run:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            if (drawing):
                mouse_position = pygame.mouse.get_pos()
                if last_pos is not None:
                    pygame.draw.line(screen, WHITE, last_pos, mouse_position, scale)
                last_pos = mouse_position
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if(last_pos is not None):
                mouse_position = pygame.mouse.get_pos()
                last_pos = mouse_position
            drawing = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                screenshot = pygame.surfarray.pixels3d(screen)
                prediction = predict_number(screenshot)
                del screenshot
                screen.fill(BLACK, textRect)
                text = font.render(f"Prediction: {prediction}", True, green, blue)
                screen.blit(text, textRect)
            elif event.key == pygame.K_c:
                screen.fill(BLACK)
                text = font.render(f"Prediction: None", True, green, blue)
                screen.blit(text, textRect)

    pygame.display.update()

