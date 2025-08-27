import pygame
from pygame_core import COLOURS, SIZE_VIEW, SCALE, Button
import httpx
import numpy
import json
import time

url = "!URL/predict"
transport = httpx.HTTPTransport(retries=1)
client = httpx.Client(transport=transport)
#SETUP
pygame.init()
#TITLE
pygame.display.set_caption('MNIST Numbers')
#LOGIC
drawing = False
last_pos = None
run = True
make_request = False
#SCREEN
screen = pygame.display.set_mode(SIZE_VIEW, vsync=1)
width = screen.get_width() 
height = screen.get_height()
#ELEMENTS
font = pygame.font.Font('GoogleSansCode.ttf', 16)

def set_text(screen, content, current_text=None):
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


text = set_text(screen, "Prediction: None")
clear_button = Button("Clear", 0 + 10, height - 30 - 10, 80, 30, font)
predict_button = Button("Predict", width -80 - 10, height - 30 - 10, 80, 30, font)
clear_button.draw(screen)
predict_button.draw(screen)
running = True


def clear_screen():
    screen.fill(COLOURS["BLACK"])
    set_text(screen, "Prediction: None", text)
    clear_button.draw(screen)
    predict_button.draw(screen)

def predict_local():
    from use_model import predict_number
    screenshot = pygame.surfarray.pixels3d(screen)
    prediction = predict_number(screenshot)
    del screenshot
    set_text(screen, f"Prediction: {prediction}", text)
    clear_button.draw(screen)
    predict_button.draw(screen)



def run_frame(is_local = False):
    global running
    global drawing
    global last_pos
    global mouse_position
    global text
    global make_request


    if make_request:
        make_request = False
        if(is_local):
            predict_local()
        else:
            screenshot : numpy.ndarray = pygame.surfarray.pixels3d(screen)
            screenshot = screenshot.tolist()
            screenshot = json.dumps(screenshot)
            
            retries = 6
            delay = 5
            request = None
            for i in range(0, retries):
                try:
                    request = httpx.post(url, json=screenshot)
                except:
                    print("Server not available yet...")
                if request is not None:
                    break
                time.sleep(delay)

            if request is not None:
                text = set_text(screen, f"Prediction: {request.json()}", text)
            else:
                text = set_text(screen, f"Connection issue, please retry", text)

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
                text = set_text(screen,"Prediction: Calculating...", text)
                make_request = True
        #MOUSE DOWN
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if(last_pos is not None):
                last_pos = mouse_position
            drawing = True
        #KEY PRESSED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                text = set_text(screen,"Prediction: Calculating...", text)
                make_request = True

            elif event.key == pygame.K_c:
                clear_screen()
        elif event.type == pygame.QUIT:
            running = False
        
    pygame.display.flip()


def run_game_local():
    while running:
        run_frame(True)

def run_one_frame():
    if running:
        run_frame()
        window.requestAnimationFrame(ffi.create_proxy(lambda _: run_one_frame()))

try:
    from pyscript import window
    from pyscript import ffi
    run_one_frame()
    print("Started Pygame", flush=True)
except ImportError as _:
    run_game_local()