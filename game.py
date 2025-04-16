import pygame, sys
import pygame.gfxdraw
from pygame.locals import *
from math import atan2, cos, hypot, sin
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

def aaline(surface, color, start_pos, end_pos, width=1):
    """ Draws wide transparent anti-aliased lines. """
    # ref https://stackoverflow.com/a/30599392/355230

    x0, y0 = start_pos
    x1, y1 = end_pos
    midpnt_x, midpnt_y = (x0+x1)/2, (y0+y1)/2  # Center of line segment.
    length = hypot(x1-x0, y1-y0)
    angle = atan2(y0-y1, x0-x1)  # Slope of line.
    width2, length2 = width/2, length/2
    sin_ang, cos_ang = sin(angle), cos(angle)

    width2_sin_ang  = width2*sin_ang
    width2_cos_ang  = width2*cos_ang
    length2_sin_ang = length2*sin_ang
    length2_cos_ang = length2*cos_ang

    # Calculate box ends.
    ul = (midpnt_x + length2_cos_ang - width2_sin_ang,
          midpnt_y + width2_cos_ang  + length2_sin_ang)
    ur = (midpnt_x - length2_cos_ang - width2_sin_ang,
          midpnt_y + width2_cos_ang  - length2_sin_ang)
    bl = (midpnt_x + length2_cos_ang + width2_sin_ang,
          midpnt_y - width2_cos_ang  + length2_sin_ang)
    br = (midpnt_x - length2_cos_ang + width2_sin_ang,
          midpnt_y - width2_cos_ang  - length2_sin_ang)

    pygame.gfxdraw.aapolygon(surface, (ul, ur, br, bl), color)
    pygame.gfxdraw.filled_polygon(surface, (ul, ur, br, bl), color)

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
                    aaline(screen,WHITE, last_pos, mouse_position, scale)
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
