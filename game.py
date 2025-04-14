import pygame, sys
from use_model import predict_number

pygame.init()

size_draw = width, height = 28, 28
size_view = width, height = 560, 560

scale = int(360/28)

screen = pygame.display.set_mode(size_view)

WHITE = (255,255,255)
BLACK = (0,0,0)

drawing = False
last_pos = None
screen.fill(BLACK)
screenshot_path = "screenshot.png"

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
                    pygame.draw.line(screen,WHITE, last_pos, mouse_position, scale)
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
                pygame.image.save(screen, screenshot_path)
                predict_number(screenshot_path)
            elif event.key == pygame.K_c:
                screen.fill(BLACK)
                
    pygame.display.update()
