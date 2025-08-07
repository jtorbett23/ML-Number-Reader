import pygame, sys
from pygame.locals import *
from use_model import predict_number
import numpy as np
from pygame_core import Button, COLOURS, set_text

pygame.init()


size_draw = width_draw, height_draw = 28, 28
size_view = width_view, height_view = 336, 336
scale = int(width_view/width_draw)

font = pygame.font.Font('freesansbold.ttf', 16)

pygame.display.set_caption('MNIST Numbers')

drawing = False
last_pos = None
run = True
screen = pygame.display.set_mode(size_view)
width = screen.get_width() 
height = screen.get_height() 
set_text(screen, font, "Prediction: None")

# button
clear_button = Button("Clear", 0 + 10, height - 30 - 10, 80, 30, font)
predict_button = Button("Predict", width -80 - 10, height - 30 - 10, 80, 30, font)
clear_button.draw(screen)
predict_button.draw(screen)


def clear_screen():
    screen.fill(COLOURS["BLACK"])
    set_text(screen, font, "Prediction: None")
    clear_button.draw(screen)
    predict_button.draw(screen)

def predict():
    screenshot = pygame.surfarray.pixels3d(screen)
    prediction = predict_number(screenshot)
    del screenshot
    set_text(screen,font, f"Prediction: {prediction}")
    clear_button.draw(screen)
    predict_button.draw(screen)

while run:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            if (drawing):
                mouse_position = pygame.mouse.get_pos()
                if last_pos is not None:
                    pygame.draw.line(screen, COLOURS["WHITE"], last_pos, mouse_position, scale)
                last_pos = mouse_position
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None
            if(clear_button.is_mouse_over(mouse_position)):
                clear_screen()
            elif(predict_button.is_mouse_over(mouse_position)):
                predict()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if(last_pos is not None):
                last_pos = mouse_position
            drawing = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                predict()
            elif event.key == pygame.K_c:
                clear_screen()
                
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
