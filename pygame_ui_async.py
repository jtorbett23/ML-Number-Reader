
import pygame, asyncio
import httpx
import json
import numpy
import time
from pygame_core import COLOURS, SIZE_VIEW, SCALE, Button

url = "!URL/predict"

async def get_prediction(screenshot):
    prediction = None
    success = False
    try:
        r = await httpx.AsyncClient().post(url, json=screenshot)
        prediction = r.json()
        success = True
    except:
        print("Server not available yet...")
    return success, prediction

def set_text(screen, content, font, current_text=None):
    if current_text is not None:
        text_rect = current_text.get_rect()
        text_rect.top += 10
        text_rect.left += 10
        screen.fill(COLOURS["BLACK"], text_rect)

    current_text = font.render(content, True, COLOURS["GREEN"])
    text_rect = current_text.get_rect()
    text_rect.top += 10
    text_rect.left += 10
    screen.fill(COLOURS["BLACK"], text_rect)
    screen.blit(current_text, text_rect)
    return current_text

def clear_screen(screen, clear_button, predict_button, text, font):
    screen.fill(COLOURS["BLACK"])
    set_text(screen, "Prediction: None", font, text)
    clear_button.draw(screen)
    predict_button.draw(screen)


async def main():
    print("Started Pygame", flush=True)
    #SETUP
    pygame.init()
    #TITLE
    pygame.display.set_caption('MNIST Numbers')
    #UI LOGIC
    drawing = False
    last_pos = None
    run = True
    #REQUEST LOGIC
    retry_limit = 5
    retry_delay = 5
    retry_count = 0
    make_request = False
    request_time = None
    #SCREEN
    screen = pygame.display.set_mode(SIZE_VIEW, vsync=1)
    width = screen.get_width() 
    height = screen.get_height()
    screenshot = None
    #ELEMENTS
    font = pygame.font.Font('GoogleSansCode.ttf', 16)
    # button
    text = set_text(screen, "Prediction: None - Web", font)
    clear_button = Button("Clear", 0 + 10, height - 30 - 10, 80, 30, font)
    predict_button = Button("Predict", width -80 - 10, height - 30 - 10, 80, 30, font)
    clear_button.draw(screen)
    predict_button.draw(screen)
   
    pygame.display.update()

    while run:

        if(make_request):
            if(request_time is None or time.time() - request_time >= retry_delay):
                success, prediction = await get_prediction(screenshot)
                if(request_time is None):
                    print("Making request", flush=True)
                if success:
                    text = set_text(screen, f"Prediction: {prediction}", font, text)
                    make_request = False
                    request_time = None
                    print("Request finished", flush=True)
                elif not success and retry_count == retry_limit:
                    text = set_text(screen, f"Connection issue, please retry", font, text)
                    make_request = False
                    request_time = None
                    print("Request finished", flush=True)
                elif not success:
                    retry_count += 1
                    request_time = time.time()


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
                    clear_screen(screen, clear_button, predict_button, text, font)
                elif(predict_button.is_mouse_over(mouse_position)):
                    text = set_text(screen,"Prediction: Calculating...", font, text)
                    screenshot : numpy.ndarray = pygame.surfarray.pixels3d(screen)
                    screenshot = screenshot.tolist()
                    screenshot = json.dumps(screenshot)
                    make_request = True
                    retry_count = 0

            #MOUSE DOWN
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if(last_pos is not None):
                    last_pos = mouse_position
                drawing = True
            #KEY PRESSED
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    text = set_text(screen,"Prediction: Calculating...", font, text)
                elif event.key == pygame.K_c:
                    clear_screen(screen, clear_button, predict_button, text, font)
        
        await asyncio.sleep(0)  # Let other tasks run
        pygame.display.update()

def start():
    # This is the program entry point
    asyncio.create_task(main())
