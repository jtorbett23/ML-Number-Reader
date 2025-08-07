import pygame, sys
from use_model import predict_number
from pygame_core import Button, COLOURS, set_text, SIZE_VIEW, SCALE

#SETUP
pygame.init()
#TITLE
pygame.display.set_caption('MNIST Numbers')
#LOGIC
drawing = False
last_pos = None
run = True
#SCREEN
screen = pygame.display.set_mode(SIZE_VIEW)
width = screen.get_width() 
height = screen.get_height()
#ELEMENTS
font = pygame.font.Font('freesansbold.ttf', 16)
set_text(screen, font, "Prediction: None")
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
        #MOUSE MOVED
        if event.type == pygame.MOUSEMOTION:
            if (drawing):
                mouse_position = pygame.mouse.get_pos()
                if last_pos is not None:
                    pygame.draw.line(screen, COLOURS["WHITE"], last_pos, mouse_position, SCALE)
                last_pos = mouse_position
        #MOUSE PRESSED & RELEASED
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None
            if(clear_button.is_mouse_over(mouse_position)):
                clear_screen()
            elif(predict_button.is_mouse_over(mouse_position)):
                predict()
        #MOUSE DOWN
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if(last_pos is not None):
                last_pos = mouse_position
            drawing = True
        #KEY PRESSED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                predict()
            elif event.key == pygame.K_c:
                clear_screen()
        #QUIT
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
