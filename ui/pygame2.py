
import pygame, asyncio

import requests
import json
import numpy

async def main():
    pygame.init()

    size_draw = width_draw, height_draw = 28, 28
    size_view = width_view, height_view = 336, 336

    scale = int(width_view/width_draw)

    screenshot_path = "screenshot.png"

    screen = pygame.display.set_mode(size_view)
    pygame.display.set_caption('MNIST Numbers')

    WHITE = (255,255,255)
    BLACK = (0,0,0)

    drawing = False
    last_pos = None
    run = True
    make_request = False

    green = (0, 255, 0)
    blue = (0, 0, 128)

    font = pygame.font.Font('freesansbold.ttf', 16)
    
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('Prediction: None', True, green, blue)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    screen.blit(text, textRect)
    # global run, drawing, last_pos
    pygame.display.update()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if (drawing):
                    mouse_position = pygame.mouse.get_pos()
                    if last_pos is not None:
                        pygame.draw.line(screen, WHITE, last_pos, mouse_position, scale)
                        pygame.display.update()
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
                    text = font.render(f"Prediction: Calculating...", True, green, blue)
                    screen.blit(text, textRect)
                    pygame.display.update()
                    make_request = True
                elif event.key == pygame.K_c:
                    screen.fill(BLACK)
                    text = font.render(f"Prediction: None", True, green, blue)
                    screen.blit(text, textRect)
                    pygame.display.update()
 
        
        await asyncio.sleep(0)  # Let other tasks run
        if make_request:
            screenshot : numpy.ndarray = pygame.surfarray.pixels3d(screen)
            # A GET request to the API
            screenshot = screenshot.tolist()
            screenshot = json.dumps(screenshot)
            # https://ml-number-reader.onrender.com
            # http://localhost:8000/predict
            response = requests.post("http://localhost:8000/predict", json=screenshot)
            # response = requests.post("https://ml-number-reader.onrender.com/predict", json=screenshot)
            # Print the response
            # print(response.json())
            # prediction = predict_number(screenshot)
            # del screenshot
            prediction = response.json()
            screen.fill(BLACK, text.get_rect())
            text = font.render(f"Prediction: {prediction}", True, green, blue)
            screen.blit(text, textRect)
            pygame.display.update(textRect)
            make_request = False


# This is the program entry point
asyncio.create_task(main())

